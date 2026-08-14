# Feature Request: [RL] 实现 MoE Routing Capture / Mask Replay 支持 expert-level 奖励分配

> **状态**: Draft — 待 Triage  
> **分类**: Feature Request / RL Enabler  
> **优先级**: P1  
> **影响范围**: vllm-ascend MoE forward path、Distributed 子系统、Model Runner V1/V2  
> **关联上游 PR**: #49577 (routed_experts_capturer 初始引入), #50874 (DP buffer 尺寸修复)

---

## 1. 技术目标

在 vllm-ascend Ascend NPU 推理/rollout 路径上，**端到端打通 MoE Routing Capture 链路**，使 RL 训练框架（如 trl、openrlhf 等）能够在 Ascend 集群上完成：

- **MoE routing 可观测**：每次 forward pass 将每层 top-k expert 选择结果 (`topk_ids`) 写入预分配 NPU device buffer，D2H 到 scheduler 侧 slot-indexed CPU 缓冲
- **Expert-level 奖励分配**：RL 框架通过 `RoutedExpertsManager.get(block_ids, num_tokens)` 按物理 KV-cache slot 回溯任意请求的 per-token × per-layer × top-k expert 路由决策，实现 credit assignment
- **DP/EP/SP 拓扑下 routing 正确性**：在 data parallelism + expert parallelism + sequence parallelism 组合场景下，保证每个 DP rank 写入自身 token 的 routing，TP 分片通过 HCCL all_gather 正确重组
- **与 sleep mode / batch-invariance 共存**：capture buffer 在 sleep/wake 周期内可正确恢复，batch-invariance 模式下不破坏 routing 确定性

---

## 2. 背景

### 2.1 上游进展

上游 vLLM 在以下两个 PR 中引入并修复了 routed_experts_capturer：

| PR | 内容 | 关键文件 |
|----|------|----------|
| **#49577** | 初始引入 `RoutedExpertsCapturer` + `RoutedExpertsManager` + `bind_routed_experts_capturer`；device buffer (GPU int32) + scheduler slot-indexed CPU buffer (numpy uint8/uint16)；worker→scheduler 数据通路 | `vllm/model_executor/layers/fused_moe/routed_experts_capturer.py` |
| **#50874** | DP buffer 尺寸修复：区分 naive dispatch / modular-kernel / SP+modular-kernel 四种 DP 布局，修复 EP + SP 场景下 `topk_ids.shape[0]` 与 DP token 数不匹配导致的越界 | `routed_experts_capturer.py:108-222` (capture 方法全重写) |

上游核心代码结构：

```python
# vllm/model_executor/layers/fused_moe/routed_experts_capturer.py:89
self.device_buffer = torch.zeros(
    (max_num_batched_tokens, num_layers, num_experts_per_tok),
    dtype=torch.int32,
    device=current_platform.device_type,
)

# vllm/model_executor/layers/fused_moe/routed_experts_capturer.py:220
self.device_buffer[:token_num_per_dp, layer_id, :] = topk_ids[start_loc:end_loc, :]

# vllm/model_executor/layers/fused_moe/routed_experts_capturer.py:251
def bind_routed_experts_capturer(model, capturer):
    for module in model.modules():
        if isinstance(module, RoutedExpertsCaptureSource):
            module.capture_fn = partial(capturer.capture, module.layer_id)
        elif isinstance(module, MoERunner):
            if isinstance(module.router, BaseRouter):
                module.router.set_capture_fn(capture_fn)
```

上游 `ModelConfig.enable_return_routed_experts` 开关 (`vllm/config/model.py:242`) 控制整条链路：worker 侧 `init_routed_experts_capturer()` → forward hook 注入 `capture_fn` → scheduler 侧创建 `RoutedExpertsManager`。

### 2.2 vllm-ascend 现状

vllm-ascend **已具备以下基础**：

| 能力 | 位置 | 说明 |
|------|------|------|
| capture 函数 monkey-patch | `vllm_ascend/patch/worker/patch_routed_experts_capture.py` | 将 upstream `RoutedExpertsCapturer.capture` 替换为 Ascend 版本，新增 `total_with_padding` (DP padded all-gather) 分支，HCCL `dist.all_gather`，区分 ALLTOALL / MC2 moe_comm_type |
| model_runner_v1 继承 | `vllm_ascend/worker/model_runner_v1.py:3718-3719` | 当 `enable_return_routed_experts=True` 时调用 upstream `init_routed_experts_capturer()` |
| D2H + RoutedExpertsLists 组装 | `model_runner_v1.py:2389-2518` | sync/async 路径均已实现 device buffer clone → pinned CPU copy → `RoutedExpertsLists` 封装 |
| slot_mapping snapshot | `model_runner_v1.py:2941-2947` | 每 step 将共享 slot_mapping 拷贝到私有 device buffer |
| MoE forward_impl | `vllm_ascend/ops/fused_moe/routed_experts.py:494-607` | `forward_impl` → `_select_experts` 产生 `topk_ids`，但**尚未调用 router.capture_fn** |
| Ascend router | `vllm_ascend/ops/fused_moe/router/fused_topk_router.py`, `grouped_topk_router.py` | 需确认是否实现 `set_capture_fn` / `capture_fn` 属性 |
| RL 基础设施 | `distributed/weight_transfer/` (HCCL engine), `batch_invariant.py`, `platform.py:110` (sleep mode available) | RL 训练必备 |

**关键缺口**：Ascend MoE router / AscendRoutedExperts 尚未将 `topk_ids` 转发到 `capture_fn`；model_runner_v2 的 routed_experts 路径尚未验证；DP EP SP 组合拓扑下 HCCL all_gather 与 buffer 尺寸对齐未覆盖完整场景。

---

## 3. 实现范围

### 3.1 Worker-side Capture Buffer (设备端)

| 项 | 上游实现 | Ascend 需要适配 |
|----|----------|----------------|
| device buffer 分配 | `torch.zeros(..., device=current_platform.device_type)` | Ascend `torch_npu.empty(...)` 或沿用 upstream（需验证 `current_platform.device_type == "npu"` 时上游能否正确分发） |
| buffer 形状 | `(max_num_batched_tokens, num_layers, num_experts_per_tok)` int32 | 相同，但需确认 Ascend memory allocator (sleep_mem_optimized) 兼容 |
| all_gather 通信 | `get_tp_group().all_gather(topk_ids, dim=0)` (NCCL) | `dist.all_gather(list(split_topk_ids), topk_ids, get_tp_group().device_group)` (HCCL) — patch 已实现 |
| DP padded all-gather | upstream 无此分支 | vllm-ascend patch 新增 `total_with_padding` 分支 |

### 3.2 MoE Forward Hook 注册

上游 `bind_routed_experts_capturer()` 通过两种路径注入 capture_fn：

```
RoutedExpertsCaptureSource (Protocol) → module.capture_fn = partial(capturer.capture, module.layer_id)
MoERunner → module.router.set_capture_fn(capture_fn)
```

Ascend 需要覆盖：

| 路径 | Ascend 对应 | 需要做什么 |
|------|-------------|-----------|
| `AscendGroupedTopKRouter` | `ops/fused_moe/router/grouped_topk_router.py` | 实现 `set_capture_fn()` + 在 `_select_experts()` 返回前调用 `self.capture_fn(topk_ids)` |
| `AscendFusedTopKRouter` | `ops/fused_moe/router/fused_topk_router.py` | 同上 |
| `AscendRoutedExperts.forward_impl` | `ops/fused_moe/routed_experts.py:494` | 或在 `forward_impl` 中 `_select_experts` 返回后直接调用（若 router 实现过于复杂） |
| Model Runner V2 | `model_runner_v1.py` V2 分支 | 验证 V2 路径是否已具备 capture hook 触发点 |

### 3.3 Scheduler-side Manager (CPU 端)

上游 `RoutedExpertsManager` 完全基于 numpy（无 device 依赖），vllm-ascend **直接可用**。仅需确认：

- `RoutedExpertsManager` 初始化时 `_get_routed_experts_shape(vllm_config)` 能正确从 Ascend model config 读取 `num_experts` / `num_experts_per_tok` / `num_layers`
- scheduler 侧 `store_batch` / `get` 调用路径与上游一致

### 3.4 DP Buffer 尺寸修复 (PR #50874)

上游 `capture()` 四个分支：

1. `n == total` — naive dispatch (DP tokens 直接拼接)
2. `n == token_num_per_dp` — modular-kernel (quant_method.apply 内 combine)
3. `n == sum(dp_metadata.local_sizes)` — naive DP+EP dispatch (SP shard 顺序 gather)
4. `n == ceil(token_num_per_dp / tp_size)` — SP + modular-kernel (TP 分片 all_gather 重组)

vllm-ascend patch 已覆盖 1/2/4，并新增：
- `n == total_with_padding` — DP padded all-gather 路径
- 分支 4 扩展：`token_num_per_dp // tp_size` (all2all 不均匀分片), `(max_tokens + tp_size - 1) // tp_size` (MC2 padding)

**缺失验证**：分支 3 (`local_sizes`) 在 Ascend DP+EP 场景是否会触发，Ascend `dp_metadata` 是否携带 `local_sizes`。

---

## 4. Ascend 适配点详解

### 4.1 GPU Buffer → NPU Buffer

```python
# 上游: routed_experts_capturer.py:89-102
self.device_buffer = torch.zeros(
    (max_num_batched_tokens, num_layers, num_experts_per_tok),
    dtype=torch.int32,
    device=current_platform.device_type,  # Ascend platform 应返回 "npu"
)
```

**验证项**：
- `vllm_ascend.platform.current_platform.device_type` 是否返回 `"npu"`
- `torch.zeros` 在 NPU 上的默认行为（应通过 `torch_npu` 后端自动分发）
- sleep mode 下 capture buffer 生命周期：是否需要 `register_buffer` 以支持 wake restore
- `torch_npu.empty` vs `torch.zeros`：zeros 有初始化开销，但能防脏数据；评估 RL 场景下是否可接受

### 4.2 NCCL all_gather → HCCL all_gather

```python
# 上游 (NCCL): routed_experts_capturer.py:198
topk_ids = get_tp_group().all_gather(topk_ids, dim=0)

# vllm-ascend patch (HCCL): patch_routed_experts_capture.py:151-168
gather_topk_ids_shape = ...  # ALLTOALL vs MC2 不同
gather_topk_ids = torch.empty(gather_topk_ids_shape, ...)
split_topk_ids = torch.tensor_split(gather_topk_ids, self.tp_size, dim=0)
dist.all_gather(list(split_topk_ids), topk_ids, get_tp_group().device_group)
topk_ids = gather_topk_ids
```

**适配要点**：
- HCCL `dist.all_gather` 要求预先分配 output buffer（list of splits），与 NCCL `all_gather(tensor, dim=0)` API 签名不同，需要 Ascend patch
- ALLTOALL 场景 `gather_topk_ids_shape` 使用 `(token_num_per_dp, topk_ids.shape[1])` 保证不小于原始 TP 分片拼接尺寸
- MC2 场景使用 `(n * tp_size, topk_ids.shape[1])` 处理 DP padding + ceil-div
- **风险**：HCCL all_gather 超时配置 (`HCCL_OP_EXPANSION_MODE`, `HCCL_TIMEOUT_SECONDS`) 在 DP > 1 + TP > 1 场景需验证

### 4.3 Routing Replay Buffer DP 尺寸对齐

四个分支需在 Ascend 全场景覆盖：

| topk_ids.shape[0] 情形 | 上游分支 | Ascend patch 分支 | Ascend 场景来源 |
|------------------------|----------|------------------|----------------|
| `total` (DP tokens 拼接) | ✓ | ✓ | MoE naive dispatch |
| `token_num_per_dp` | ✓ | ✓ | Ascend MoECommType.ALLTOALL 直通 |
| `total_with_padding` | ✗ | ✓ | Ascend MC2 / FUSED_MC2 DP padded all-gather |
| `sum(local_sizes)` | ✓ | ✗ | **Ascend DP+EP SP shard gather — 需验证是否触发** |
| `ceil(token_num_per_dp / tp_size)` | ✓ | ✓ | Ascend TP SP 分片 |
| `token_num_per_dp // tp_size` | ✗ | ✓ | Ascend all2all 不均匀分片 |
| `(max_tokens + tp_size - 1) // tp_size` | ✗ | ✓ | Ascend MC2 DP padding + SP ceil-div |

### 4.4 Ascend MoE FusedMoE Capture Hook 注册

上游 `bind_routed_experts_capturer` 调用路径：

```
bind_routed_experts_capturer(model, capturer)
 ├── module is RoutedExpertsCaptureSource → module.capture_fn = partial(capturer.capture, module.layer_id)
 └── module is MoERunner
      ├── quant_method.is_monolithic → fused_experts.set_capture_fn() (Ascend 不走此路径: is_monolithic=False)
      └── isinstance(module.router, BaseRouter) → module.router.set_capture_fn()
```

Ascend 需确认：

1. `AscendGroupedTopKRouter` / `AscendFusedTopKRouter` 是否继承 upstream `BaseRouter`
2. `set_capture_fn(topk_ids)` 是否在 router 内正确调用
3. 如 router 不支持，备选路径：在 `AscendRoutedExperts._select_experts()` 返回前调用 `self.router.capture_fn(topk_ids)`

### 4.5 Sleep Mode / Batch-Invariance 兼容

vllm-ascend 已实现 sleep mode (`platform.py:110` `is_sleep_mode_available()`) 和 batch-invariance (`batch_invariant.py`, 设置 `HCCL_DETERMINISTIC=strict`)。capture 适配点：

- Sleep mode Level-2 会丢弃非 parameter/buffer 的 NPU tensor — capture buffer (`self.routed_experts_capturer.device_buffer`) 需注册为 named buffer 才能在 wake 后恢复
- Batch-invariance 模式下 `HCCL_DETERMINISTIC=strict` 要求 all_gather 确定性 — capture buffer int32 dtype 不受影响，但需确认 router topk 输出在 batch-invariant 模式下确定性

---

## 5. 预期收益

| 收益类别 | 说明 |
|----------|------|
| **RL 训练能力解锁** | trl/openrlhf 等 RLHF/RL 框架依赖 routed_experts 做 expert-level credit assignment；当前 Ascend 用户无法在 MoE 模型上做 reward model 的 expert 分配 |
| **MoE Routing 可观测性** | 通过 `RoutedExpertsManager.get(block_ids, num_tokens)` 回溯任意请求的 per-token × per-layer 路由决策，用于 routing 分布分析、负载均衡诊断、EPLB 效果评估 |
| **DP 场景正确性** | upstream PR #50874 修复了 DP+EP+SP 组合拓扑下 buffer 越界风险，Ascend patch 补充了 MC2/ALLTOALL 特有布局，覆盖更全 |
| **vllm-ascend upstream 同步** | 确保 Ascend 侧 routed_experts_capturer 与 upstream 主分支持续同步，避免 RL 新特性引入时的额外适配成本 |
| **社区贡献基础** | 完成此功能后可向上游 vLLM 提交 Ascend 平台 capture 适配（如 `current_platform.device_type` 已正确返回 "npu" 则无需上游改动） |

---

## 6. 上游参考

| 引用 | URL | 说明 |
|------|-----|------|
| **PR #49577** | `https://github.com/vllm-project/vllm/pull/49577` | 初始引入 RoutedExpertsCapturer + RoutedExpertsManager |
| **PR #50874** | `https://github.com/vllm-project/vllm/pull/50874` | DP buffer 尺寸修复，capture() 方法四分支逻辑 |
| `routed_experts_capturer.py` | `vllm/model_executor/layers/fused_moe/routed_experts_capturer.py` | 核心实现，313 行（含文档） |
| `gpu_model_runner.py:7815-7855` | init_routed_experts_capturer 实现 | device buffer + pinned CPU buffer + slot_mapping device buffer 分配 |
| `outputs.py:179-243` | RoutedExpertsTensors / RoutedExpertsLists NamedTuple | Worker→Scheduler 数据传递格式 |
| `scheduler.py:340-351, 1414, 1923` | RoutedExpertsManager 初始化与使用 | store_batch / get 调用时机 |
| `config/model.py:242` | `enable_return_routed_experts: bool = False` | 功能开关 |

---

## 7. 贡献指南

### 7.1 仓库位置

- **主仓库**: `https://github.com/vllm-project/vllm-ascend`
- **Issue 标签**: `good first issue` / `moepedia` / `rl` / `serving` / `feature`
- **关联上游**: `https://github.com/vllm-project/vllm`

### 7.2 关键文件变更清单

#### 新增文件

| 文件路径 | 职责 |
|----------|------|
| `vllm_ascend/distributed/routing_capture.py` | Ascend 专属 capture 适配层：封装 `torch_npu.empty` buffer 分配、HCCL all_gather 辅助、DP padded all-gather 尺寸计算。可替代当前 `patch_routed_experts_capture.py` 的 monkey-patch 方式，改为显式继承/扩展 |

#### 修改文件

| 文件路径 | 修改内容 |
|----------|----------|
| `vllm_ascend/patch/worker/patch_routed_experts_capture.py` | **当前**: 已实现 capture monkey-patch。需评估是否迁移到 `distributed/routing_capture.py` 或保持 patch 模式。补充 `local_sizes` 分支覆盖 (PR #50874 新增但 patch 未实现) |
| `vllm_ascend/ops/fused_moe/routed_experts.py:436-492` (`_select_experts`) | 在 router 返回 `topk_ids` 后，若 `self.router.capture_fn is not None` 则调用 `self.router.capture_fn(topk_ids)` |
| `vllm_ascend/ops/fused_moe/router/grouped_topk_router.py` | 确认/实现 `set_capture_fn(fn)` + 在 `_select_experts()` 内调用 `capture_fn(topk_ids)` |
| `vllm_ascend/ops/fused_moe/router/fused_topk_router.py` | 同上 |
| `vllm_ascend/worker/model_runner_v1.py` | V2 model runner 路径补充 `init_routed_experts_capturer` 调用验证 + `clear_buffer` 在 step 开始时重置 |
| `vllm_ascend/platform.py` | 确认 `current_platform.device_type` 返回 `"npu"`（若已返回则无需改动） |

#### 删除/重构

| 文件路径 | 原因 |
|----------|------|
| `vllm_ascend/patch/worker/patch_routed_experts_capture.py` | 迁移到 `distributed/routing_capture.py` 模块化（可选，取决于团队偏好 patch vs 显式适配） |

### 7.3 测试路径

#### 扩展现有测试

| 测试文件 | 补充用例 |
|----------|---------|
| `tests/ut/worker/test_routing_replay.py` | 补充 DP padded all-gather 分支、ALLTOALL vs MC2 不同 `gather_topk_ids_shape`、`total_with_padding` 与 `total` 重叠场景 |
| `tests/ut/patch/worker/test_patch_routed_experts_capture.py` | 补充 HCCL all_gather mock + 验证 `get_tp_group().device_group` 传入正确 |
| `tests/ut/ops/test_routed_experts.py` | 补充 `capture_fn` 调用触发验证（mock router.capture_fn） |

#### 新增测试

| 测试文件 | 覆盖场景 |
|----------|---------|
| `tests/ut/distributed/test_routing_capture.py` | DP=1/2/4, TP=1/2/4, EP=1/2 组合拓扑下 capture buffer 正确性；sleep mode 恢复后 capture 正确性；batch-invariance 模式下 routing 确定性 |
| `tests/e2e/singlecard/test_routing_capture_e2e.py` | 端到端：`enable_return_routed_experts=True` → 生成 → `RoutedExpertsManager.get()` 恢复 per-token routing → 与 forward 内 topk_ids 对比 |

#### 参考上游测试

- upstream `tests/v1/worker/test_gpu_model_runner.py` 中 routed_experts 相关测试
- upstream 可能的 DP buffer 尺寸边界测试（PR #50874 引入）

### 7.4 开发步骤建议

1. **Phase 1 — Router hook 打通**（优先级高，单卡即可验证）
   - 在 `AscendRoutedExperts._select_experts` 或 Ascend router 中注入 `capture_fn` 调用
   - 单卡 forward 验证 device buffer 正确写入
   
2. **Phase 2 — DP/TP 拓扑覆盖**（需要多卡 NPU 集群）
   - 扩展 patch `capture()` 覆盖 `local_sizes` 分支
   - ALLTOALL / MC2 两种 MoECommType 分别验证 all_gather 正确性
   - DP padded all-gather 尺寸边界测试（不等 token_counts 跨 DP ranks）

3. **Phase 3 — 工程化与验证**
   - Sleep mode 恢复测试
   - Batch-invariance 确定性测试
   - 迁移 patch → `distributed/routing_capture.py`（如团队同意）
   - V2 model runner 验证

---

## 8. 验收标准

> 所有标准可通过自动化测试或端到端脚本验证。

| # | 标准 | 验证方式 |
|---|------|---------|
| **1** | 单卡推理 `enable_return_routed_experts=True` 时，forward 后 `RoutedExpertsCapturer.device_buffer[:num_tokens]` 与 router 原始 `topk_ids` 逐元素相等 | 单卡单元测试：在 `_select_experts` 末尾 mock 记录 topk_ids，与 capture buffer 切片对比 |
| **2** | DP=2/TP=2/EP=1 拓扑下，每个 DP rank 的 capture buffer 仅包含本 rank token 的 routing（无跨 rank 污染） | 多卡测试：每 rank 在 forward 中注入 rank-标记 token，capture 后验证 |
| **3** | Ascend MC2 / FUSED_MC2 MoECommType 下，padded all-gather + ceil-div SP 路径的 `topk_ids.shape[0]` 被正确识别并触发正确的 DP slice | 构造 DP token 数不等 + TP>1 场景，验证 AssertionError 不触发且 buffer 内容正确 |
| **4** | `RoutedExpertsManager.get(block_ids, num_tokens)` 恢复的 routing 数据与 worker 侧 capture 原始数据在 slot_mapping 对齐后完全一致 | e2e 测试：生成完整请求 → 取 block_ids → get → 对比 |
| **5** | Sleep mode enable → sleep → wake 后，`enable_return_routed_experts` 链路不报错且 buffer 内容恢复正确（无脏数据、无 device mismatch） | 调用 `device.sleep()` / `device.wake()` 后重新 forward，验证 capture |

---

## 9. 前置问题

> 以下问题需要在开发前确认，部分可能影响实现方案。

| # | 问题 | 影响 | 建议责任人 |
|---|------|------|-----------|
| **Q1** | Ascend 910 上 capture buffer 显存开销估算：`max_num_batched_tokens(8192) × num_layers(60) × top_k(4) × int32(4B)` ≈ **7.5 MB** / worker。是否需要按实际模型尺寸验证？ | 若模型层数多或 max_tokens 大，可能达数十 MB，需确认 sleep mode memory manager 是否正确纳入此 buffer | 贡献者 |
| **Q2** | vllm-ascend patch `capture()` 缺失 upstream `local_sizes` 分支（PR #50874 新增）。Ascend DP+EP 场景是否会触发此分支？若会，Ascend `dp_metadata` 是否携带 `local_sizes` 属性？ | 若不覆盖，DP+EP 场景会抛 AssertionError 或 silent wrong result | 贡献者 + EPLB 负责人 |
| **Q3** | HCCL all_gather 在 DP+TP 组合拓扑下的 group 初始化是否与 NCCL 语义一致？`get_tp_group().device_group` 在 Ascend 上是否等价于 NCCL process group？ | 若不一致，all_gather 可能 hang 或 gather 错数据 | distributed 负责人 |
| **Q4** | Ascend MoECommType 中 `ALLTOALL` 和 `MC2` 对 `topk_ids.shape[0]` 的具体影响是否已在 patch 中完整覆盖？新增 MoECommType 是否需要同步更新 patch？ | MoE 通信路径变更时 capture 可能 silent break | MoE 负责人 |
| **Q5** | Model Runner V2 路径是否需要 routing capture？`model_runner_v1.py:3718` 的 `init_routed_experts_capturer()` 在 V2 模式下是否被正确调用？ | V2 是未来主推路径，若遗漏将影响升级 | model runner 负责人 |
| **Q6** | `AscendRoutedExperts.is_monolithic = False` 导致 upstream `bind_routed_experts_capturer` 走 `router.set_capture_fn` 分支。Ascend router 是否实现此接口？当前测试 `test_routing_replay.py` 显示 binder 能绑定成功，但 router 内部是否真正调用 `capture_fn`？ | 若 router 未调用 capture_fn，device buffer 全零，RL 数据无效 | router 负责人 |

---

## 10. 里程碑建议

| 里程碑 | 产出 | 预计 |
|--------|------|------|
| **M1** | Router capture_fn 注入 + 单卡 e2e capture 正确性 | 1–2 天 |
| **M2** | DP/TP/EP 多卡拓扑覆盖 + MC2/ALLTOALL all_gather | 3–5 天 |
| **M3** | Sleep mode + batch-invariance 兼容 | 1–2 天 |
| **M4** | 模块化重构（patch → distributed/routing_capture）+ 完整测试套件 | 2–3 天 |

**总计**: 约 7–12 人天

---

## 附录 A: 数据流全景（ASCII）

```
                     ┌─────────────────────────────────────────┐
                     │          RL 训练框架 (trl/openrlhf)      │
                     │   RoutedExpertsManager.get(block_ids)    │
                     └──────────────────┬──────────────────────┘
                                        │ 读取
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Scheduler 进程 (CPU)                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ RoutedExpertsManager                                                │    │
│  │ routed_experts_by_slot: np.zeros(slots, layers, top_k, uint8/uint16)│    │
│  │ store_batch(data, slot_mapping) → fancy-index assign               │    │
│  │ get(block_ids, num_tokens) → fancy-index read → copy               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                          ▲ RoutedExpertsLists                                │
│                          │ D2H + tolists()                                   │
│  ┌───────────────────────┴───────────────────────────────────────────┐    │
│  │ GPUModelRunner (继承 + vllm_ascend 扩展)                             │    │
│  │ init_routed_experts_capturer()                                      │    │
│  │  ├─ RoutedExpertsCapturer (upstream)                                │    │
│  │  │   └─ device_buffer: torch.empty(max_tokens, layers, top_k, int32)│    │
│  │  ├─ routed_experts_cpu (pinned)                                     │    │
│  │  └─ routed_experts_slot_mapping_device                              │    │
│  └──────────────────────────┬──────────────────────────────────────────┘    │
│                             │ forward pass                                  │
└─────────────────────────────┼───────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Worker 进程 (NPU)                                    │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │ AscendMoERunner / AscendRoutedExperts                             │       │
│  │                                                                  │       │
│  │  router._select_experts(hidden_states, router_logits)            │       │
│  │    → topk_weights, topk_ids                                      │       │
│  │    → router.capture_fn(topk_ids) ──────► RoutedExpertsCapturer   │       │
│  │                                          .capture(layer_id, ids)  │       │
│  │                                                                  │       │
│  │  [patch_routed_experts_capture.py 覆盖的 capture 逻辑]:            │       │
│  │    naive dispatch           → cumsum slice                        │       │
│  │    modular-kernel path      → whole tensor                        │       │
│  │    total_with_padding (新)  → dp_rank * max_tokens slice         │       │
│  │    SP + TP all_gather (HCCL) → split + dist.all_gather            │       │
│  │      ALLTOALL 形状: (token_num_per_dp, top_k)                     │       │
│  │      MC2 形状:     (n * tp_size, top_k)                           │       │
│  └──────────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 附录 B: DP Buffer 尺寸判定逻辑（vllm-ascend patch 完整伪代码）

```python
def capture(self, layer_id, topk_ids):
    ctx = get_forward_context()
    if ctx.dp_metadata is None:          # single DP
        start, end, per_dp = 0, n, n
    else:
        tokens_dp = ctx.dp_metadata.num_tokens_across_dp_cpu
        per_dp = int(tokens_dp[self.dp_rank].item())
        total = int(tokens_dp.sum().item())
        max_tokens = int(tokens_dp.max().item())
        total_with_pad = max_tokens * len(tokens_dp)
        n = topk_ids.shape[0]

        if n == total:                            # naive dispatch
            end = int(torch.cumsum(tokens_dp, 0)[self.dp_rank])
            start = end - per_dp
        elif n == per_dp:                         # modular-kernel path
            start, end = 0, per_dp
        elif n == total_with_pad:                 # Ascend DP padded all-gather
            start = self.dp_rank * max_tokens
            end = start + per_dp
        elif self.tp_size > 1 and (
            n == (per_dp + tp_size - 1) // tp_size
            or n == per_dp // tp_size
            or n == (max_tokens + tp_size - 1) // tp_size
        ):                                        # SP + TP (HCCL all_gather)
            if moe_comm_type == ALLTOALL:
                shape = (per_dp if per_dp >= tp_size else tp_size, topk_ids.shape[1])
            else:                                 # MC2 / FUSED_MC2
                shape = (n * tp_size, topk_ids.shape[1])
            gather = torch.empty(shape, dtype=topk_ids.dtype, device=topk_ids.device)
            splits = torch.tensor_split(gather, tp_size, dim=0)
            dist.all_gather(list(splits), topk_ids, get_tp_group().device_group)
            topk_ids = gather
            start, end = 0, per_dp
        else:
            raise AssertionError(...)

    self.device_buffer[:per_dp, layer_id, :] = topk_ids[start:end, :]
```
