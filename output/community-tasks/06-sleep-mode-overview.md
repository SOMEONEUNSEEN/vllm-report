# [Sleep Mode] HCCL 通信域轻量化操作 + ACL Graph 原地恢复 — 总体规划

> **标签建议**: `enhancement`, `sleep-mode`, `MRV2`, `aclgraph`, `hccl`, `good first issue`
> **关联上游**: [#45623 Offload CUDA graph + NCCL communicator memory](https://github.com/vllm-project/vllm/pull/45623) 、 [#51485 Release NCCL communicator memory](https://github.com/vllm-project/vllm/pull/51485)

---

## ⚠️ 拆分说明 · 全部可并行（2026-08-14）

本文件是总体规划，已拆分为 **4 个独立、可并行实现的子任务**。每个都有明确的 done 标准、内置调研步骤、以及降级路径——**无任何硬前置依赖**，开源贡献者可随意挑选任何一个开始。

| # | 文件 | 难度 | 可独立交付 | 与其他任务冲突 |
|---|------|------|-----------|---------------|
| 08 | [HCCL 通信域 destroy→suspend/resume 轻量化](file:///c:/code/vllm-report/output/community-tasks/08-hccl-suspend-resume-refactor.md) | 🟡 中等 | ✅ 是 | 软冲突: `sleep_mem_optimized.py` 中改 HcclSleepWakeupManager 类（与 09/10 的 AclGraphSleepWakeupManager 类不同，merge 几乎零冲突） |
| 09 | [ACL Graph Workspace 单独释放](file:///c:/code/vllm-report/output/community-tasks/09-aclgraph-workspace-release.md) | 🟢 简单 | ✅ 是 (good first issue) | 软冲突: `aclgraph_utils.py` / `acl_graph.py`（与 10 同文件但改不同逻辑层） |
| 10 | [ACL Graph 原地恢复（vmap + remap）](file:///c:/code/vllm-report/output/community-tasks/10-aclgraph-inplace-restore.md) | 🔴 困难 | ✅ 是（可独立 PoC） | 软冲突: `sleep_mem_optimized.py` + `aclgraph_utils.py` + `acl_graph.py`（建议 09 先合入，10 在此基础上 rebase）|
| 11 | [接入上游 SleepModeBackend 抽象](file:///c:/code/vllm-report/output/community-tasks/11-sleepmodebackend-integration.md) | 🟡 中等 | ✅ 是 | **零冲突**：新建 `ascend_sleep_backend.py` + 改 `platform.py` / `worker.py`，不碰 08/09/10 的任何文件 |

**关键设计：没有硬依赖**

- 调研内容（CANN HCCL suspend/resume API 是否存在？vmap 是否可用？）**内联到每个任务的 Step 0**，不是前置关卡
- 每个任务都有**降级路径**：即使平台 API 不存在，任务仍能推进（如 08 降级为 "把 HCCL buffer 走 CaMemAllocator"；10 降级为 "跳过，仅推进 09 的 workspace 释放"）
- 所有任务可以**在同一个 base commit 上并行开 fork 分支独立开发**，最后按 "11 → 08 → 09 → 10" 的顺序合入（merge 冲突最小化）

**推荐合入顺序**（软建议，不是硬阻塞）：
```
PR#1: 11 (backend)          → 零冲突，任何人都可以先提
PR#2: 08 (HCCL suspend)    → 只改 patch_distributed + sleep_mem_optimized（不同类）
PR#3: 09 (workspace)        → 改 aclgraph_utils + sleep_mem_optimized（不同类）
PR#4: 10 (inplace restore)  → 基于 09 的 workspace save/restore 扩展 graph pool offload
```

**每个子任务独立可发布为 GitHub Issue**。

---

## 1. 技术目标（总体规划）

优化 vllm-ascend Sleep/Wake 模式的恢复效率：

1. **HCCL 通信域轻量化操作**：Sleep 时用 suspend/resume 替代 destroy/recreate，保留 communicator identity 和拓扑，只释放其动态 NPU buffer
2. **ACL Graph 原地恢复**：Wake 后不再重新执行 `profile_run + capture_model()`，而是将 graph memory 从 CPU 原地恢复到 NPU，保持 capture 结果不变

---

## 2. 背景与当前问题

### 2.1 上游 vLLM 的演进方向

上游 vLLM 正在把 Sleep/Wake 从"只 offload 权重/KV cache"扩展到释放更多 GPU 内存：

| 上游 PR | 核心思路 | 释放量 | 恢复方式 |
|---------|----------|--------|----------|
| **#45623** | CUDA graph pool 路由进 CuMemAllocator + 原地恢复 | CUDA graph ~90 MiB/GPU（dense ~99%）| **In-place restore（无 re-capture）** |
| **#45623 / #51485** | NCCL 用 `ncclCommSuspend(NCCL_SUSPEND_MEM)` + `ncclCommResume` | NCCL ~960 MiB/GPU（TP2~TP8）| **In-place resume（保留 communicator）** |

上游的关键设计原则：**"释放 buffer，不销毁 identity"**，这样恢复是零创建成本的。

### 2.2 vllm-ascend 当前做法（问题所在）

vllm-ascend 有两套机制：
- **CaMemAllocator**（始终开启）：权重/KV cache offload → CaMemAllocator 用 CANN-mem 做 D2H/H2D
- **SleepWakeupManager**（`enable_sleep_mode_extra_cleanup=True` 才开启）：额外清理 HCCL + ACL graph

关键问题对比：

| 维度 | 上游 vLLM | vllm-ascend 当前 | 差距 |
|------|----------|------------------|------|
| **Communicator** | `ncclCommSuspend` / `ncclCommResume`（保留 identity，只释放 buffer） | `destroy_process_group` + `new_group`（**硬销毁 + 硬重建**） | TP/PP/DP 多 group 时开销显著 |
| **Graph** | CuMemAllocator 原地恢复（**no re-capture**） | `capture_model()`（**重新 profile_run + ACL graph capture**） | FULL graph 重捕获耗时（DeepSeek V4 ~30s+）|
| **Total freed** | ~1 GiB/GPU（NCCL 960 + graphs 90） | 未知（取决于 HCCL buffer + graph workspace 大小）| ACL graph workspace 可能达 GB 级 |

### 2.3 vllm-ascend 代码路径速查

| 文件 | 作用 |
|------|------|
| `vllm_ascend/worker/worker.py:221-269` | `NPUWorker.sleep()` / `wake_up()` 入口 |
| `vllm_ascend/device_allocator/sleep_mem_optimized.py:67-128` | `AclGraphSleepWakeupManager` — sleep 清空 graph，wake **重跑 capture_model()** |
| `vllm_ascend/device_allocator/sleep_mem_optimized.py:131-186` | `HcclSleepWakeupManager` — sleep 走 destroy_hccl，wake 走 restore_hccl |
| `vllm_ascend/patch/worker/patch_distributed.py:300-316` | `destroy_hccl()` / `restore_hccl()` — destroy 走 `destroy_process_group`，restore 走 `new_group("hccl")` |
| `vllm_ascend/patch/worker/_hccl_pg_registry.py:94-158` | `HcclPgRegistry` — refcount 注册表，destroy 时 entry 删除 |
| `vllm_ascend/worker/v2/aclgraph_utils.py:68-168` | `ModelAclGraphManager` — FULL 模式完整 ACL graph capture |
| `vllm_ascend/compilation/acl_graph.py:60-249` | `ACLGraphWrapper` — PIECEWISE 模式 ACL graph capture/replay |

---

## 3. 实现范围

### 3.1 Part A — HCCL 通信域轻量化操作（P1）

#### 核心思路

类似上游 `ncclCommSuspend/Resume`，在 Ascend 上找到或实现等价机制：

```
HCCL Sleep 流程（当前）:
  destroy_process_group(group)        # 销毁 communicator 全部资源（buffer + identity）
  → HcclPgRegistry.release(key)
  → entry 删除

HCCL Sleep 流程（目标）:
  hcclCommSuspend(group)              # 保留 identity/拓扑/连接，只释放动态 buffer
  → registry 标记为 suspended（不删除 entry）
```

#### 待确认 API

> ⚠️ **前置确认**：CANN 7.x 的 HCCL 是否提供了类似 `ncclCommSuspend(NCCL_SUSPEND_MEM)` / `ncclCommResume` 的 API？
>
> - 如果有 → 直接调用，ctypes shim 或 pyhccl wrapper 封装
> - 如果没有 → 需要研究 HCCL communicator 内部 buffer 的独立释放方式（类似 PyHcclCommunicator 的 buffer 成员），或者**降级方案**：在不 destroy HCCL 的前提下，将 HCCL communicator 移入特定 sleep_persistent memory pool

#### 代码改动点

| 文件 | 改动 |
|------|------|
| `vllm_ascend/patch/worker/patch_distributed.py` | 新增 `suspend_hccl()` / `resume_hccl()`，替代 `destroy_hccl()` / `restore_hccl()` |
| `vllm_ascend/patch/worker/_hccl_pg_registry.py` | 新增 suspended 状态标记 + refcount 保留，destroy 仅在 refcount 归零时触发 |
| `vllm_ascend/device_allocator/sleep_mem_optimized.py:131-186` | `HcclSleepWakeupManager.sleep()` → 调 `suspend_hccl()`；`wakeup()` → 调 `resume_hccl()` |
| `vllm_ascend/distributed/hccl_wrapper.py`（新增或扩展） | 封装 CANN HCCL suspend/resume API（若存在） |

#### 验证手段

```python
# 伪代码验证 HCCL buffer 释放效果
def test_hccl_suspend_memory_release():
    # 1. 建立 TP4 HCCL communicator
    # 2. 调用 torch.npu.synchronize()；记录 before = torch.cuda.memory_allocated()
    # 3. suspend_hccl()；synchronize()；记录 after = torch.cuda.memory_allocated()
    # 4. 断言 before - after >= 500 MiB（上游 NCCL 在 TP4 下释放 ~960 MiB/rank）
    # 5. resume_hccl()；验证 communicator 仍可用（all_reduce 正确性）
    # 6. 循环 sleep/wake 10 次，确认每次释放量一致，无累积泄漏
```

---

### 3.2 Part B — ACL Graph 原地恢复（P1）

#### 核心思路

类似上游 CuMemAllocator 的 `graphs` tag offload：

```
ACL Graph Sleep 流程（当前）:
  wrapper.concrete_aclgraph_entries.clear()     # 直接清空 capture 结果
  first_run_finished = False
  model_runner.cudagraph_manager.graphs.clear()
  model_runner._graphs_captured = False

ACL Graph Sleep 流程（目标）:
  遍历 model_runner._acl_graph_wrappers
  → 对每个 wrapper 的 graph capture memory 做 D2H offload
  → CaMemAllocator 新增 "acl_graph" tag（或复用 CuMemAllocator 已有的机制）

ACL Graph Wake 流程（当前）:
  model_runner.capture_model()                   # 完整重跑 profile_run → dummy_run → capture

ACL Graph Wake 流程（目标）:
  遍历 model_runner._acl_graph_wrappers
  → 对每个 wrapper 的 graph memory 做 H2D restore（保持 virtual address！）
  → 直接恢复 concrete_aclgraph_entries 指针
  → **不调用 capture_model()**
```

#### 代码改动点

| 文件 | 改动 |
|------|------|
| `vllm_ascend/device_allocator/sleep_mem_optimized.py:67-128` | `AclGraphSleepWakeupManager.sleep()` → graph memory D2H offload；`wakeup()` → graph memory H2D restore（**不再调 capture_model**）|
| `vllm_ascend/worker/v2/aclgraph_utils.py` | 新增 `ModelAclGraphManager.save_graph_memory()` / `restore_graph_memory()` |
| `vllm_ascend/compilation/acl_graph.py` | 新增 `ACLGraphWrapper.save_entries_to_cpu()` / `restore_entries_from_cpu()` |
| `vllm_ascend/device_allocator/camem.py` | CaMemAllocator 扩展：支持 acl_graph tag 的 vmap 级别 restore（保证 virtual address 不变）|

#### 关键技术难点

**难点 1：ACL graph 内存如何追踪和释放？**

上游 vLLM 通过 CUDA MemPool routing 把 graph capture 的显存自动归入一个可 tag 的 pool。Ascend 侧的 ACL graph memory 来源：
- `torch.npu.NPUGraph` 对象自身的 graph memory（capture 时由 CANN 分配）
- `_graph_params` 中的 attention workspace（独立分配，可能不走 torch pool）

解决方案选项：
- **选项 A**（推荐）：类似 CuDA VMM + `cuMemCreate` + `cuMemMap`，用 CANN 的 `aclrtMallocAlign` + `aclrtMemMap` 让 graph memory 可被 CaMemAllocator 管控
- **选项 B**：直接遍历 `_graph_params.workspaces` + `ACLGraphWrapper.concrete_aclgraph_entries`，把每个 tensor 做 D2H/H2D

**难点 2：Wake 后 memory pointer 不变？**

上游 CuMemAllocator 的关键 trick：`cuMemCreate + cuMemMap` → sleep 时 `cuMemUnmap` + offload；wake 时重新 `cuMemMap` **到同一个 virtual address**。这样 CUDA graph capture 时写入的指针地址完全不变。

Ascend 侧需要确认 CANN 7.x 是否提供等价的 vmap + remap API（`aclrtMemMallocAsyncWithConfig` / `aclrtMemMap`），且 NPUGraph 对象是否在指针不变时可直接 replay。

#### 验证手段

```python
# 伪代码验证 ACL graph 原地恢复正确性
def test_acl_graph_inplace_restore():
    # 1. 启动 model，正常 capture ACL graph
    # 2. 跑 warmup，记录 baseline 输出（bit-exact）
    # 3. 执行 sleep（新流程：graph memory D2H）
    # 4. 执行 wake（新流程：graph memory H2D restore，不重 capture）
    # 5. 用相同输入跑推理，断言输出与 baseline bit-exact
    # 6. 测时间：新流程 wake 耗时 vs 旧流程 wake + capture_model 耗时
    # 预期：新流程 wake 耗时 << 旧流程（省掉了 profile_run + capture）
```

---

## 4. 实现后的 Sleep/Wake 流程（目标状态）

```
Sleep (level 2, enable_sleep_mode_extra_cleanup=True):
  ├─ CaMemAllocator.sleep(offload_tags=("weights", "kv_cache"))
  │   └─ D2H memcpy → pin-memory + unmap_and_release → NPU 显存释放
  │
  ├─ AclGraphSleepWakeupManager.sleep()
  │   └─ graph memory → CPU pin-memory（保留 concrete_aclgraph_entries 指针）
  │
  └─ HcclSleepWakeupManager.sleep()
      └─ suspend_hccl() → release_hccl_buffers（保留 communicator identity）

Wake (tags=None):
  ├─ HcclSleepWakeupManager.wakeup()          ← 先恢复 HCCL（通信域就绪）
  │   └─ resume_hccl() → restore_hccl_buffers
  │
  ├─ AclGraphSleepWakeupManager.wakeup()      ← 后恢复 graph（依赖 HCCL 就绪）
  │   └─ graph memory ← H2D memcpy（原地 restore，不重 capture！）
  │
  └─ CaMemAllocator.wake_up(tags)             ← 最后恢复权重/KV cache
      └─ create_and_map + H2D memcpy
```

---

## 5. 预期技术收益

| 指标 | 旧流程（destroy + re-capture） | 新流程（suspend + in-place restore） |
|------|-------------------------------|--------------------------------------|
| **HCCL wake 耗时** | TP4: 4× new_group() collective + init ~5-10s | resume_hccl() ~1s（只 release/restore buffer）|
| **ACL graph wake 耗时** | profile_run + dummy_run + capture_model() ~15-60s（模型越大越慢） | H2D memcpy（只恢复 memory）~1-3s |
| **总 wake 加速比** | 1× | **5-15×** |
| **sleep 释放 NPU 内存** | HCCL buffer（~几 GiB）+ graph workspace | 相同释放量，但保留 identity |
| **RL 训练场景** | PPO/GRPO 每次 rollout 之间 sleep/wake 开销大 | sleep/wake 几乎免费，rollout 密度提升 |
| **正确性** | Bit-exact（重新 capture 保证确定性）| 同样 Bit-exact（memory 原地恢复，graph 未变）|

**对 RL 训练的特殊意义**：PPO/GRPO/DPO 等 online RL 算法在 rollout 之间频繁切换 sleep/wake 状态。当前 destroy + re-capture 模式让每次 wake 都要重建 HCCL + 重 capture graph，**wake 耗时约占一个 rollout step 的 20-40%**。优化后 wake 耗时可以降到毫秒级，训练吞吐量可提升 **20-50%**。

---

## 6. 上游参考资料

### 6.1 核心 PR

| PR | 状态 | 核心机制 | 关键文件 |
|----|------|----------|----------|
| [#45623 Offload CUDA graph + NCCL communicator memory](https://github.com/vllm-project/vllm/pull/45623) | **Draft** | CuMemAllocator `graphs` tag + graph pool pin + `ncclCommSuspend` | `gpu_worker.py`（_pin_sleep_mode_graph_pool）、`cudagraph_pool.py`、`nccl_suspend.py`（ctypes shim）|
| [#51485 Release NCCL communicator memory](https://github.com/vllm-project/vllm/pull/51485) | **Draft**（#45623 的 NCCL 部分被拆分出来，可独立 review）| Communicator `suspend()` / `resume()` 通用接口 + PyNccl 实现 | `sleep_mode_backend.py`（新增 suspend/resume hook）、`communicator/suspend.py` |

### 6.2 关键上游代码位置（本地仓库 `.tmp_vllm`）

```
.tmp_vllm/vllm/
├── device_allocator/
│   ├── sleep_mode_backend.py         ← SleepModeBackend 抽象 + CuMemBackend 实现
│   ├── camem_allocator.py            ← CuMemAllocator tag + MemPool 路由
│   └── cudagraph_pool.py             ← CUDAGraphWrapper + BreakableCUDAGraphWrapper
├── v1/worker/
│   ├── gpu_worker.py:193-250         ← upstream GPUWorker 的 sleep/wake 入口
│   ├── gpu_model_runner.py:          ← _pin_sleep_mode_graph_pool()（PR #45623 新增）
│   └── nccl_suspend.py               ← ctypes shim 调用 ncclCommSuspend/Resume（PR #51485）
└── distributed/
    └── communicator/suspend.py       ← 通用 suspend()/resume() hook（PR #51485）
```

### 6.3 Ascend 侧关键代码位置（`repos/vllm-ascend`）

```
repos/vllm-ascend/vllm_ascend/
├── worker/worker.py:221-269                    ← sleep() / wake_up() 顶层入口
├── device_allocator/
│   ├── sleep_mem_optimized.py:67-128           ← AclGraphSleepWakeupManager
│   ├── sleep_mem_optimized.py:131-186          ← HcclSleepWakeupManager
│   └── camem.py:113-220                        ← CaMemAllocator.sleep()（D2H + unmap）
│   └── camem.py:222-249                        ← CaMemAllocator.wake_up()（create_and_map）
├── patch/worker/
│   ├── patch_distributed.py:300-316             ← destroy_hccl() / restore_hccl()
│   └── _hccl_pg_registry.py:94-158              ← HcclPgRegistry（destroy 时删除 entry）
├── worker/v2/
│   └── aclgraph_utils.py:68-168                 ← ModelAclGraphManager（FULL graph capture）
└── compilation/
    └── acl_graph.py:60-249                      ← ACLGraphWrapper（PIECEWISE capture）
```

---

## 7. 贡献指南

### 7.1 代码仓库

- **主仓库**：`https://github.com/vllm-project/vllm-ascend`
- **关联上游**：`https://github.com/vllm-project/vllm`（需同步跟进 #45623 / #51485 的最终合入形态）
- **fork 分支**：建议在自己的 fork 上创建 `feature/sleep-mode-optimization` 分支

### 7.2 建议改动文件清单

```
# Part A: HCCL 通信域轻量化
vllm_ascend/patch/worker/patch_distributed.py          ← 新增 suspend_hccl() / resume_hccl()
vllm_ascend/patch/worker/_hccl_pg_registry.py          ← 新增 suspended 状态 + 保持 entry
vllm_ascend/device_allocator/sleep_mem_optimized.py    ← HcclSleepWakeupManager 改用 suspend/resume
vllm_ascend/distributed/hccl_suspend.py（新增）         ← 封装 CANN HCCL suspend/resume API

# Part B: ACL Graph 原地恢复
vllm_ascend/device_allocator/sleep_mem_optimized.py    ← AclGraphSleepWakeupManager 改用 D2H/H2D
vllm_ascend/worker/v2/aclgraph_utils.py                ← ModelAclGraphManager.save/restore
vllm_ascend/compilation/acl_graph.py                   ← ACLGraphWrapper.save/restore
vllm_ascend/device_allocator/camem.py                  ← CaMemAllocator 扩展 acl_graph tag

# 测试
tests/ut/device_allocator/test_sleep_wakeup.py（新增）  ← HCCL suspend/resume UT
tests/ut/device_allocator/test_aclgraph_inplace.py（新增） ← ACL graph 原地恢复 UT
tests/e2e/pull_request/one_card/test_sleep_wake_aclgraph.py ← E2E correctness
tests/e2e/pull_request/two_card/test_sleep_wake_distributed.py ← TP/PP 多 HCCL group 场景
```

### 7.3 测试路径

```bash
# UT
python -m pytest tests/ut/device_allocator/test_sleep_wakeup.py -v
python -m pytest tests/ut/device_allocator/test_aclgraph_inplace.py -v

# E2E（单卡）
# 1. 启动 sleep mode: level=2 + enable_sleep_mode_extra_cleanup=True
# 2. 跑推理 → sleep → wake → 跑推理 → 对比 bit-exact
python tests/e2e/pull_request/one_card/test_sleep_wake_aclgraph.py

# E2E（多卡 TP/PP）
# 1. TP4 + PP2 场景，多 HCCL group（TP comm + EP comm + PP comm）
# 2. 多轮 sleep/wake，验证 communicator identity 保持
python tests/e2e/pull_request/two_card/test_sleep_wake_distributed.py
```

### 7.4 提交规范

```
commit message 模板:

[Feature][Sleep] 优化 Sleep/Wake：HCCL 通信域 suspend/resume + ACL Graph 原地恢复

- Part A: HCCL
  - 新增 suspend_hccl() / resume_hccl()，替代 destroy_hccl() / restore_hccl()
  - HcclPgRegistry 支持 suspended 状态，保留 refcount
  - 待确认：CANN 7.x HCCL suspend/resume API 是否可用
- Part B: ACL Graph
  - AclGraphSleepWakeupManager.sleep() 改为 graph memory D2H offload
  - AclGraphSleepWakeupManager.wakeup() 改为 graph memory H2D restore
  - 不再调用 capture_model()，wake 耗时从 15-60s 降到 1-3s
- 测试：
  - UT: test_sleep_wakeup.py, test_aclgraph_inplace.py
  - E2E: test_sleep_wake_aclgraph.py (单卡), test_sleep_wake_distributed.py (多卡)

关联上游: vllm-project/vllm#45623, vllm-project/vllm#51485
```

---

## 8. 验收标准

1. ✅ **HCCL suspend/resume 可用**：sleep 后所有 TP/PP/DP HCCL communicator 保留 identity，wake 后 communicator 直接可用，不重新 new_group
2. ✅ **HCCL buffer 释放量 ≥ 500 MiB/rank**：在 TP4 + EP 场景下验证 sleep 释放 ≥ 500 MiB/NPU
3. ✅ **ACL graph wake 后不重 capture**：wake 流程 profile 确认不再调用 `capture_model()`
4. ✅ **ACL graph 原地恢复后 bit-exact**：相同输入的推理输出与 sleep 前 bit-exact（配合 `VLLM_BATCH_INVARIANT=1`）
5. ✅ **Wake 耗时 ≥ 5× 加速**：对比旧流程，新流程 wake 耗时显著降低
6. ✅ **多轮 sleep/wake 稳定**：循环 sleep/wake 10 次，每次释放量一致，无累积内存泄漏
7. ✅ **Rollout 场景无回归**：RL 训练场景（examples/rl/）完整跑通，batch invariant 保持
8. ✅ **Full/Draft 双模式兼容**：FULL graph（ModelAclGraphManager）和 DRAFT graph（DFlash/Eagle/DSpark）均覆盖
9. ✅ **不影响默认路径**：`enable_sleep_mode_extra_cleanup=False` 时行为不变（向后兼容）

---

## 9. 前置问题 / 待确认事项

### Q1: CANN 7.x HCCL 是否提供 suspend/resume API？

> 如果有 → 直接调用（ctypes shim 或 pyhccl wrapper）
> 如果没有 → 需要研究 HCCL communicator 内部 buffer 的独立释放方式；或考虑让 HCCL communicator 使用 CaMemAllocator 的 sleep_persistent pool（不释放 HCCL，改为释放 graph workspace）

**确认路径**：
1. 查 CANN 7.x release notes / 公开 API 文档
2. 在 `pyhccl_wrapper.py` 或 `torch_npu` 中 grep `hcclCommSuspend` / `hcclCommResume`
3. 联系 CANN/HCCL 团队

### Q2: ACL graph memory 是否可走 vmap + remap？

> 类似 CuDA VMM：`aclrtMallocAsyncWithConfig` + `aclrtMemMap` → sleep 时 unmap + D2H；wake 时 H2D + remap 到相同 virtual address

**确认路径**：查 CANN 7.x 的 vmap API 可用性，以及 NPUGraph 对象是否在指针不变时可直接 replay

### Q3: Sleep mode 在 ascend 上的主要使用场景？

> - **RL 训练**：PPO/GRPO/DPO rollout 之间频繁切换
> - **多任务混合**：推理/训练任务交替运行
> - **推理实例动态扩缩**

需要确认哪个场景是**优先优化目标**，这会影响 Part A 和 Part B 的优先级排序。

### Q4: 是否需要同步接入上游 SleepModeBackend 抽象？

> 上游 `SleepModeBackend` 抽象（`preserves_communicators()` / `preserves_compiled_artifacts()` / `preserves_graphs_with_communicators()`）已经在 `.tmp_vllm/vllm/device_allocator/sleep_mode_backend.py` 定义。Ascend 当前是绕过这个抽象。

建议：**同步接入**，把 Ascend 的 `SleepWakeupManager` 重构为注册在上游 SleepModeBackendFactory 上的 `AscendSleepModeBackend`。这样后续 vllm 增加新 sleep backend（如 CRIU checkpoint）时 Ascend 自动兼容。

---

## 10. 里程碑建议

| 里程碑 | 内容 | 预估周期 |
|--------|------|----------|
| M1 | CANN HCCL suspend/resume API 确认 + vmap API 可行性评估 | 1-2 周（需要平台侧确认）|
| M2 | Part A：HCCL suspend/resume 实现 + UT | 1-2 周 |
| M3 | Part B：ACL graph D2H/H2D offload + 原地恢复 + UT | 2-3 周 |
| M4 | E2E 集成测试 + RL rollout 场景验证 | 1-2 周 |
| M5 | 接入上游 SleepModeBackend 抽象 + 文档更新 | 1 周 |

---

## 11. 附录：Memory Delta 日志（来自上游 PR #51485）

| 配置 | GPUs | Comms suspended | NCCL freed/rank | Output preserved |
|------|------|-----------------|----------------|------------------|
| TP2 | 2 | 2 | 958 MiB | ✓ |
| TP4 | 4 | 2 | 960 MiB | ✓ |
| TP8 | 8 | 2 | 960 MiB | ✓ |
| TP4 + EP | 4 | 2 | 960 MiB | ✓ |
| TP8 + EP | 8 | 2 | 960 MiB | ✓ |
| TP4 + DP2 + EP | 8 | 3 | 1438 MiB | ✓ |
| TP2 + PP2 | 4 | 3 | 1438 MiB | ✓ |

**Ascend 预期**：HCCL communicator buffer 大小取决于 TP/PP/DP 组合和 max_tokens 配置，**预估释放量与 NCCL 相当（500-1500 MiB/rank）**。具体数值需 M1 阶段实测。
