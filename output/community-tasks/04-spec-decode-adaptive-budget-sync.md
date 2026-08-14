# Feature Request: [Spec Decode] 同步自适应 token budget 与 CUDA graph fusion 优化

<!--
在 GitHub Issue 上发布时，请将以下「元信息」移除，保留 Markdown 正文。
标签建议：enhancement, speculative-decoding, v2-worker, good-first-issue, npu-ascend
难度：Medium — High
预计改动文件数：6-10
-->

---

## 技术目标

将 vLLM 上游 2025 年 H2 引入的 **自适应 Speculative Token Budget**（PR #51725）、**AR Speculator Multi-Step CUDA Graph Fusion**（PR #46849）以及 **DSpark Confidence-Scheduled Verification** 同步到 `vllm-ascend`，使 Ascend 910X/XE 上的 DSpark / DFlash / Eagle / MTP 推理在**高并发**场景下 TTFT 降低 50-60%，并减少 pipeline bubble。

---

## 背景

Speculative Decoding 在 batch size 1 时几乎是免费的（GPU memory-bound），但 batch size 256 时 draft token 会与 real token 争抢算力，**被拒绝的 token 纯粹是浪费**。上游 Kimi K3 DSpark 的线上数据显示，acceptance rate 随并发快速衰减，静态 `num_speculative_tokens` 在全负载区间无法工作。

### 上游已落地的三项关键优化

| 优化 | 上游文件 | 核心机制 | PR |
|------|---------|---------|----|
| Adaptive Verification | `vllm/v1/worker/gpu/spec_decode/adaptive_verification.py:114` `AdaptiveVerificationManager` | 每 step 按 per-request confidence 的 survival probability 做全局 top-k，选出最优 draft budget；CPU 侧 cost model 从 cudagraph 回放 profile 得到 draft/verify 曲线 | [#51725](https://github.com/vllm-project/vllm/pull/51725) |
| AR Multi-Step CUDA Graph Fusion | `vllm/v1/worker/gpu/spec_decode/autoregressive/cudagraph_utils.py:20` `SpeculatorCudaGraphManager` | 把 Eagle/MTP 的 prefill + N-step decode 全部 capture 进同一张 FULL graph，消除每步 kernel launch gap | [#46849](https://github.com/vllm-project/vllm/pull/46849) |
| DSpark Confidence-Scheduled Verification | `vllm/v1/worker/gpu/spec_decode/dspark/speculator.py:82-87` `draft_token_confidence_probs` + `enable_adaptive_verification` | DSpark 自带 confidence head，每个 (request, step) slot 输出生存概率；与 AdaptiveVerificationManager 直接对接 | 随 PR #51725 合入 |

### 配置层入口（上游已就位，Ascend 直接透传）

```python
# vllm/config/speculative.py:241
enable_adaptive_verification: bool = False
# 以及 vllm/config/speculative.py:181 的 batch-size based fallback
num_speculative_tokens_per_batch_size: list[tuple[int, int, int]] | None = None
```

使用示例（上游文档 `docs/features/speculative_decoding/adaptive_verification.md:20`）：

```bash
vllm serve deepseek-ai/DeepSeek-V4-Flash-DSpark \
  --tokenizer-mode deepseek_v4 --trust-remote-code \
  --speculative-config '{
    "method": "dspark",
    "model": "deepseek-ai/DeepSeek-V4-Flash-DSpark",
    "num_speculative_tokens": 7,
    "draft_sample_method": "probabilistic",
    "enable_adaptive_verification": true
  }'
```

---

## Ascend 适配点

vllm-ascend 当前的 Spec Decode 实现**没有** `enable_adaptive_verification` 和 `AdaptiveVerificationManager` 的适配；AR speculator 的 multi-step graph fusion 也只做了静态 `decode_query_len` 粒度。Ascend 已有 DFlash FullGraph 作为基础（`vllm_ascend/worker/v2/spec_decode/dflash/aclgraph.py:26` `DFlashAclGraphManager`）。

### 1. AdaptiveVerificationManager 在 Ascend 上的初始化与 profile

**现状**：`maybe_create_adaptive_verification_manager`（`vllm/v1/worker/gpu/spec_decode/adaptive_verification.py:438`）使用 `torch.cuda.Stream` / `torch.cuda.Event` / `torch.cuda.CUDAGraph`，Ascend 上需替换为 `torch.npu.*`。

**适配动作**：
- 在 `vllm_ascend/worker/v2/aclgraph_utils.py` 或新文件 `vllm_ascend/worker/v2/spec_decode/adaptive_verification.py` 中，提供 `AscendAdaptiveVerificationManager` 子类或 monkey-patch，将 `torch.cuda` 设备调用替换为 `torch.npu`
- 依赖 cudagraph cost profiling：`AdaptiveVerificationManager.batches_to_profile`（`adaptive_verification.py:171`）和 `set_initial_cost_curves`（`adaptive_verification.py:195`）要求 FULL graph；Ascend 的 `ModelAclGraphManager.capture`（`aclgraph_utils.py:139`）已经走 FULL 路径，只需确保 `StepTimingCollector.collect()` 在 NPU stream 上能正确读 event
- `torch.compile` 的 `_assign_draft_token_budget_compiled`（`adaptive_verification.py:63`）在 Ascend 上走 CANN graph，需要验证是否需要额外的 `dynamic=True` 参数或降级到 eager

**关键代码引用**：
- 上游 `vllm/v1/worker/gpu/spec_decode/adaptive_verification.py:114-165` — `AdaptiveVerificationManager.__init__` 中 stream/event 创建
- 上游 `vllm/v1/worker/gpu/spec_decode/adaptive_verification.py:405` — `_assign_draft_token_budget_compiled` 调用点
- Ascend `vllm_ascend/worker/v2/aclgraph_utils.py:68` — `ModelAclGraphManager` 已有完整 FULL graph capture 基础

### 2. Attention 后端对 device-decided query lengths 的支持

**现状**：Adaptive Verification 需要 attention backend 容忍 device 侧决定的 query lengths（因为 CPU 只给 upper bound）。上游通过 `get_query_lens_mismatch_unsupported_backend`（`adaptive_verification.py:453`）检测并拒绝不支持的 backend，且要求 `AttentionCGSupport.ALWAYS`（`adaptive_verification.py:462-469`）。

**适配动作**：
- Ascend attention backends（`AscendAttentionBackend` / `AscendMLABackend` / `AscendDSABackend`，见 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py:212-218`）需要上报 `AttentionCGSupport.ALWAYS`
- DSA/SFA 在 NPU 上当前是否支持 varlen decode？需要确认 `AscendDSABackend` 的 `get_attn_cg_support()` 返回值

### 3. DSpark Confidence Head 与 AscendDSparkSpeculator 对接

**现状**：上游 `DSparkSpeculator` 在 `__init__` 中读取 `speculative_config.enable_adaptive_verification`（`dspark/speculator.py:85-87`），在 `load_draft_model` 中校验 `model.model.confidence_head` 存在（`dspark/speculator.py:111-117`）。

Ascend 侧 `AscendDSparkSpeculator`（`vllm_ascend/worker/v2/spec_decode/dspark/speculator.py:34`）直接 `super().__init__` 继承了这段逻辑，因此：
- confidence head 的 forward 本身是 torch op，**不需要 NPU 特定适配**
- 但 confidence 从 device 异步 copy 回 CPU 的流程（`AdaptiveVerificationManager.record_confidences`，`adaptive_verification.py:239`）使用 `torch.cuda.current_stream` 和 `torch.cuda.Stream`，**必须 patch**

**关键代码引用**：
- Ascend `vllm_ascend/worker/v2/spec_decode/dspark/speculator.py:41-47` — `init_cudagraph_manager` 已将 `update_stream` 关联到 speculator，可复用此 stream
- 上游 `vllm/v1/worker/gpu/spec_decode/adaptive_verification.py:261-264` — 关键的 stream wait + copy_to_cpu + event record 代码段

### 4. AR Speculator Multi-Step CUDA Graph Fusion 对齐

**现状**：Ascend 的 `AscendAutoRegressiveSpeculator._multi_step_decode`（`vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py:306-326`）在 FULL 模式下走一次 `run_fullgraph`，已经是 multi-step fusion 的基础路径。上游的改进在于 `SpeculatorCudaGraphManager._init_candidates`（`autoregressive/cudagraph_utils.py:20`）按每 step 真实 token count 细化 capture descriptor，以及 `use_fused_multi_step_decode` flag（上游 `autoregressive/speculator.py:45, 98-100`）。

**适配动作**：
- 确认 Ascend `decode_cudagraph_manager`（`aclgraph_utils.py` 中由 `ModelCudaGraphManager` patch 而来）的 `_init_candidates` 已覆盖 `decode_query_len` 的 `round_up` 粒度（`cudagraph_utils.py:241`）
- 验证 Ascend FULL graph 模式下 draft model 的 `is_draft_model` / `is_draft_model_prefill` 标记（`ModelWithContext`，`aclgraph_utils.py:171-212`）在 multi-step decode 场景下的行为是否一致

### 5. Varlen Decode CUDA Graph（Adaptive Verification 的硬依赖）

**现状**：`AdaptiveVerificationManager` 要求 `AttentionCGSupport.ALWAYS`，即 attention backend 在 FULL graph 下能接受 varlen query lengths。Ascend 上 DFlash 已有 varlen decode graph（`DFlashAclGraphManager` 继承 `DFlashCudaGraphManager`），DSpark 走同一条 DFlash 基类路径。

**需要确认**：Ascend SFA/DSA/MLA 的 FULL graph 模式下，`max_query_len` 参数能否工作。上游 `cudagraph_utils.py:219-236` 有专门的 `capture_varlen_decode` 分支，Ascend 需要走通这条路径。

---

## 预期收益

| 指标 | 预期提升 | 说明 |
|------|---------|------|
| DSpark TTFT（高并发 batch size 256） | 降低 50-60% | 仅 verify confidence 最高的 draft slots，减少无效 compute |
| Pipeline bubble | 显著减少 | 全局 budget 分配让高 confidence request 拿到更多 verify 额度 |
| Spec decode 在全负载区间的可用性 | 从"需要手动调 K" → "开箱即用" | 一个 config 在所有 batch size 都工作 |

> 参考上游 Kimi K3 DSpark TTFT ~60% 提升（PR #51725 描述）。Ascend 上由于 NPU 的 launch overhead 相对 GPU 更高，**graph fusion 的收益会更显著**，同时 adaptive verification 在高并发下的 compute 节省也更有价值。

---

## 上游参考

| 类别 | 文件路径 | 关键类/函数 | 行号 |
|------|---------|-----------|------|
| Adaptive Verification 核心 | `vllm/v1/worker/gpu/spec_decode/adaptive_verification.py` | `AdaptiveVerificationManager` | :114 |
| | | `_assign_draft_token_budget` | :34 |
| | | `build_cost_tables_from_curves` | :68 |
| | | `record_confidences` | :239 |
| | | `get_num_tokens` | :267 |
| | | `reallocate_drafts` | :377 |
| 配置项 | `vllm/config/speculative.py` | `enable_adaptive_verification` | :241 |
| | | `num_speculative_tokens_per_batch_size` | :181 |
| DSpark Speculator | `vllm/v1/worker/gpu/spec_decode/dspark/speculator.py` | `DSparkSpeculator` confidence 字段 | :82-87 |
| | | `load_draft_model` confidence head 校验 | :111-117 |
| DFlash Speculator（基类） | `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` | — | — |
| AR Speculator | `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` | `AutoRegressiveSpeculator` | :29 |
| | | `use_fused_multi_step_decode` flag | :45, :98-100 |
| AR CudaGraph | `vllm/v1/worker/gpu/spec_decode/autoregressive/cudagraph_utils.py` | `SpeculatorCudaGraphManager` | :20 |
| GPU CudaGraph 基类 | `vllm/v1/worker/gpu/cudagraph_utils.py` | `CudaGraphManager` | :102 |
| | | `ModelCudaGraphManager` | :441 |
| | | `_init_candidates`（varlen decode 分支） | :173-301, :219-236 |
| | | `prepare_inputs_to_capture` | :606 |
| 文档 | `docs/features/speculative_decoding/adaptive_verification.md` | 完整设计说明 | — |
| 测试 | `tests/v1/spec_decode/test_adaptive_verification.py` | — | — |

---

## vllm-ascend 关键文件地图

### Spec Decode 入口与 speculators

```
vllm_ascend/worker/v2/spec_decode/
├── __init__.py                          # init_speculator 工厂（:23-57）
├── autoregressive/speculator.py         # AscendAutoRegressiveSpeculator（:68）
├── dspark/speculator.py                 # AscendDSparkSpeculator（:34）
├── dflash/
│   ├── speculator.py                    # AscendDFlashSpeculator
│   └── aclgraph.py                      # DFlashAclGraphManager（:26）← 已有 FULL graph
├── eagle/speculator.py                  # AscendEagleSpeculator
├── eagle/aclgraph.py                    # Eagle AclGraph
└── mtp/speculator.py                    # AscendMTPSpeculator
```

### Graph 与平台

```
vllm_ascend/worker/v2/
├── aclgraph_utils.py                    # ModelAclGraphManager（:68）← 继承 ModelCudaGraphManager
├── compilation/acl_graph.py             # set_graph_params / update_full_graph_params
└── attn_utils.py                        # build_attn_metadata_wrapper

vllm_ascend/
├── platform.py                          # num_speculative_tokens_per_batch_size 校验（:1401）
├── attention/attention_v1.py            # AscendAttentionBackend
├── attention/mla_v1.py                  # AscendMLABackend
└── attention/dsa_v1.py                  # AscendDSABackend
```

### 测试路径

```
tests/ut/spec_decode/
├── test_dynamic_sd.py                   # batch-size based Dynamic SD 已有
├── test_dspark_proposer.py
└── test_eagle_aclgraph_source_regression.py

tests/e2e/pull_request/
├── one_card/spec_decode/
│   ├── test_dspark.py
│   ├── test_dflash.py
│   ├── test_eagle.py
│   └── test_dynamic.py
└── four_card/spec_decode/
    ├── test_dspark_deepseekv4.py
    └── test_mtp_qwen3_next.py
```

### 当前**缺失**的文件（需要新增）

| 文件 | 职责 | 参考上游 |
|------|------|---------|
| `vllm_ascend/worker/v2/spec_decode/adaptive_verification.py` | Ascend 版 AdaptiveVerificationManager（torch.npu 替换） | `vllm/v1/worker/gpu/spec_decode/adaptive_verification.py` |
| `tests/ut/spec_decode/test_adaptive_verification.py` | 单元测试 | `tests/v1/spec_decode/test_adaptive_verification.py` |

---

## 贡献指南

### 仓库位置

- 上游：`https://github.com/vllm-project/vllm`（分支 `main`，关注 2025 H2 合入的 speculative decoding PR）
- Ascend 移植层：`https://github.com/vllm-project/vllm-ascend`（工作目录：`vllm_ascend/worker/v2/spec_decode/`）

### 开发步骤

1. **同步上游基线**：先将本地 `.tmp_vllm` submodule 更新到包含 PR #51725 和 #46849 的 commit
2. **通读上游 adaptive_verification.py**：理解 cost model + confidence-based top-k 分配 + D2H 异步 copy 三件事如何配合
3. **创建 Ascend 适配层**：从 `AdaptiveVerificationManager` 继承或 monkey-patch，将所有 `torch.cuda.*` 替换为 `torch.npu.*`
4. **打通 AttentionCGSupport.ALWAYS**：在每个 Ascend attention backend 的 `get_attn_cg_support()` 方法中上报正确等级
5. **端到端验证**：用 DSpark + DeepSeek-V4 / Qwen3-DSpark checkpoint 跑通 profile → 首次 serve → 多轮并发

### 提交规范

vllm-ascend 使用 DCO，提交消息格式：
```
spec_decode: [DSpark/Eagle/MTP] sync adaptive verification

- Patch AdaptiveVerificationManager for torch.npu streams/events
- Report AttentionCGSupport.ALWAYS on AscendSFA
- Add unit test for confidence-based budget allocation
- Closes #<issue-number>
```

### 测试命令

```bash
# UT（无 NPU 也可跑，覆盖 budget 分配逻辑）
python -m pytest tests/ut/spec_decode/ -v

# E2E（需要 NPU）
pytest tests/e2e/pull_request/one_card/spec_decode/test_dspark.py \
  -k adaptive -v

# 性能回归
pytest tests/e2e/pull_request/four_card/spec_decode/test_dspark_deepseekv4.py \
  -v --benchmark-enable
```

---

## 验收标准

- [ ] **功能正确**：`enable_adaptive_verification: true` 时 DSparK 在 Ascend 上成功 profile 并产出 `draft_cost_table` / `verify_cost_table`，且 acceptance rate 不低于静态 K 方案的 95%
- [ ] **性能达标**：batch size 256 下 TTFT 相比 `enable_adaptive_verification: false` 降低 ≥ 40%（目标 50-60%，下限 40% 即算达标）
- [ ] **端到端可用**：`vllm serve` 带 `enable_adaptive_verification: true` 不报错，日志中可见 `DSpark cost tables: (...)`（`adaptive_verification.py:237` logger）
- [ ] **与 AR graph fusion 兼容**：有/无 `num_speculative_tokens_per_batch_size` 两种路径在 FULL graph 模式下均正常
- [ ] **通过 UT/E2E**：新增 UT + 现有 `test_dspark.py` / `test_dflash.py` / `test_eagle.py` 全部 pass
- [ ] **无 regression**：`enforce_eager=true` 时行为与之前一致；非 DSpark 方法不受影响

---

## 前置问题与限制

| 问题 | 影响 | 建议路径 |
|------|------|---------|
| Ascend FULL graph 模式下 attention backend 是否全部支持 varlen decode（`max_query_len`） | 若某个 backend 不支持，Adaptive Verification 会在启动时被拒绝 | 在 AscendSFA / AscendMLABackend / AscendDSABackend 上逐个验证 `AttentionCGSupport.ALWAYS`；DCP 禁用时先跳过 |
| CANN graph 对 `torch.compile` 的支持 | `_assign_draft_token_budget_compiled` 在 Ascend 上可能无法 trace | 降级到 eager 实现（函数本身很简单：cumprod + masked_fill + topk），后续优化 |
| DSpark Confidence Head 是否在 Ascend checkpoint 上存在 | `enable_adaptive_verification=true` 时若无 confidence head 会在 `load_draft_model` 时报错 | 文档提示用户使用带 confidence head 的 checkpoint（如 DeepSeek-V4-Flash-DSpark） |
| Ascend 910B 单卡显存限制 | FULL graph 对 prefill + decode 都要 capture，spec decode 额外的 KV cache 和 confidence buffer 占显存 | 先在 910X/XE 验证，910B 用 PIECEWISE 模式兜底 |
| Pipeline Parallelism（PP）限制 | 上游 adaptive verification 文档明确标注不支持 PP（cost curves 只在最后一个 rank） | Ascend 先限定 TP+DP 场景，PP 后续再处理 |
| LoRA + Adaptive Verification 冲突 | 上游文档明确标注不支持 LoRA | 暂不实现，先跑通 base model 路径 |

---

## 任务拆分（可独立认领）

| # | 子任务 | 预计难度 | 依赖 |
|---|--------|---------|------|
| 04-a | 调研 + 设计文档：确认 Ascend attention backends 的 AttentionCGSupport 能力，画通 torch.npu 替换的详细 patch 点 | Low | — |
| 04-b | AdaptiveVerificationManager Ascend 适配（torch.npu stream/event/cudagraph） | Medium | 04-a |
| 04-c | Attention backend AttentionCGSupport.ALWAYS 上报 | Low | 04-a |
| 04-d | DSpark confidence-scheduled verification 端到端跑通 | Medium | 04-b, 04-c |
| 04-e | AR speculator multi-step graph fusion 对齐 | Low-Medium | — |
| 04-f | Unit test + E2E test 补齐 | Medium | 04-d, 04-e |
| 04-g | 性能调优 + regression benchmark | Medium | 04-d, 04-e |

---

## 附录：核心代码片段

### `torch.cuda` → `torch.npu` patch 清单（AdaptiveVerificationManager）

```python
# adaptive_verification.py:125 — stream
self._copy_stream = torch.cuda.Stream(device)          # → torch.npu.Stream(device)

# adaptive_verification.py:160 — events
self._copy_events = [torch.cuda.Event(blocking=True)   # → torch.npu.Event(blocking=True)
                     for _ in range(2)]

# adaptive_verification.py:261-264 — copy 流程
current_stream = torch.cuda.current_stream(self.req_states.device)  # → torch.npu.current_stream
self._copy_stream.wait_stream(current_stream)                       # 不变
with stream(self._copy_stream, current_stream):                     # 确认 vllm.forward_context.stream 支持 NPU
    write_slot.copy_to_cpu()
    self._copy_events[write_idx].record()                           # 不变

# adaptive_verification.py:185 — capturing 判断
if torch.npu.is_current_stream_capturing():                         # 对应 ModelWithContext.forward 已有
```

### AttentionCGSupport 上报接口（上游约定）

```python
# 每个 Ascend attention backend 需实现
def get_attn_cg_support() -> AttentionCGSupport:
    # FULL varlen decode 需要 ALWAYS
    return AttentionCGSupport.ALWAYS
```

---

<!-- 发布说明：
- 将本文件内容复制到 GitHub Issue，移除所有注释块（<!-- ... -->）
- 将标题「Feature Request」改为「[Feature Request]」以匹配社区规范
- 去掉 Markdown 元信息表头（技术目标 / 背景前的分隔线和表格），直接保留正文
- 在 GitHub 上使用 issue template（800-others.yml 或 750-RFC.yml）
-->
