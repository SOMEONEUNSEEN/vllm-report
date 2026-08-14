# [Sleep Mode] ACL Graph 原地恢复（Wake 后跳过重 capture）

> **难度**: 🔴 困难（预计 4-6 天）
> **可并行**: ✅ 无硬前置，可与 08/09/11 同时开发；Step 0 内联 vmap API 调研
> **文件冲突预警**: 与 09 在 `aclgraph_utils.py` / `acl_graph.py` 同文件；建议 09 先合入，10 基于其 workspace save/restore 扩展 graph pool offload
> **依赖改动**: aclgraph_utils.py, acl_graph.py, camem.py, sleep_mem_optimized.py
> **关联上游**: vllm-project/vllm#45623（CuMemAllocator graphs tag + vmap+remap）
> **标签**: `enhancement`, `sleep-mode`, `aclgraph`

---

## 1. 问题描述

当前 Wake 流程中，ACL graph 必须重新走 `profile_run → dummy_run 热身 → ModelAclGraphManager.capture_model()` 完整流程。对大模型（DeepSeek V4 FULL graph），这个重捕获耗时 **~30s+**。

**上游 vllm 的解法**（PR #45623）：
1. 把 CUDA graph capture pool 路由进 CuMemAllocator 的 `graphs` tag
2. 用 CuDA VMM（`cuMemMap`/`cuMemUnmap`）让 graph memory 可管理
3. sleep 时 graph memory → D2H offload（保留 virtual address 映射关系）
4. wake 时 graph memory → H2D restore **到同一个 virtual address**
5. **因为指针地址不变，CUDA graph capture 时写入的所有地址都是对的 → 不需要 re-capture**

**核心关键**：VMM + remap 到相同 virtual address。

---

## 2. Step 0：5 分钟 PoC 验证（动手前先跑）

> 这不是前置关卡。开 fork 分支 → 先跑这个 PoC → 根据结果决定是否按原方案推进。**即使 PoC 不通过，你仍然可以先实现 workspace 部分（同任务 09），降级交付。**

### PoC 脚本：CANN vmap + remap 能否保持 pointer 不变

```python
import torch, ctypes, os

# 尝试加载 CANN runtime
# 查头文件
for root, dirs, files in os.walk("/usr/local/Ascend"):
    for f in files:
        if f in ("aclrt_api.h", "aclrt_mem.h"):
            path = os.path.join(root, f)
            for line in open(path):
                if "aclrtMemMap" in line or "aclrtMemUnmap" in line:
                    print(f"✅ Found vmap API in: {path}")

# 运行时尝试绑定
lib_path = "/usr/local/Ascend/ascend-toolkit/latest/lib64/libascendcl.so"
if os.path.exists(lib_path):
    lib = ctypes.CDLL(lib_path)
    for name in ["aclrtMemMap", "aclrtMemUnmap", "aclrtMallocWithConfig",
                 "aclrtMemCreate", "aclrtMemMapAddr"]:
        try:
            getattr(lib, name); print(f"✅ {name}")
        except AttributeError:
            print(f"❌ {name}")
else:
    print("❌ libascendcl.so not found")
```

### PoC 脚本：NPUGraph pointer 不变时能否 replay

```python
import torch, torch_npu

# 1. 分配一块 memory 并 capture graph
x = torch.ones(1024, device="npu")
g = torch.npu.NPUGraph()
with torch.npu.graph(g):
    y = x * 2 + 1
orig_ptr = y.data_ptr()

# 2. 模拟 sleep：让 tensor 被 D2H + device memory 释放
x_cpu = x.cpu()
del x, y
torch.npu.empty_cache()

# 3. 模拟 wake：在 SAME POINTER 位置重新分配
# （这一步需要 vmap API，如果没有就跳过直接用相同大小 malloc）
x2 = x_cpu.to("npu")
torch.npu.synchronize()
new_ptr = x2.data_ptr()

print(f"orig_ptr: 0x{orig_ptr:x}")
print(f"new_ptr:  0x{new_ptr:x}")
print(f"match: {orig_ptr == new_ptr}")

# 4. 尝试 replay graph
g.replay()
print(f"graph replay OK, y = {x2 * 2 + 1}")
```

### 根据结果选路径

| PoC 结果 | 结论 | 本任务还能做吗 |
|----------|------|---------------|
| ✅ vmap API 可用 + pointer 不变 + NPUGraph replay 正确 | 完美推进 graph pool offload | 按原方案推进 |
| ❌ vmap API 不存在 | **降级**：跳过 graph pool offload，只实现 workspace 独立释放（等价于任务 09）| 能交付，收益减半 |
| ✅ vmap 可用但 NPUGraph replay 不工作 | 需要研究 NPUGraph 内部依赖（communicator / workspace / 其他隐式引用）| 部分推进，可能只需要 dummy_run 热身而跳过 capture |

---

## 3. 核心方案

### 3.1 技术路径（参考上游 CuMemAllocator）

```
当前 graph memory 来源:
  torch.npu.NPUGraph 对象自身的 graph memory
  + _graph_params.workspaces（attention workspace）
  + graph pool 中 pre-allocated memory blocks
  （这些都由 CANN 自动分配，不在我们直接管控下）

改造后 graph memory 来源:
  CaMemAllocator 的 "acl_graph" tag pool  ← 统一管理
  用 CANN vmap API (aclrtMemMap/aclrtMemUnmap) 让这块内存可 unmap/remap
```

### 3.2 改造后的 Sleep/Wake 流程

```
Sleep (enable_sleep_mode_extra_cleanup=True):
  CaMemAllocator.sleep(offload_tags=("weights", "kv_cache", "acl_graph"))
    ├─ weights/kv_cache → D2H memcpy + unmap
    └─ acl_graph pool → aclrtMemUnmap + D2H memcpy（保留 handle + VA 映射）
  
  然后释放（不是销毁！）:
    HcclSleepWakeupManager.sleep()   ← suspend_hccl()（任务 08）

Wake (tags=None):
  HcclSleepWakeupManager.wakeup()    ← resume_hccl()（先恢复通信域）
  
  CaMemAllocator.wake_up(tags)
    ├─ weights/kv_cache → create_and_map + H2D memcpy
    └─ acl_graph pool → H2D memcpy + aclrtMemMap(同一个 VA！)
  
  关键: **不调用 model_runner.capture_model()**
  graph 直接 replay → 指针地址全对
```

### 3.3 代码改动点

#### A. CaMemAllocator — 扩展 acl_graph tag + vmap 支持

**文件**: `vllm_ascend/device_allocator/camem.py`

**新增**：
```python
class CaMemAllocator:
    def __init__(self, ...):
        self.vmap_handles: dict[int, VmapHandle] = {}   # ptr → vmap 信息
    
    def register_vmap(self, ptr: int, size: int, handle: "aclrtMemHandle"):
        """注册一块被 vmap 管理的内存，支持后续 unmap/remap。"""
        self.vmap_handles[ptr] = VmapHandle(ptr, size, handle)
    
    def unmap_all_vmap(self) -> None:
        """Sleep 时 unmap 所有 vmap 内存（释放 NPU memory，但保留 VA 映射）。"""
        for ptr, vh in self.vmap_handles.items():
            aclrtMemUnmap(ptr, vh.size)
    
    def remap_all_vmap(self) -> None:
        """Wake 时 remap 所有 vmap 内存（回到原来的 VA）。"""
        for ptr, vh in self.vmap_handles.items():
            aclrtMemMap(ptr, vh.size, vh.handle)  # 注意: ptr 不变！
```

#### B. ACLGraphWrapper — capture 前 pin 到 acl_graph pool

**文件**: `vllm_ascend/compilation/acl_graph.py`

**参考上游**：`gpu_model_runner.py:_pin_sleep_mode_graph_pool()`（PR #45623 新增）

```python
def capture_model(self, ...):
    # 关键：capture 前，把 graph pool 指针 override 到 CaMemAllocator 的 acl_graph tag pool
    # 这样 capture 时分配的所有 memory 都会被 CaMemAllocator 管控
    old_graph_pool = _override_global_graph_pool(CaMemAllocator.get_default().get_pool("acl_graph"))
    try:
        # 正常 capture...
        model_runner._do_capture(...)
    finally:
        _override_global_graph_pool(old_graph_pool)
    
    # capture 完成后，把所有被分配的 tensor 注册到 vmap_handles
    for ptr in captured_tensor_ptrs:
        CaMemAllocator.get_default().register_vmap(ptr, size, handle)
```

#### C. AclGraphSleepWakeupManager — 不再调用 capture_model()

**文件**: `vllm_ascend/device_allocator/sleep_mem_optimized.py`

**当前 wakeup()**：
```python
def wakeup(self, tags=None):
    ...
    model_runner.capture_model()    # ← 这行是性能杀手
```

**改动后**：
```python
def wakeup(self, tags=None):
    if tags is not None and "kv_cache" not in tags:
        return
    
    # Step 1: restore workspace（如果走任务 09 的独立保存逻辑）
    for wrapper in self._acl_graph_wrappers:
        wrapper.restore_workspaces_from_cpu()
    
    # Step 2: 验证 graph pool 已被 CaMemAllocator 恢复
    # （CaMemAllocator.wake_up() 已经做了 remap_all_vmap()）
    
    # Step 3: 不调用 capture_model()！graph 可以直接 replay
    # 可选：跑一个 dummy inference 验证 graph replay 正确
    # model_runner._dummy_run_for_verify()
```

#### D. ModelAclGraphManager — FULL 模式等价改动

**文件**: `vllm_ascend/worker/v2/aclgraph_utils.py`

需要 FULL 模式的完整 graph memory 也走 vmap。改法类似 ACLGraphWrapper：capture 前 pin pool，capture 后 register vmap。

---

## 4. 降级路径

**如果 CANN 7.x 没有 vmap + remap API**：
- 直接关闭此任务，保留任务 09 的 workspace 单独释放方案
- 或者：如果 graph memory 可以通过其他方式保持指针（如固定 virtual address 分配），也可以尝试

**如果 NPUGraph 在指针不变时仍不能 replay**：
- 需要研究 NPUGraph 对象内部是否有对 communicator 或 workspace 的隐式依赖
- 如果有 → 可能需要在 wake 时只跑 dummy_run 热身（不跑 capture），耗时远低于完整重 capture

---

## 5. 验证

### 核心验证：指针地址不变

```python
def test_graph_memory_preserved_ptr():
    # 1. capture graph → 记录 captured_tensor_ptrs = [t.data_ptr() for t in ...]
    # 2. sleep（新流程：aclrtMemUnmap + D2H）
    # 3. wake（新流程：H2D + aclrtMemMap 到同一 VA）
    # 4. 重新获取 tensor → 断言 data_ptr() == 之前记录的
    # 5. graph replay → bit-exact
```

### 核心验证：wake 不调用 capture_model()

```python
def test_wake_does_not_recapture():
    # 1. monkeypatch model_runner.capture_model 成 raise AssertionError("should not call!")
    # 2. 跑 sleep → wake
    # 3. 正常 inference → bit-exact
    # 4. 断言 capture_model 从未被调用
```

### 性能验证

```bash
python -c "
import time
t0 = time.time()
# old: sleep + wake + capture_model()
# new: sleep + wake（no capture_model）
print(f'Old wake total: {time.time()-t0:.1f}s')

t0 = time.time()
# new path
print(f'New wake total: {time.time()-t0:.1f}s')
"
# 预期：new << old，加速比 ≥ 10×
```

### E2E：多轮 sleep/wake bit-exact

```bash
VLLM_BATCH_INVARIANT=1 python tests/e2e/test_sleep_wake_inplace.py \
    --model deepseek-v4 --num-rounds 10 --aclgraph-mode full
```

---

## 6. 验收标准

- [ ] CaMemAllocator 扩展了 vmap 管理（unmap/remap 循环，ptr 不变）
- [ ] ACLGraphWrapper / ModelAclGraphManager 的 graph memory 全部走 acl_graph tag pool
- [ ] wake 流程**不调用** `model_runner.capture_model()`（assert 验证）
- [ ] wake 耗时 **≥ 10× 加速**（DeepSeek V4 FULL graph：旧 ~30s → 新 ~3s）
- [ ] 多轮 sleep/wake 10 次，bit-exact，无内存泄漏
- [ ] RL rollout 场景完整跑通，batch invariant 保持
- [ ] PIECEWISE 和 FULL 两种 ACL graph 模式都覆盖
- [ ] UT + E2E 全部通过

---

## 7. 贡献者指南

**这是一个难度较高的任务**，建议：
1. 先完成任务 07 的 API 确认，确定 CANN vmap 可用再动手
2. 实现前先写一个最小 PoC：
   ```python
   import aclrt
   # 1. aclrtMalloc 分配一块 memory
   # 2. aclrtMemMap → aclrtMemUnmap → aclrtMemMap（同一 VA）
   # 3. assert ptr 不变，且 memory 内容正确
   ```
3. 先在 PIECEWISE 模式验证通，再上 FULL 模式
4. 参考上游 vllm PR #45623 的改动文件列表（6 个文件，+394 行），对照着做 Ascend 适配

---

## 8. 参考资料

| 上游 | 位置 |
|------|------|
| CuMemAllocator graph pool 路由 | `vllm/device_allocator/camem_allocator.py`（PR #45623）|
| graph pool pin | `vllm/v1/worker/gpu_model_runner.py:_pin_sleep_mode_graph_pool()` |
| ctypes shim for nccl | `vllm/v1/worker/nccl_suspend.py`（PR #45623）|
| VMM remap 保持 VA | PR #45623 核心 trick，`cuMemMap(addr=same_va, ...)` |

| Ascend 侧 | 位置 |
|-----------|------|
| CaMemAllocator | `vllm_ascend/device_allocator/camem.py:113-249` |
| AclGraphSleepWakeupManager | `vllm_ascend/device_allocator/sleep_mem_optimized.py:67-128` |
| ACLGraphWrapper | `vllm_ascend/compilation/acl_graph.py:60-249` |
| ModelAclGraphManager (FULL) | `vllm_ascend/worker/v2/aclgraph_utils.py:68-168` |
