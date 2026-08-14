# [Sleep Mode] HCCL 通信域 destroy → suspend/resume 轻量化改造

> **难度**: 🟡 中等（预计 2-3 天）
> **可并行**: ✅ 无硬前置，可与 09/10/11 同时开发
> **Step 0 调研内联**: 任务开头自带 5 分钟 benchmark 脚本，确认 CANN HCCL suspend/resume API 是否存在
> **文件冲突预警**: 与 09/10 在 `sleep_mem_optimized.py` 上改不同类（HcclSleepWakeupManager vs AclGraphSleepWakeupManager），merge 几乎零冲突
> **依赖改动**: patch_distributed.py, _hccl_pg_registry.py, sleep_mem_optimized.py
> **关联上游**: vllm-project/vllm#51485 (ncclCommSuspend/Resume)
> **标签**: `enhancement`, `sleep-mode`, `hccl`, `distributed`

---

## 1. 问题描述

当前 vllm-ascend 的 SleepWakeupManager 在 sleep 时调用 `destroy_hccl()` → 完全销毁 HCCL process group（destroy_process_group + HcclPgRegistry.release），wake 时调用 `restore_hccl()` → 重新 new_group("hccl")。

这个 destroy + recreate 模式在 TP/PP/DP 多 group 场景下开销显著：
- TP4 + EP 场景下至少 2 个 HCCL group（TP comm + EP comm），每个都要 destroy + recreate
- TP4 + DP2 + EP 场景下 3 个 group
- 每次 new_group 是 collective 操作 + HCCL communicator 初始化，**实测耗时 5-10s/TP4**
- 这个开销在 RL 训练场景尤其痛苦：PPO/GRPO 每次 rollout 之间 sleep/wake，wake 耗时约占 rollout step 的 20-40%

---

## 2. 核心思路

**目标**：sleep 时"释放 buffer，不销毁 identity"，wake 时"恢复 buffer，保持 identity"。

### 路径 A（优先）：原生 suspend/resume API

如果 CANN HCCL 提供了类似 `hcclCommSuspend(NCCL_SUSPEND_MEM)` / `hcclCommResume` 的 API（见任务 07 调研）：

```
当前:  destroy_process_group(group)     # 销毁全部：buffer + identity + connection
目标:  hcclCommSuspend(group)            # 只释放动态 buffer，保留 identity/topology/connection
```

参考上游 vllm 的做法（vllm PR #51485）：
- 通过 ctypes 加载 libhccl.so
- 封装 `suspend(comm)` / `resume(comm)` 函数
- gracefully degrade：如果 API 不存在或返回错误码，fall back 到 destroy/recreate

### 路径 B（降级）：让 HCCL communicator 用 sleep_persistent pool

如果没有原生 suspend/resume API：
- 保持当前 destroy/recreate 逻辑不动
- 但**缩小 destroy 的范围**：只 destroy HCCL communicator buffer，不 destroy process group
- 或者：让 HCCL communicator 的 buffer 分配到 CaMemAllocator 的 `sleep_persistent` tag，这样 sleep 时 CaMemAllocator 会自动释放（不需要显式 destroy）

---

## 2.5 Step 0：5 分钟快速调研（动手前先跑）

> 这个调研**不是前置关卡**，就是你开 fork 分支后跑的第一个脚本。根据结果选路径 A 或路径 B，不需要等任何人确认。

### 脚本 1：HCCL suspend/resume API 是否存在

```bash
# 在已安装 CANN 环境上跑
python -c "
import ctypes, os

# 尝试加载 libhccl.so
paths = [
    '/usr/local/Ascend/ascend-toolkit/latest/lib64/libhccl.so',
    os.environ.get('ASCEND_HOME_PATH', '') + '/lib64/libhccl.so',
]
lib = None
for p in paths:
    if os.path.exists(p):
        try:
            lib = ctypes.CDLL(p); print(f'Loaded: {p}'); break
        except: pass

if lib is None:
    print('❌ libhccl.so not found → 路径 B（降级）')
    exit()

# 尝试绑定 suspend/resume 符号
for name in ['hcclCommSuspend', 'hcclCommResume', 'hcomSuspend', 'hcomResume']:
    try:
        getattr(lib, name)
        print(f'✅ Found: {name} → 路径 A（原生 suspend/resume）')
    except AttributeError:
        print(f'❌ Not found: {name}')

# 最终判断
if not hasattr(lib, 'hcclCommSuspend') and not hasattr(lib, 'hcomSuspend'):
    print('❌ 无 suspend/resume API → 路径 B（降级：把 HCCL buffer 走 CaMemAllocator）')
"
```

### 脚本 2：当前 destroy/recreate 实际开销

```python
# benchmark_hccl_destroy_recreate.py
import torch, time
import torch.distributed as dist

dist.init_process_group("hccl", rank=int(os.environ["RANK"]), world_size=int(os.environ["WORLD_SIZE"]), ...)
group = dist.new_group(backend="hccl")

# warmup
for _ in range(3):
    dist.destroy_process_group(group)
    group = dist.new_group(backend="hccl")

# measure
t_d = []; t_c = []
for _ in range(10):
    t0 = time.time()
    dist.destroy_process_group(group)
    t_d.append(time.time() - t0)
    t0 = time.time()
    group = dist.new_group(backend="hccl")
    t_c.append(time.time() - t0)

print(f"destroy avg: {sum(t_d)/len(t_d)*1000:.0f} ms")
print(f"create  avg: {sum(t_c)/len(t_c)*1000:.0f} ms")

# memory freed
b_before = torch_npu.npu.memory_allocated()
dist.destroy_process_group(group)
torch.npu.synchronize()
b_after = torch_npu.npu.memory_allocated()
print(f"HCCL buffer freed per PG: {(b_before-b_after)/1024**2:.0f} MiB")
```

### 根据结果选路径

| 调研结果 | 选哪条路径 | 这个任务还能做吗 |
|----------|-----------|----------------|
| ✅ 有 `hcclCommSuspend/Resume` | **路径 A**（ctypes shim 调原生 API） | 完美推进 |
| ❌ 没有 | **路径 B**（降级：HCCL buffer 走 CaMemAllocator） | 能做，只是最终 wake 还是要 recreate（但 buffer 释放效果一样） |

**两种路径都可以提交 PR，路径 A 标记为 enhancement。**

---

## 3. 代码改动点

### 3.1 patch_distributed.py — 新增 suspend_hccl() / resume_hccl()

**文件**: `vllm_ascend/patch/worker/patch_distributed.py`

**当前代码**（L300-316）:
```python
def destroy_hccl(self) -> bool:
    destroyed = self._release_hccl_resources()
    if hasattr(self, "device_group"):
        self.device_group = None
    return destroyed

def restore_hccl(self) -> bool:
    if self.device_group is not None:
        return False
    self._init_device_groups(create_cpu_group=False)
    self._init_device_communicator()
    return True
```

**新增方法**:
```python
def suspend_hccl(self) -> bool:
    """释放 HCCL communicator buffer，保留 identity/topology/connection。
    
    优先调用 CANN HCCL 原生 suspend API；如果不可用，
    gracefully fall back 到 destroy_process_group（降级）。
    """
    if not hasattr(self, "device_group") or self.device_group is None:
        return False
    
    if hccl_suspend_available():          # 路径 A
        for group in self._unshared_hccl_groups:
            hccl_comm_suspend(group)
        return True
    else:                                  # 路径 B：降级
        return self.destroy_hccl()

def resume_hccl(self) -> bool:
    """恢复 HCCL communicator buffer。"""
    if hccl_suspend_available():
        for group in self._unshared_hccl_groups:
            hccl_comm_resume(group)
        return True
    else:
        return self.restore_hccl()
```

### 3.2 _hccl_pg_registry.py — 新增 suspended 状态

**文件**: `vllm_ascend/patch/worker/_hccl_pg_registry.py`

**当前**: refcount 归零时 → `destroy_process_group(handle)` 并删除 entry

**改动**: 新增 `suspend()` / `resume()` 方法，entry 保留但标记状态：
```python
class HcclPgRegistry:
    def __init__(self):
        self._registry: dict[str, RegistryEntry] = {}
    
    def suspend(self, key: str) -> None:
        """标记 entry 为 suspended，但保留 refcount 和 handle。"""
        if key in self._registry:
            self._registry[key].suspended = True
    
    def resume(self, key: str) -> None:
        """清除 suspended 标记。"""
        if key in self._registry:
            self._registry[key].suspended = False
    
    def is_suspended(self, key: str) -> bool:
        return self._registry.get(key, None)?.suspended ?? False
```

**关键约束**：destroy_process_group 只在 refcount 归零且非 suspended 时触发。

### 3.3 sleep_mem_optimized.py — HcclSleepWakeupManager 改用 suspend/resume

**文件**: `vllm_ascend/device_allocator/sleep_mem_optimized.py`

**当前**（L157-186）:
```python
def sleep(self) -> None:
    ...
    for coord in self._coordinators:
        coord.destroy_hccl()

def wakeup(self) -> None:
    ...
    for coord in self._coordinators:
        coord.restore_hccl()
```

**改动**:
```python
def sleep(self) -> None:
    ...
    for coord in self._coordinators:
        coord.suspend_hccl()

def wakeup(self) -> None:
    ...
    for coord in self._coordinators:
        coord.resume_hccl()
```

### 3.4 hccl_suspend.py — 新建 ctypes shim

**新建文件**: `vllm_ascend/distributed/hccl_suspend.py`

参考上游 vllm PR #51485 的 `nccl_suspend.py` 实现：

```python
"""ctypes shim for CANN HCCL suspend/resume APIs.

Gracefully degrades to no-op if the APIs are not available in the
installed HCCL version — callers should fall back to destroy/recreate.
"""
import ctypes
import os
from typing import Optional

# libhccl.so 动态加载
def _load_libhccl():
    for path in ["/usr/local/Ascend/ascend-toolkit/latest/lib64/libhccl.so",
                 os.environ.get("ASCEND_HOME_PATH", "") + "/lib64/libhccl.so"]:
        if os.path.exists(path):
            try:
                return ctypes.CDLL(path)
            except OSError:
                pass
    return None

_libhccl = _load_libhccl()

# 尝试绑定符号
def _try_bind(lib, name):
    try:
        return getattr(lib, name)
    except AttributeError:
        return None

hccl_comm_suspend = _try_bind(_libhccl, "hcclCommSuspend") if _libhccl else None
hccl_comm_resume  = _try_bind(_libhccl, "hcclCommResume")  if _libhccl else None

def hccl_suspend_available() -> bool:
    """Return True if native suspend/resume API is available."""
    return hccl_comm_suspend is not None and hccl_comm_resume is not None

def suspend(comm: "torch.distributed.ProcessGroup") -> Optional[int]:
    """Release HCCL communicator buffer via native suspend API.
    
    Returns error code on failure, None if API unavailable.
    Gracefully degrades: caller checks hccl_suspend_available() first.
    """
    if not hccl_suspend_available():
        return None
    # ... ctypes 调用逻辑（参考 nccl_suspend.py）

def resume(comm: "torch.distributed.ProcessGroup") -> Optional[int]:
    """Restore HCCL communicator buffer via native resume API."""
    if not hccl_suspend_available():
        return None
    # ... ctypes 调用逻辑
```

---

## 4. 降级路径（无原生 API 时）

**如果 CANN 7.x 没有 suspend/resume API**，不要让整个任务阻塞：

**降级方案**（预计 0.5 天即可实现）：
- 保持 destroy_hccl() / restore_hccl() 的 destroy+recreate 逻辑不变
- 但**把 HCCL communicator buffer 的分配走 CaMemAllocator**：
  ```python
  # 在 GroupCoordinator._init_device_groups() 中：
  with CaMemAllocator.get_default().use_memory_pool(tag="sleep_persistent"):
      self._init_device_groups(create_cpu_group=False)
  ```
- 这样 sleep 时 CaMemAllocator 会自动 unmap HCCL buffer（不需要显式 destroy）
- **收益**：即使是 destroy/recreate 模式，HCCL buffer 也会被 CaMemAllocator 统一管理，后续任务 10（ACL graph 原地恢复）可以复用同样的 vmap + remap 机制

**降级收益**：sleep 时 HCCL buffer 被释放（内存效果和 suspend 一样），只是 wake 还是要 recreate（速度没变）。但这为后续演进铺路了。

---

## 5. 验证

### Unit Test

```python
# tests/ut/distributed/test_hccl_suspend.py
class TestHcclSuspendResume:
    def test_suspend_resume_available(self):
        assert hccl_suspend_available() in (True, False)  # 至少不 crash
    
    def test_suspend_resume_roundtrip(self):
        # 1. 建立 TP2 HCCL PG
        # 2. 验证 initial state
        # 3. suspend → 检查 buffer 释放（torch_npu.npu.memory_allocated() 降低）
        # 4. resume → 检查 buffer 恢复
        # 5. all_reduce → 验证 communicator 仍可用（bit-exact）
    
    def test_hccl_pg_registry_suspended_state(self):
        # 1. register → suspend → registry.is_suspended() == True
        # 2. resume → registry.is_suspended() == False
        # 3. suspended 状态下 destroy_process_group 不应被调用
    
    def test_fallback_to_destroy(self):
        # 模拟 hccl_suspend_available() == False
        # 验证 suspend_hccl() 调用 destroy_hccl()（降级）
```

### 内存释放验证

```bash
# TP4 + EP 场景，sleep 后检查内存
python examples/benchmark/benchmark_hccl_sleep.py \
    --tp-size 4 --ep-size 2 \
    --before-sleep --after-suspend --after-wake \
    --json-metrics
```

预期输出格式：
```json
{
  "tp_size": 4,
  "ep_size": 2,
  "hccl_groups": 2,
  "hccl_freed_per_rank_mib": 512,
  "wake_time_before_ms": 8500,
  "wake_time_after_ms": 1200,
  "speedup": 7.1
}
```

### E2E 正确性

```bash
# 跑 RL rollout 场景，多轮 sleep/wake，验证 batch invariant
VLLM_BATCH_INVARIANT=1 python examples/rl/ppo_rollout.py \
    --model xxx --sleep-between-rollouts --num-rollouts 5
```

---

## 6. 验收标准

- [ ] `suspend_hccl()` / `resume_hccl()` 方法已实现，且**优雅降级**（原生 API 不可用时 fallback 到 destroy/recreate）
- [ ] HcclPgRegistry 支持 suspended 状态，suspended 时 refcount 保留
- [ ] TP4 + EP 场景下，sleep 释放 HCCL buffer **≥ 500 MiB/rank**
- [ ] wake 耗时对比旧流程加速 **≥ 3×**（如果有原生 API）或内存释放量相同（降级路径）
- [ ] 多轮 sleep/wake 循环 10 次，HCCL 可用、all_reduce 正确、无累积泄漏
- [ ] `enable_sleep_mode_extra_cleanup=False` 时行为不变（向后兼容）
- [ ] UT 覆盖：`test_hccl_suspend.py` 全部通过

---

## 7. 提交规范

```
commit message:
[Feature][Sleep] HCCL 通信域 suspend/resume 轻量化改造

- 新增 hccl_suspend.py ctypes shim，封装 CANN HCCL suspend/resume API
- GroupCoordinator.suspend_hccl() / resume_hccl() 替代 destroy_hccl() / restore_hccl()
- HcclPgRegistry 新增 suspended 状态，refcount 保留
- 优雅降级：无原生 API 时 fallback 到 destroy/recreate（同时把 HCCL buffer 走 CaMemAllocator）
- UT: tests/ut/distributed/test_hccl_suspend.py

关联上游: vllm-project/vllm#51485
前置调研: 任务 07
```

---

## 8. 贡献者指南

1. **Fork** `https://github.com/vllm-project/vllm-ascend`，创建分支 `feature/sleep-mode-hccl-suspend`
2. 先跑任务 07 的 benchmark 脚本，确认你的 CANN 版本是否有 suspend/resume API
3. 如果有 → 实现路径 A；如果没有 → 实现路径 B（降级）
4. 两种路径都可以提交 PR，路径 A 会被标记为 enhancement
5. 提交前跑 UT：`python -m pytest tests/ut/distributed/test_hccl_suspend.py -v`

---

## 9. 参考资料

| 上游 | 位置 |
|------|------|
| NCCL 2.29 suspend/resume API | [NVIDIA NCCL Release Notes](https://docs.nvidia.com/deeplearning/nccl/release-notes/rel_2-29.html) |
| vllm PR #45623 nccl_suspend ctypes shim | `vllm/v1/worker/nccl_suspend.py`（PR 文件变更）|
| vllm PR #51485 communicator 抽象 | `vllm/distributed/communicator/suspend.py` |

| Ascend 侧 | 位置 |
|-----------|------|
| HCCL PG destroy/restore | `vllm_ascend/patch/worker/patch_distributed.py:300-316` |
| HcclPgRegistry | `vllm_ascend/patch/worker/_hccl_pg_registry.py:94-158` |
| HcclSleepWakeupManager | `vllm_ascend/device_allocator/sleep_mem_optimized.py:131-186` |
| PyHcclCommunicator | `vllm_ascend/distributed/pyhccl_wrapper.py` |
