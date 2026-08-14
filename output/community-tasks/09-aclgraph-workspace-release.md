# [Sleep Mode] ACL Graph Workspace 单独释放（Wake 仍重 capture）

> **难度**: 🟢 简单（预计 1 天，good first issue）
> **前置**: 无（可独立交付）
> **依赖改动**: sleep_mem_optimized.py, aclgraph_utils.py
> **关联上游**: vllm-project/vllm#45623（CUDA graph pool offload 思路）
> **标签**: `enhancement`, `sleep-mode`, `aclgraph`, `good first issue`
> **可并行**: ✅ 无任何前置，可与 08/10/11 同时开发
> **文件冲突预警**: 与 08 在 `sleep_mem_optimized.py` 改不同类（AclGraphSleepWakeupManager vs HcclSleepWakeupManager）；与 10 在 `aclgraph_utils.py` / `acl_graph.py` 同文件但改不同逻辑层（workspace save/restore vs graph pool offload），建议 09 先合入
> **good first issue**: 改动范围极小（~80 行，2 个文件），有明确 UT 验证

---

## 1. 问题描述

当前 `AclGraphSleepWakeupManager.sleep()` 做了两件事：
1. 清空 `_graph_params.workspaces`（attention workspace）→ 释放部分 NPU 内存
2. **清空所有 graph capture 结果**（`concrete_aclgraph_entries.clear()` + `cudagraph_manager.graphs.clear()`）

第 2 步意味着 wake 后必须调用 `model_runner.capture_model()` 重新跑 profile_run + dummy_run + capture，完整重捕获。

**问题**：即使只想释放 attention workspace（不碰 graph pool memory），当前实现也把 graph 全清了。这让 sleep → wake 这条路径必须付出一次完整重 capture 的成本（DeepSeek V4 FULL graph ~30s+）。

---

## 2. 这个任务做什么（中间收益）

**目标**：sleep 时把 attention workspace 从 graph capture 的"总清除"中独立出来，做到：

```
Sleep 时:
  ✅ attention workspace → D2H offload（或释放）        ← 本任务新增
  ❌ graph capture 结果 → 保留（不清空）                ← 本任务改动
  ❌ graph pool memory → 不释放（依赖任务 10 的 vmap+remap）

Wake 时:
  ✅ attention workspace → H2D restore                  ← 本任务新增
  ❌ graph capture → 仍然调用 capture_model()            ← 暂不改（任务 10 做）
```

**为什么这是独立有价值的中间步骤**：
- 即使 graph 还是要重 capture，attention workspace（通常几百 MiB ~ 几 GiB）也会被单独释放
- 改动范围**极小**（只改 AclGraphSleepWakeupManager 的 sleep/wake 方法 + ACLGraphWrapper 加两个 save/restore 方法）
- 为任务 10（真正的原地恢复）铺路：workspace 的 D2H/H2D 是 graph memory 原地恢复的子集

> ⚠️ **与任务 10 的关系**：10 做的是 ACL graph **整个 pool** 的 vmap + remap（wake 后连 capture_model 都跳过）。09 做的是 graph pool 内 **attention workspace** 的单独 D2H/H2D。10 的 workspace 部分会覆盖 09 的实现，但 09 可以先独立交付——10 的实现者在 09 合入后只需 rebase 即可。**两者并行开发完全没问题**。

---

## 3. 代码改动点

### 3.1 AclGraphSleepWakeupManager — 拆分 sleep/wake 逻辑

**文件**: `vllm_ascend/device_allocator/sleep_mem_optimized.py`

**当前 sleep()**（L86-118）:
```python
def sleep(self) -> None:
    for wrapper in self._acl_graph_wrappers:
        wrapper.concrete_aclgraph_entries.clear()          # 清 graph
        wrapper.first_run_finished = False
        # ... 还有 cudagraph_manager.graphs.clear()
    # ... 清空 _graph_params.workspaces                    # 清 workspace
```

**改动后 sleep()**:
```python
def sleep(self) -> None:
    # Step 1: 单独保存 workspace 到 CPU pin-memory        ← 新增
    for wrapper in self._acl_graph_wrappers:
        wrapper.save_workspaces_to_cpu()

    # Step 2: 只清空 graph capture 结果（不变）
    for wrapper in self._acl_graph_wrappers:
        wrapper.concrete_aclgraph_entries.clear()
        wrapper.first_run_finished = False
    # ... cudagraph_manager.graphs.clear() 不变
```

**当前 wakeup()**（L121-128）:
```python
def wakeup(self, tags=None) -> None:
    if tags is not None and "kv_cache" not in tags:
        return
    model_runner = self._model_runner_getter()
    model_runner.capture_model()       # 重跑 capture
```

**改动后 wakeup()**:
```python
def wakeup(self, tags=None) -> None:
    if tags is not None and "kv_cache" not in tags:
        return
    model_runner = self._model_runner_getter()

    # Step 1: 先恢复 workspace 到 NPU                     ← 新增
    for wrapper in self._acl_graph_wrappers:
        wrapper.restore_workspaces_from_cpu()

    # Step 2: 然后 capture（不变）
    model_runner.capture_model()
```

### 3.2 ACLGraphWrapper — 新增 save/restore workspace

**文件**: `vllm_ascend/compilation/acl_graph.py`（PIECEWISE 模式）
和 **文件**: `vllm_ascend/worker/v2/aclgraph_utils.py`（FULL 模式）

**新增方法**:
```python
def save_workspaces_to_cpu(self) -> None:
    """把 _graph_params.workspaces 中的 tensor 从 NPU 搬到 CPU pin-memory，
    保留 data_ptr 映射。workspace 字典本身保留（key=num_tokens → data_ptr）。"""
    if not self._graph_params:
        return
    for num_tokens, ws_tensor in list(self._graph_params.workspaces.items()):
        if ws_tensor is not None and ws_tensor.device.type == "npu":
            self._saved_workspaces[num_tokens] = ws_tensor.cpu().pin_memory()
            # 注意：不要把原 tensor 置 None（wake 后 capture_model 会重新分配）
            # 这里只是 D2H offload，释放 NPU memory

def restore_workspaces_from_cpu(self) -> None:
    """把保存的 workspace 从 CPU 搬回 NPU。
    注意：capture_model() 会重新分配 workspace tensor，这里的 restore 是
    在 capture_model 之前把数据搬回去（为了 capture 时能正确初始化）。"""
    for num_tokens, cpu_tensor in self._saved_workspaces.items():
        npu_tensor = cpu_tensor.to("npu", non_blocking=True)
        self._graph_params.workspaces[num_tokens] = npu_tensor
    self._saved_workspaces.clear()
```

### 3.3 ModelAclGraphManager — FULL 模式等价改动

**文件**: `vllm_ascend/worker/v2/aclgraph_utils.py`

如果 FULL 模式的 workspace 管理路径不同（不走 `_graph_params.workspaces`），需要找到等价的 tensor 容器，加上 save/restore。

---

## 4. 预期效果

| 指标 | 旧流程 | 本任务后 | 任务 10 完成后 |
|------|--------|---------|---------------|
| sleep 释放 workspace | ✅（但连带清 graph）| ✅（独立释放）| ✅ |
| sleep 释放 graph pool | ❌ 未释放 | ❌ 未释放 | ✅ |
| wake 重 capture | ✅ 必须 | ✅ 必须 | ❌ **跳过** |
| wake 耗时（DeepSeek V4）| ~30s | ~30s（不变）| **~3s** |
| 本任务**独立收益** | — | sleep 时 workspace 被 D2H offload（~几 GiB）| — |

**说明**：本任务完成后，wake 耗时**不会显著降低**（因为还是要 capture_model）。但 sleep 时可以多释放一块 workspace memory（几百 MiB ~ 几 GiB），为 RL 训练等场景在 sleep 期间腾出更多 NPU 显存。**同时本任务是任务 10 的必要前置**：如果 workspace 还没独立出来，就没法进一步让 graph pool memory 也走 D2H/H2D。

---

## 5. 验证

```python
# tests/ut/device_allocator/test_aclgraph_workspace_release.py
class TestAclGraphWorkspaceRelease:
    def test_workspace_d2h_offload(self):
        # 1. capture graph → 确认 _graph_params.workspaces 有值
        # 2. save_workspaces_to_cpu()
        # 3. 断言 torch_npu.npu.memory_allocated() 降低了 ~X MiB
        # 4. 断言 _saved_workspaces 中有对应条目（在 CPU pin-memory）
    
    def test_workspace_h2d_restore_before_capture(self):
        # 1. save_workspaces_to_cpu()
        # 2. restore_workspaces_from_cpu()
        # 3. 断言 _graph_params.workspaces 恢复
        # 4. capture_model() → 正常
        # 5. 推理 → bit-exact
    
    def test_workspace_not_lost_after_sleep_wake(self):
        # sleep → wake → capture_model → 用相同输入推理
        # 输出 vs baseline（sleep 前）bit-exact
```

---

## 6. 验收标准

- [ ] `ACLGraphWrapper.save_workspaces_to_cpu()` / `restore_workspaces_from_cpu()` 已实现
- [ ] `AclGraphSleepWakeupManager.sleep()` 先 save workspace，再清 graph
- [ ] `AclGraphSleepWakeupManager.wakeup()` 先 restore workspace，再 capture
- [ ] FULL 模式（ModelAclGraphManager）等价改动
- [ ] sleep 时 attention workspace 被 D2H offload（memory_allocated 降低 ≥ 100 MiB）
- [ ] wake + capture_model 后推理输出 bit-exact
- [ ] UT 全部通过：`pytest tests/ut/device_allocator/test_aclgraph_workspace_release.py -v`
- [ ] 不影响默认路径（enable_sleep_mode_extra_cleanup=False 时行为不变）

---

## 7. 贡献者指南

1. **Fork** `https://github.com/vllm-project/vllm-ascend`，创建分支 `feature/sleep-mode-workspace-release`
2. 先跑一个小模型（如 `Qwen2.5-7B`）开启 ACL graph，确认 `_graph_params.workspaces` 里有什么
3. 在 PIECEWISE 模式和 FULL 模式都验证（改动分布在 `acl_graph.py` 和 `aclgraph_utils.py`）
4. 提交前跑 UT

---

## 8. 参考资料

| 上游 | 说明 |
|------|------|
| [vllm PR #45623](https://github.com/vllm-project/vllm/pull/45623) | CUDA graph pool 路由进 CuMemAllocator + `graphs` tag offload 思路 |

| Ascend 侧 | 位置 |
|-----------|------|
| AclGraphSleepWakeupManager | `vllm_ascend/device_allocator/sleep_mem_optimized.py:67-128` |
| ACLGraphWrapper (PIECEWISE) | `vllm_ascend/compilation/acl_graph.py:60-249` |
| ModelAclGraphManager (FULL) | `vllm_ascend/worker/v2/aclgraph_utils.py:68-168` |
| NPUWorker.sleep/wake_up 入口 | `vllm_ascend/worker/worker.py:221-269` |
