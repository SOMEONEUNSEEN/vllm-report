# [Sleep Mode] 接入上游 SleepModeBackend 抽象（架构对齐）

> **难度**: 🟡 中等（预计 2 天）
> **前置**: 无（可独立交付）
> **依赖改动**: 新增 ascend_sleep_backend.py；worker.py 小改
> **关联上游**: vllm-project/vllm SleepModeBackend RFC #34303
> **标签**: `refactor`, `sleep-mode`, `architecture`
> **可并行**: ✅ 零文件冲突！与 08/09/10 完全独立，可以最先合入
> **文件冲突预警**: 仅改 `platform.py` + `worker.py`，新建 `ascend_sleep_backend.py`——这些文件 08/09/10 全不碰
> **推荐合入顺序**: 所有 sleep-mode 任务中最先合入，为后续任务提供统一入口

---

## 1. 问题描述

上游 vllm 已经引入了 `SleepModeBackend` 抽象（RFC #34303），并通过工厂模式 `SleepModeBackendFactory` 注册。当前 vllm-ascend 的做法是**绕过这个抽象**——在 `NPUWorker.sleep()` / `wake_up()` 中自行维护 `SleepWakeupManager`，没有注册到上游工厂。

### 为什么这是个问题？

| 问题 | 说明 |
|------|------|
| **上游演进不同步** | 上游如果增加新的 SleepModeBackend（如 CRIU checkpoint、CUDA memory checkpoint），Ascend 不会自动兼容 |
| **能力标志未上报** | `SleepModeBackend` 有 `preserves_communicators()` / `preserves_compiled_artifacts()` / `preserves_graphs_with_communicators()` 等能力标志，Ascend 当前没有声明 |
| **代码分叉** | 上游 GPUWorker 的 sleep/wake 逻辑和 Ascend NPUWorker 的逻辑在两个地方维护，容易漂移 |

### 上游当前状态

```python
# vllm/device_allocator/sleep_mode_backend.py（当前 .tmp_vllm）

class SleepModeBackend(ABC):
    @classmethod
    @abstractmethod
    def name(cls) -> str: ...
    
    @abstractmethod
    def suspend(self, level: int = 1) -> None: ...
    
    @abstractmethod
    def resume(self, tags: list[str] | None = None) -> None: ...
    
    # 能力标志（子类 override）
    @classmethod
    def preserves_communicators(cls) -> bool: return False
    @classmethod
    def preserves_compiled_artifacts(cls) -> bool: return False
    @classmethod
    def preserves_graphs_with_communicators(cls) -> bool: return False


class CuMemBackend(SleepModeBackend):
    """上游默认后端：只做 allocator 级别的 offload/remap。"""
    @classmethod
    def preserves_communicators(cls) -> bool: return True   # NCCL 不动
    @classmethod
    def preserves_compiled_artifacts(cls) -> bool: return True  # compiled kernel 不动
    @classmethod
    def preserves_graphs_with_communicators(cls) -> bool: return True  # graph pool 不动


class SleepModeBackendFactory:
    @staticmethod
    def create(platform: str) -> SleepModeBackend:
        # 根据平台创建对应的 backend
        # 当前只有 CUDA → CuMemBackend
        # Ascend 没有注册！
```

---

## 2. 本任务做什么

**目标**：把 Ascend 的 `SleepWakeupManager` 重构为注册在上游 `SleepModeBackendFactory` 上的 `AscendSleepModeBackend`。

### 设计决策：创建一个还是两个 Backend？

Ascend 有两种 sleep 场景需要不同处理：

| 场景 | Backend | 能力标志 |
|------|---------|----------|
| **仅 CaMemAllocator**（`enable_sleep_mode_extra_cleanup=False`）| `AscendCuMemBackend`（继承 CuMemBackend）| `preserves_communicators=True`, `preserves_graphs_with_communicators=True` |
| **CaMemAllocator + HCCL + ACL graph**（`enable_sleep_mode_extra_cleanup=True`）| `AscendExtraCleanupBackend` | `preserves_communicators=False`（要 destroy/suspend HCCL）, `preserves_compiled_artifacts=False`（要清 graph）|

**建议**：创建 `AscendSleepModeBackend` 基类，包含两种模式的统一逻辑。

> 💡 **提示贡献者**：这个任务是纯架构对齐，**代码改动量极小**（新建 ~150 行的 backend 类 + worker.py 入口几行改动），零业务逻辑变更。但它是让 Ascend 的 Sleep/Wake 跟上上游演进的关键一步——后续上游如果增加新的 sleep backend（如 CRIU、memory checkpoint），Ascend 会自动兼容。

---

## 3. 代码改动点

### 3.1 新增 `ascend_sleep_backend.py`

**新建文件**: `vllm_ascend/device_allocator/ascend_sleep_backend.py`

```python
"""Ascend 平台的 SleepModeBackend 实现。

注册到上游 vllm 的 SleepModeBackendFactory，供 vllm-ascend 使用。
支持两种模式：
  - basic: 仅 CaMemAllocator（权重/KV cache offload）
  - extra_cleanup: CaMemAllocator + HCCL suspend + ACL graph workspace offload
"""
from vllm.device_allocator.sleep_mode_backend import (
    SleepModeBackend,
    SleepModeBackendFactory,
)

class AscendSleepModeBackend(SleepModeBackend):
    """Ascend 默认 backend：CaMemAllocator，可选 HCCL + ACL graph 清理。"""
    
    @classmethod
    def name(cls) -> str:
        return "ascend_camem"
    
    @classmethod
    def preserves_communicators(cls) -> bool:
        # 如果 enable_sleep_mode_extra_cleanup=True，我们会 suspend/destroy HCCL
        # 所以 communicators 不被保留（或者任务 08 完成后变成"保留 identity"）
        return not _extra_cleanup_enabled()
    
    @classmethod
    def preserves_compiled_artifacts(cls) -> bool:
        # extra_cleanup=True 时清 ACL graph → compiled artifacts 不保留
        return not _extra_cleanup_enabled()
    
    @classmethod
    def preserves_graphs_with_communicators(cls) -> bool:
        # 同上
        return not _extra_cleanup_enabled()
    
    def __init__(self, vllm_config, worker):
        self._config = vllm_config
        self._worker = worker
        self._camem = worker.device_allocator  # CaMemAllocator
        self._extra_cleanup = _extra_cleanup_enabled()
        if self._extra_cleanup:
            from vllm_ascend.device_allocator.sleep_mem_optimized import SleepWakeupManager
            self._sleep_wakeup_manager = SleepWakeupManager(vllm_config, worker, ...)
    
    def suspend(self, level: int = 1) -> None:
        """对应 Ascend 的 sleep(level)。"""
        # Step 1: CaMemAllocator sleep（权重/KV cache）
        self._camem.sleep(self._offload_tags_for_level(level))
        
        # Step 2: extra_cleanup（可选，任务 08/09/10 的入口点）
        if self._extra_cleanup:
            self._sleep_wakeup_manager.sleep()
    
    def resume(self, tags: list[str] | None = None) -> None:
        """对应 Ascend 的 wake_up(tags)。"""
        # Step 1: extra_cleanup wakeup（先恢复 HCCL，再恢复 graph）
        if self._extra_cleanup:
            self._sleep_wakeup_manager.wakeup(tags)
        
        # Step 2: CaMemAllocator wake_up（权重/KV cache，最后恢复）
        self._camem.wake_up(tags)
    
    def _offload_tags_for_level(self, level: int) -> tuple[str, ...]:
        if level == 1:
            return ("weights",)
        elif level == 2:
            return ("weights", "kv_cache")
        else:
            raise ValueError(f"Unknown sleep level: {level}")
```

### 3.2 注册到 SleepModeBackendFactory

**修改文件**: `vllm_ascend/platform.py` 或新建 `vllm_ascend/device_allocator/__init__.py`

```python
# 在 platform.py 的 is_sleep_mode_available() 附近
from vllm_ascend.device_allocator.ascend_sleep_backend import AscendSleepModeBackend

# 注册（需要确认上游 Factory 的注册 API：装饰器？register() 方法？）
SleepModeBackendFactory.register("ascend_npu", AscendSleepModeBackend)
```

### 3.3 NPUWorker 小改：用 Factory 创建 backend

**文件**: `vllm_ascend/worker/worker.py`

**当前**:
```python
# NPUWorker 有自己的 sleep_wakeup_manager
self.sleep_wakeup_manager = SleepWakeupManager(...)

# sleep / wake_up 自己写完整逻辑
def sleep(self, level):
    self.sleep_wakeup_manager.sleep()
    self.device_allocator.sleep(...)

def wake_up(self, tags):
    self.device_allocator.wake_up(tags)
    self.sleep_wakeup_manager.wakeup(tags)
```

**改动后**:
```python
def __init__(self, ...):
    # 让 Factory 创建 backend
    from vllm.device_allocator.sleep_mode_backend import SleepModeBackendFactory
    self._sleep_backend = SleepModeBackendFactory.create("ascend_npu")

def sleep(self, level):
    self._sleep_backend.suspend(level)

def wake_up(self, tags):
    self._sleep_backend.resume(tags)
```

### 3.4 worker.py 中 CaMemAllocator 的创建

需要确认 CaMemAllocator 是否也需要注册到上游的 allocator 抽象层。但这个任务的 scope 只到 SleepModeBackend，CaMemAllocator 保持现状。

---

## 4. 改动边界

**不要做的**：
- ❌ 不重写 CaMemAllocator（保持现状）
- ❌ 不改动 SleepWakeupManager 的内部实现（只是重构它的**入口点**）
- ❌ 不改动 HcclSleepWakeupManager / AclGraphSleepWakeupManager 内部逻辑
- ❌ 不尝试同时实现 suspend_hccl() / workspace save/restore（那是任务 08/09）

**只做的**：
- ✅ 新建 AscendSleepModeBackend 继承 SleepModeBackend
- ✅ 注册到 Factory
- ✅ NPUWorker 通过 Factory 获取 backend，sleep/wake 方法变成调 backend.suspend/resume

---

## 5. 验证

### 行为等价性

```python
# tests/ut/device_allocator/test_ascend_sleep_backend.py
class TestAscendSleepModeBackend:
    def test_factory_registration(self):
        backend = SleepModeBackendFactory.create("ascend_npu")
        assert isinstance(backend, AscendSleepModeBackend)
    
    def test_basic_suspend_resume_roundtrip(self):
        # 创建 backend（enable_sleep_mode_extra_cleanup=False）
        backend.suspend(level=2)
        backend.resume()
        # 推理 → bit-exact
    
    def test_extra_cleanup_suspend_resume_roundtrip(self):
        # 创建 backend（enable_sleep_mode_extra_cleanup=True）
        backend.suspend(level=2)
        backend.resume()
        # 推理 → bit-exact
    
    def test_preserves_flags(self):
        basic_backend = AscendCuMemBackend(...)
        assert basic_backend.preserves_communicators() == True
        assert basic_backend.preserves_graphs_with_communicators() == True
        
        extra_backend = AscendExtraCleanupBackend(...)
        assert extra_backend.preserves_communicators() == False
        assert extra_backend.preserves_graphs_with_communicators() == False
    
    def test_backward_compat(self):
        # 确认 enable_sleep_mode_extra_cleanup=False 时行为与之前完全一致
        # 通过 golden output 对比
```

---

## 6. 验收标准

- [ ] `AscendSleepModeBackend` 类已创建，继承 `SleepModeBackend`
- [ ] 已注册到 `SleepModeBackendFactory`，`SleepModeBackendFactory.create("ascend_npu")` 能返回正确实例
- [ ] `NPUWorker.sleep()` / `wake_up()` 改为通过 backend 调用
- [ ] UT 通过：`test_ascend_sleep_backend.py`
- [ ] E2E：单卡 sleep/wake bit-exact，多卡 TP sleep/wake bit-exact
- [ ] `enable_sleep_mode_extra_cleanup=False/True` 两种模式都覆盖
- [ ] **性能零回归**：重构后的 sleep/wake 耗时与之前完全相同（架构对齐不应引入开销）

---

## 7. 贡献者指南

1. **Fork** `https://github.com/vllm-project/vllm-ascend`，创建分支 `feature/sleep-mode-backend`
2. 先读上游 `.tmp_vllm/vllm/device_allocator/sleep_mode_backend.py` 完整代码，理解 Factory 的注册 API
3. 在 `vllm_ascend/device_allocator/ascend_sleep_backend.py` 创建 Backend 类
4. 在 `platform.py` 注册
5. 修改 `worker.py` 入口（**最小化改动，保持向后兼容**）
6. 跑 UT + E2E

---

## 8. 参考资料

| 上游 | 说明 |
|------|------|
| `vllm/device_allocator/sleep_mode_backend.py` | SleepModeBackend 抽象 + CuMemBackend + SleepModeBackendFactory |
| RFC #34303 | Pluggable sleep-mode backend abstraction |
| GPUWorker sleep/wake 实现 | `vllm/v1/worker/gpu_worker.py:193-250` |

| Ascend 侧 | 说明 |
|-----------|------|
| NPUWorker sleep/wake | `vllm_ascend/worker/worker.py:221-269` |
| SleepWakeupManager | `vllm_ascend/device_allocator/sleep_mem_optimized.py:34-186` |
| CaMemAllocator | `vllm_ascend/device_allocator/camem.py:113-249` |
| `is_sleep_mode_available()` | `vllm_ascend/platform.py:110-119` |
