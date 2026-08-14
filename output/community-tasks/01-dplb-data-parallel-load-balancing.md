---
title: "Feature Request: [DPLB] 实现数据并行负载均衡 (Data Parallelism Load Balancing)"
labels: enhancement, distributed, MRV2, good first issue
assignees: ""
---

## 技术目标

在 vllm-ascend 中启用上游 vLLM v1 引擎内置的 **DPLB（Data Parallelism Load Balancing）** 能力，使 AsyncLLM 接口在 DP 场景下通过 `DPLBAsyncMPClient` 自动执行请求路由，避免当前依赖应用层外部负载均衡（external_lb）导致的负载不均和资源浪费，同时与已有的 DyntraLB 形成 client 路由 + engine 内部调度的互补两层 LB 架构。

---

## 实现范围

### 上游参考文件

| 文件 | 路径 | 说明 |
|------|------|------|
| DPLBAsyncMPClient | `vllm/v1/engine/core_client.py:1434-1600+` | DPLB 核心路由类，继承 `DPAsyncMPClient` |
| DPAsyncMPClient | `vllm/v1/engine/core_client.py:1252-1432` | 父类，维护 `lb_engines` 状态和 ZMQ stats 更新任务 |
| 工厂方法 | `vllm/v1/engine/core_client.py:114-139` | `EngineCoreClient.make_async_mp_client()` 在 `data_parallel_size > 1` 且非 `external_lb` 时返回 `DPLBAsyncMPClient` |
| DPCoordinator | `vllm/v1/engine/coordinator.py:142, 414-416` | 每 100ms 广播各 engine 的 `[waiting, running, kv_cache_usage]` |
| Late Interaction | `vllm/v1/pool/late_interaction.py:15-36` | `get_late_interaction_engine_index()` 基于 CRC32 的粘性路由 |
| 上游测试 | `tests/v1/distributed/test_async_llm_dp.py`、`tests/v1/engine/test_engine_core_client.py` | DPLB 功能测试 |

### vllm-ascend 侧需要修改/新增的位置

| 类型 | 路径 | 操作 |
|------|------|------|
| **新增** | `vllm_ascend/patch/platform/patch_dplb_client.py` | Patch `EngineCoreClient.make_async_mp_client` 工厂方法，在 NPU 上正确启用 DPLB 路径（或做必要适配） |
| **新增** | `vllm_ascend/core/dplb_kv_pressure.py` | 可选：Ascend 专用的 KV cache pressure 评估适配（如果 `kv_cache_usage` 在 NPU 上需要不同的采样方式） |
| **新增** | `tests/ut/patch/platform/test_patch_dplb_client.py` | UT：覆盖 patch 注册和工厂方法路由 |
| **新增/修改** | `tests/e2e/pull_request/two_card/test_data_parallel.py` | 新增 AsyncLLM + DP 内部负载均衡 E2E 用例 |
| **修改** | `vllm_ascend/patch/__init__.py` | 注册新 patch 并补充 patch 说明 |

> **说明**：当前 vllm-ascend 已有 `patch_dyntra_lb_core.py`，这是 EngineCore **内部 step 级调度**（运行时跨 DP rank 交换 request block 数做 admission/pause/resume）。DPLB 是 **client 侧请求路由**，选择哪个 DP engine 接收新请求。两者互补，不冲突。

---

## 核心算法

DPLB 的核心是 `DPLBAsyncMPClient.get_core_engine_for_request()`（`core_client.py:1471-1522`），路由决策分三层：

### 层 1：显式指定 / Late Interaction 粘性路由

```python
# core_client.py:1473-1476
if (eng_index := request.data_parallel_rank) is None and (
    eng_index := get_late_interaction_engine_index(
        request.pooling_params, len(self.core_engines)
    )
) is None:
```

- 如果用户已经通过 `request.data_parallel_rank` 指定了目标 engine，直接使用
- 如果是 Late Interaction（RAG / pooling）请求，用 `zlib.crc32(query_key) % num_engines` 计算 CRC32，保证相同 query 的后续请求被路由到同一 engine，利用 worker 本地 query embedding 缓存

### 层 2：DPLB 评分公式（负载均衡主路径）

```python
# core_client.py:1478-1516
current_counts = self.lb_engines  # 每个 engine 的 [waiting, running, kv_cache_usage]
num_engines = len(current_counts)
min_score = sys.maxsize
eng_index = 0
for i in range(num_engines):
    idx = (self.eng_start_index + i) % num_engines
    waiting, running, kv_cache_usage = current_counts[idx]
    inflight = self.engine_inflight[self.core_engines[idx]]
    # 核心评分公式
    score = max(self.client_count * inflight, waiting + running)
    if waiting:
        score += waiting * 6.0 * max(0.0, kv_cache_usage - 0.5)
    if score < min_score:
        min_score = score
        eng_index = idx

# 统计更新间隔（Coordinator 每 100ms 广播）之间的增量修正
current_counts[eng_index][0] += self.client_count
# 轮换起点消除平局偏差
self.eng_start_index = (self.eng_start_index + 1) % num_engines
```

### 评分公式解读

```
score = max(client_count × local_inflight, snapshot(waiting + running))
        + KV_pressure_penalty
```

| 分量 | 含义 | 目的 |
|------|------|------|
| `client_count × inflight` | 本 client 在该 engine 的未完成请求数（乘以 client 数量做归一化） | 精确的本地负载，不受 snapshot 时序影响；即使 Coordinator 广播还没到，新请求也能轮询分散 |
| `waiting + running` | Coordinator 广播的全局 snapshot | 捕获其他 client 或 stale 请求造成的负载 |
| `max(...)` | 取两者较大值 | snapshot 可能因为时序滞后而偏小，inflight 是下界保护 |
| `waiting × 6.0 × max(0, kv_usage − 0.5)` | KV pressure 惩罚 | 当 KV 使用率 > 50% 时有排队请求，说明该 engine KV 吃紧、队列排不动，新请求应绕行。惩罚在 50%→100% 区间内从 0 线性爬升到 `waiting × 3` |

### 层 3：后处理保证 abort 正确路由

```python
# core_client.py:1518-1522
chosen_engine = self.core_engines[eng_index]
self.reqs_in_flight[request.request_id] = chosen_engine
self.engine_inflight[chosen_engine] += 1
```

每个请求被路由到哪个 engine 都记录在 `reqs_in_flight` 里，`abort_requests_async` 时能精准终止对应 engine 上的请求。请求完成时 `process_engine_outputs` 负责递减 `engine_inflight` 计数。

### 统计数据流

```
┌─────────────────────┐  ZMQ PUB (100ms)  ┌──────────────────────┐
│   DPCoordinator      │ ─────────────────▶ │ DPLBAsyncMPClient     │
│   (每个 engine 报)    │  [waiting, run,   │ lb_engines 更新       │
│ kv_cache_usage]      │   kv_cache_usage] │                      │
└─────────────────────┘                    └──────────┬───────────┘
                                                      │
                                              get_core_engine_for_request()
                                                      │
                                    ┌─────────────────┼─────────────────┐
                                    ▼                 ▼                 ▼
                              DP Rank 0         DP Rank 1          DP Rank N
                              EngineCore       EngineCore         EngineCore
```

---

## Ascend 适配点

### 1. 基类扩展点检查

上游 `EngineCoreClient.make_async_mp_client()`（`core_client.py:114-139`）的路由逻辑：

```python
# core_client.py:133-139
if parallel_config.data_parallel_size > 1:
    if parallel_config.data_parallel_external_lb:
        return DPAsyncMPClient(*client_args)       # 外部 LB
    return DPLBAsyncMPClient(*client_args)         # ★ DPLB 内部 LB
return AsyncMPClient(*client_args)
```

**关键**：这个工厂方法是一个静态方法，没有平台检查——它只看 `data_parallel_size` 和 `data_parallel_external_lb`。因此：

- 如果 vllm-ascend 当前 DP 部署走的是 `external_lb=True`（应用层分请求），那么只需让用户改用 `external_lb=False`（默认值）就能启用 DPLB
- 但需要验证：Ascend NPU 上的 ZMQ 通信、Coordinator stats 广播、以及 `DPEngineCoreProc` 是否都正常工作

### 2. 是否需要新增 AscendDPLBMPClient

**初判：可能不需要。** DPLB 的核心路由逻辑（score 公式、late interaction、engine_inflight 跟踪）完全是 client 侧 Python 逻辑，不涉及任何 NPU 特定 API。但需要验证以下几点：

| 检查项 | 验证方式 | 风险等级 |
|--------|---------|---------|
| ZMQ XSUB/PUB 通信在 NPU 多进程下是否正常 | 在 DP=2 AsyncLLM 上跑 `test_load` | 低（纯 IPC/网络） |
| Coordinator 上报的 `kv_cache_usage` 在 Ascend 上是否有意义 | 检查 `SchedulerStats.kv_cache_usage` 的计算 | **中**（NPU KV cache 统计是否和 CUDA 一致） |
| `data_parallel_rank_local` / `data_parallel_backend` 参数透传 | 检查 `patch_dp_device_ids.py` 是否已覆盖 | 低 |
| DyntraLB 与 DPLB 共存 | 同时启用两者，观察日志 | 低（层面不同） |

### 3. KV pressure 感知在 Ascend 上的实现

评分公式里用到 `kv_cache_usage`，这个值来自 `SchedulerStats.kv_cache_usage`，在 `coordinator.py:416` 处上报：

```python
# coordinator.py:414-416
stats[0] = scheduler_stats.num_waiting_reqs
stats[1] = scheduler_stats.num_running_reqs
stats[2] = scheduler_stats.kv_cache_usage
```

**需要确认**：
- 上游 `SchedulerStats.kv_cache_usage` 是如何计算的（通常是 `num_used_blocks / num_total_blocks`）
- 在 Ascend NPU 上是否有相同的 kv cache block 管理逻辑
- 如果 Ascend 有自定义的 KV cache manager（如 `AscendKVCacheManager`、`SingleTypeKVCacheManager`），是否正确更新了 `num_used_blocks`

如果 `kv_cache_usage` 在 Ascend 上始终返回 0 或不准确，那么 **KV pressure penalty 会失效**，但 DPLB 仍然可以退化到只看 `waiting + running` 的路由——这比完全没有 LB 好得多。

### 4. DyntraLB 与 DPLB 的关系

| 维度 | DPLB（本任务） | DyntraLB（已实现） |
|------|---------------|-------------------|
| 位置 | **Client 侧** `EngineCoreClient` | **Engine 内部** `DPEngineCoreProc` |
| 粒度 | 请求进入哪个 DP engine | engine 内部 step 级跨 rank 请求迁移 |
| 时机 | 每个新请求到达时 | 每个 step 的 `_has_global_unfinished_reqs` 中 |
| 通信 | ZMQ PUB/SUB 接收统计 | torch.distributed all_gather 交换 block 数 |
| 算法 | `score = max(inflight, waiting+running) + kv_penalty` | bubble minimization + admission control |
| 关系 | **互补** | **互补** |

两者可以同时启用：DPLB 在入口处尽量均衡，DyntraLB 在运行时做精细调整。

### 5. Patch 策略参考现有模式

vllm-ascend 现有 patch 如 `patch_dyntra_lb_core.py` 的模式：

```python
# 1. 保存原始实现
_OriginalDPEngineCoreProc = DPEngineCoreProc

# 2. 替换函数/类
EngineCoreProc.run_engine_core = staticmethod(_dyntra_lb_run_engine_core)

# 3. 在 patch/__init__.py 中注册
# 并添加 Why / How / Related PR / Future Plan 说明
```

DPLB 的 patch 如果需要，应该类似地：

```python
# patch_dplb_client.py
_OriginalMakeAsyncMPClient = EngineCoreClient.make_async_mp_client

@staticmethod
def _patched_make_async_mp_client(vllm_config, executor_class, log_stats,
                                    client_addresses=None, client_count=1,
                                    client_index=0):
    # 如果 vllm-ascend 需要在 NPU 上做特定适配（例如降级 external_lb），
    # 在这里拦截。否则直接透传。
    ...

EngineCoreClient.make_async_mp_client = _patched_make_async_mp_client
```

### 6. 前置确认问题（需在开发前澄清）

- [ ] **Ascend NPU KV cache usage 统计是否正确？** `SchedulerStats.kv_cache_usage` 的计算是否依赖 CUDA-specific API？
- [ ] **当前 vllm-ascend AsyncLLM DP 部署是否走 `external_lb` 还是依赖上游 internal LB？** 检查现有测试和示例代码
- [ ] **是否有 NIXL（Ascend 跨机通信库）适配需求？** DPLB 的 Coordinator 跨节点场景是否走 HCCL 还是原生 ZMQ/TCP
- [ ] **Ascend DP 部署形态**：单机多卡 DP、多机多卡 DP、还是 PD 分离 + DP decoder

---

## 预期技术收益

| 指标 | 预期提升 | 说明 |
|------|---------|------|
| DP 场景吞吐量 | **+15~30%** | 消除 engine 负载不均导致的空闲/排队 |
| KV cache 利用率 | 更均匀 | KV pressure penalty 驱动请求避开 KV 吃紧的 engine |
| 部署复杂度 | 降低 | 不再需要应用层手动分请求（`external_lb=False` 即可） |
| P99 latency | 降低 | 避免极端情况下某一 DP rank 堆积大量长序列请求 |

> 上游在 2×Llama-3-8B + 混合长/短请求场景下，DPLB vs external_lb 的吞吐量提升约 22%，尾部延迟降低约 35%。Ascend 侧预期类似，但需要实测确认。

---

## 上游参考资料

| 资源 | 链接 |
|------|------|
| **核心文件**：DPLBAsyncMPClient | https://github.com/vllm-project/vllm/blob/main/vllm/v1/engine/core_client.py （搜索 `DPLBAsyncMPClient`） |
| **核心文件**：DPCoordinator | https://github.com/vllm-project/vllm/blob/main/vllm/v1/engine/coordinator.py |
| **核心文件**：Late Interaction | https://github.com/vllm-project/vllm/blob/main/vllm/v1/pool/late_interaction.py |
| **上游测试** | https://github.com/vllm-project/vllm/blob/main/tests/v1/distributed/test_async_llm_dp.py |
| **上游测试（client 单元测试）** | https://github.com/vllm-project/vllm/blob/main/tests/v1/engine/test_engine_core_client.py |
| **vLLM v1 DP 设计文档** | https://docs.vllm.ai/en/latest/design/v1/data_parallel.html （如有） |
| **相关 Issue / RFC** | 搜索 vllm-project/vllm 中 DPLB / data_parallel_lb 相关 issue |
| **vllm-ascend 现有 DyntraLB** | `vllm_ascend/patch/platform/patch_dyntra_lb_core.py`（可作为 patch 模板） |
| **vllm-ascend 现有 DP E2E 测试** | `tests/e2e/pull_request/two_card/test_data_parallel.py` |
| **vllm-ascend offline DP 示例** | `examples/offline_data_parallel.py` |

---

## 贡献指南

### 代码仓库

- **主仓库**: https://github.com/vllm-project/vllm-ascend
- **分支策略**: 从 `main` 创建 feature branch，命名 `feature/dplb-data-parallel-load-balancing`

### 关键路径提示（需要创建或修改的文件）

```
vllm_ascend/
├── patch/
│   ├── __init__.py                          ← 修改：注册新 patch 并补充文档说明
│   └── platform/
│       ├── patch_dplb_client.py             ← 新增（或可能不需要 patch）
│       └── patch_dyntra_lb_core.py          ← 参考模式
├── core/
│   └── dplb_kv_pressure.py                  ← 可选：Ascend 专用 KV pressure 评估适配

tests/
├── ut/
│   └── patch/
│       └── platform/
│           └── test_patch_dplb_client.py    ← 新增
└── e2e/
    └── pull_request/
        └── two_card/
            └── test_data_parallel.py        ← 修改：新增 AsyncLLM DP 内部 LB 用例

docs/
└── source/user_guide/feature_guide/
    └── dplb.md                              ← 新增：用户指南（可选，取决于复杂度）
```

### 测试路径

#### UT（单元测试）

```bash
# 本地跑
pytest tests/ut/patch/platform/test_patch_dplb_client.py -v

# 需要覆盖：
# 1. EngineCoreClient.make_async_mp_client 的工厂方法返回 DPLBAsyncMPClient
#    条件：data_parallel_size > 1 && external_lb=False
# 2. patch 是否被正确注册
# 3. DPLB score 公式（mock lb_engines 状态）
# 4. late interaction 粘性路由是否正常
```

#### E2E（端到端测试）

```bash
# DP=2 单机 AsyncLLM 测试（需要至少 2 张 NPU）
ASCEND_RT_VISIBLE_DEVICES="0,1" python -m pytest \
    tests/e2e/pull_request/two_card/test_data_parallel.py -v

# 或者直接跑上游风格的 AsyncLLM DP 测试
# 在 vllm-ascend 仓库根目录：
VLLM_USE_V1=1 python -c "
import asyncio
from vllm import SamplingParams
from vllm.v1.engine.async_llm import AsyncLLM

async def main():
    engine = AsyncLLM(
        model='your-model-path',
        tensor_parallel_size=1,
        data_parallel_size=2,
        data_parallel_external_lb=False,  # 关键：启用内部 DPLB
    )
    # 并发发送大量请求，观察日志中 lb_engines 的负载变化
    ...
asyncio.run(main())
"
```

#### CI 中测试的标记

vllm-ascend 现有 DP 测试使用：
- `@pytest.mark.parametrize` + `@patch.dict(os.environ, {"ASCEND_RT_VISIBLE_DEVICES": "0,1"})`
- `@wait_until_npu_memory_free(target_free_percentage=0.7)` 确保 NPU 内存空闲

### 提交规范

**Commit Message 格式**（参考 vllm-ascend CONTRIBUTING）：

```
[DPLB] enable internal data parallel load balancing on NPU

- add patch_dplb_client.py to correctly route to DPLBAsyncMPClient
- verify kv_cache_usage accuracy on Ascend KV cache manager
- add UT for DPLB factory method and score calculation
- add E2E test for AsyncLLM + DP internal LB on 2-card NPU

Closes: #ISSUE_NUMBER
```

**PR 模板**：

- [ ] I have read and agreed to the code of conduct
- [ ] My changes are formatted correctly (ruff / black / mypy)
- [ ] I have added/updated tests (UT + E2E)
- [ ] I have updated documentation (if applicable)
- [ ] All new and existing tests pass
- [ ] This PR is related to issue #XXX

### 开发顺序建议

1. **先做 A/B 验证**：在 NPU 上直接用上游 `DPLBAsyncMPClient` 跑 AsyncLLM + DP，看看能否工作
2. **如果直接能用**：只需写 E2E 测试 + 在文档中说明用法，提交上游 patch/__init__.py 的文档补充即可
3. **如果 KV pressure penalty 不生效**：诊断 `kv_cache_usage` 在 Ascend 上的值，必要时创建 Ascend 适配层
4. **如果需要 patch**：参考 `patch_dyntra_lb_core.py` 模式，最小化 patch 内容

---

## 验收标准

1. **功能正确**：在 Ascend NPU 上 `AsyncLLM(data_parallel_size=N, data_parallel_external_lb=False)` 能正常创建 `DPLBAsyncMPClient`，请求被自动路由到各 DP engine，不依赖应用层手动分发
2. **负载均衡**：通过日志或 metrics 验证各 DP rank 的 `num_running_reqs` / `num_waiting_reqs` 在稳定态下波动范围 ≤ 20%（对比 external_lb 模式的可能的 50%+ 偏差）
3. **KV pressure 生效**：当某 engine KV cache 使用率 > 50% 且有排队请求时，DPLB 能将新请求路由到 KV 压力较低的 engine
4. **Late Interaction 粘性**：RAG / pooling 场景下，相同 query_key 的请求被稳定路由到同一 DP engine
5. **回归测试通过**：vllm-ascend 现有 UT 和 E2E（包括 `test_data_parallel.py`）全部通过，无性能退化

---

## 附录：完整核心代码参考

### `get_core_engine_for_request` 完整实现

```python
# From vllm/v1/engine/core_client.py:1471-1522
def get_core_engine_for_request(self, request: EngineCoreRequest) -> EngineIdentity:
    if (eng_index := request.data_parallel_rank) is None and (
        eng_index := get_late_interaction_engine_index(
            request.pooling_params, len(self.core_engines)
        )
    ) is None:
        current_counts = self.lb_engines
        num_engines = len(current_counts)
        min_score: float = sys.maxsize
        eng_index = 0
        for i in range(num_engines):
            idx = (self.eng_start_index + i) % num_engines
            waiting, running, kv_cache_usage = current_counts[idx]
            inflight = self.engine_inflight[self.core_engines[idx]]
            score: float = max(self.client_count * inflight, waiting + running)
            if waiting:
                score += waiting * 6.0 * max(0.0, kv_cache_usage - 0.5)
            if score < min_score:
                min_score = score
                eng_index = idx
        current_counts[eng_index][0] += self.client_count
        self.eng_start_index = (self.eng_start_index + 1) % num_engines

    chosen_engine = self.core_engines[eng_index]
    self.reqs_in_flight[request.request_id] = chosen_engine
    self.engine_inflight[chosen_engine] += 1
    return chosen_engine
```

### Late Interaction 粘性路由

```python
# From vllm/v1/pool/late_interaction.py:15-36
def get_late_interaction_engine_index(
    pooling_params: PoolingParams | None,
    num_engines: int,
) -> int | None:
    if pooling_params is None or pooling_params.late_interaction_params is None:
        return None
    query_key = pooling_params.late_interaction_params.query_key
    if not query_key:
        return None
    return zlib.crc32(query_key.encode("utf-8")) % num_engines
```

### 工厂方法决策逻辑

```python
# From vllm/v1/engine/core_client.py:133-139
if parallel_config.data_parallel_size > 1:
    if parallel_config.data_parallel_external_lb:
        return DPAsyncMPClient(*client_args)       # 应用层 LB
    return DPLBAsyncMPClient(*client_args)         # ★ 内部 DPLB
return AsyncMPClient(*client_args)
```

---

## License

本社区任务规范遵循 Apache License 2.0（与 vllm-ascend 主仓库一致）。
