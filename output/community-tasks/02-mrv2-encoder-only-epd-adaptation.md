---
name: "Feature Request: [MRV2] 支持 Encoder-Only 模型与 EPD 分离部署"
about: "为 vllm-ascend Ascend NPU 适配上游 EncoderOnlyModelState 与 Encoder-Prefill-Decoder 分离部署能力"
title: "[MRV2] 支持 Encoder-Only 模型与 EPD 分离部署 (Encoder-Only & Encoder-Prefill-Decoder separation)"
labels: ["mrv2", "encoder-only", "epd", "feature-request", "good-first-issue"]
assignees: ""
---

# Feature Request: [MRV2] 支持 Encoder-Only 模型与 EPD 分离部署 (Encoder-Only & Encoder-Prefill-Decoder separation)

## 技术目标

在 vllm-ascend Ascend NPU 平台上实现对 vLLM 上游 MRV2 (ModelRunner V2) `EncoderOnlyModelState` 的完整适配，使 BERT/RoBERTa 等 encoder-only 模型能够在 NPU 上以 MRV2 路径高效推理，并支持 Encoder-Prefill-Decoder (EPD) 分离部署场景下的 encoder-only 实例独立运行。

## 实现范围

### 关键 ascend 侧文件

| 文件路径 | 作用 | 适配要点 |
|---------|------|---------|
| `vllm_ascend/worker/v2/model_runner.py` | MRV2 NPUModelRunner | 验证 `EncoderOnlyModelState` 分支路径、`is_encoder_only` 短路逻辑 |
| `vllm_ascend/attention/attention_v1.py` | AscendAttentionBackend (FIA) | encoder-only 模式无 KV cache、bidirectional attention |
| `vllm_ascend/attention/sfa_v1.py` | AscendSFABackend (MLA/SFA) | encoder-only 模式适配 |
| `vllm_ascend/attention/utils.py` | AscendCommonAttentionMetadata 等 | 检查 block_table / slot_mapping 依赖 |
| `vllm_ascend/worker/v2/attn_utils.py` | MRV2 attention 初始化 | encoder-only attention 类型的识别与处理 |

### 上游参考文件

| 文件路径 | 作用 |
|---------|------|
| `vllm/v1/worker/gpu/model_states/encoder_only.py` | **EncoderOnlyModelState 核心实现** |
| `vllm/model_executor/layers/attention/encoder_only_attention.py` | **EncoderOnlyAttention 层 + 动态 backend 包装器** |
| `vllm/v1/worker/gpu/model_states/__init__.py` | `init_model_state()` 路由逻辑 |
| `vllm/v1/worker/gpu/model_runner.py` | GPUModelRunner `is_encoder_only` 分支 |
| `vllm/v1/attention/backend.py` | `AttentionType.ENCODER_ONLY` 枚举 + `supports_non_causal()` |
| `vllm/v1/attention/selector.py` | attention backend 选择器中的 `ENCODER_ONLY` 映射 |
| `vllm/v1/kv_cache_interface.py` | `EncoderOnlyAttentionSpec` / `KVCacheSpecKind.ENCODER_ONLY_ATTENTION` |
| `vllm/v1/outputs.py` | `make_empty_encoder_model_runner_output()` |

## 背景

### 上游新增 EncoderOnlyModelState

vLLM 上游通过一系列 PR（见下方「上游参考资料」）在 MRV2 架构中引入了完整的 **encoder-only 模型支持**：

1. **新的 ModelState 子类** `EncoderOnlyModelState`（`vllm/v1/worker/gpu/model_states/encoder_only.py`），继承自 `DefaultModelState`，核心特征：
   - **无 KV cache**：encoder attention 不需要 KV cache，`EncoderOnlyAttention.get_kv_cache_spec()` 返回 `None`
   - **双向 self-attention**：非 causal 的 varlen full self-attention
   - **独立 metadata 构建**：`EncoderOnlyModelState` 自己构建 encoder attention 的 metadata，不进入 `kv_cache_config.kv_cache_groups` 路径
   - **dummy block_table / slot_mapping**：因为 encoder attention 不读 block_table，但 metadata builder 要求两者存在

2. **新的 Attention 层** `EncoderOnlyAttention`（`vllm/model_executor/layers/attention/encoder_only_attention.py`），通过 `create_encoder_only_attention_backend()` 动态包装底层 attention backend，强制 `causal=False`。

3. **ModelState 路由**：`init_model_state()` 自动检测模型中的 `EncoderOnlyAttention` 层并返回 `EncoderOnlyModelState`。

4. **ModelRunner 短路路径**：`GPUModelRunner` 中多处 `if self.is_encoder_only:` 短路：
   - `get_kv_cache_spec()` 返回空 dict
   - `_dummy_run()` 返回空 tensor
   - `profile_run()` 跳过 dummy run + gc 后直接返回
   - `capture_model()` 跳过 CUDA graph capture
   - `execute_model()` 跳过 forward，返回 `make_empty_encoder_model_runner_output()`
   - `ec_connector` 路径：encoder-only 实例直接 encode 发布，跳过 `get_mm_embeddings` gather

5. **任务类型支持**：`token_embed`、`token_classify`、`reward`（sequence/token reward）等 pooling 任务类型依赖 encoder-only 模型。

### EPD 分离部署 Encoder-Only 实例

在 Encoder-Prefill-Decoder (EPD) 分离部署场景中，encoder-only 实例独立运行 encoder 模型（如 BERT），只负责：
- 接收 multimodal 输入（图像、音频等）
- 通过 `EncoderCache` / `ECConnector` 进行 encode 并发布结果
- **不参与** token 生成、KV cache 管理、sampler 等 decoder 路径

上游 `GPUModelRunner.execute_model()` 的 `is_encoder_only` 分支代码（简化）：

```python
# vllm/v1/worker/gpu/model_runner.py:1543-1560
with self.ec_connector.maybe_get_output(scheduler_output) as ec_connector_output:
    if self.is_encoder_only:
        # Encode and publish, nothing else: this instance runs no
        # language model, so the gather inside get_mm_embeddings
        # would build an inputs_embeds nobody reads -- and it
        # raises "Encoder cache miss" for any scheduled item this
        # instance did not encode, taking the engine down with it.
        self.model_state.execute_mm_encoder(scheduled_encoder_inputs)
    else:
        inputs_embeds = self.model_state.get_mm_embeddings(
            scheduled_encoder_inputs, input_batch, self.req_states
        )

if self.is_encoder_only:
    output = make_empty_encoder_model_runner_output(scheduler_output)
    output.ec_connector_output = ec_connector_output
    return output
```

## Ascend 适配点

### 1. NPUModelRunner EncoderOnlyModelState 分支验证

**问题**：`NPUModelRunner`（`vllm_ascend/worker/v2/model_runner.py`）继承自 `GPUModelRunner`，父类 `__init__` 已设置 `self.is_encoder_only = vllm_config.is_encoder_only`。但 NPUModelRunner 重写了多个方法（`initialize_kv_cache`、`profile_run`、`prepare_inputs`、`execute_model` 等），需要验证这些方法在 `is_encoder_only=True` 时不会因 NPU 特定逻辑（如 seq_lens_cpu 准备、EPLB、ACL graph manager）而出错。

**具体检查点**：
- `NPUModelRunner.__init__` 中的 `AscendEagleSpeculator` 初始化、`AscendRequestState`/`AscendInputBuffers` 重建是否与 encoder-only 兼容
- `initialize_kv_cache()` 的 `graph_manager_wrapper` 上下文管理器在 encoder-only 下是否安全（上游 `get_kv_cache_spec()` 返回 `{}`）
- `profile_run()` 中的 `mc2_tokens_capacity` dummy run 是否需要额外跳过
- `prepare_inputs()` 是否在 encoder-only 场景下仍能正确处理（特别是 `_update_seq_lens_cpu` 调用）
- `execute_model()` 的 `flashcomm_dispatch_wrapper` 和 SP all_gather 路径

### 2. Ascend Attention Backend Encoder-Only 模式适配

**问题**：上游 `EncoderOnlyAttention` 通过 `create_encoder_only_attention_backend()` 动态包装底层 backend，核心是在 metadata builder 中强制 `causal=False`。Ascend 的两个主要 attention backend 需要验证：

**a) AscendAttentionBackend (FIA)**

`AscendAttentionMetadataBuilder.build()` 中已有 `causal` 透传（`attention_v1.py:387`）：
```python
causal=common_attn_metadata.causal,
```
但需要检查：
- `AttentionMaskBuilder.get_attention_mask(False, ...)` 是否能正确生成双向（非 causal）attention mask
- `AscendAttentionBackendImpl` 的 forward 路径中 `sparse_mode` 计算（`attention_v1.py:868`）：
  ```python
  sparse_mode = 4 if self.sliding_window else 3 if attn_metadata.causal else 0
  ```
  非 causal 时 `sparse_mode=0`，这是正确的
- 无 KV cache 时 FIA 的 block_table 参数如何处理：上游使用 dummy block_table

**b) AscendSFABackend (MLA/SFA)**

需要验证：
- `AscendSFABackend` 是否注册为支持 `ENCODER_ONLY` attention 类型
- `AscendSFAMetadataBuilder` 中的 `seq_lens_cpu`、`cum_query_lens` 在 encoder-only 下的正确性
- encoder-only 模型通常不使用 MLA/SFA，重点在 FIA backend

### 3. BlockTable / SlotMapping Encoder-Only 短路逻辑

**问题**：上游 `EncoderOnlyModelState` 不使用 KV cache，encoder attention 不需要读 block_table 和 slot_mapping。但 NPUModelRunner 的 `prepare_inputs()`、attention metadata builder 等路径中可能硬依赖这些 tensor 的形状和内容。

**上游处理方式**（`encoder_only.py:90-95`）：
```python
self._dummy_block_table = torch.zeros(
    self.max_num_reqs, 1, dtype=torch.int32, device=device
)
self._dummy_slot_mapping = torch.zeros(
    self.max_num_tokens, dtype=torch.int64, device=device
)
```

**需要适配的位置**：
- `NPUModelRunner.prepare_inputs()` 中构建的 `input_batch` 是否包含 encoder-only 不需要的字段
- `AscendAttentionMetadataBuilder.build()` 对 `block_table_tensor` 的访问（`attention_v1.py:301`）
- `AscendSFAMetadataBuilder._build()` 对 `block_table` 和 `slot_mapping` 的使用（`sfa_v1.py:346-347`）
- `_pad_query_start_loc_for_fia()` 在 encoder-only 场景下的必要性

### 4. EPD 分离部署 Encoder-Only 实例 MM Embedding Gather 跳过

**问题**：上游在 `is_encoder_only=True` 时直接调用 `model_state.execute_mm_encoder()` 并跳过 `get_mm_embeddings()`。这条路径的关键前提是 `ECConnector` 和 `EncoderCache` 的正常工作。

**需要验证的点**：
- NPU 上 `ECConnector`（`get_ec_connector()`）是否正常初始化
- `EncoderCache` 是否在 NPU device 上正确创建和管理
- `make_empty_encoder_model_runner_output()` 返回空 output 后，NPUModelRunner 的 `execute_model()` 后处理逻辑（如 `flashcomm_dispatch_wrapper` 中的 SP all_gather）是否会干扰 encoder-only 实例
- `self.pooling_runner` 初始化路径：encoder-only pooling 模型需要 `PoolingRunner`

### 5. get_kv_cache_spec / initialize_kv_cache 空字典路径

**关键上游代码**（`model_runner.py:483-486`）：
```python
def get_kv_cache_spec(self):
    if self.is_encoder_only:
        return {}
    return get_kv_cache_spec(self.vllm_config)
```

当 `get_kv_cache_spec()` 返回 `{}` 时，`initialize_kv_cache()` 中的循环不会执行：
```python
for kv_cache_group in kv_cache_config.kv_cache_groups:
    # ... 不会进入
```

但 NPUModelRunner 的 `initialize_kv_cache()` 包装在 `graph_manager_wrapper` 中，后者替换了 `ModelCudaGraphManager`。需要确认空 `kv_cache_config` 下这些包装器不会出错。

## 预期技术收益

- ✅ **支持 BERT/RoBERTa 等 encoder-only 模型在 Ascend NPU 上通过 MRV2 推理**
- ✅ **支持 EPD 分离部署场景下的 encoder-only 实例独立运行**
- ✅ **覆盖 reward model 场景**：sequence reward 和 token reward（`token_classify` 任务）
- ✅ **embedding / pooling 模型统一走 encoder-only 路径**
- ✅ **利用 encoder-only 零 KV cache 开销**：与标准 decoder 模型相比，显存占用显著降低

## 上游参考资料

### 核心 PR

| PR | 标题 | 核心改动 |
|----|------|---------|
| **#48791** | Encoder-only models in vLLM v2 | 引入 `EncoderOnlyModelState`、`EncoderOnlyAttention`、token_classify 任务支持 |
| **#51222** | EncoderOnlyModelState: EPD separation path | 完善 EPD 分离部署下的 encoder-only 实例独立运行路径、跳过 MM embedding gather |
| **#51251** | Encoder-only attention metadata builder: support non-causal + varlen | 修复 encoder-only attention metadata 构建、dummy block_table/slot_mapping |

### 核心代码路径

```
init_model_state()
  ├─ EncoderOnlyAttention 检测
  │    └─ return EncoderOnlyModelState
  └─ DefaultModelState (fallback)

EncoderOnlyModelState
  ├─ __init__(): 构建 encoder_attn_groups, dummy_block_table, dummy_slot_mapping
  ├─ prepare_attn(): super + _build_encoder_attn_metadata()
  └─ _build_encoder_attn_metadata(): 用 dummy tensors 构建 CommonAttentionMetadata

EncoderOnlyAttention
  ├─ get_kv_cache_spec() → None (无 KV cache)
  └─ create_encoder_only_attention_backend(): 动态包装底层 backend, causal=False

GPUModelRunner (is_encoder_only 分支)
  ├─ get_kv_cache_spec() → {}
  ├─ _dummy_run() → 空 tensor
  ├─ profile_run() → 跳过 dummy run
  ├─ capture_model() → 返回 0
  └─ execute_model() → 跳过 forward, 返回 make_empty_encoder_model_runner_output()
       └─ ec_connector: execute_mm_encoder() 而不是 get_mm_embeddings()
```

## 贡献指南

### 仓库

- **主仓库**: `https://github.com/vllm-project/vllm-ascend`
- **分支策略**: 基于 `main` 创建 feature 分支，命名格式 `feature/mrv2-encoder-only`

### 关键文件清单

需要修改/验证的 Ascend 侧文件：

```
vllm_ascend/
├── worker/v2/
│   ├── model_runner.py          # NPUModelRunner encoder-only 分支验证
│   ├── attn_utils.py            # attention 初始化
│   └── input_batch.py           # AscendInputBatch encoder-only 兼容
├── attention/
│   ├── attention_v1.py          # AscendAttentionBackend encoder-only
│   ├── sfa_v1.py                # AscendSFABackend encoder-only (次要)
│   ├── utils.py                 # CommonAttentionMetadata 扩展
│   └── attention_mask.py        # 非 causal attention mask 生成
└── ascend_forward_context.py    # MRV2 profile_run 适配
```

### 测试路径

**现有测试（可作为参考）**：
- `tests/ut/attention/a2/test_attention_v1_precision.py::test_encoder_only_backend_correctness` — 已有 encoder-only attention backend 精度测试
- 上游测试参考：`tests/v1/attention/test_attention_backends.py`

**需要新增的测试**：
- `tests/ut/worker/a2/test_model_runner_v2.py` 中新增 encoder-only 场景
- EPD 分离部署 encoder-only 实例集成测试
- PoolingRunner 在 NPU 上的 encoder-only 模型测试（BERT-base 简单 sequence classification）

### 提交规范

- 每个适配点一个 commit，便于 review
- Commit message 格式：`feat(mrv2): [encoder-only] 适配 AscendAttentionBackend 无 KV cache 路径`
- 确保 `mypy` 和 lint 通过
- 关联本 issue

### 开发注意事项

- encoder-only 模型在 MRV2 下 **不使用 KV cache**，所有与 KV cache 分配、block table 构建、slot mapping 填充相关的代码路径都要检查是否会导致错误
- encoder attention 是 **bidirectional (非 causal)** 的，attention mask 生成逻辑必须正确支持
- dummy block_table / slot_mapping 是 placeholder，形状需要满足 attention kernel 的最低要求

## 验收标准

1. **BERT/RoBERTa encoder-only 模型在 Ascend NPU 上通过 MRV2 加载成功**，无 KV cache 分配错误
2. **encoder-only 模型推理正确性验证**：token_embed、token_classify 任务输出与 GPU 一致（精度在可接受范围内）
3. **EPD 分离部署 encoder-only 实例可独立运行**：ECConnector 路径正常，无 "Encoder cache miss" 错误
4. **PoolingRunner 在 NPU 上正常工作**：sequence classification、reward model 推理
5. **NPUModelRunner.is_encoder_only=True 时 profile_run 和 capture_model 正确短路**，无多余内存分配
6. **ACL graph 模式兼容**：encoder-only 路径不尝试 graph capture
7. **不影响现有 decoder-only 模型功能**：所有现有测试继续通过

## 前置问题

1. **EPD 分离部署在 Ascend 集群的实际需求确认**：当前 Ascend 部署场景中是否已存在需要 encoder-only 实例独立运行的实际需求？（如多模态 + LLM 的分离部署架构）
2. **encoder-only attention kernel 在 NPU 上的性能确认**：无 KV cache 的 varlen self-attention 在 Ascend FlashAttention (FIA) backend 上是否已有优化路径？还是目前走的是通用 varlen attention 路径？
3. **PoolingRunner 在 NPU MRV2 上的当前状态**：`vllm_ascend/worker/v2/pooling_runner.py` 是否已适配，还是需要同步验证？
4. **上游 PR 合入状态**：确认 `#48791`、`#51222`、`#51251` 已全部合入 vLLM main 分支

---

**Issue 分类**: 🏗️ 功能适配 · 🎯 MRV2 关键路径
**预计工作量**: 2~3 人天（含测试）
**难度**: 中等
