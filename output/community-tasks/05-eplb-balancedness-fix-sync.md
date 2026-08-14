# Issue/Task: [EPLB] 同步 upstream balancedness 计算修复并验证 Ascend EPLB 正确性

## 技术目标

对比 upstream `vllm.distributed.eplb` 与 vllm-ascend 两条 EPLB 实现线的 **balancedness（负载均衡度）计算逻辑**，确认 Ascend 是否存在同类 bug，或输出一份完整的验证报告。

---

## 背景

### upstream 侧

vllm 主仓库的 EPLB 在 PR #51813（待确认 PR 编号，以下游 merge commit 为准）中修复了 `eplb_state.py` 的 balancedness 计算。核心修复涉及：

**文件**：`vllm/distributed/eplb/eplb_state.py`

```python
# eplb_state.py:64-69 — upstream 最终版
def _compute_eplb_load_stats(
    num_tokens_per_rank: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    avg_tokens = num_tokens_per_rank.mean(dim=1).sum()
    max_tokens = num_tokens_per_rank.max(dim=1).values.sum()
    return avg_tokens, max_tokens
```

balancedness 定义（`eplb_state.py:604`）：

```python
balancedness = avg_tokens / max_tokens if max_tokens > 0 else 0.0
```

其中 `num_tokens_per_rank` 形状为 `(num_moe_layers, num_ranks)`，即**先按 layer 内各 rank 求均值/最大值，再跨 layer 求和**。

### Ascend 侧（关键：有两条独立实现线）

vllm-ascend 仓库**同时维护两套 EPLB 路径**，必须都验证：

| 路径 | 入口 | 状态 |
|------|------|------|
| **路径 A：继承 upstream** | `vllm_ascend/distributed/eplb_state.py:81` `AscendEplbState` 继承 `vllm.distributed.eplb.EplbState` | 直接使用 upstream 的 balancedness 计算，bug 自动同步 |
| **路径 B：完全独立重写** | `vllm_ascend/eplb/` 整个包（4 种策略） | ⚠️ 独立实现，**不走 upstream 的 `_compute_eplb_load_stats`** |

路径 B 的 TODO 注释已经明写最终目标是移除：

- `vllm_ascend/eplb/core/policy/policy_default_eplb.py:2` — `Todo: Once https://github.com/vllm-project/vllm/pull/24069 is merged in vllm. Remove this policy.`
- `vllm_ascend/eplb/core/policy/policy_flashlb.py:2` — `Todo: Remove this policy after vllm-project/vllm/pull/24069 is merged into vllm.`

但在此之前，路径 B 是独立运行的，其 balancedness 计算逻辑与 upstream 有**语义差异**（下文详述）。

---

## 对比点（4 个关键维度）

### 1. 负载窗口更新逻辑（滑动窗口 vs 固定窗口）

| 仓库 | 机制 | 代码位置 |
|------|------|---------|
| upstream | **环形滑动窗口**，`expert_load_window_step` 递增取模，写入 `expert_load_window[step]`，窗口大小 `eplb_config.window_size` | `eplb_state.py:620-633` |
| Ascend 路径 A | 继承 upstream，完全一致 | `vllm_ascend/distributed/eplb_state.py:88-96` 仅加了 `_has_fresh_recorded_load` 门控 |
| Ascend 路径 B (FlashLB) | **独立滑动窗口**，在 `register_hotness()` 中用环形 buffer + `(start + t) % window_length` 更新 | `policy_flashlb.py:678-729` |

**潜在风险**：窗口数据来源不同 — upstream 从 `expert_load_window.sum(dim=0)` 聚合（`eplb_state.py:788`），FlashLB 从 `hotness_window["buffer"]` 取 `[start : start+length] % max_obs`（`policy_flashlb.py:920-921`）。如果 upstream 修复涉及窗口**聚合方式**（如 `.sum(dim=0)` 对环形窗口是否正确），FlashLB 可能有不同表现。

### 2. balancedness 计算公式（核心对比）

**upstream 定义**（`eplb_state.py:604`）：

```
balancedness = Σ_layer mean(layer_load_per_rank) / Σ_layer max(layer_load_per_rank)
```

**Ascend 路径 B 各策略的定义**（⚠️ 与 upstream 语义不同）：

| 策略 | 指标名 | 公式 | 代码位置 |
|------|--------|------|---------|
| DefaultEplb | 无显式 balancedness | 用 `max_heat_per_layer_after / max_heat_per_layer_before` 比较前后 | `policy_default_eplb.py:341` |
| FlashLB | `average_to_peak_ratio = 1 / score` | `score = (max_load * D + ε) / (total_load + ε)`，即 **max / avg** 的近似 | `policy_flashlb.py:293-323` (`compute_score`) |
| SwiftBalanceEplb | `imbalance = max_load / avg_load` | 每 layer 内 `max(rank_load) / avg(rank_load)` | `policy_swift_balancer.py:106-137` |
| RandomLoadBalance | 无 | 只做固定两个卡的 expert 交换 | `policy_random.py:11-26` |

**关键发现**：SwiftBalanceEplb 的 `calculate_imbalance`（`policy_swift_balancer.py:106-137`）公式中存在一个**可疑的分母** — 它用的是 `total_load / self.num_ranks`，而 `total_load` 已经是所有 rank 负载之和，所以 `avg_load = total_load / num_ranks` 看起来是对的。但让我们验证一下...

```python
# policy_swift_balancer.py:121-134（简化）
total_load = 0
for rank in layer:
    rank_load = 0
    for expert_id in rank:
        update_workload = cur_experts_load[layer_id][expert_id] / num_per_expert[layer_id][expert_id]
        rank_load += update_workload
        total_load += update_workload          # ← 累加到 total_load
    cur_layer_max_load = max(cur_layer_max_load, rank_load)
avg_load = total_load / self.num_ranks        # ← 除的是 num_ranks
cur_layer_imbalance = cur_layer_max_load / avg_load
```

这里有个值得检查的点：`total_load` 的累加位置是在内层 `for expert_id in rank` 循环中，而不是在外层 `for rank in layer` 循环之后。这意味着它累加的是每个 expert 分片的 workload，然后除以 rank 数。数学上是否等价于 `Σrank rank_load / num_ranks`？理论上是的（加法交换律），但如果 rank_load 在某个条件下没被正确累加，就会出错。**这个需要用 UT 验证**。

### 3. replicate_experts 权重分配

| 仓库 | 算法 | 代码位置 |
|------|------|---------|
| upstream DefaultEplbPolicy | 贪心：每次给 `argmax(weight / logcnt)` 的 expert 加 replica | `policy/default.py:97-101` |
| Ascend DefaultEplb | 非层级化贪心：每次给 `max(avg_weight)` 的 expert 加，更新为 `new_avg = raw_weight / (cur_redundancy+1)` | `policy_default_eplb.py:125-135` |
| Ascend FlashLB | 3 种可选策略：`min_max_replica`（给 max value expert 加）、`max_delta`、`percentage`（按比例） | `policy_flashlb.py:24-172` |
| Ascend SwiftBalanceEplb | 节点内（intra-node）贪心：受 `num_max_com`（通信上限）约束 | `policy_swift_balancer.py:175-225` (`compute_redundant_assignments`) |

### 4. balanced_packing 贪心策略

| 仓库 | 算法 | 代码位置 |
|------|------|---------|
| upstream | 按 group 分三层（group→node→GPU），每层用贪心法装桶，装完标记为 `np.inf` 不再参与 | `policy/default.py:38-73` |
| Ascend DefaultEplb | 单层面贪心法装桶，先把所有 weighted item 按权重排序再依次找最轻的 box | `policy_default_eplb.py:125-190` |
| Ascend FlashLB | LPT 贪心部署到 device，同时考虑方差和协方差（`compute_updated_device_variance`） | `policy_flashlb.py:211-290` (`lpt_deployment`) |
| Ascend SwiftBalanceEplb | 先 redundancy，再 node 内 rank 间 swap 交换（`swap_experts_between_ranks`），最多 100 轮 | `policy_swift_balancer.py:510-633` |

---

## 预期收益

- **Bug 修复（如果发现）**：路径 B 的 balancedness 计算如果有 bug（如 SwiftBalanceEplb 的 `total_load` 累加位置、FlashLB 的 `compute_score` epsilon 引入偏差），修复后避免长期运行时 expert 负载不均衡累积。
- **验证报告（如果无 bug）**：为 upstream PR #51813 在 Ascend 平台上的影响提供一个完整的对比基线，为最终移除路径 B 提供依据。
- **测试覆盖率**：补充 Ascend 特有的 UT 覆盖 balancedness 边界情况（全零负载、单 expert、单 rank）。

---

## 上游参考

| 项目 | 路径 |
|------|------|
| PR #51813（balancedness fix） | `https://github.com/vllm-project/vllm/pull/51813` |
| upstream balancedness 计算 | `vllm/distributed/eplb/eplb_state.py:64-69` (`_compute_eplb_load_stats`) |
| upstream balancedness 使用处 | `vllm/distributed/eplb/eplb_state.py:592-604` |
| upstream window 更新 | `vllm/distributed/eplb/eplb_state.py:620-633` |
| upstream DefaultEplbPolicy | `vllm/distributed/eplb/policy/default.py` |
| upstream 测试 | `tests/distributed/test_eplb_algo.py:15-28` (`test_eplb_load_stats_reduce_across_ranks`) |

---

## Ascend 代码路径速查

```
vllm-ascend/
├── vllm_ascend/
│   ├── distributed/
│   │   ├── eplb_state.py          ← 路径 A：继承 upstream 的 AscendEplbState (L81)
│   │   └── eplb_communicator.py   ← HCCL communicator 包装 (L7)
│   └── eplb/                       ← 路径 B：独立重写的 4 种策略
│       ├── eplb_updator.py        ← updator 入口（L32, 负载收集窗口逻辑）
│       └── core/policy/
│           ├── policy_default_eplb.py     ← DefaultEplb (L27, balanced_pack 入口 L125)
│           ├── policy_flashlb.py          ← FlashLB (L515, compute_score L293, sliding window L590/682)
│           ├── policy_random.py            ← RandomLoadBalance (L11)
│           └── policy_swift_balancer.py   ← SwiftBalanceEplb (L29, calculate_imbalance L106)
tests/ut/
├── eplb/test_eplb_updator.py               ← updator UT
└── distributed/test_eplb_state.py           ← eplb_state UT
```

---

## 贡献指南

### 仓库位置

- **upstream**: `https://github.com/vllm-project/vllm`（分支匹配 PR #51813 的 base）
- **vllm-ascend**: `https://github.com/vllm-project/vllm-ascend`

### 对比方法（建议步骤）

**Step 1 — 确认 upstream PR #51813 的具体变更**

```bash
cd .tmp_vllm
git fetch origin pull/51813/head:pr-51813
git diff main...pr-51813 -- vllm/distributed/eplb/eplb_state.py
```

重点关注：
- `_compute_eplb_load_stats` 的修复（是否从 per-step 变成了跨 layer 聚合？或者修复了 `.sum()` 维度？）
- `expert_load_window` 的聚合方式（`eplb_state.py:788` 的 `global_expert_load_window = logical_expert_load_window.sum(dim=0)`）

**Step 2 — 路径 A 验证**

路径 A 直接继承 upstream 的 balancedness 计算，理论上 upstream 修复后自动生效。需要确认的是：Ascend 是否覆盖了 `step()` 或 `rearrange()` 改变了 balancedness 计算路径。

检查 `vllm_ascend/distributed/eplb_state.py`：
- `AscendEplbState.step()` (L88-96)：只加了 `_has_fresh_recorded_load`，然后 `super().step()` — **不改变 balancedness 计算** ✅
- `AscendEplbState.rearrange()` (L124-149)：只加了 freshness gate 和 routing table 刷新，然后 `super().rearrange()` — **不改变 balancedness 计算** ✅

**Step 3 — 路径 B 验证**

这是核心工作。建议：

3a. **FlashLB `compute_score`**（`policy_flashlb.py:293-323`）：
   - 当前公式：`(max_load * D + 1e-2) / (total_load + 1e-2)`
   - 对比 upstream：upstream 用 `mean / max`（即 `Σlayer mean_ranks / Σlayer max_ranks`），FlashLB 用 `max_device_load / avg_device_load`
   - **关键问题**：upstream 是跨 layer 求和后相除，FlashLB 是 per-step（time step）计算后 mean。这两种指标在数学上不等价！
   - 验证 UT：构造一个 layer 间负载差异极大的场景，看 FlashLB 的 `average_to_peak_ratio` 是否与 upstream `balancedness` 趋势一致

3b. **SwiftBalanceEplb `calculate_imbalance`**（`policy_swift_balancer.py:106-137`）：
   - 确认 `total_load` 在 expert 循环内累加是否正确
   - 对比 upstream 的 balancedness 方向（upstream：越大越好，Swift：imbalance 越小越好）

3c. **DefaultEplb 无显式 balancedness**：它用 `max_heat_per_layer_after / max_heat_per_layer_before` 作为改进率，这是**前后对比指标**而非绝对 balancedness。需要确认这个比率的语义是否等价于 upstream 的 balancedness 变化量。

### UT 路径

| 测试 | 位置 | 覆盖范围 |
|------|------|---------|
| upstream balancedness 计算 | `tests/distributed/test_eplb_algo.py:15-28` | `_compute_eplb_load_stats` reduce 维度 |
| Ascend updator | `tests/ut/eplb/test_eplb_updator.py` | `compute_and_set_moe_load` 维度 |
| Ascend eplb_state | `tests/ut/distributed/test_eplb_state.py` | `AscendEplbState` 继承行为 |
| Ascend load collection | `tests/ut/worker/v2/test_eplb_load_collection_phase.py` | `_should_record_current_step` 窗口门控 |

### 建议新增 UT 覆盖

1. **SwiftBalanceEplb `calculate_imbalance` 正确性** — 构造已知 workload 和 deployment，手算 imbalance 并对比函数输出
2. **FlashLB `compute_score` 边界情况** — 全零 expert load（epsilon 保护是否合理）
3. **跨 layer 聚合一致性** — 构造 layer 负载差异场景，对比 upstream balancedness vs FlashLB average_to_peak_ratio 的趋势方向
4. **窗口环形写入正确性** — 窗口 size=2, step interval=5, 验证各 step 的 window 内容与理论一致

---

## 验收标准

- [ ] **交付物 1：对比报告**（Markdown），包含：
  - upstream PR #51813 的具体 diff 摘要
  - 路径 A 确认：继承 upstream，bug 自动同步 ✓
  - 路径 B 4 策略逐一对比 balancedness 计算公式，标注与 upstream 的差异
  - 如果发现 bug → 见交付物 2
- [ ] **交付物 2：Bug 修复 PR**（仅当验证发现 bug 时）
  - 路径 B 的 balancedness 计算修复
  - 对应 UT 覆盖
  - 回归测试通过（`pytest tests/ut/eplb/ tests/ut/distributed/test_eplb_state.py -v`）
- [ ] **交付物 3：最终结论**
  - 如果路径 B 无 bug：标注"路径 B balancedness 计算与 upstream 语义不同但数学正确"，并建议将其纳入 upstream 的测试矩阵以最终废弃
  - 如果路径 B 有 bug：修复并标注修复内容

---

## 前置说明（重要）

Ascend EPLB 可能**没有这个 bug**，因为它的路径 B 是独立重写，根本不走 upstream 的 `_compute_eplb_load_stats`。在这种情况下，任务价值转变为：

1. **验证报告**：确认路径 B 的 balancedness 计算在数学上是正确的，只是**语义定义不同**（FlashLB/Swift 用的是 `max/avg` 比，upstream 用的是 `avg/max` 比）
2. **为废弃路径 B 做准备**：4 个策略文件都有 TODO 标注等待 upstream PR #24069 merge 后移除，验证报告可以加速这个进程
3. **提升 UT 覆盖率**：Ascend 的 4 策略目前缺少 balancedness 边界情况测试

**判断路径 B 是否有 bug 的快速方法**：构造一个简单场景

```python
# 手动验证：4 个 rank，2 个 layer，某 rank 极不均衡
import numpy as np

# Layer 0: rank0=100, rank1=0, rank2=0, rank3=0
# Layer 1: rank0=0, rank1=100, rank2=0, rank3=0
# upstream balancedness = (25 + 25) / (100 + 100) = 50/200 = 0.25
# FlashLB compute_score ≈ 最大 device 负载 * D / total_load
# SwiftBalanceEplb imbalance = max/avg = 100/25 = 4.0 per layer

# 如果某策略输出的结果与预期方向相反（例如 balancedness 高时它却报高 imbalance），
# 可能存在分母或分子的维度错误
```

---

## 标签

`good-first-issue` · `help-wanted` · `eplb` · `balancedness` · `upstream-sync`
