# MRV2 每日报告
生成时间: 2026-07-23 10:34:56
统计范围: 最近 30 天

**MRV2 定义**: `vllm/v1/worker/gpu/model_runner.py` 及其依赖的所有组件

MRV2 相关 commits 总数: 125

## 2026-07-22
### vllm
- **[6049424b](https://github.com/vllm-project/vllm/commit/6049424b7e81d0c22a25b202449fa2007be454d7)** ([#49364](https://github.com/vllm-project/vllm/pull/49364)) 在 capture 时始终构建 attention metadata
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `cudagraph`, `attention`, `spec-decode`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+34/-17)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/cudagraph_utils.py` (+1/-4)
  - Ascend 影响: ✓ 无影响

- **[a1c15bcb](https://github.com/vllm-project/vllm/commit/a1c15bcb0fc64c5211240a1a043081bceb0e20e1)** ([#49356](https://github.com/vllm-project/vllm/pull/49356)) [CI][Bugfix] 修复并接入 streaming-input 测试
  - 标签: `chore`, `low-risk`, `ci`, `tests`, `streaming-input`
  - 变更文件:
  - 修改 `.buildkite/test_areas/misc.yaml` (+2/-0)
  - 修改 `tests/v1/streaming_input/test_gpu_model_runner_streaming.py` (+3/-1)
  - 修改 `tests/v1/streaming_input/test_gpu_model_runner_v2_streaming.py` (+3/-3)
  - 修改 `tests/v1/streaming_input/test_scheduler_streaming.py` (+5/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-21
### vllm
- **[f890e1db](https://github.com/vllm-project/vllm/commit/f890e1dbe2fe5deddd5417250b4e1e2db71e9314)** ([#48843](https://github.com/vllm-project/vllm/pull/48843)) [BugFix] 在 FULL CUDA graph 捕获前设置 graph_pool_id
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `cudagraph`, `model-runner`
  - 变更文件:
  - 新增 `tests/v1/cudagraph/test_cudagraph_manager.py` (+111/-0)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+5/-0)
  - Ascend 影响: ✓ 无影响

- **[6700813f](https://github.com/vllm-project/vllm/commit/6700813f86552a2e0787989dd9f468fddcb88bac)** ([#44456](https://github.com/vllm-project/vllm/pull/44456)) [3/N][KV-Cache 布局重构] 标准化 Mamba cache；移除 get_transfer_cache_regions
  - 标签: `refactor`, `mrv2`, `high-risk`, `kv-cache`, `mamba`, `kv-connector`, `model-runner`, `attention`
  - 变更文件:
  - 修改 `tests/v1/kv_connector/unit/offloading_connector/test_worker.py` (+1/-2)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/utils.py` (+0/-28)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/mooncake/mooncake_connector.py` (+3/-3)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py` (+51/-61)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/offloading/worker.py` (+7/-20)
  - 修改 `vllm/model_executor/layers/attention_layer_base.py` (+10/-0)
  - 修改 `vllm/model_executor/layers/mamba/abstract.py` (+18/-0)
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+11/-87)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+9/-22)
  - 修改 `vllm/v1/worker/utils.py` (+5/-2)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的核心覆盖路径 vllm/v1/worker/gpu/attn_utils.py（+11/-87），重构移除了 get_transfer_cache_regions 接口并大幅简化 attention metadata 构建逻辑。vllm-ascend 有自己的 attn_utils 实现，需同步移除对 get_transfer_cache_regions 的依赖并适配标准化的 Mamba cache 布局接口。gpu_model_runner.py 的变更也可能影响 NPUModelRunner 子类。
    - 建议测试区域: `vllm-ascend attn_utils get_transfer_cache_regions 依赖检查`, `Mamba 模型 Ascend KV cache 布局验证`, `NPUModelRunner cache 布局适配验证`

- **[1134545b](https://github.com/vllm-project/vllm/commit/1134545b6f0064e5fa1459455d18b05d8ffaae1f)** ([#49033](https://github.com/vllm-project/vllm/pull/49033)) 回退"[Sampler] 在 apply_sampling_params 中停止将 logits 上转为 fp32"
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `sampler`, `revert`
  - 变更文件:
  - 修改 `tests/v1/sample/test_topk_topp_sampler.py` (+0/-38)
  - 修改 `vllm/v1/sample/ops/topk_topp_sampler.py` (+4/-6)
  - 修改 `vllm/v1/sample/ops/topk_topp_triton.py` (+13/-19)
  - 修改 `vllm/v1/worker/gpu/sample/logit_bias.py` (+1/-3)
  - 修改 `vllm/v1/worker/gpu/sample/sampler.py` (+7/-19)
  - Ascend 影响: ✓ 无影响

- **[ea0e9c8f](https://github.com/vllm-project/vllm/commit/ea0e9c8f2e4b037e6fa4d914c82bf178c9f65f55)** ([#47985](https://github.com/vllm-project/vllm/pull/47985)) 添加 encoder cache profiling 实现
  - 标签: `feature`, `mrv2`, `medium-risk`, `multimodal`, `encoder-cache`, `model-runner`, `profiler`
  - 变更文件:
  - 修改 `vllm/multimodal/encoder_budget.py` (+28/-1)
  - 修改 `vllm/v1/worker/gpu/mm/encoder_cache.py` (+1/-1)
  - 修改 `vllm/v1/worker/gpu/mm/encoder_runner.py` (+43/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+21/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的核心覆盖路径 vllm/v1/worker/gpu/model_runner.py（+21/-0），NPUModelRunner 继承 GPUModelRunner，新增的 encoder cache profiling 钩子会传递到 Ascend 子类。vllm-ascend 需评估 NPUModelRunner 是否需要适配 profiling 接口，以及 Ascend 上 encoder cache profiling 的正确性。
    - 建议测试区域: `NPUModelRunner encoder cache profiling 适配`, `Ascend 多模态 encoder profiling 正确性`

- **[97a66815](https://github.com/vllm-project/vllm/commit/97a668152b9033caf602b37b88289f03e8faffd8)** ([#44214](https://github.com/vllm-project/vllm/pull/44214)) [RL Infra][FlashInfer] 启用 FlashInfer 单体 MoE kernel 的 router replay 输出
  - 标签: `feature`, `medium-risk`, `moe`, `flashinfer`, `rl-infra`
  - 变更文件（共 11 个）:
  - 新增 `tests/kernels/moe/test_routed_experts_capture_monolithic.py` (+880/-0)
  - 修改 `tests/model_executor/test_routed_experts_capture.py` (+55/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/experts/trtllm_bf16_moe.py` (+13/-1)
  - 修改 `vllm/model_executor/layers/fused_moe/experts/trtllm_fp8_moe.py` (+23/-1)
  - 修改 `vllm/model_executor/layers/fused_moe/experts/trtllm_mxfp4_moe.py` (+11/-1)
  - 修改 `vllm/model_executor/layers/fused_moe/experts/trtllm_mxint4_moe.py` (+14/-1)
  - 修改 `vllm/model_executor/layers/fused_moe/experts/trtllm_nvfp4_moe.py` (+13/-1)
  - 修改 `vllm/model_executor/layers/fused_moe/modular_kernel.py` (+51/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/routed_experts_capturer.py` (+11/-1)
  - 修改 `vllm/model_executor/layers/quantization/utils/flashinfer_mxint4_moe.py` (+2/-0)
  - ... 及其他 1 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-07-20
### vllm-ascend
- **[fd69c96a](https://github.com/vllm-project/vllm-ascend/commit/fd69c96a5aad41108523b7e8bdcc167bd2093f0a)** ([#12017](https://github.com/vllm-project/vllm-ascend/pull/12017)) [特性] 为 DSpark 支持 FullGraph
  - 标签: `feature`, `mrv2`, `medium-risk`, `spec-decode`, `dspark`, `aclgraph`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+13/-1)
  - 修改 `vllm_ascend/worker/v2/aclgraph_utils.py` (+12/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dspark/speculator.py` (+44/-2)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-19
### vllm
- **[b6ff8a2f](https://github.com/vllm-project/vllm/commit/b6ff8a2f509cc7ac9c58176f5115a836aa1e08bd)** ([#46570](https://github.com/vllm-project/vllm/pull/46570)) [Core] 为 MLA 添加虚拟批次 Prefill Context Parallelism 支持
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `attention`, `distributed`, `kv-cache`, `mla`, `pcp`, `tests`
  - 变更文件（共 39 个）:
  - 修改 `.buildkite/test_areas/lm_eval.yaml` (+22/-0)
  - 新增 `tests/evals/gsm8k/configs/GLM-5.2-NVFP4-TP1-PCP4-EP.yaml` (+16/-0)
  - 新增 `tests/evals/gsm8k/configs/GLM-5.2-NVFP4-TP2-PCP2-EP.yaml` (+17/-0)
  - 新增 `tests/evals/gsm8k/configs/models-pcp.txt` (+2/-0)
  - 修改 `tests/evals/gsm8k/gsm8k_eval.py` (+15/-1)
  - 修改 `tests/evals/gsm8k/test_gsm8k_correctness.py` (+1/-0)
  - 修改 `tests/v1/attention/test_attention_splitting.py` (+16/-0)
  - 修改 `tests/v1/attention/test_sparse_mla_backends.py` (+7/-0)
  - 修改 `tests/v1/kv_offload/test_factory.py` (+4/-4)
  - 修改 `tests/v1/simple_kv_offload/test_scheduler.py` (+16/-24)
  - ... 及其他 29 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的多个核心覆盖路径：(1) vllm/v1/worker/gpu/model_runner.py - vllm-ascend 通过 vllm_ascend.worker.model_runner_v1.NPUModelRunner 继承 GPUModelRunner，新增的 self.pcp_manager 字段、prepare_input_batch/prepare_attn/prepare_dummy_slot_mappings/sample 中的 PCP 处理逻辑会传递到 Ascend 子类；(2) vllm/v1/worker/gpu/attn_utils.py - vllm-ascend 有自己的 attn_utils 实现，supports_pcp 接口需在 Ascend backend 中实现；(3) vllm/v1/worker/gpu/model_states/default.py - vllm-ascend 覆盖该路径，prepare_attn 中的 PCP 处理需评估；(4) vllm/v1/worker/gpu/block_table.py 与 vllm/v1/worker/block_table.py - vllm-ascend 通过 vllm_ascend.patch.worker.block_table_patch 打补丁，PCP 相关的 block table 操作需验证；(5) vllm/v1/attention/backend.py 与 selector.py - vllm-ascend 有自己的 attention backend，supports_pcp 接口需实现；(6) vllm/model_executor/layers/attention/mla_attention.py - DeepSeek V3/R1 在 Ascend 上使用 MLA，use_pcp 字段与 PCP+DCP 组合的 all-gather/LSE reduce 需验证；(7) vllm/distributed/parallel_state.py 与 vllm/config/parallel.py - 通用分布式与配置路径，PCP group 初始化需验证。vllm-ascend 必须评估是否需要在 NPUModelRunner 中集成 PCPManager、是否需要在 Ascend attention backend 中实现 supports_pcp、以及 MLA + PCP 在 Ascend 通信库（HCCL）下的 all-gather/LSE reduce 正确性。
    - 建议测试区域: `DeepSeek V3/R1 PCP 功能验证`, `MLA + PCP 通信正确性（HCCL all-gather/LSE reduce）`, `Ascend attention backend supports_pcp 接口实现`, `NPUModelRunner PCPManager 集成验证`, `block_table_patch 在 PCP 启用时的行为`, `PCP+DCP 组合在 Ascend 上的正确性`

---

## 2026-07-18
### vllm
- **[c233d90a](https://github.com/vllm-project/vllm/commit/c233d90aa826df072872df47b201450059be8e71)** ([#48496](https://github.com/vllm-project/vllm/pull/48496)) [重构] 移除更多不必要的 load_weights 方法
  - 标签: `refactor`, `medium-risk`, `model-runner`
  - 变更文件（共 44 个）:
  - 修改 `vllm/model_executor/models/AXK1.py` (+1/-13)
  - 修改 `vllm/model_executor/models/aria.py` (+22/-128)
  - 修改 `vllm/model_executor/models/bailing_moe.py` (+24/-92)
  - 修改 `vllm/model_executor/models/bloom.py` (+15/-30)
  - 修改 `vllm/model_executor/models/cohere2_moe.py` (+1/-3)
  - 修改 `vllm/model_executor/models/deepencoder.py` (+3/-10)
  - 修改 `vllm/model_executor/models/deepseek_mtp.py` (+4/-1)
  - 修改 `vllm/model_executor/models/deepseek_v2.py` (+1/-18)
  - 修改 `vllm/model_executor/models/ernie45_moe.py` (+31/-136)
  - 修改 `vllm/model_executor/models/funaudiochat.py` (+17/-32)
  - ... 及其他 34 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/model_executor/models/utils.py 与各模型的 load_weights 路径是通用模型加载接口，vllm-ascend 的模型加载同样依赖该路径。需验证 GLM4/Qwen3 等在 vllm-ascend 上权重加载无回归

- **[d96aee09](https://github.com/vllm-project/vllm/commit/d96aee09518a57fdfe1e83369d2f4ab515f78c30)** ([#48025](https://github.com/vllm-project/vllm/pull/48025)) [修复] 在 process_weights_after_loading 后重新同步 parameter tp_rank（修复 replicated/disable_tp 权重重新加载）
  - 标签: `bugfix`, `medium-risk`, `model-runner`, `distributed`
  - 变更文件:
  - 修改 `vllm/model_executor/layers/linear.py` (+11/-7)
  - 修改 `vllm/model_executor/model_loader/reload/layerwise.py` (+5/-0)
  - 修改 `vllm/model_executor/model_loader/utils.py` (+7/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - linear.py 的权重加载与 tp_rank 同步是通用张量并行路径，vllm-ascend 在 TP 场景同样使用。需验证 disable_tp / replicated 权重在 Ascend 上的加载行为

- **[c71a583a](https://github.com/vllm-project/vllm/commit/c71a583aa9f81400528e67e3d818f66b804e8340)** ([#48110](https://github.com/vllm-project/vllm/pull/48110)) [性能][Hybrid] 将 _copy_mamba_state_block 向量化为 uint64 以优化 temporal 模型
  - 标签: `performance`, `low-risk`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/mamba_utils.py` (+54/-16)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/worker/mamba_utils.py 是 hybrid 模型通用状态管理路径，若 vllm-ascend 支持 Mamba/Hybrid 模型需验证 uint64 向量化在 NPU 上的正确性与性能

- **[425c4eaf](https://github.com/vllm-project/vllm/commit/425c4eafb064f3804538a93584ec07c196d14cf9)** ([#48641](https://github.com/vllm-project/vllm/pull/48641)) [采样器] 在 apply_sampling_params 中停止将 logits 上转为 fp32
  - 标签: `performance`, `medium-risk`, `sample`, `mrv2`
  - 变更文件:
  - 修改 `tests/v1/sample/test_topk_topp_sampler.py` (+38/-0)
  - 修改 `vllm/v1/sample/ops/topk_topp_sampler.py` (+6/-4)
  - 修改 `vllm/v1/sample/ops/topk_topp_triton.py` (+19/-13)
  - 修改 `vllm/v1/worker/gpu/sample/logit_bias.py` (+3/-1)
  - 修改 `vllm/v1/worker/gpu/sample/sampler.py` (+19/-7)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/worker/gpu/sample/sampler.py 与 topk_topp 采样路径是 V2 采样核心，vllm-ascend 的采样器需要关注 logits 精度处理变更是否影响 Ascend 上的采样数值一致性

- **[41ea2dd4](https://github.com/vllm-project/vllm/commit/41ea2dd44a3a20c46ebeb985de0022c7673fb953)** ([#47680](https://github.com/vllm-project/vllm/pull/47680)) [修复][V1/V2] 修复 prompt_logprobs 使其遵循 logprobs_mode
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `model-runner`, `sample`
  - 变更文件（共 11 个）:
  - 修改 `tests/v1/sample/test_logprobs.py` (+38/-0)
  - 修改 `vllm/config/model.py` (+2/-0)
  - 修改 `vllm/config/vllm.py` (+0/-7)
  - 修改 `vllm/model_executor/models/diffusion_gemma.py` (+4/-2)
  - 修改 `vllm/v1/sample/rejection_sampler.py` (+8/-2)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+4/-1)
  - 修改 `vllm/v1/worker/gpu/sample/logprob.py` (+12/-5)
  - 修改 `vllm/v1/worker/gpu/sample/prompt_logprob.py` (+17/-11)
  - 修改 `vllm/v1/worker/gpu/sample/sampler.py` (+8/-6)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler.py` (+5/-3)
  - ... 及其他 1 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改 vllm/v1/worker/gpu_model_runner.py（V1 MR 路径，vllm-ascend 覆盖）与 vllm/v1/worker/gpu/model_runner.py（V2 MR 路径）。重命名 compute_topk_logprobs → compute_topk_scores 并新增 logits_mode 参数，vllm-ascend 若覆盖或调用该采样工具需同步适配；prompt_logprobs 计算分支变更影响 logprobs_mode=raw_logits/processed_logits 的行为
    - 建议测试区域: `prompt_logprobs with raw_logits mode`, `prompt_logprobs with processed_logits mode`, `prompt_logprobs with raw_logprobs / processed_logprobs mode`, `spec_decode rejection_sampler 兼容性`

- **[fcd2255d](https://github.com/vllm-project/vllm/commit/fcd2255d16bd3c62493bae5dee769ce998098f21)** ([#37524](https://github.com/vllm-project/vllm/pull/37524)) [硬件][GPU] 扩展 Profiler 配置范围与注解细节
  - 标签: `feature`, `medium-risk`, `model-runner`, `profiler`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_profiler.py` (+63/-1)
  - 修改 `vllm/config/profiler.py` (+17/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+62/-12)
  - 修改 `vllm/v1/worker/gpu_worker.py` (+98/-13)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/worker/gpu_model_runner.py 是 vllm-ascend 覆盖的关键路径，profiler 注入点扩展可能影响 vllm-ascend 的 model_runner 适配。vllm-ascend 的 profiler 实现需同步评估是否需要扩展对应注解

- **[cc25f028](https://github.com/vllm-project/vllm/commit/cc25f028b76844024fddd0b4ca18d4ca169b32be)** ([#46868](https://github.com/vllm-project/vllm/pull/46868)) [加载器] 改进 InstantTensor 加载
  - 标签: `feature`, `medium-risk`, `model-runner`
  - 变更文件:
  - 修改 `requirements/test/cpu.txt` (+1/-1)
  - 修改 `requirements/test/cuda.in` (+1/-1)
  - 修改 `requirements/test/cuda.txt` (+1/-1)
  - 修改 `requirements/test/nightly-torch.txt` (+1/-1)
  - 修改 `requirements/test/rocm.in` (+1/-1)
  - 修改 `requirements/test/rocm.txt` (+1/-1)
  - 修改 `setup.py` (+1/-1)
  - 修改 `tests/model_executor/model_loader/instanttensor_loader/test_weight_utils.py` (+0/-2)
  - 修改 `vllm/model_executor/model_loader/weight_utils.py` (+20/-5)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/model_executor/model_loader/weight_utils.py 是通用权重加载路径，vllm-ascend 同样使用。InstantTensor 加载逻辑变更需验证不影响 Ascend 上的模型加载

---

## 2026-07-17
### vllm
- **[69d4f5ef](https://github.com/vllm-project/vllm/commit/69d4f5ef6323a44621b10e0f269c2775db510cc5)** [Bugfix][Multimodal] Fix Qwen3-Omni use_audio_in_video with mixed image/video inputs (#46213)
  - 变更文件:
  - 修改 `tests/models/multimodal/processing/test_qwen2_5_omni_embed.py` (+87/-7)
  - 修改 `tests/v1/worker/test_encoder_runner.py` (+26/-0)
  - 修改 `vllm/model_executor/models/qwen2_5_omni_thinker.py` (+77/-66)
  - 修改 `vllm/model_executor/models/qwen3_omni_moe_thinker.py` (+5/-5)
  - 修改 `vllm/multimodal/utils.py` (+38/-0)
  - 修改 `vllm/v1/worker/gpu/mm/encoder_runner.py` (+8/-1)
  - 修改 `vllm/v1/worker/gpu/model_states/mm_pruning.py` (+13/-3)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+12/-1)
  - Ascend 影响: ✓ 无影响

- **[3b6c96a1](https://github.com/vllm-project/vllm/commit/3b6c96a101651c78737b23b2bd8f1026c02f22e2)** [Bugfix][Pooling] Fix wrong scores for chunked prefill under torch.compile (#48901)
  - 变更文件:
  - 修改 `tests/models/language/pooling/test_all_pooling_plus_chunked_prefill.py` (+51/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

- **[251f7e47](https://github.com/vllm-project/vllm/commit/251f7e478e8eb0c90a01eb8fff40056da2aa3ff7)** [Model] Add PW CUDA graph support for Inkling [2/N] (#48822)
  - 变更文件:
  - 修改 `tests/models/inkling/test_contract_validation.py` (+5/-5)
  - 修改 `tests/v1/cudagraph/test_breakable_cudagraph.py` (+50/-0)
  - 修改 `vllm/config/vllm.py` (+2/-0)
  - 修改 `vllm/models/inkling/nvidia/attention.py` (+2/-0)
  - 修改 `vllm/models/inkling/nvidia/ops/sconv.py` (+4/-4)
  - 修改 `vllm/models/inkling/nvidia/sconv_swa_attn.py` (+1/-3)
  - 修改 `vllm/models/inkling/nvidia/short_conv.py` (+2/-2)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+23/-16)
  - 修改 `vllm/v1/worker/gpu/model_states/default.py` (+5/-1)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/cudagraph_utils.py` (+4/-1)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[b269feee](https://github.com/vllm-project/vllm-ascend/commit/b269feeed211b1de089c9ad23f8b1a94ed981c58)** ([#12094](https://github.com/vllm-project/vllm-ascend/pull/12094)) [CI][BugFix] 修复 MRV2 的 logprobs 函数签名
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `model-runner`, `tests`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+4/-2)
  - 修改 `vllm_ascend/worker/v2/sample/logprob.py` (+10/-5)
  - Ascend 影响: ✓ 无影响

- **[929ef87a](https://github.com/vllm-project/vllm-ascend/commit/929ef87a0b8b534e094a1ea296e729001de41864)** ([#11895](https://github.com/vllm-project/vllm-ascend/pull/11895)) [Feature] 为 DFlash 投机解码支持 FullGraph
  - 标签: `feature`, `medium-risk`, `mrv2`, `model-runner`, `aclgraph`, `spec-decode`, `tests`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+13/-1)
  - 修改 `vllm_ascend/attention/attention_mask.py` (+9/-0)
  - 修改 `vllm_ascend/patch/worker/__init__.py` (+1/-0)
  - 新增 `vllm_ascend/patch/worker/patch_v2/patch_dflash_speculator.py` (+25/-0)
  - 修改 `vllm_ascend/worker/v2/aclgraph_utils.py` (+30/-2)
  - 新增 `vllm_ascend/worker/v2/spec_decode/dflash/aclgraph.py` (+117/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dflash/speculator.py` (+49/-2)
  - 修改 `vllm_ascend/worker/v2/spec_decode/eagle/aclgraph.py` (+11/-16)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-16
### vllm
- **[8bfd6839](https://github.com/vllm-project/vllm/commit/8bfd6839016f9670508cf07c16c68891f83ea117)** ([#48787](https://github.com/vllm-project/vllm/pull/48787)) [Spec Decode] 新增：添加 kv_cache_dtype speculative_config control separately from target
  - 标签: `feature`, `low-risk`, `spec-decode`
  - 变更文件:
  - 修改 `vllm/config/speculative.py` (+4/-0)
  - 修改 `vllm/engine/arg_utils.py` (+4/-0)
  - 修改 `vllm/v1/spec_decode/llm_base_proposer.py` (+9/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/utils.py` (+8/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dspark/utils.py` (+8/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/eagle/utils.py` (+9/-1)
  - Ascend 影响: ✓ 无影响

- **[6a9f24aa](https://github.com/vllm-project/vllm/commit/6a9f24aa8cb856235528d01a829a4ba85fc1c19d)** ([#48764](https://github.com/vllm-project/vllm/pull/48764)) [ROCm] [CI] 修复：修复 CUDA graph mem profile issue
  - 标签: `bugfix`, `mrv2`, `high-risk`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+13/-10)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了 vLLM 核心接口文件 vllm/v1/worker/gpu_model_runner.py，可能影响 vllm-ascend 的适配实现
    - 建议测试区域: `整体功能回归测试`

- **[ecf4aa5c](https://github.com/vllm-project/vllm/commit/ecf4aa5ce2ccd4069f12318ca9d3fcef7c9f6257)** ([#48167](https://github.com/vllm-project/vllm/pull/48167)) [Bugfix] 修复：修复 FlashInfer non-causal draft 注意力 DFlash/DSpark Blackwell
  - 标签: `bugfix`, `mrv2`, `high-risk`, `model-runner`, `attention`, `spec-decode`, `tests`
  - 变更文件（共 12 个）:
  - 新增 `tests/v1/spec_decode/test_dflash_causality.py` (+55/-0)
  - 修改 `tools/pre_commit/generate_attention_backend_docs.py` (+3/-1)
  - 修改 `vllm/model_executor/models/qwen3_dflash.py` (+24/-12)
  - 修改 `vllm/platforms/cuda.py` (+6/-1)
  - 修改 `vllm/v1/attention/backends/flashinfer.py` (+2/-1)
  - 修改 `vllm/v1/spec_decode/dflash.py` (+5/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+4/-3)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+35/-10)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/utils.py` (+5/-11)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dspark/speculator.py` (+0/-2)
  - ... 及其他 2 个文件
  - Ascend 影响: ✓ 无影响

- **[b7950e79](https://github.com/vllm-project/vllm/commit/b7950e798f2094b1163c22787c0ba2e3231bf01b)** ([#47460](https://github.com/vllm-project/vllm/pull/47460)) [Bugfix] 更新：Initialize draft CUDA-graph keys native draft_model proposer
  - 标签: `bugfix`, `mrv2`, `high-risk`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+2/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了 vLLM 核心接口文件 vllm/v1/worker/gpu_model_runner.py，可能影响 vllm-ascend 的适配实现
    - 建议测试区域: `整体功能回归测试`

### vllm-ascend
- **[e77502ef](https://github.com/vllm-project/vllm-ascend/commit/e77502ef715f612f2cc6f3c833174431f26cb765)** ([#11949](https://github.com/vllm-project/vllm-ascend/pull/11949)) [Refactor] 更新：移除 weight prefetch config
  - 标签: `refactor`, `mrv2`, `high-risk`, `model-runner`, `attention`, `spec-decode`, `ops`, `quantization`, `ci`, `tests`, `docs`
  - 变更文件（共 43 个）:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+2/-2)
  - 修改 `docs/hooks/nav_titles.py` (+0/-1)
  - 修改 `docs/source/_templates/Model-Deployment-Tutorial-Template.md` (+7/-8)
  - 修改 `docs/source/_templates/Model-Deployment-Tutorial-Template.zh.md` (+5/-6)
  - 修改 `docs/source/locale/zh_CN/LC_MESSAGES/user_guide/configuration/additional_config.po` (+0/-29)
  - 删除 `docs/source/locale/zh_CN/LC_MESSAGES/user_guide/feature_guide/weight_prefetch.po` (+0/-137)
  - 修改 `docs/source/locale/zh_CN/LC_MESSAGES/user_guide/support_matrix/supported_models.po` (+4/-6)
  - 修改 `docs/source/user_guide/configuration/additional_config.md` (+0/-24)
  - 删除 `docs/source/user_guide/feature_guide/weight_prefetch.md` (+0/-73)
  - 修改 `docs/source/user_guide/support_matrix/supported_models.md` (+29/-29)
  - ... 及其他 33 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-07-15
### vllm
- **[05eed72a](https://github.com/vllm-project/vllm/commit/05eed72aec6c05e6d500c7276b47f7652bb37af6)** ([#48526](https://github.com/vllm-project/vllm/pull/48526)) [ROCm] 更新：Re-enable cudagraph 内存 profiling captured current stream
  - 标签: `mrv2`, `high-risk`, `model-runner`, `distributed`
  - 变更文件:
  - 修改 `vllm/distributed/parallel_state.py` (+10/-2)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+20/-1)
  - 修改 `vllm/v1/worker/gpu_worker.py` (+7/-5)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了 vLLM 核心接口文件 vllm/distributed/parallel_state.py，可能影响 vllm-ascend 的适配实现
    - 建议测试区域: `整体功能回归测试`

- **[3ca242d1](https://github.com/vllm-project/vllm/commit/3ca242d1b6282084b2a41e247810e632450c639a)** ([#48622](https://github.com/vllm-project/vllm/pull/48622)) [Bugfix] [R3] 更新：Exclude draft routers from expert capture
  - 标签: `bugfix`, `mrv2`, `high-risk`, `model-runner`, `tests`
  - 变更文件:
  - 修改 `tests/model_executor/test_routed_experts_capture.py` (+34/-6)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[6e784075](https://github.com/vllm-project/vllm-ascend/commit/6e784075dcc36b603296f03a50cdc005cffe5c61)** ([#11727](https://github.com/vllm-project/vllm-ascend/pull/11727)) [BugFix] 修复：修复 quant DP full graph mode mrv2
  - 标签: `bugfix`, `mrv2`, `low-risk`, `model-runner`, `spec-decode`, `quantization`, `ci`, `tests`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+2/-0)
  - 新增 `tests/e2e/pull_request/two_card/model_runner_v2/test_data_parallel.py` (+95/-0)
  - 修改 `tests/ut/worker/a2/test_worker_v1.py` (+2/-4)
  - 修改 `vllm_ascend/quantization/method_adapters.py` (+9/-0)
  - 修改 `vllm_ascend/worker/v2/aclgraph_utils.py` (+1/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/eagle/aclgraph.py` (+2/-2)
  - 修改 `vllm_ascend/worker/worker.py` (+2/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-14
### vllm
- **[26587f95](https://github.com/vllm-project/vllm/commit/26587f9519e22a5c4549ead7595ad9ca3229c4fd)** ([#48261](https://github.com/vllm-project/vllm/pull/48261)) [BugFix] [ModelRunner V2] 修复：修复 stale attn metadata speculator prefill cudagraph capture
  - 标签: `bugfix`, `mrv2`, `high-risk`, `model-runner`, `spec-decode`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+17/-35)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+7/-3)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/cudagraph_utils.py` (+11/-45)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` (+14/-12)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/cudagraph.py` (+2/-3)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+11/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/speculator.py` (+10/-8)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[f6b33f49](https://github.com/vllm-project/vllm-ascend/commit/f6b33f49cd732733769374c19b68d26a5c210ec0)** ([#11899](https://github.com/vllm-project/vllm-ascend/pull/11899)) [Refactor] [Attention] 更新：移除 paged 注意力
  - 标签: `refactor`, `high-risk`, `model-runner`, `attention`, `tests`, `docs`
  - 变更文件（共 15 个）:
  - 修改 `csrc/attention/kv_quant_sparse_flash_attention/op_host/kv_quant_sparse_flash_attention_tiling.cpp` (+0/-1)
  - 修改 `docs/source/faqs.md` (+0/-4)
  - 修改 `docs/source/locale/zh_CN/LC_MESSAGES/faqs.po` (+0/-18)
  - 修改 `docs/source/locale/zh_CN/LC_MESSAGES/user_guide/configuration/additional_config.po` (+0/-9)
  - 修改 `docs/source/tutorials/features/suffix_speculative_decoding.md` (+1/-1)
  - 修改 `docs/source/tutorials/models/Qwen3-Dense.md` (+1/-1)
  - 修改 `docs/source/user_guide/configuration/additional_config.md` (+0/-1)
  - 修改 `tests/e2e/pull_request/two_card/test_qwen3_performance.py` (+1/-1)
  - 修改 `tests/e2e/weekly/single_node/configs/Qwen3-32B.yaml` (+0/-1)
  - 修改 `tests/ut/_310p/attention/test_attention_v1_310.py` (+1/-4)
  - ... 及其他 5 个文件
  - Ascend 影响: ✓ 无影响

- **[5083d884](https://github.com/vllm-project/vllm-ascend/commit/5083d8844310831258f085ea6dfcac4a2f76ef58)** ([#11709](https://github.com/vllm-project/vllm-ascend/pull/11709)) [CI] 更新：main2main 0710
  - 标签: `chore`, `mrv2`, `high-risk`, `model-runner`, `sample`, `distributed`, `spec-decode`, `kv-cache`, `patch`, `ci`, `tests`
  - 变更文件（共 19 个）:
  - 修改 `.github/vllm-main-verified.commit` (+1/-1)
  - 修改 `pyproject.toml` (+1/-1)
  - 修改 `requirements.txt` (+1/-1)
  - 修改 `tests/e2e/pull_request/one_card/spec_decode/test_extract_hidden_states.py` (+5/-25)
  - 修改 `tests/ut/patch/platform/test_patch_deepseek_v4_tool_call_parser.py` (+11/-1)
  - 新增 `tests/ut/patch/test_hunyuan_vl_processor_compat.py` (+388/-0)
  - 修改 `vllm_ascend/__init__.py` (+5/-0)
  - 修改 `vllm_ascend/core/single_type_kv_cache_manager.py` (+16/-6)
  - 修改 `vllm_ascend/distributed/kv_transfer/kv_pool/cpu_offload/cpu_kv_cache_manager.py` (+5/-1)
  - 修改 `vllm_ascend/patch/__init__.py` (+24/-0)
  - ... 及其他 9 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-07-13
### vllm
- **[1be6e937](https://github.com/vllm-project/vllm/commit/1be6e937b2b49bae652370d80294f6171bd7b981)** ([#48483](https://github.com/vllm-project/vllm/pull/48483)) 更新：降低 内存 所需 捕获 CUDA图 大 cudagraph 尺寸
  - 标签: `mrv2`, `high-risk`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+5/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了 vLLM 核心接口文件 vllm/v1/worker/gpu_model_runner.py，可能影响 vllm-ascend 的适配实现
    - 建议测试区域: `整体功能回归测试`

### vllm-ascend
- **[41ff81e1](https://github.com/vllm-project/vllm-ascend/commit/41ff81e1a7a92e6e3f546198d80702d78b7a50b7)** 新增功能，涉及 Model Runner 模块，修改 .github/workflows/scripts/test_config.yaml；新增 tests/e2e/pull_request/one_card/spec_decode/test_dspark.py；修改 tests/e2e/pull_request/one_card/spec_decode/utils.py；及其他 9 个文件，变更 410 行，删除 24 行。
  - 标签: `feature`, `low-risk`, `model-runner`, `spec-decode`, `ops`, `patch`, `ci`, `tests`
  - 变更文件（共 12 个）:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+9/-0)
  - 新增 `tests/e2e/pull_request/one_card/spec_decode/test_dspark.py` (+87/-0)
  - 修改 `tests/e2e/pull_request/one_card/spec_decode/utils.py` (+8/-0)
  - 修改 `vllm_ascend/ops/triton/spec_decode/utils.py` (+8/-2)
  - 修改 `vllm_ascend/patch/__init__.py` (+18/-0)
  - 修改 `vllm_ascend/patch/worker/__init__.py` (+1/-0)
  - 新增 `vllm_ascend/patch/worker/patch_qwen3_dspark.py` (+15/-0)
  - 修改 `vllm_ascend/spec_decode/__init__.py` (+3/-0)
  - 修改 `vllm_ascend/spec_decode/dflash_proposer.py` (+2/-2)
  - 新增 `vllm_ascend/spec_decode/dspark_proposer.py` (+196/-0)
  - ... 及其他 2 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-07-12
### vllm
- **[a02984ed](https://github.com/vllm-project/vllm/commit/a02984ed471488c0f0e8f73cab21be4325992d4c)** ([#47006](https://github.com/vllm-project/vllm/pull/47006)) [Perf] 更新：Qwen Replace MoE all-reduce reduce-scatter
  - 标签: `performance`, `model-runner`, `medium-risk`, `attention`
  - 变更文件:
  - 修改 `vllm/model_executor/layers/mamba/gdn/qwen_gdn_linear_attn.py` (+2/-0)
  - 修改 `vllm/model_executor/models/qwen3_5.py` (+9/-0)
  - 修改 `vllm/model_executor/models/qwen3_next.py` (+102/-11)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 涉及 vLLM 核心代码变更（vllm/model_executor/layers/mamba/gdn/qwen_gdn_linear_attn.py, vllm/model_executor/models/qwen3_5.py, vllm/model_executor/models/qwen3_next.py），可能影响 vllm-ascend 的相应模块实现。建议 Ascend 侧关注接口兼容性。
    - 建议测试区域: `vllm/model_executor/layers/mamba/gdn/qwen_gdn_linear_attn.py`, `vllm/model_executor/models/qwen3_5.py`, `vllm/model_executor/models/qwen3_next.py`

- **[fc1c5480](https://github.com/vllm-project/vllm/commit/fc1c548093029f6487bbdc9c612995dfe7621a75)** ([#46725](https://github.com/vllm-project/vllm/pull/46725)) 更新：Runtime Draft Weight 更新 Speculative Decoding
  - 标签: `docs`, `worker`, `engine`, `model-runner`, `low-risk`, `distributed`
  - 变更文件（共 12 个）:
  - 修改 `docs/training/weight_transfer/base.md` (+4/-0)
  - 修改 `tests/entrypoints/openai/test_openai_schema.py` (+1/-0)
  - 修改 `tests/v1/worker/test_gpu_worker_weight_transfer.py` (+6/-0)
  - 修改 `vllm/distributed/weight_transfer/base.py` (+18/-0)
  - 修改 `vllm/distributed/weight_transfer/sparse_nccl_engine.py` (+1/-0)
  - 修改 `vllm/engine/protocol.py` (+4/-0)
  - 修改 `vllm/entrypoints/llm.py` (+4/-0)
  - 修改 `vllm/entrypoints/serve/dev/rlhf/api_router.py` (+6/-0)
  - 修改 `vllm/v1/engine/async_llm.py` (+4/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+6/-0)
  - ... 及其他 2 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 涉及 vLLM 核心代码变更（vllm/distributed/weight_transfer/base.py, vllm/distributed/weight_transfer/sparse_nccl_engine.py, vllm/engine/protocol.py），可能影响 vllm-ascend 的相应模块实现。建议 Ascend 侧关注接口兼容性。
    - 建议测试区域: `vllm/distributed/weight_transfer/base.py`, `vllm/distributed/weight_transfer/sparse_nccl_engine.py`, `vllm/engine/protocol.py`, `vllm/entrypoints/llm.py`, `vllm/entrypoints/serve/dev/rlhf/api_router.py`

- **[481e481b](https://github.com/vllm-project/vllm/commit/481e481be786c1ca3229e26aa34c15ffd22375af)** ([#46384](https://github.com/vllm-project/vllm/pull/46384)) [2/N] 修复：核心 支持 partial prefix 缓存 hit hybrid model
  - 标签: `worker`, `engine`, `model-runner`, `config`, `scheduler`, `prefix-caching`, `bugfix`, `distributed`, `medium-risk`
  - 变更文件（共 21 个）:
  - 新增 `tests/v1/core/prefix_cache/test_partial_prefix_cache_hits.py` (+816/-0)
  - 修改 `tests/v1/core/test_deferred_block_free.py` (+62/-0)
  - 修改 `tests/v1/core/test_kv_cache_utils.py` (+60/-0)
  - 修改 `tests/v1/core/test_prefix_caching.py` (+4/-1)
  - 修改 `tests/v1/core/test_single_type_kv_cache_manager.py` (+8/-6)
  - 修改 `tests/v1/kv_connector/unit/test_mooncake_store_coordinator.py` (+15/-15)
  - 修改 `tests/v1/kv_connector/unit/test_mooncake_store_hma_e2e.py` (+1/-0)
  - 修改 `vllm/config/cache.py` (+10/-10)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/coordinator.py` (+17/-9)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/worker.py` (+3/-1)
  - ... 及其他 11 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 涉及 vLLM 核心代码变更（vllm/config/cache.py, vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/coordinator.py, vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/worker.py），可能影响 vllm-ascend 的相应模块实现。建议 Ascend 侧关注接口兼容性。
    - 建议测试区域: `vllm/config/cache.py`, `vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/coordinator.py`, `vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/worker.py`, `vllm/engine/arg_utils.py`, `vllm/v1/core/block_pool.py`

### vllm-ascend
- **[d19628a1](https://github.com/vllm-project/vllm-ascend/commit/d19628a1b292cba1ef33593a6446d3777f28574e)** 变更：[BugFix]Added the store_kv_block_metadata ascendC operator (#11865)
  - 标签: `kernels`, `spec-decode`, `bugfix`, `model-runner`, `medium-risk`, `ascend`, `attention`, `worker`
  - 变更文件（共 27 个）:
  - 修改 `csrc/attention/store_kv_block/op_host/CMakeLists.txt` (+0/-37)
  - 修改 `csrc/attention/store_kv_block/op_host/store_kv_block_infershape.cpp` (+0/-7)
  - 修改 `csrc/attention/store_kv_block/op_host/store_kv_block_tiling.cpp` (+11/-7)
  - 修改 `csrc/attention/store_kv_block/op_kernel/store_kv_block.h` (+11/-12)
  - 修改 `csrc/attention/store_kv_block/store_kv_block_torch_adpt.h` (+0/-92)
  - 新增 `csrc/attention/store_kv_block_metadata/CMakeLists.txt` (+10/-0)
  - 新增 `csrc/attention/store_kv_block_metadata/op_api/aclnn_store_kv_block_metadata.cpp` (+79/-0)
  - 新增 `csrc/attention/store_kv_block_metadata/op_api/aclnn_store_kv_block_metadata.h` (+36/-0)
  - 新增 `csrc/attention/store_kv_block_metadata/op_api/l0_store_kv_block_metadata.cpp` (+53/-0)
  - 新增 `csrc/attention/store_kv_block_metadata/op_api/l0_store_kv_block_metadata.h` (+26/-0)
  - ... 及其他 17 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-07-11
### vllm
- **[04d553f3](https://github.com/vllm-project/vllm/commit/04d553f390fd37e09ab111936ef1592881299957)** [Misc] Use meta tensor for KV cache stride calculation (#47316)
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

- **[9c18e90f](https://github.com/vllm-project/vllm/commit/9c18e90f6c94b90ecdaa99b2230389ba40e0fc69)** [BugFix] Fix packed HND KV cache reshape for FlashAttention (#47314)
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-10
### vllm
- **[08dfd686](https://github.com/vllm-project/vllm/commit/08dfd68610d2e05a0d8ddc99c23488da6163df3f)** [Model] Add LongCat-Flash-Lite (n-gram embedding) (#47857)
  - 变更文件（共 16 个）:
  - 修改 `CMakeLists.txt` (+1/-0)
  - 新增 `csrc/libtorch_stable/ngram_embedding_kernels.cu` (+96/-0)
  - 修改 `csrc/libtorch_stable/ops.h` (+9/-0)
  - 修改 `csrc/libtorch_stable/torch_bindings.cpp` (+13/-0)
  - 修改 `tests/models/registry.py` (+7/-0)
  - 修改 `tests/models/utils.py` (+7/-2)
  - 修改 `vllm/_custom_ops.py` (+31/-0)
  - 修改 `vllm/config/speculative.py` (+1/-1)
  - 修改 `vllm/config/vllm.py` (+1/-0)
  - 修改 `vllm/model_executor/models/config.py` (+19/-1)
  - ... 及其他 6 个文件
  - Ascend 影响: ✓ 无影响

- **[433f2911](https://github.com/vllm-project/vllm/commit/433f291195ded3ca8d278bc78da9280c5d4e5329)** ([#48186](https://github.com/vllm-project/vllm/pull/48186)) [CI] 维护：Right-size test-area timeouts from nightly durations
  - 标签: `chore`, `mrv2`
  - 变更文件（共 30 个）:
  - 修改 `.buildkite/test_areas/attention.yaml` (+3/-3)
  - 修改 `.buildkite/test_areas/basic_correctness.yaml` (+2/-2)
  - 修改 `.buildkite/test_areas/benchmarks.yaml` (+2/-2)
  - 修改 `.buildkite/test_areas/compile.yaml` (+11/-11)
  - 修改 `.buildkite/test_areas/cuda.yaml` (+2/-2)
  - 修改 `.buildkite/test_areas/disaggregated.yaml` (+12/-12)
  - 修改 `.buildkite/test_areas/distributed.yaml` (+10/-10)
  - 修改 `.buildkite/test_areas/docker.yaml` (+1/-1)
  - 修改 `.buildkite/test_areas/e2e_integration.yaml` (+5/-5)
  - 修改 `.buildkite/test_areas/engine.yaml` (+11/-11)
  - ... 及其他 20 个文件
  - Ascend 影响: ✓ 无影响

- **[95ed0fea](https://github.com/vllm-project/vllm/commit/95ed0feaa5cd7fb16d72c53ce04950aaf07c4698)** ([#40996](https://github.com/vllm-project/vllm/pull/40996)) 新增：DCP supports hybrid 注意力
  - 标签: `chore`, `mrv2`, `distributed`, `attention`, `python`, `model-runner`, `low-risk`
  - 变更文件（共 26 个）:
  - 修改 `tests/distributed/test_context_parallel.py` (+8/-0)
  - 修改 `tests/distributed/test_pynccl.py` (+47/-0)
  - 修改 `tests/models/language/generation/test_hybrid.py` (+13/-1)
  - 修改 `tests/models/multimodal/generation/test_vit_cudagraph.py` (+1/-0)
  - 修改 `tests/test_config.py` (+4/-4)
  - 修改 `tests/v1/streaming_input/test_gpu_model_runner_streaming.py` (+1/-0)
  - 新增 `tests/v1/worker/test_cp_utils.py` (+45/-0)
  - 修改 `tests/v1/worker/test_gpu_input_batch.py` (+6/-0)
  - 修改 `tests/v1/worker/test_gpu_model_runner.py` (+3/-0)
  - 修改 `vllm/config/model.py` (+2/-5)
  - ... 及其他 16 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 可能影响 vllm-ascend 的接口或实现
    - 建议测试区域: `vllm/config/model.py`, `vllm/v1/attention/backend.py`, `vllm/v1/attention/backends/flash_attn.py`, `vllm/v1/core/kv_cache_coordinator.py`, `vllm/v1/core/kv_cache_utils.py`, `vllm/v1/core/single_type_kv_cache_manager.py`, `vllm/v1/kv_cache_interface.py`, `vllm/v1/worker/block_table.py`, `vllm/v1/worker/cp_utils.py`, `vllm/v1/worker/gpu_input_batch.py`, `vllm/v1/worker/gpu_model_runner.py`, `vllm/v1/worker/tpu_input_batch.py`

- **[766469a4](https://github.com/vllm-project/vllm/commit/766469a4c460043ae52cda19b1c52f0dc87e555c)** ([#48154](https://github.com/vllm-project/vllm/pull/48154)) [ROCm] 修复：Revert Part `[ROCm 修复 pooling startup workspace lock`
  - 标签: `bugfix`, `low-risk`, `mrv2`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu_worker.py` (+3/-22)
  - Ascend 影响: ✓ 无影响

- **[ff8d3488](https://github.com/vllm-project/vllm/commit/ff8d3488f248acc8b5c1d23243723eeb00c74914)** ([#48132](https://github.com/vllm-project/vllm/pull/48132)) [Bugfix] 新增：MRV2 Reset num_accepted_tokens add_request all modes
  - 标签: `chore`, `mrv2`, `low-risk`, `python`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+2/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 可能影响 vllm-ascend 的接口或实现
    - 建议测试区域: `vllm/v1/worker/gpu/model_states/mamba_hybrid.py`

- **[e08a9151](https://github.com/vllm-project/vllm/commit/e08a9151468190575114de1c996275b993ec940a)** ([#48135](https://github.com/vllm-project/vllm/pull/48135)) [Bugfix] 更新：Preserve tensor causal metadata grouped 注意力
  - 标签: `chore`, `low-risk`, `python`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+4/-2)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 可能影响 vllm-ascend 的接口或实现
    - 建议测试区域: `vllm/v1/worker/gpu/attn_utils.py`

- **[67e7ea89](https://github.com/vllm-project/vllm/commit/67e7ea8977bc4281d4d33dd3a81a5c5fab3df920)** ([#48146](https://github.com/vllm-project/vllm/pull/48146)) [ROCm] 维护：CI Set all timeout_in_minutes 180
  - 标签: `chore`, `mrv2`
  - 变更文件:
  - 修改 `.buildkite/test-amd.yaml` (+27/-27)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-09
### vllm
- **[85b3a726](https://github.com/vllm-project/vllm/commit/85b3a7264b6c4e4e89a1c45a2c4ccfd1b8c342dc)** [Bugfix][Model Runner V2] Order uniform decodes first so spec decodes aren't misclassified as prefills (#47381)
  - 变更文件:
  - 新增 `tests/v1/worker/test_gpu_batch_ordering.py` (+70/-0)
  - 修改 `vllm/model_executor/models/deepseek_v2.py` (+6/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+10/-2)
  - Ascend 影响: ✓ 无影响

- **[1cd75b3d](https://github.com/vllm-project/vllm/commit/1cd75b3dd4b3bf90e4ef81831b6f0dd91fde2fe1)** [Bugfix] Fix race condition in KVBlockZeroer (#48085)
  - 变更文件:
  - 新增 `tests/v1/worker/test_kv_block_zeroer.py` (+44/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+1/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-0)
  - 修改 `vllm/v1/worker/utils.py` (+37/-20)
  - Ascend 影响: ✓ 无影响

- **[95d6d6f4](https://github.com/vllm-project/vllm/commit/95d6d6f4bba8234088e62124ff20a482acd98714)** ([#48046](https://github.com/vllm-project/vllm/pull/48046)) [Bugfix] 更新：Use int8 workspace FlashInfer MLA decode
  - 标签: `bugfix`, `low-risk`, `mrv2`
  - 变更文件:
  - 修改 `tests/kernels/attention/test_flashinfer_mla_decode.py` (+87/-45)
  - 修改 `vllm/v1/attention/backends/mla/flashinfer_mla.py` (+3/-1)
  - 修改 `vllm/v1/attention/backends/mla/flashinfer_mla_sparse.py` (+3/-1)
  - Ascend 影响: ✓ 无影响

- **[26831949](https://github.com/vllm-project/vllm/commit/26831949b48a0d81fba379dcaf7e378206fd9087)** ([#47912](https://github.com/vllm-project/vllm/pull/47912)) [ROCm] 修复：修复 pooling startup workspace lock
  - 标签: `bugfix`, `low-risk`, `mrv2`
  - 变更文件:
  - 修改 `vllm/v1/attention/backends/rocm_attn.py` (+3/-0)
  - 修改 `vllm/v1/attention/backends/triton_attn.py` (+1/-0)
  - 修改 `vllm/v1/attention/ops/triton_prefill_attention.py` (+14/-2)
  - 修改 `vllm/v1/worker/gpu_worker.py` (+22/-3)
  - Ascend 影响: ✓ 无影响

- **[a5d19cbb](https://github.com/vllm-project/vllm/commit/a5d19cbb95872c4b426c06735733568542fa33db)** ([#48014](https://github.com/vllm-project/vllm/pull/48014)) [Core] 更新：Move MRV1 `late_interaction_runner.py` out MRV2 subtree
  - 标签: `chore`, `mrv2`
  - 变更文件:
  - 修改 `tests/v1/worker/test_late_interaction_runner.py` (+1/-1)
  - 重命名 `vllm/v1/pool/late_interaction_runner.py` (+0/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-08
### vllm
- **[0d12618e](https://github.com/vllm-project/vllm/commit/0d12618e98ff2d21d36081e0e9b4eb23573b6d38)** [Spec Decode] Support hybrid (SWA + full attention) DFlash drafters (#47914)
  - 变更文件:
  - 修改 `vllm/config/vllm.py` (+17/-0)
  - 修改 `vllm/model_executor/models/qwen3_dflash.py` (+17/-9)
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+5/-3)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/cudagraph.py` (+4/-7)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+15/-5)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/utils.py` (+5/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dspark/utils.py` (+5/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/eagle/utils.py` (+9/-1)
  - 修改 `vllm/v1/worker/gpu/spec_decode/speculator.py` (+2/-1)
  - Ascend 影响: ✓ 无影响

- **[2afa3f7e](https://github.com/vllm-project/vllm/commit/2afa3f7e950264bb179d030c23a1ed1f46558fd9)** ([#47631](https://github.com/vllm-project/vllm/pull/47631)) [Perf] 新增：Minimax M3 - 支持 cross-layer allreduce-norm 融合
  - 标签: `performance`, `medium-risk`, `model-runner`, `MoE`
  - 变更文件:
  - 修改 `vllm/model_executor/layers/fused_moe/layer.py` (+13/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/runner/moe_runner.py` (+7/-1)
  - 修改 `vllm/model_executor/models/deepseek_v2.py` (+2/-0)
  - 修改 `vllm/models/deepseek_v32/nvidia/model.py` (+4/-4)
  - 修改 `vllm/models/deepseek_v32/nvidia/mtp.py` (+1/-1)
  - 修改 `vllm/models/minimax_m3/nvidia/model.py` (+37/-10)
  - 修改 `vllm/v1/attention/backends/mla/prefill/selector.py` (+1/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: MiniMax-M3 和 DeepseekV2 模型的 MoE 层 all-reduce 逻辑发生变化，Ascend 侧的模型实现可能需要同步调整以支持 reduce_results 参数和 fused_allreduce_gemma_rms_norm 融合路径。
    - 建议测试区域: `vllm/models/minimax_m3/`, `vllm/models/deepseek_v32/`, `tests/e2e/`

- **[7bd15437](https://github.com/vllm-project/vllm/commit/7bd154375dc505046a6e59e6d8c884a9c6b8fc0f)** [Bugfix] Fix mamba+dflash for MRV2 (#47698)
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+1/-4)
  - Ascend 影响: ✓ 无影响

- **[dd127d82](https://github.com/vllm-project/vllm/commit/dd127d82ed29c40b7daf6e751add49ff371b1d9d)** [Core][Engine] only materialize tokens when thinking budget is in req (#47053)
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_model_runner.py` (+26/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+3/-5)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-07
### vllm
- **[65dcde16](https://github.com/vllm-project/vllm/commit/65dcde16957c26cfd65f581b67787c871cea3206)** 修复PD分离+MTP在Qwen3.5(GDN)上的正确性问题。主要修改包括：1) 在combine_sampled_and_draft_tokens kernel中正确处理prompt-tail slots，只重写generated-token slots；2) 修复mamba_hybrid中spec-decode行的检测逻辑，使用num_scheduled_tokens == num_draft_tokens + 1判断decode行；3) 移除states.py中add_request对last_sampled_tokens的冗余写入。
  - 标签: `bugfix`, `pd-disagg`, `mtp`, `high-risk`
  - 变更文件:
  - 修改 `tests/v1/kv_connector/nixl_integration/config_sweep_accuracy_test.sh` (+1/-0)
  - 修改 `tests/v1/kv_connector/nixl_integration/run_accuracy_test.sh` (+7/-2)
  - 修改 `vllm/v1/worker/gpu/input_batch.py` (+4/-2)
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+9/-4)
  - 修改 `vllm/v1/worker/gpu/states.py` (+0/-10)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-4)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了vllm/v1/worker/gpu/input_batch.py中_combine_sampled_and_draft_tokens_kernel的token写入逻辑，vllm/worker/gpu/model_states/mamba_hybrid.py中spec-decode行检测逻辑，以及vllm/v1/worker/gpu/states.py中add_request的last_sampled_tokens写入。vllm-ascend的NPUModelRunner如果重写了这些方法或依赖这些行为，需要同步更新。
    - 建议测试区域: `vllm_ascend/worker/model_runner_v1.py`, `vllm_ascend/worker/worker.py`

- **[d3e69fd6](https://github.com/vllm-project/vllm/commit/d3e69fd6714e9d1bb6e8e4f03157090dc32e7960)** 使用blocking CUDA events避免忙等CUDA driver lock。在async_utils.py、spec_decode/utils.py、gpu_model_runner.py中，将torch.cuda.Event()改为torch.cuda.Event(blocking=True)，使CPU线程在等待GPU事件时进入睡眠状态而不是忙等，减少CUDA driver锁竞争。
  - 标签: `performance`, `cuda`, `medium-risk`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/async_utils.py` (+4/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/utils.py` (+2/-1)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+7/-3)
  - Ascend 影响: ✓ 无影响

- **[2f71b2bd](https://github.com/vllm-project/vllm/commit/2f71b2bd9f693f06973a8abf3823f095bd46ef69)** 在V2 runner中对齐混合encoder-decoder KV cache视图。当decoder self-attention（K/V-first布局）和cross-attention（blocks-first布局）共享同一raw allocation时，通过_align_mixed_attention_kv_cache_views函数重新调整blocks-first视图的stride，使其与K/V-first存储布局兼容。
  - 标签: `bugfix`, `rocm`, `attention`, `medium-risk`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+82/-0)
  - Ascend 影响: ✓ 无影响

- **[69f31509](https://github.com/vllm-project/vllm/commit/69f3150981e4bc8a09439eb7cae0095605b964b4)** 修复XPU上PP（流水线并行）的精度问题。在broadcast方法中，在切换到broadcast stream之前同步main stream，确保所有操作在broadcast前完成。
  - 标签: `bugfix`, `xpu`, `pipeline-parallel`, `low-risk`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/pp_utils.py` (+5/-0)
  - Ascend 影响: ✓ 无影响

- **[567a7843](https://github.com/vllm-project/vllm/commit/567a78432d8e00ac17e4288a4c15ca795c6a1bb4)** 修复DP+MTP hang问题。当DP各rank对input_fits_in_drafter判断不一致时，通过dummy_run防止hang。重构了draft proposal逻辑，将GPU token和CPU token的draft proposal路径分离，确保DP rank在drafter执行上保持一致。
  - 标签: `bugfix`, `data-parallel`, `mtp`, `speculative-decoding`, `high-risk`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+45/-18)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了vllm/v1/worker/gpu_model_runner.py中propose_draft_token_ids逻辑，新增了dummy_run调用和draft_after_bookkeeping路径。vllm-ascend的NPUModelRunner如果重写了draft proposal逻辑，需要同步更新以处理DP rank不一致的情况。
    - 建议测试区域: `vllm_ascend/worker/model_runner_v1.py`, `vllm_ascend/patch/worker/spec_decode_patch.py`

- **[04adc884](https://github.com/vllm-project/vllm/commit/04adc8843bbe0711fed8edf50d6d4cd4fca400e7)** 修复DeepSeek-V4 fp8_ds_mla KV cache reshape问题。在get_kv_cache_spec中传递kv_quant_mode参数，确保在_reshape_kv_cache_tensors中能正确获取cache_dtype_str。修复了当kv_cache_spec有cache_dtype_str属性时优先使用该值而不是self.cache_config.cache_dtype。
  - 标签: `bugfix`, `deepseek`, `kv-cache`, `mla`, `medium-risk`
  - 变更文件:
  - 修改 `vllm/models/deepseek_v4/attention.py` (+6/-1)
  - 修改 `vllm/v1/attention/backends/mla/sparse_swa.py` (+2/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+6/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了vllm/v1/worker/gpu_model_runner.py中_reshape_kv_cache_tensors方法，优先使用kv_cache_spec的cache_dtype_str属性。vllm-ascend的NPUModelRunner如果重写了KV cache reshape逻辑，需要同步更新。同时修改了vllm/models/deepseek_v4/attention.py和vllm/v1/attention/backends/mla/sparse_swa.py中get_kv_cache_spec方法，新增kv_quant_mode参数。
    - 建议测试区域: `vllm_ascend/worker/model_runner_v1.py`, `vllm_ascend/attention/attention_v1.py`

### vllm-ascend
- **[beb54c2a](https://github.com/vllm-project/vllm-ascend/commit/beb54c2ab96d628baef7eef09163156ec364c887)** 支持 V1 PP + MTP 混合部署，并修复 PP token handoff 的精度问题。核心变更：1) 将 PP 的 sampled token 传递从 GPU broadcast 改为通过 scheduler IPC (`CachedRequestData.new_token_ids`)；2) 非 last PP rank 从 IPC 重建本地 `prev_sampled_token_ids` 状态；3) PP+MTP 的 draft/spec token 通过 `ModelRunnerOutput.spec_token_ids` 回写到 scheduler；4) 添加 request 级别的 in-flight fence 防止 decode 请求被重复调度。这是一个大规模的功能变更，涉及 scheduler、model runner、patch 等多个模块，风险较高。
  - 标签: `feature`, `high-risk`, `scheduler`, `model-runner`, `patch`, `pp_mtp`
  - 变更文件:
  - 修改 `tests/ut/patch/platform/test_patch_pp_mtp.py` (+266/-0)
  - 修改 `tests/ut/test_platform.py` (+0/-42)
  - 修改 `vllm_ascend/patch/__init__.py` (+70/-1)
  - 修改 `vllm_ascend/patch/platform/patch_pp_mtp.py` (+263/-0)
  - 修改 `vllm_ascend/platform.py` (+0/-29)
  - 修改 `vllm_ascend/worker/model_runner_v1.py` (+126/-25)
  - Ascend 影响: ✓ 无影响

- **[ef74bd88](https://github.com/vllm-project/vllm-ascend/commit/ef74bd886cbf7efa77e71c01f17707224a8a8a59)** 修复 CI：跳过 MRV2 DFlash 端到端测试。由于 vLLM 新提交导致 DFlash 测试失败，暂时跳过。同时修复了 `test_w4a16_mxfp4.py` 中 `swiglu_limit` 的默认值问题。
  - 标签: `ci`, `bugfix`, `low-risk`, `test`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+1/-0)
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_uva.py` (+1/-0)
  - 修改 `tests/ut/quantization/methods/test_w4a16_mxfp4.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-06
### vllm
- **[5bce653e](https://github.com/vllm-project/vllm/commit/5bce653e09ca62c870ea18d01a4180dc48d3bacb)** 该commit对Transformers建模后端进行了重大性能优化，通过引入图融合（fuser）机制，将HF模型中的GLU（gate+up投影）、QKV投影和RMSNorm自动检测并融合为vLLM的原生算子（MergedColumnParallelLinear、QKVParallelLinear、RMSNorm/GemmaRMSNorm），使Transformers后端的性能与原生vLLM模型实现一致。核心实现包括：1) 新增`fuser.py`和`fusers/`子模块，包含`GLUFuser`、`QKVFuser`、`RMSNormFuser`等具体融合器；2) 新增`fx_utils.py`提供FX图追踪和AST源码重写引擎；3) 修改`base.py`中的`recursive_replace`方法，使用融合器替换子模块；4) MoE模块也支持通过`MoEBlockFuser`进行融合；5) 移除了旧的`replace_rms_norm_class`函数。该变更大幅提升了Transformers后端的推理速度，同时保持了与原生vLLM相同的精度。
  - 标签: `feature`, `performance`, `model-runner`, `transformers`, `high-risk`
  - 变更文件（共 23 个）:
  - 修改 `.buildkite/test-amd.yaml` (+4/-4)
  - 修改 `.buildkite/test_areas/models_basic.yaml` (+4/-3)
  - 修改 `.buildkite/test_areas/models_distributed.yaml` (+1/-1)
  - 修改 `.github/CODEOWNERS` (+1/-1)
  - 修改 `docs/models/supported_models.md` (+4/-2)
  - 新增 `tests/models/transformers/__init__.py` (+0/-0)
  - 新增 `tests/models/transformers/fusers/__init__.py` (+0/-0)
  - 新增 `tests/models/transformers/fusers/test_linear.py` (+480/-0)
  - 新增 `tests/models/transformers/fusers/test_moe.py` (+299/-0)
  - 新增 `tests/models/transformers/fusers/test_rms_norm.py` (+227/-0)
  - ... 及其他 13 个文件
  - Ascend 影响: ✓ 无影响

- **[07f9baf7](https://github.com/vllm-project/vllm/commit/07f9baf7564b42ba7218ce9167bfcc4128028473)** 该commit回退了之前将`torch.cuda.Event`替换为`torch.Event`的变更（PR #47140）。原因是`torch.Event`在某些平台上（如XPU）可能不兼容，导致`RuntimeError: dummy base class`。回退后，所有使用`torch.Event`的地方恢复为`torch.cuda.Event`，同时在XPU平台上通过`torch.cuda.Event = torch.xpu.Event`进行适配。涉及多个模块，包括benchmarks、分布式通信、KV transfer、LoRA、MoE、DeepSeek V4 attention等。
  - 标签: `bugfix`, `refactor`, `distributed`, `attention`, `lora`, `high-risk`
  - 变更文件（共 31 个）:
  - 修改 `benchmarks/benchmark_topk_topp.py` (+4/-2)
  - 修改 `benchmarks/kernels/benchmark_moe_defaults.py` (+2/-2)
  - 修改 `benchmarks/kernels/benchmark_selective_state_update.py` (+2/-2)
  - 修改 `tests/v1/kv_connector/unit/test_hf3fs_connector.py` (+1/-1)
  - 修改 `tools/pre_commit/check_torch_cuda.py` (+1/-9)
  - 修改 `vllm/distributed/eplb/eplb_state.py` (+2/-2)
  - 修改 `vllm/distributed/eplb/eplb_utils.py` (+2/-2)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/example_hidden_states_connector.py` (+4/-4)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/hf3fs_client.py` (+1/-1)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/hf3fs_connector.py` (+3/-3)
  - ... 及其他 21 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 影响。`torch.cuda.Event`的回退影响多个模块。vllm-ascend的`NPUWorker`、`NPUModelRunner`、`AscendAttentionBackend`等组件中如果使用了`torch.Event`（来自PR #47140的变更），需要确认是否已回退为`torch.cuda.Event`。vllm-ascend的`NPUPlatform`中可能已有对`torch.cuda.Event`的适配（如重定向到`torch.npu.Event`），需确保兼容。

- **[f2aaf591](https://github.com/vllm-project/vllm/commit/f2aaf5915102cd56b3a60f8e6e59c4a7f31268dd)** 该commit为Bailing混合模型添加了MTP（Multi-Token Prediction）推测解码支持。主要变更包括：1) 新增`bailing_moe_mtp.py`模型实现，包含`BailingMoeV25MTPModel`、`BailingMoeV25MultiTokenPredictor`和`BailingMoeV25MultiTokenPredictorLayer`；2) 在`linear_attn.py`中添加`BailingLinearAttentionBackend`和`BailingLinearAttentionMetadataBuilder`，支持MTP下的spec decode metadata构建；3) 在`bailing_linear_attn.py`中添加`bailing_linear_attention_decode_spec` Triton kernel，支持多步draft token的线性注意力解码；4) 在`speculative.py`中添加Bailing模型的hf_config_override；5) 在`model_arch_config_convertor.py`中添加`BailingHybridMTPModelArchConfigConvertor`。
  - 标签: `feature`, `spec-decode`, `bailing`, `attention`, `high-risk`
  - 变更文件（共 11 个）:
  - 新增 `tests/config/test_bailing_mtp_config.py` (+52/-0)
  - 修改 `tests/models/registry.py` (+6/-0)
  - 新增 `tests/v1/attention/test_linear_attention_metadata_builder.py` (+188/-0)
  - 修改 `vllm/config/speculative.py` (+16/-0)
  - 修改 `vllm/model_executor/layers/mamba/linear/bailing_linear_attn.py` (+322/-3)
  - 修改 `vllm/model_executor/models/bailing_moe_linear.py` (+4/-0)
  - 新增 `vllm/model_executor/models/bailing_moe_mtp.py` (+380/-0)
  - 修改 `vllm/model_executor/models/registry.py` (+1/-0)
  - 修改 `vllm/transformers_utils/model_arch_config_convertor.py` (+7/-0)
  - 修改 `vllm/v1/attention/backends/linear_attn.py` (+212/-1)
  - ... 及其他 1 个文件
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[fef5feb6](https://github.com/vllm-project/vllm-ascend/commit/fef5feb6a56864f528463c4c4a0064e75c2f7a35)** 修复了MambaSpec投机解码场景下的block table溢出问题。在`may_reinitialize_input_batch()`中，当计算`max_num_blocks_per_req`时，`num_speculative_blocks`被错误地包含在`mamba_blocks_per_req`的`max()`比较中，导致在长上下文且禁用prefix caching时，投机解码所需的额外block被忽略。修复后将`num_speculative_blocks`移到`max()`调用之后，确保它总是被添加到content block计数之上。
  - 标签: `bugfix`, `medium-risk`, `scheduler`, `model-runner`
  - 变更文件:
  - 修改 `vllm_ascend/worker/model_runner_v1.py` (+2/-1)
  - Ascend 影响: ✓ 无影响

- **[3e46e203](https://github.com/vllm-project/vllm-ascend/commit/3e46e203f02516630de87d6400e02a6be0bf9aea)** 该 commit 在 Model Runner V2 中引入了对 DFlash 投机解码的支持。变更的核心是新增了 `vllm_ascend/worker/v2/spec_decode/dflash/` 子模块，其中 `AscendDFlashSpeculator` 继承自 vLLM 上游的 `DFlashSpeculator`，并通过 `build_attn_metadata_wrapper` 上下文管理器重写了 `propose` 方法，以适配 Ascend NPU 的 attention metadata 构建逻辑。同时，新增了一个 Triton kernel `_prepare_dflash_inputs_kernel_ascend`，该 kernel 是上游 GPU 版本的 Ascend 适配，用于在 NPU 上高效地准备 DFlash 的输入数据（如 slot mapping、positions 等）。此外，将 `init_speculator` 函数从 eagle 子模块提升到 `spec_decode/__init__.py`，使其能根据 `speculative_config` 分发到 Eagle 或 DFlash 的 speculator，这是一个合理的重构。`build_attn_metadata_wrapper` 也被从 eagle 模块重构到 `attn_utils.py` 中，实现了代码复用。另外，修复了 `rotary_embedding.py` 中一个潜在的 bug：在无 forward context 时（如 DFlash 的 draft model 场景），直接访问 `_EXTRA_CTX` 会导致错误，通过 `is_forward_context_available()` 检查来避免。测试方面，为 MRV2 的 DFlash 和 UVA 测试用例增加了 metrics 验证，并新增了 DFlash 的端到端测试。潜在风险：1) `_prepare_dflash_inputs_kernel_ascend` 是一个新的 Triton kernel，其正确性依赖于 Triton-Ascend 的兼容性，可能存在未发现的边界情况；2) `build_attn_metadata_wrapper` 的 monkey-patch 方式虽然实现了功能，但可能与其他上下文管理器或并发场景产生冲突；3) 该 commit 明确标注 "Future Work: Support FULL Graph"，说明当前 DFlash 在 MRV2 下不支持 FULL Graph 模式，这是一个已知限制。
  - 标签: `feature`, `medium-risk`, `spec_decode`, `model-runner`, `triton`, `refactor`, `bugfix`
  - 变更文件（共 11 个）:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+56/-0)
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_uva.py` (+56/-0)
  - 修改 `tests/ut/ops/test_rotary_embedding.py` (+2/-1)
  - 修改 `vllm_ascend/ops/rotary_embedding.py` (+3/-2)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+16/-0)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+1/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/__init__.py` (+42/-0)
  - 新增 `vllm_ascend/worker/v2/spec_decode/dflash/__init__.py` (+0/-0)
  - 新增 `vllm_ascend/worker/v2/spec_decode/dflash/speculator.py` (+191/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/eagle/__init__.py` (+0/-18)
  - ... 及其他 1 个文件
  - Ascend 影响: ✓ 无影响

- **[cd76505e](https://github.com/vllm-project/vllm-ascend/commit/cd76505e8afa6dc428947b81f734b1525ffc6b2e)** 这是一个大型的main2main同步提交，将vLLM上游的多个PR适配到vllm-ascend。主要变更包括：1) 权重传输引擎适配新的`WeightTransferEngine`接口；2) 添加`torch.accelerator.get_memory_info()`的补丁；3) 包装DFlashQwen3ForCausalLM的`_read_mask_embedding()`以忽略可选mask embedding下载失败；4) 更新`AscendInputBatch`构造以匹配上游接口；5) 为`DeepseekV2MLAAttention`添加`reduce_results`参数；6) 为`NPUCommunicator`注册no-op的`all2all_manager`；7) 移除routed expert参数别名逻辑；8) 移除DeepSeek-V2模型级all-gather路径；9) 移除MoE权重转置后的`.contiguous()`调用以减少峰值内存。
  - 标签: `refactor`, `high-risk`, `distributed`, `model-runner`, `ops`, `patch`
  - 变更文件（共 13 个）:
  - 修改 `.github/vllm-main-verified.commit` (+1/-1)
  - 修改 `tests/ut/distributed/weight_transfer/test_npu_ipc_engine.py` (+19/-7)
  - 修改 `vllm_ascend/_310p/fused_moe/fused_moe.py` (+16/-8)
  - 修改 `vllm_ascend/distributed/device_communicators/npu_communicator.py` (+18/-0)
  - 修改 `vllm_ascend/distributed/weight_transfer/hccl_engine.py` (+39/-15)
  - 修改 `vllm_ascend/distributed/weight_transfer/npu_ipc_engine.py` (+32/-7)
  - 修改 `vllm_ascend/ops/fused_moe/fused_moe.py` (+11/-30)
  - 修改 `vllm_ascend/patch/platform/patch_torch_accelerator.py` (+10/-0)
  - 修改 `vllm_ascend/patch/worker/patch_deepseek_v2.py` (+79/-0)
  - 修改 `vllm_ascend/patch/worker/patch_qwen3_dflash.py` (+17/-1)
  - ... 及其他 3 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-07-05
### vllm
- **[cc1d020d](https://github.com/vllm-project/vllm/commit/cc1d020d01949d11b7ef70dabb0eb196b3f39f53)** 该commit为MRV2（多模态推理V2）启用mm prefix双向注意力支持。核心变更包括：1) 在`vllm/v1/worker/gpu/attn_utils.py`中新增`compute_mm_prefix_ranges`函数，用于计算多模态token的PrefixLM双向注意力范围，并支持滑动窗口过滤；2) 修改`build_attn_metadata`函数，新增`mm_req_doc_ranges`参数，将多模态前缀范围传递给注意力元数据构建器；3) 在`vllm/v1/worker/gpu/model_states/default.py`的`prepare_attn`方法中，当模型支持多模态输入且为mm_prefix_lm时，调用`compute_mm_prefix_ranges`计算范围并传递给`build_attn_metadata`；4) 将`vllm/config/model.py`中的`is_mm_prefix_lm`属性从`@property`改为`@cached_property`，避免重复计算；5) 新增测试文件`tests/models/multimodal/generation/test_mm_prefix_lm.py`，验证Gemma3的prefix-LM mask正确性。实现方式是通过在注意力元数据构建时传入多模态token的文档范围，使注意力后端能够为这些token应用双向注意力mask。潜在风险：新增的`mm_req_doc_ranges`参数需要所有注意力后端的元数据构建器支持，否则可能导致兼容性问题。
  - 标签: `feature`, `medium-risk`, `attention`, `model-runner`, `multimodal`
  - 变更文件:
  - 修改 `.buildkite/test_areas/models_multimodal.yaml` (+2/-1)
  - 新增 `tests/models/multimodal/generation/test_mm_prefix_lm.py` (+119/-0)
  - 修改 `vllm/config/model.py` (+1/-1)
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+27/-0)
  - 修改 `vllm/v1/worker/gpu/model_states/default.py` (+16/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) `vllm/v1/worker/gpu/attn_utils.py`中`build_attn_metadata`函数新增`mm_req_doc_ranges`参数，AscendAttentionBackend的元数据构建器（`AscendAttentionMetadataBuilder`）需要支持该参数以正确处理多模态前缀双向注意力。2) `vllm/v1/worker/gpu/attn_utils.py`中新增`compute_mm_prefix_ranges`函数，NPUModelRunner在`prepare_attn`方法中需要调用此函数计算多模态前缀范围。3) `vllm/v1/worker/gpu/model_states/default.py`中`prepare_attn`方法新增对`compute_mm_prefix_ranges`的调用逻辑，NPUModelRunner需要同步更新其注意力准备逻辑。4) `vllm/config/model.py`中`is_mm_prefix_lm`从`@property`改为`@cached_property`，NPUPlatform或相关配置补丁需要确保缓存行为一致。
    - 建议测试区域: `tests/models/multimodal/generation/test_mm_prefix_lm.py`

- **[b6cc46ec](https://github.com/vllm-project/vllm/commit/b6cc46ec3b903c71405f4355c1e9ecb47ae54bb2)** 该commit支持无需数据并行（DP）的序列并行，实现1.9%~5.0%的端到端吞吐量提升。核心变更包括：1) 在`vllm/config/parallel.py`中移除`use_sequence_parallel_moe`对`data_parallel_size > 1`的依赖，使序列并行可以在无DP时独立启用；2) 在`vllm/distributed/device_communicators/base_device_communicator.py`中，all2all管理器的初始化条件扩展为包含`use_sequence_parallel_moe`，确保序列并行EP时也初始化all2all通信；3) 在`vllm/forward_context.py`中，DPMetadata的创建逻辑扩展为支持序列并行场景，当无DP时直接使用本地token数量；4) 在`vllm/model_executor/layers/fused_moe/config.py`和`runner/moe_runner.py`中，all2all kernel和naive dispatch/combine的条件扩展为包含序列并行；5) 在`vllm/model_executor/models/deepseek_v2.py`中优化了序列并行的padding逻辑，使用更简洁的`(-hidden_states.shape[0]) % tp_world_size`计算padding大小；6) 在`vllm/model_executor/models/gpt_oss.py`中，当使用LoRA时禁用序列并行。这是一个性能优化变更，涉及分布式通信、MoE层和模型执行等多个模块。潜在风险：序列并行与LoRA的兼容性需要额外关注。
  - 标签: `performance`, `medium-risk`, `distributed`, `moe`, `model-runner`
  - 变更文件:
  - 修改 `vllm/config/parallel.py` (+2/-3)
  - 修改 `vllm/distributed/device_communicators/base_device_communicator.py` (+5/-4)
  - 修改 `vllm/forward_context.py` (+15/-3)
  - 修改 `vllm/model_executor/layers/fused_moe/config.py` (+1/-1)
  - 修改 `vllm/model_executor/layers/fused_moe/runner/moe_runner.py` (+2/-2)
  - 修改 `vllm/model_executor/models/deepseek_v2.py` (+4/-8)
  - 修改 `vllm/model_executor/models/gpt_oss.py` (+4/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) `vllm/distributed/device_communicators/base_device_communicator.py`中all2all管理器初始化条件变更，NPUCommunicator的`__init__`方法需要同步更新，确保在`use_sequence_parallel_moe`为True时也初始化all2all通信。2) `vllm/forward_context.py`中DPMetadata创建逻辑变更，Ascend的分布式上下文设置（如`set_forward_context`的patch）需要支持无DP时的序列并行场景。3) `vllm/config/parallel.py`中`use_sequence_parallel_moe`属性变更，NPUPlatform或相关配置补丁需要确保序列并行可以在无DP时独立启用。4) `vllm/model_executor/layers/fused_moe/config.py`和`runner/moe_runner.py`中all2all和dispatch/combine条件变更，Ascend的MoE实现需要同步更新这些条件判断。
    - 建议测试区域: `tests/distributed/test_sequence_parallel.py`, `tests/models/test_moe.py`

- **[fa4321de](https://github.com/vllm-project/vllm/commit/fa4321de3d894c50c5ca0766dffa352d3fb07423)** 该commit修复TurboQuant注意力后端中KV cache dtype丢失的问题。变更内容：在`vllm/v1/worker/gpu/attn_utils.py`的`_reshape_kv_cache`和`_update_hybrid_attention_layout`函数中，当KV cache spec是`TQFullAttentionSpec`类型时，即使`kv_quant_mode`为`NONE`，也强制使用`cache_dtype`而非`"auto"`。这是因为TurboQuant后端需要明确的dtype信息来正确计算KV cache形状。这是一个低风险的bug修复，仅影响TurboQuant注意力后端。
  - 标签: `bugfix`, `low-risk`, `attention`, `quantization`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+6/-1)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[9154baad](https://github.com/vllm-project/vllm-ascend/commit/9154baadc9dbac857fe197d03bccb1731664f3df)** 此 commit 修复了 310P 设备上 Qwen3.5 模型使用 MTP 和 FULL ACLGraph 时的精度问题。根本原因是连续批处理导致运行时请求数小于 graph 捕获的固定 shape，而 310P 的 GDN 投机解码路径未能正确填充虚拟请求的元数据（如 spec_query_start_loc、state indices、num_accepted_tokens 和 conv1d 重放缓冲区），导致隐藏状态/ logits 被污染。修复方案包括：1) 在 `gdn_310.py` 中新增 `_zero_padded_tokens`、`_mask_padded_recurrent_accepted_tokens` 和 `_pad_spec_conv1d_host_args_shape_consistent_dummy_310p` 函数，用于填充和屏蔽虚拟请求；2) 在 `gdn_attn_builder_310.py` 中新增 `_pad_spec_decode_metadata` 和 `_pad_decode_metadata` 方法，在 graph 重放前将元数据填充到固定大小的 buffer 中；3) 在 `model_runner_310p.py` 中修改 `_model_forward` 方法，确保 MTP full-graph 重放前更新和同步 graph 参数；4) 在 `patch_idex_310.py` 中将 Qwen GDN 的 attention 后端替换为 310P 专用后端。潜在风险：此修复仅针对 310P 设备，不影响主线和其它设备。但新增的填充逻辑可能增加内存开销和延迟，需要性能测试验证。
  - 标签: `bugfix`, `high-risk`, `model-runner`, `attention`, `spec_decode`, `compilation`
  - 变更文件:
  - 新增 `tests/ut/_310p/ops/test_gdn_310.py` (+107/-0)
  - 修改 `tests/ut/_310p/test_model_runner_310p.py` (+40/-0)
  - 修改 `vllm_ascend/_310p/model_runner_310p.py` (+46/-8)
  - 修改 `vllm_ascend/_310p/ops/fla/gdn_310.py` (+111/-11)
  - 修改 `vllm_ascend/_310p/ops/gdn_attn_builder_310.py` (+159/-3)
  - 修改 `vllm_ascend/patch/worker/patch_idex_310.py` (+4/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-04
### vllm
- **[07516fda](https://github.com/vllm-project/vllm/commit/07516fda67d2133e26c0fd7386c0b0c8641e2a6e)** 该 commit 使 Dynamic Speculative Decoding (DSD) 兼容 Full CUDA Graphs（MRv2）。主要变更：1) 在 CudaGraphManager._init_candidates 中，当使用 DSD 时，会为每个可能的 decode query length（来自 num_speculative_tokens_per_batch_size 调度表）捕获 FULL decode graph；2) 在 CompilationConfig.resolve_cudagraph_mode_and_sizes 中新增 use_v2_model_runner 参数，MRv2 不再调整 cudagraph capture sizes；3) 移除了 VllmConfig 中 DSD 对 MRv2 的限制；4) 更新了文档，说明 Full Cudagraph 仅支持 MRv2；5) 新增了全面的测试用例。潜在风险：变更涉及 CUDA Graph 捕获逻辑的核心部分，但测试覆盖了各种边界情况。
  - 标签: `feature`, `high-risk`, `spec-decode`, `cuda-graph`, `model-runner`
  - 变更文件:
  - 修改 `docs/features/speculative_decoding/dynamic_speculative_decoding.md` (+2/-5)
  - 修改 `tests/test_config.py` (+31/-0)
  - 新增 `tests/v1/spec_decode/test_dynamic_sd_cug.py` (+328/-0)
  - 修改 `vllm/config/compilation.py` (+6/-2)
  - 修改 `vllm/config/vllm.py` (+3/-4)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+58/-19)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+4/-3)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+4/-3)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 影响 vllm-ascend 的编译和模型运行模块。1) CompilationConfig.resolve_cudagraph_mode_and_sizes 新增了 use_v2_model_runner 参数，NPUModelRunner 在调用此方法时需要传递此参数（已在 MRv2 路径中传递 True）。2) CudaGraphManager._init_candidates 中 Dynamic SD 的 FULL graph 捕获逻辑发生变更，vllm-ascend 的 ACLGraphWrapper 需要同步更新其候选图生成逻辑以支持 DSD 的多个 decode query length。3) VllmConfig._maybe_override_dynamic_sd_cudagraph_mode 中新增了 use_v2_model_runner 检查，NPUPlatform 需要确认其编译配置是否受影响。
    - 建议测试区域: `vllm_ascend/compilation/acl_graph.py`, `vllm_ascend/worker/model_runner_v1.py`

- **[67ff0ae3](https://github.com/vllm-project/vllm/commit/67ff0ae30fe6b1ab1a912e10977d99ddb169c4b2)** 该 commit 支持了 nvfp4 KV cache 与 kv-cache-dtype-skip-layers 和 sliding_window 的组合使用。主要变更：1) 在 CacheConfig 中新增 skip_page_size_padded 字段；2) 在 AttentionLayer.get_kv_cache_spec 中，为 sliding window 层选择最大的 kernel block size 以适配 padded page；3) 在 Platform 基类中新增 _align_heterogeneous_kv_block_size 方法，用于对齐不同 KV dtype 的 block size；4) 在 GPUModelRunner 的 KV cache reshape 逻辑中，为 skip layers 使用 'auto' cache dtype；5) 更新了文档。潜在风险：变更涉及 KV cache 分配的核心逻辑，但通过 _align_heterogeneous_kv_block_size 方法进行了统一处理。
  - 标签: `feature`, `medium-risk`, `kv-cache`, `quantization`, `attention`
  - 变更文件:
  - 修改 `docs/features/quantization/quantized_kvcache.md` (+26/-0)
  - 修改 `vllm/config/cache.py` (+6/-0)
  - 修改 `vllm/model_executor/layers/attention/attention.py` (+51/-1)
  - 修改 `vllm/platforms/interface.py` (+117/-0)
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+18/-2)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+9/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 影响 vllm-ascend 的多个模块。1) Platform 基类新增了 _align_heterogeneous_kv_block_size 方法，NPUPlatform 需要检查是否需要覆盖此方法以支持 Ascend NPU 上的异构 KV cache block size 对齐。2) AttentionLayer.get_kv_cache_spec 中 sliding window 的 block_size 选择逻辑变更，AscendAttentionBackend 需要确认其 get_supported_kernel_block_sizes 返回的值是否兼容新的选择逻辑。3) GPUModelRunner._reshape_kv_cache_tensors 中新增了 per-layer cache_dtype 逻辑，NPUModelRunner 需要同步更新其 KV cache reshape 逻辑。4) attn_utils.py 中的 _reshape_kv_cache 和 _update_hybrid_attention_layout 也新增了 per-layer cache_dtype 逻辑，vllm-ascend 的 attention 相关 patch 需要检查。
    - 建议测试区域: `vllm_ascend/platform.py`, `vllm_ascend/worker/model_runner_v1.py`, `vllm_ascend/attention/attention_v1.py`

### vllm-ascend
- **[8c28b0eb](https://github.com/vllm-project/vllm-ascend/commit/8c28b0eb1383c12635c78f2f00bcf0cd6f7a5417)** 此提交将 vLLM 主分支的验证提交从 `a30addc` 升级到 `b9a7cd4`，并适配了上游 API 变更。这是一个大规模的兼容性更新，涉及多个模块：1) 在 `__init__.py` 中为 v2 model runner 设置环境变量。2) 更新了调度器补丁以适配上游 `throttle_prefills` 参数。3) 更新了 Ngram 和 Suffix 投机解码 proposer 以适配上游 Dynamic SD 的签名变更。4) 更新了 encoder ACL Graph 以适配上游图集（graph set）存储。5) 更新了 fused_moe 以适配上游 `get_current_vllm_config`。6) 更新了 v2 model runner 的 ACL Graph 管理器以适配 LoRA 捕获参数。7) 更新了 Eagle ACL Graph 以适配上游注意力状态重命名。8) 由于上游解析器重构，跳过了 GLM4.7 和 MiniMax M2 的补丁和测试。这是一个高风险变更，因为涉及大量上游 API 适配，需要确保所有适配路径的正确性。
  - 标签: `chore`, `high-risk`, `ci`, `compilation`, `spec_decode`, `scheduler`, `distributed`
  - 变更文件（共 20 个）:
  - 修改 `.github/vllm-main-verified.commit` (+1/-1)
  - 修改 `tests/e2e/pull_request/one_card/test_guided_decoding.py` (+73/-31)
  - 修改 `tests/ut/patch/platform/test_patch_glm47_tool_call_parser.py` (+16/-6)
  - 修改 `tests/ut/patch/platform/test_patch_minimax_m2_tool_call_parser.py` (+13/-4)
  - 修改 `tests/ut/patch/platform/test_patch_minimax_usage_accounting.py` (+11/-4)
  - 修改 `vllm_ascend/core/scheduler_profiling_chunk.py` (+1/-1)
  - 修改 `vllm_ascend/ops/fused_moe/fused_moe.py` (+8/-9)
  - 修改 `vllm_ascend/patch/__init__.py` (+3/-1)
  - 修改 `vllm_ascend/patch/platform/__init__.py` (+6/-3)
  - 修改 `vllm_ascend/patch/platform/patch_balance_schedule.py` (+6/-2)
  - ... 及其他 10 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-07-03
### vllm
- **[3775d5fc](https://github.com/vllm-project/vllm/commit/3775d5fcabf7bc5d4d92768485d860d132c6e1b6)** 为ROCm平台添加新的CI测试分组，包括MRCR评估、vLLM IR测试、KDA kernel测试、Model Runner V2系列测试（core/examples/distributed/PP/spec decode）、GGUF插件测试等。同时修复了Triton kernel在AMD后端上的num_stages兼容性问题（chunk_delta_h kernel在ROCm上不支持num_stages=4）。这是一个纯CI和ROCm平台适配的变更。
  - 标签: `ci`, `test`, `rocm`
  - 变更文件:
  - 修改 `.buildkite/test-amd.yaml` (+186/-1)
  - 修改 `vllm/model_executor/layers/fla/ops/chunk_delta_h.py` (+3/-1)
  - Ascend 影响: ✓ 无影响

- **[979f5511](https://github.com/vllm-project/vllm/commit/979f5511d78b317760d45df9290233c27793a0af)** 修复Gemma4模型中图像双向注意力超出滑动窗口的问题。主要变更：1) 在Attention类中添加mm_prefix_clamp_sliding_window属性；2) Gemma4模型在滑动层上设置此属性为True；3) Gemma4ForConditionalGeneration类设置mm_prefix_clamp_sliding_window=True；4) 在FlashAttention和TritonAttention后端中实现滑动窗口钳制逻辑；5) GPUModelRunner中根据此属性决定是否跳过超出滑动窗口的mm_prefix范围。
  - 标签: `bugfix`, `attention`, `model`
  - 变更文件:
  - 修改 `vllm/model_executor/layers/attention/attention.py` (+4/-0)
  - 修改 `vllm/model_executor/models/gemma4.py` (+7/-0)
  - 修改 `vllm/model_executor/models/gemma4_mm.py` (+7/-0)
  - 修改 `vllm/v1/attention/backends/flash_attn.py` (+32/-4)
  - 修改 `vllm/v1/attention/backends/triton_attn.py` (+3/-0)
  - 修改 `vllm/v1/attention/ops/triton_attention_helpers.py` (+13/-2)
  - 修改 `vllm/v1/attention/ops/triton_unified_attention.py` (+9/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+14/-3)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: Attention类新增mm_prefix_clamp_sliding_window属性，AscendAttentionBackend需要处理此属性。GPUModelRunner中mm_prefix逻辑变更（新增_clamps_in_kernel判断），NPUModelRunner需要同步更新。FlashAttention和TritonAttention后端中的mm_prefix_clamp_sliding_window实现逻辑需要AscendAttentionBackend参考实现。
    - 建议测试区域: `vllm_ascend/tests/models/test_gemma4.py`, `vllm_ascend/tests/attention/test_attention_backend.py`

- **[276b837d](https://github.com/vllm-project/vllm/commit/276b837dc4d6a15ec7a82099dccd4c997eec916b)** 修复ModelRunner V2在shutdown时未释放所有模型引用的问题。在shutdown方法中添加了删除model_state和speculator引用的逻辑，确保模型权重被正确释放。
  - 标签: `bugfix`, `model-runner`, `memory`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+4/-0)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[7e5cfda3](https://github.com/vllm-project/vllm-ascend/commit/7e5cfda32ac08aefca46eb7d2df08384bbae7435)** 此commit修复了一个Bug，即当vLLM上游根据模型架构、Triton可用性等条件自动启用v2模型运行器时，Ascend NPU的v2路径可能不兼容，导致崩溃。修复方式是通过monkey-patch `VllmConfig.use_v2_model_runner`属性，使其仅读取`VLLM_USE_V2_MODEL_RUNNER`环境变量，忽略上游的自动启用逻辑。同时，更新了`worker.py`和`platform.py`中的相关代码，使其通过`vllm_config.use_v2_model_runner`访问此属性，从而受益于补丁逻辑。此变更确保了Ascend平台对v2模型运行器的控制权。
  - 标签: `bugfix`, `medium-risk`, `patch`, `worker`
  - 变更文件:
  - 修改 `vllm_ascend/patch/__init__.py` (+23/-0)
  - 修改 `vllm_ascend/patch/worker/__init__.py` (+6/-0)
  - 新增 `vllm_ascend/patch/worker/patch_v2/patch_use_v2_model_runner.py` (+20/-0)
  - 修改 `vllm_ascend/platform.py` (+1/-1)
  - 修改 `vllm_ascend/worker/worker.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-02
### vllm
- **[a47f38f8](https://github.com/vllm-project/vllm/commit/a47f38f82569c236d7d23b7ad0c8792ac6d62247)** 修复推测解码中block verification kernel的int32偏移溢出问题。当词表较大（如GLM约155k）时，logit_idx * vocab_stride会超过int32范围。变更将Triton kernel中的索引变量（req_state_idx, start_idx, logit_idx）显式转换为int64，避免乘法溢出。同时添加了测试用例验证高索引位置下的正确性。
  - 标签: `bugfix`, `low-risk`, `spec-decode`, `kernel`
  - 变更文件:
  - 新增 `tests/v1/worker/test_gpu_rejection_sampler_i64.py` (+144/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py` (+4/-4)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py中的Triton kernel。vllm-ascend的推测解码补丁（vllm_ascend.patch.worker.spec_decode_patch）如果覆盖了此文件，需要同步更新kernel中的int64转换逻辑。

- **[3e158ae6](https://github.com/vllm-project/vllm/commit/3e158ae62d1c227004fa9f702a51126e58ebbcb2)** 修复Mamba2模型在非推测解码模式下崩溃的问题。在prepare_attn方法中，num_accepted_tokens的创建逻辑仅在推测解码启用时（num_speculative_tokens > 0）才执行，避免了非推测解码场景下访问未初始化变量的错误。
  - 标签: `bugfix`, `low-risk`, `model-runner`, `mamba`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+1/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了vllm/v1/worker/gpu/model_states/mamba_hybrid.py。vllm-ascend的NPUModelRunner如果使用了MambaHybridModelState或相关逻辑，需确保此修复已同步。

- **[a2f71300](https://github.com/vllm-project/vllm/commit/a2f713002df9fd08c0fe13272c76547421721f2d)** 默认启用V2 Model Runner（对所有dense模型）。变更修改了DEFAULT_V2_MODEL_RUNNER_ARCHITECTURES，移除了显式列出的架构（如LlamaForCausalLM），改为通过_is_default_v2_model_runner_model属性判断：非MoE、非hybrid、非attention-free的generate类型模型默认启用V2。同时更新了相关测试用例，处理V2下async scheduling的max_concurrent_batches计算差异，以及V2下resumed request作为NewRequestData而非cached request的调度行为变化。
  - 标签: `feature`, `medium-risk`, `model-runner`, `config`
  - 变更文件:
  - 修改 `.buildkite/test_areas/model_runner_v2.yaml` (+1/-3)
  - 修改 `tests/distributed/test_multiproc_executor.py` (+8/-3)
  - 修改 `tests/distributed/test_ray_v2_executor.py` (+7/-1)
  - 修改 `tests/test_config.py` (+23/-1)
  - 修改 `tests/v1/kv_connector/unit/test_remote_prefill_lifecycle.py` (+8/-4)
  - 修改 `vllm/config/vllm.py` (+8/-5)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: V2 Model Runner默认启用影响所有模型执行路径。vllm-ascend的NPUModelRunner继承自GPUModelRunner，需确保：1) V2下的输入准备、模型执行、采样流程兼容；2) async scheduling的max_concurrent_batches计算逻辑（V2下+1）已适配；3) scheduler中resumed request的处理方式（NewRequestData vs cached request）已同步。vllm-ascend的补丁（vllm_ascend.patch.worker.engine_core_patch, scheduler_patch等）需检查是否覆盖了这些变更。
    - 建议测试区域: `vllm_ascend/tests/test_model_runner.py`, `vllm_ascend/tests/test_scheduler.py`

- **[2b753ad2](https://github.com/vllm-project/vllm/commit/2b753ad200d52a2dc16e61ff3c92a45711e2750c)** 为DSpark推测器添加checkpoint支持。支持speculators格式的checkpoint，其中draft_vocab_size可以小于target vocab_size，并包含d2t/t2d remap表。修改了DSparkMarkovHead的markov_w2输出维度为draft_vocab_size，添加了compute_draft_logits和map_draft_to_target方法，以及d2t scatter逻辑用于probabilistic rejection sampling。同时添加了update_dspark配置转换函数。
  - 标签: `feature`, `medium-risk`, `spec-decode`, `model`
  - 变更文件:
  - 修改 `vllm/model_executor/models/qwen3_dspark.py` (+37/-5)
  - 修改 `vllm/models/deepseek_v4/nvidia/dspark.py` (+11/-0)
  - 修改 `vllm/transformers_utils/configs/speculators/algos.py` (+44/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dspark/speculator.py` (+48/-11)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 修改了vllm/v1/worker/gpu/spec_decode/dspark/speculator.py和多个模型文件。vllm-ascend的推测解码补丁（vllm_ascend.patch.worker.spec_decode_patch）需同步更新DSparkSpeculator的实现，特别是：1) load_draft_model中的d2t scatter逻辑；2) _sample_sequential中的compute_draft_logits和map_draft_to_target调用；3) dspark_bonus_anchor配置处理。

---

## 2026-07-01
### vllm
- **[f5a8d733](https://github.com/vllm-project/vllm/commit/f5a8d73377d0f0a4e00cba172f9fbd0d50471b07)** 新增 DSpark 推测解码支持，这是一种半自回归并行草稿生成方法。DSpark 在单个并行前向中生成整个 token 块（类似 DFlash），然后通过轻量级顺序 Markov 头注入块内依赖。变更涉及多个模块：1) 配置层新增 'dspark' 方法类型和 use_dspark() 方法；2) 新增 Qwen3DSparkModel 和 DSparkDeepseekV4ForCausalLM 模型实现；3) Scheduler 中 num_lookahead_tokens 计算逻辑调整；4) GPUModelRunner 中 speculative_config.method 检查新增 'dspark'；5) 新增 DSparkSpeculator 类，继承自 DFlashSpeculator；6) 稀疏 SWA 注意力构建器支持非因果索引；7) 模型注册表新增 DSparkDraftModel 和 Qwen3DSparkModel 条目。这是一个高风险的大规模 feature 变更，涉及推测解码核心流程。
  - 标签: `feature`, `high-risk`, `spec_decode`, `scheduler`, `attention`, `model-runner`
  - 变更文件（共 24 个）:
  - 修改 `tests/models/registry.py` (+13/-0)
  - 修改 `tests/models/test_registry.py` (+4/-0)
  - 新增 `tests/v1/attention/test_dspark_noncausal_sparse_mla.py` (+529/-0)
  - 修改 `tests/v1/e2e/spec_decode/test_spec_decode.py` (+61/-0)
  - 修改 `vllm/benchmarks/datasets/datasets.py` (+1/-0)
  - 修改 `vllm/config/speculative.py` (+36/-3)
  - 修改 `vllm/config/vllm.py` (+24/-5)
  - 修改 `vllm/model_executor/models/qwen3_dflash.py` (+9/-3)
  - 新增 `vllm/model_executor/models/qwen3_dspark.py` (+153/-0)
  - 修改 `vllm/model_executor/models/registry.py` (+2/-0)
  - ... 及其他 14 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) Scheduler 中 num_lookahead_tokens 计算逻辑新增 DSpark 分支（self.num_lookahead_tokens = self.num_spec_tokens），vllm-ascend 的 scheduler_patch 需要同步更新。2) GPUModelRunner 中 speculative_config.method 检查新增 'dspark'，vllm-ascend 的 block_table_patch 需要更新。3) SpeculativeConfig 新增 use_dspark() 方法，vllm-ascend 的 spec_decode_patch 需要评估。4) SparseSWAMetadataBuilder 新增非因果索引构建逻辑和 is_dspark 标志，vllm-ascend 的 attention_backend_patch 需要评估。5) DFlashSpeculator 的 _prepare_dflash_inputs_kernel 新增 SAMPLE_FROM_ANCHOR 参数和 max_model_len 参数，vllm-ascend 的 spec_decode_patch 需要同步更新。
    - 建议测试区域: `vllm_ascend/patch/platform/scheduler_patch`, `vllm_ascend/patch/worker/block_table_patch`, `vllm_ascend/patch/worker/spec_decode_patch`, `vllm_ascend/patch/worker/attention_backend_patch`

- **[e7d0fcbc](https://github.com/vllm-project/vllm/commit/e7d0fcbc0954382f10fb4c9cee1df6f3a16113e8)** 修复 main 分支上的多个 CI 失败问题。包括：1) 权重传输测试中移除平台条件判断，始终设置 Ray 环境变量；2) Mamba prefix cache 测试中添加 load_format='dummy'；3) 修复 fused_moe 中 weight_loader 调用错误；4) DeepSeek-V2 模型中添加 residual 连续性保证；5) Gemma3 多模态编码器 CUDA Graph 捕获接口添加 path 参数。这是一个中等风险的 bugfix 集合。
  - 标签: `bugfix`, `medium-risk`, `ci`, `distributed`, `model-runner`
  - 变更文件:
  - 修改 `tests/distributed/test_weight_transfer.py` (+8/-13)
  - 修改 `tests/v1/e2e/general/test_mamba_prefix_cache.py` (+2/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/routed_experts.py` (+1/-1)
  - 修改 `vllm/model_executor/models/deepseek_v2.py` (+4/-0)
  - 修改 `vllm/model_executor/models/gemma3_mm.py` (+3/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) DeepSeek-V2 模型中新增 residual.contiguous() 调用，vllm-ascend 的 model_registry_patch 需要评估是否需要在 Ascend 实现中做同样处理。2) fused_moe 中 weight_loader 调用修复（self.weight_loader -> param.weight_loader），vllm-ascend 的 MoE 相关补丁需要评估。

- **[77a9c5ae](https://github.com/vllm-project/vllm/commit/77a9c5ae28a3d054e6caf60c7e14082453b3ae47)** 权重同步系统重构。主要变更包括：1) 将稀疏 NCCL 引擎从密集 NCCL 引擎中分离为独立的 SparseNCCLWeightTransferEngine；2) 简化 WeightTransferEngine 基类，移除 receive_sparse_weights 和 trainer_send_sparse_weights 方法，将 layerwise reload 生命周期移到 start_weight_update/finish_weight_update 中；3) Worker 端的权重更新流程简化，移除稀疏补丁应用逻辑；4) 新增 nccl_common.py 共享 NCCL 初始化逻辑；5) 更新所有示例和文档。这是一个高风险的大规模 refactor。
  - 标签: `refactor`, `high-risk`, `distributed`, `weight-transfer`
  - 变更文件（共 32 个）:
  - 修改 `docs/training/layerwise.md` (+1/-1)
  - 修改 `docs/training/weight_transfer/README.md` (+3/-2)
  - 修改 `docs/training/weight_transfer/base.md` (+28/-15)
  - 修改 `docs/training/weight_transfer/ipc.md` (+2/-2)
  - 修改 `docs/training/weight_transfer/nccl.md` (+14/-11)
  - 修改 `examples/rl/rlhf_async_new_apis.py` (+1/-1)
  - 修改 `examples/rl/rlhf_http_ipc.py` (+3/-7)
  - 修改 `examples/rl/rlhf_http_nccl.py` (+3/-7)
  - 修改 `examples/rl/rlhf_ipc.py` (+1/-1)
  - 修改 `examples/rl/rlhf_ipc_fsdp_ep.py` (+3/-10)
  - ... 及其他 22 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) WeightTransferEngine 基类构造函数签名变更：parallel_config 参数替换为 vllm_config + device，vllm-ascend 的 executor_patch 和 worker_base_patch 需要同步更新。2) WeightTransferEngine 新增 start_weight_update/finish_weight_update 抽象方法，vllm-ascend 的 worker_base_patch 需要实现这些方法。3) GPUModelRunner 中移除了 apply_sparse_weight_patches 方法，vllm-ascend 的 block_table_patch 需要移除相关引用。4) GPUWorker 中 update_weights/finish_weight_update 逻辑简化，vllm-ascend 的 worker_base_patch 需要同步更新。5) WeightTransferEngineFactory.create_engine 签名变更，vllm-ascend 的 executor_patch 需要更新。
    - 建议测试区域: `vllm_ascend/patch/worker/worker_base_patch`, `vllm_ascend/patch/worker/executor_patch`, `vllm_ascend/patch/worker/block_table_patch`

- **[9969466a](https://github.com/vllm-project/vllm/commit/9969466a597810db6e06b4942dd6cc2086885ee2)** 为 MiMo 模型添加 SWA（滑动窗口注意力）+ DFlash 推测解码支持。主要变更包括：1) qwen3_dflash.py 中新增 _resolve_layer_attention 函数，支持从配置中解析每层的滑动窗口和因果性；2) DFlashQwen3Attention 支持滑动窗口和 attention_sink_bias；3) DFlashQwen3Model 支持独立的 mask_embedding；4) MiMoV2Model 添加 EagleModelMixin 支持；5) FlashAttentionMetadata 新增 sliding_window 字段，支持非因果滑动窗口的对称化。这是一个中等风险的 feature。
  - 标签: `feature`, `medium-risk`, `spec_decode`, `attention`, `model-runner`
  - 变更文件:
  - 修改 `tests/models/registry.py` (+1/-1)
  - 修改 `vllm/model_executor/models/mimo_v2.py` (+16/-3)
  - 修改 `vllm/model_executor/models/qwen3_dflash.py` (+193/-4)
  - 修改 `vllm/v1/attention/backends/flash_attn.py` (+33/-17)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) FlashAttentionMetadata 新增 sliding_window 字段，vllm-ascend 的 attention_backend_patch 需要评估是否需要同步更新。2) FlashAttentionMetadataBuilder 中新增 _maybe_symmetrize_window 函数，vllm-ascend 的 attention_backend_patch 需要评估。3) DFlashQwen3ForCausalLM 中新增 _read_mask_embedding 方法，vllm-ascend 的 spec_decode_patch 需要评估。

### vllm-ascend
- **[1930088f](https://github.com/vllm-project/vllm-ascend/commit/1930088f960aba65eeaae82e9617d090283edc1f)** 此提交旨在支持 DeepSeek V4 的 MTP (Multi-Token Prediction) 图捕获。主要变更包括：1) 在 `llm_base_proposer` 的 `dummy_run` 中添加了正确的参数，特别是为不同 draft step 创建了独立的 RoPE 缓冲区，以解决低接受率问题。2) 修改了 `_pad_query_start_loc_for_fia` 方法，使其接受一个 `query_start_loc` 参数，从而允许目标模型和 draft 模型使用各自的变量，避免了 `copy_to_gpu` 时的竞态条件。3) 在 DSA attention 后端中，为 draft 步骤创建了独立的 `spec_sas_metadata` 缓冲区，并修改了 `get_cos_and_sin_dsa` 以支持按 draft 索引缓存 RoPE。4) 在 `llm_base_proposer` 的 `dummy_run` 和 `_propose` 方法中，增加了对 `block_table`、`slot_mapping`、`seq_lens` 和 `query_start_loc` 的按 draft 步骤复制逻辑，以确保图捕获时每个步骤的元数据独立。此变更涉及 `attention`、`spec_decode`、`ops` 和 `worker` 模块，风险较高，因为它修改了投机解码的核心数据流和图捕获逻辑。
  - 标签: `feature`, `high-risk`, `spec_decode`, `attention`, `ops`, `model-runner`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/test_deepseek_v4.py` (+1/-1)
  - 修改 `tests/ut/spec_decode/a2/test_eagle_proposer.py` (+4/-1)
  - 修改 `vllm_ascend/_310p/model_runner_310p.py` (+5/-4)
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+20/-2)
  - 修改 `vllm_ascend/ops/rope_dsv4.py` (+41/-5)
  - 修改 `vllm_ascend/spec_decode/llm_base_proposer.py` (+43/-9)
  - 修改 `vllm_ascend/worker/model_runner_v1.py` (+18/-7)
  - Ascend 影响: ✓ 无影响

- **[801a6b41](https://github.com/vllm-project/vllm-ascend/commit/801a6b41d29d23399bd8c9ebc2ea8883e2beefae)** 此提交将 vLLM-Ascend 适配到上游 vLLM 的新版本 (a30addc7)。主要变更包括：1) 更新了 `test_extract_hidden_states.py` 以使用新的 `example_hidden_states_connector` API。2) 更新了 `test_patch_tool_choice_none_content.py` 以调用新的 `_extract_tool_calls` 方法。3) 在 `fused_moe.py` 中，更新了导入路径并简化了 `_needs_routed_expert_parameter_aliases` 逻辑，仅保留对 `gpt_oss` 的兼容。4) 在 `attn_utils.py` 中，为 `build_attn_metadata` 添加了 `causal` 参数。5) 在 `model_runner.py` 中，修复了 `decode_query_len` 的初始化方式。此变更是常规的版本升级适配，风险中等，涉及多个模块的接口适配。
  - 标签: `chore`, `medium-risk`, `model-runner`, `ops`, `test`
  - 变更文件:
  - 修改 `.github/vllm-main-verified.commit` (+1/-1)
  - 修改 `requirements-dev.txt` (+1/-1)
  - 修改 `tests/e2e/pull_request/one_card/spec_decode/test_extract_hidden_states.py` (+27/-7)
  - 修改 `tests/ut/patch/platform/test_patch_tool_choice_none_content.py` (+2/-2)
  - 修改 `vllm_ascend/ops/fused_moe/fused_moe.py` (+6/-28)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+2/-0)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-06-30
### vllm
- **[e840f0d3](https://github.com/vllm-project/vllm/commit/e840f0d3f5d26803e907d64a84be521d9568900a)** 将项目中所有 `torch.cuda.Event` 替换为 `torch.Event`，并添加 pre-commit 检查禁止新的 `torch.cuda.Event` 使用。这是平台抽象化工作的一部分，使代码能在非 CUDA 设备上运行。变更涉及 130 个文件，包括 benchmarks、测试、分布式 KV 传输、LoRA、模型层、采样器、spec decode 等多个模块。
  - 标签: `refactor`, `platform`, `low-risk`
  - 变更文件（共 31 个）:
  - 修改 `benchmarks/benchmark_topk_topp.py` (+2/-4)
  - 修改 `benchmarks/kernels/benchmark_moe_defaults.py` (+2/-2)
  - 修改 `benchmarks/kernels/benchmark_selective_state_update.py` (+2/-2)
  - 修改 `tests/v1/kv_connector/unit/test_hf3fs_connector.py` (+1/-1)
  - 修改 `tools/pre_commit/check_torch_cuda.py` (+9/-1)
  - 修改 `vllm/distributed/eplb/eplb_state.py` (+2/-2)
  - 修改 `vllm/distributed/eplb/eplb_utils.py` (+2/-2)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/example_hidden_states_connector.py` (+4/-4)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/hf3fs_client.py` (+1/-1)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/hf3fs_connector.py` (+3/-3)
  - ... 及其他 21 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 Ascend 平台。vllm-ascend 的 `vllm/v1/worker/xpu_model_runner.py` 中原本有 `torch.cuda.Event = torch.Event` 的 patch，该 patch 需要移除。同时 vllm-ascend 的 worker 和 attention 模块中如果使用了 `torch.cuda.Event`，需要替换为 `torch.Event`。
    - 建议测试区域: `vllm_ascend/worker/`, `vllm_ascend/attention/`, `vllm_ascend/patch/`

- **[db808b39](https://github.com/vllm-project/vllm/commit/db808b39614384a0349378268a46a1a0feabcec3)** 实现 block verification 拒绝采样方法（Sun et al., 2024）。新增 `use_block_verification` 参数，在 `rejection_sample` 中实现 block verification 逻辑：1) 计算累积联合比率 `cumulative_log_p`；2) 计算残差质量 `residual_mass`；3) 使用 block verification 阈值 `h` 决定接受长度；4) 在 resample 阶段根据 block verification 调整目标分布。新增多个 Triton kernel 支持这些计算。同时更新 `SpeculativeConfig` 支持 `"block"` 作为 `rejection_sample_method`。
  - 标签: `feature`, `spec-decode`, `sampler`, `high-risk`
  - 变更文件:
  - 修改 `tests/v1/spec_decode/test_rejection_sampler_utils.py` (+103/-0)
  - 修改 `vllm/config/speculative.py` (+4/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler.py` (+6/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py` (+528/-81)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 影响 Ascend 的投机解码模块。vllm-ascend 的 `vllm_ascend/spec_decode/` 模块实现了投机解码的 Ascend 适配，新增的 block verification 方法需要 Ascend 实现对应的 Triton kernel 或使用 CPU fallback。`RejectionSampleMethod` 类型新增 `"block"` 值，影响 `SpeculativeConfig` 的解析。
    - 建议测试区域: `vllm_ascend/spec_decode/`, `vllm_ascend/sample/`

- **[8cc24233](https://github.com/vllm-project/vllm/commit/8cc242335de805cac390580f0dcd9e69b6ed86c0)** 优化XPU Worker的关闭逻辑，防止资源泄漏。主要变更包括：1) 在XPUPlatform.check_and_update_config中，当shutdown_timeout为0时自动设置为5秒，确保oneCCL/Level Zero资源有足够时间释放；2) 在GPUModelRunner.shutdown()中，将ROCm特定的内存清理逻辑扩展为同时适用于ROCm和XPU；3) 在GPUWorker.shutdown()中，将CuMemAllocator的release_pools调用限制在cuda_alike平台，避免XPU平台错误调用；4) 新增XPUWorker.shutdown()方法，调用父类shutdown后释放XpuMemAllocator的内存池；5) 更新测试工具以支持XPU平台的内存查询；6) 调整CI配置以包含新的测试。这是一个低风险的优化，主要影响XPU平台的资源管理。
  - 标签: `performance`, `low-risk`, `worker`, `xpu`, `resource-management`
  - 变更文件:
  - 修改 `.buildkite/intel_jobs/basic_correctness.yaml` (+1/-0)
  - 修改 `.buildkite/intel_jobs/lora_intel.yaml` (+1/-1)
  - 修改 `tests/utils.py` (+7/-0)
  - 修改 `vllm/platforms/xpu.py` (+10/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-1)
  - 修改 `vllm/v1/worker/gpu_worker.py` (+4/-3)
  - 修改 `vllm/v1/worker/xpu_worker.py` (+17/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 影响GPUModelRunner.shutdown()和GPUWorker.shutdown()方法。GPUModelRunner.shutdown()中增加了对XPU平台的内存清理逻辑（gc.collect + empty_cache + synchronize），NPUModelRunner继承自GPUModelRunner，需要确认Ascend平台是否也需要类似的清理。GPUWorker.shutdown()中将CuMemAllocator.release_pools()限制在cuda_alike平台，NPUWorker继承自WorkerBase而非GPUWorker，但NPUWorker有自己的shutdown逻辑，需要确认是否也需要类似的平台条件判断。

- **[fb42e521](https://github.com/vllm-project/vllm/commit/fb42e5219edcbce66fb1e758c004e610e618f70a)** 将 `torch.cuda.mem_get_info` 替换为 `torch.accelerator.get_memory_info`。这是平台抽象化工作的一部分，使内存查询代码能在非 CUDA 设备上运行。变更涉及测试、模型层、worker、内存工具等多个模块。同时更新 pre-commit 检查，禁止新的 `torch.cuda.mem_get_info` 和 `current_platform.mem_get_info` 使用。从 CPU 平台类中移除 `mem_get_info` 方法。
  - 标签: `refactor`, `platform`, `medium-risk`
  - 变更文件（共 17 个）:
  - 修改 `tests/basic_correctness/test_mem.py` (+13/-13)
  - 修改 `tests/kernels/moe/test_moe.py` (+1/-1)
  - 修改 `tests/models/multimodal/generation/test_memory_leak.py` (+1/-1)
  - 修改 `tests/utils_/test_mem_utils.py` (+11/-9)
  - 修改 `tests/v1/kv_connector/unit/test_rixl_gpu_mem_diag.py` (+1/-2)
  - 修改 `tests/v1/sample/test_logprobs.py` (+1/-1)
  - 修改 `tests/v1/sample/test_topk_topp_sampler.py` (+1/-1)
  - 修改 `tools/pre_commit/check_torch_cuda.py` (+2/-1)
  - 修改 `vllm/model_executor/models/gemma4_mm.py` (+2/-3)
  - 修改 `vllm/platforms/cpu.py` (+0/-5)
  - ... 及其他 7 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 Ascend 平台。vllm-ascend 的 `vllm/v1/worker/xpu_model_runner.py` 中原本有 `torch.cuda.mem_get_info = torch.xpu.mem_get_info` 的 patch，该 patch 需要移除。同时 vllm-ascend 中如果使用了 `current_platform.mem_get_info`，需要替换为 `torch.accelerator.get_memory_info`。
    - 建议测试区域: `vllm_ascend/worker/`, `vllm_ascend/patch/`

- **[61ab70ec](https://github.com/vllm-project/vllm/commit/61ab70ec3bd13dd422b86f3b80207d322994a5e7)** V2 Model Runner 支持 mamba hybrid 模型的 align prefix cache。主要变更：1) 移除 V2 runner 对 align mamba cache mode 的限制；2) 在 `MambaHybridModelState` 中添加 `preprocess_state` 和 `postprocess_state` 方法，实现 GPU 上的 align 状态迁移；3) 新增 `preprocess_mamba_align_fused_kernel` 和 `precopy_mamba_align_fused_kernel` Triton kernel；4) 重构 `postprocess_mamba_fused_kernel` 支持 V2 的 idx_mapping 和预计算的新 computed tokens；5) 更新 `MambaSpecDecodeGPUContext` 添加 `run_fused_precopy` 和 `run_fused_postprocess_align` 方法；6) 更新 warmup 逻辑为 align 模式预留额外 block。
  - 标签: `feature`, `model-runner`, `mamba`, `spec-decode`, `high-risk`
  - 变更文件:
  - 新增 `tests/kernels/mamba/test_precopy_mamba_align.py` (+180/-0)
  - 修改 `tests/v1/e2e/general/test_mamba_prefix_cache.py` (+280/-16)
  - 修改 `vllm/config/vllm.py` (+0/-11)
  - 修改 `vllm/model_executor/models/diffusion_gemma.py` (+3/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+13/-1)
  - 修改 `vllm/v1/worker/gpu/model_states/interface.py` (+16/-1)
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+174/-8)
  - 修改 `vllm/v1/worker/gpu/warmup.py` (+12/-3)
  - 修改 `vllm/v1/worker/mamba_utils.py` (+367/-91)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 影响 Ascend 的 model runner 和 mamba 模块。`MambaHybridModelState` 新增 `preprocess_state` 和 `postprocess_state` 方法，`ModelSpecificState` 接口新增 `preprocess_state` 方法。`postprocess_state` 的签名已更改，新增 `num_computed_tokens` 参数。`MambaSpecDecodeGPUContext` 新增 `run_fused_precopy` 和 `run_fused_postprocess_align` 方法。vllm-ascend 的 `NPUModelRunner` 如果使用了 mamba 模型，需要同步更新。
    - 建议测试区域: `vllm_ascend/worker/`, `vllm_ascend/ops/mamba/`

---

## 2026-06-29
### vllm
- **[a2abce64](https://github.com/vllm-project/vllm/commit/a2abce646f7db07f2169dfc59433d4128bc404de)** 修复EPLB负载记录中的padding token问题。核心变更：1) 在`EplbState`中新增`num_unpadded_tokens_tensors`列表，记录每个ubatch中真实（非padding）token的数量；2) 在`base_router.py`的Triton kernel中新增`HAS_NUM_UNPADDED`常量，当提供时跳过padding token的负载记录；3) 新增`EplbState.prepare_forward`方法，在每次前向传播前更新unpadded token计数；4) 在`GPUModelRunner`和spec decode的多个speculator中调用`prepare_forward`；5) 新增`compute_hash_cached`工具函数缓存config hash；6) 更新测试用例。
  - 标签: `bugfix`, `medium-risk`, `distributed`
  - 变更文件（共 17 个）:
  - 修改 `tests/distributed/test_eplb_fused_moe_layer_dep_nvfp4.py` (+6/-0)
  - 修改 `tests/kernels/moe/test_moe_layer.py` (+3/-0)
  - 修改 `tests/kernels/moe/test_routing.py` (+66/-0)
  - 修改 `tests/model_executor/test_routed_experts_capture.py` (+1/-0)
  - 修改 `vllm/config/utils.py` (+20/-0)
  - 修改 `vllm/distributed/elastic_ep/elastic_execute.py` (+3/-1)
  - 修改 `vllm/distributed/eplb/eplb_state.py` (+68/-5)
  - 修改 `vllm/model_executor/layers/fused_moe/router/base_router.py` (+35/-8)
  - 修改 `vllm/models/deepseek_v4/nvidia/model.py` (+6/-0)
  - 修改 `vllm/v1/spec_decode/extract_hidden_states.py` (+13/-0)
  - ... 及其他 7 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) `EplbLayerState`新增`num_unpadded_tokens_tensors`字段，影响所有使用EPLB的MoE层。vllm-ascend中如果有自定义EPLB实现，需要同步更新。2) `eplb_map_to_physical_and_record`函数新增`num_unpadded_tokens`参数，影响路由器的EPLB映射调用。3) `EplbState`新增`prepare_forward`方法，影响EPLB状态管理。4) `GPUModelRunner`新增`eplb.prepare_forward`调用，影响模型执行流程。5) spec decode的多个speculator新增`_prepare_eplb_forward`调用，影响推测解码流程。
    - 建议测试区域: `vllm_ascend/tests/test_eplb.py`, `vllm_ascend/tests/test_routing.py`

- **[04724365](https://github.com/vllm-project/vllm/commit/0472436541c842ecda6d249411f1d35649291a79)** 优化推测解码中draft prefill的hidden states收集逻辑。当`last_hidden_states is hidden_states`时（即模型返回了与输入相同的张量对象），直接使用`sample_hidden_states`而非通过索引`hidden_states[last_token_indices]`收集，避免冗余的gather操作。
  - 标签: `performance`, `low-risk`, `spec-decode`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` (+4/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-06-28
### vllm
- **[5c91039c](https://github.com/vllm-project/vllm/commit/5c91039c41bc0b6a4a4ab2dc5f62115946e38a30)** 将 DeepSeek-V2 模型的 MoE all-reduce 替换为 reduce-scatter，以提升 3.1%~3.2% 的端到端吞吐。实现方式：在 `DeepseekV2DecoderLayer` 中新增 `use_sequence_parallel_moe` 标志，当启用时，在 attention 输出后执行 reduce-scatter 将 hidden states 分散到各 TP rank，MoE 在分散后的数据上计算，最后通过 all-gather 恢复完整结果。这减少了 MoE 计算前的 all-reduce 通信开销。同时修改了 `DeepseekV2MoE` 的 `forward` 方法以支持 `already_sequence_parallel` 参数。
  - 标签: `performance`, `high-risk`, `distributed`, `model-runner`
  - 变更文件:
  - 修改 `vllm/model_executor/models/deepseek_v2.py` (+86/-12)
  - Ascend 影响: ✓ 无影响

- **[6eb63a1d](https://github.com/vllm-project/vllm/commit/6eb63a1da6996abad00323dc7e845dc868996524)** 修复 DeepSeek-V3.2 模型中索引器权重加载的问题。当 `index_topk_freq>1` 时，只有部分层构建了 indexer，但 checkpoint 中所有层都包含 indexer 权重。变更在 `load_weights` 中检查当前层是否实际构建了 indexer，如果没有则跳过加载对应的 checkpoint 权重，避免 KeyError 或错误加载。
  - 标签: `bugfix`, `low-risk`, `model-runner`
  - 变更文件:
  - 修改 `vllm/model_executor/models/deepseek_v2.py` (+10/-0)
  - Ascend 影响: ✓ 无影响

- **[c7ca0bcc](https://github.com/vllm-project/vllm/commit/c7ca0bccae667934c29c654544131cdab046adfd)** 为 GLM-4.5/6/7 模型添加 Fused Shared Expert (FSE) 支持。当 AITER 的 fused MoE 和 fusion shared experts 都启用时，将 shared experts 的权重合并到 routed experts 中，通过 FusedMoE 统一处理。变更涉及 `glm4_moe.py` 和 `glm4_moe_mtp.py` 中的权重加载逻辑，将 `mlp.shared_experts` 的权重按 `n_shared_experts` 切分后映射为额外的 routed expert 权重。
  - 标签: `feature`, `high-risk`, `model-runner`, `rocm`
  - 变更文件:
  - 修改 `vllm/model_executor/models/glm4_moe.py` (+138/-63)
  - 修改 `vllm/model_executor/models/glm4_moe_mtp.py` (+116/-42)
  - Ascend 影响: ✓ 无影响

- **[c6741b2a](https://github.com/vllm-project/vllm/commit/c6741b2ad48a46e87d2cce35d113c4ae0950af91)** 新增 Unlimited-OCR 模型支持。该模型基于 DeepSeek-OCR 架构，但使用 DeepSeek-V2 MoE 语言骨干（64 routed + 2 shared experts）和 plain MHA（非 MLA）。核心特性：1) 使用 Reference Sliding Window Attention (R-SWA) 进行注意力计算，通过 FA4 的 mask_mod 或 FlexAttention 实现；2) 支持最多 32 个 local crops（vs DeepSeek-OCR 的 6 个）；3) 多图像请求时禁用 crop 模式。变更涉及模型定义、配置、处理器、tokenizer、KV cache 管理（新增 `RSWASpec` 和 `RSWAManager`）、注意力后端（FA4 和 FlexAttention 的 R-SWA mask_mod）等多个模块。
  - 标签: `feature`, `high-risk`, `model-runner`, `attention`, `multimodal`
  - 变更文件（共 35 个）:
  - 修改 `docs/models/supported_models.md` (+1/-0)
  - 修改 `tests/models/registry.py` (+3/-0)
  - 修改 `tests/v1/core/test_single_type_kv_cache_manager.py` (+51/-1)
  - 修改 `vllm/config/model.py` (+4/-0)
  - 修改 `vllm/config/model_arch.py` (+3/-0)
  - 修改 `vllm/model_executor/layers/attention/__init__.py` (+2/-0)
  - 新增 `vllm/model_executor/layers/attention/rswa_attention.py` (+37/-0)
  - 修改 `vllm/model_executor/models/config.py` (+134/-0)
  - 修改 `vllm/model_executor/models/deepseek_ocr.py` (+4/-2)
  - 修改 `vllm/model_executor/models/deepseek_v2.py` (+25/-12)
  - ... 及其他 25 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) `vllm/v1/attention/backend.py` 中 `CommonAttentionMetadata` 新增 `rswa_prefix_lens` 字段，所有注意力后端（包括 AscendAttentionBackend）的元数据结构需要适配。2) `vllm/v1/core/single_type_kv_cache_manager.py` 中 `remove_skipped_blocks` 方法签名变更（新增 `num_prompt_tokens` 参数），影响 Ascend 的 KV cache manager patch。3) `vllm/v1/worker/gpu/input_batch.py` 中 `InputBatch` 新增 `rswa_prefix_lens` 字段，影响 Ascend 的 input batch 处理。4) `vllm/v1/kv_cache_interface.py` 新增 `RSWASpec`，如果 Ascend 需要支持 R-SWA 则需要实现对应的 spec 和 manager。

- **[11a12305](https://github.com/vllm-project/vllm/commit/11a12305c0522c5c1ed273d7d3dc2304ac0cd495)** 修复 Model Runner V2 中 MTP draft 模型的 hidden states 处理。将 `AutoRegressiveSpeculator` 的 `model_returns_tuple` 属性移除，改为在 `_run_model` 中通过 `isinstance(ret_hidden_states, tuple)` 动态判断返回值类型。这样 MTP 模型（如 DeepSeek）可以返回 `(logits_hidden, feedback_hidden)` 元组，而无需声明 `model_returns_tuple=True`。同时移除了 `Gemma4Speculator` 和 `MTPSpeculator` 中的 `model_returns_tuple` 属性。
  - 标签: `bugfix`, `low-risk`, `spec-decode`
  - 变更文件:
  - 新增 `tests/v1/worker/test_gpu_autoregressive_speculator.py` (+82/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` (+3/-11)
  - 修改 `vllm/v1/worker/gpu/spec_decode/gemma4/speculator.py` (+0/-7)
  - 修改 `vllm/v1/worker/gpu/spec_decode/mtp/speculator.py` (+0/-4)
  - Ascend 影响: ✓ 无影响

- **[b6caeb5a](https://github.com/vllm-project/vllm/commit/b6caeb5a0966103c6df22f019270d66233e1b687)** 修复 Spec Decode 中 rejection sampling 的随机数精度问题。将 `tl_rand64`（64-bit 随机数）替换为 `tl_rand32`（32-bit 随机数），并使用 fp32 均匀分布阈值进行 acceptance 判断。这避免了 fp64 随机数生成的开销，同时保持足够的精度。
  - 标签: `performance`, `low-risk`, `spec-decode`, `kernels`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/sample/gumbel.py` (+9/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py` (+3/-3)
  - Ascend 影响: ✓ 无影响

---

## 2026-06-27
### vllm
- **[c6dd32a8](https://github.com/vllm-project/vllm/commit/c6dd32a810aa8c4eda5696722c807e53d9f595a5)** 为 ModelRunner V2 支持实时 embeddings。主要变更包括：1) 在 `vllm/v1/worker/gpu/mm/encoder_runner.py` 中，`gather_mm_embeddings` 方法增加了对实时模型的支持，当模型支持实时推理时，不再跳过 decode 请求的 embeddings 收集；2) 在 `vllm/v1/worker/gpu/model_runner.py` 中，`execute_model` 方法在 dummy run 时使用预分配的 dummy inputs_embeds，避免调用 encoder；3) 在 `vllm/v1/worker/gpu/model_states/interface.py` 中，`gather_mm_embeddings` 的参数名从 `num_computed_prefill_tokens_np` 改为 `num_computed_tokens_np`；4) 在 `vllm/v1/worker/gpu/model_states/default.py` 中新增 `dummy_inputs_embeds` 方法。风险中等，因为修改了 ModelRunner 的核心逻辑和接口参数名，可能影响继承 `GPUModelRunner` 的外部实现。
  - 标签: `feature`, `medium-risk`, `model-runner`, `multimodal`
  - 变更文件:
  - 修改 `tests/v1/worker/test_encoder_runner.py` (+3/-3)
  - 修改 `vllm/model_executor/models/diffusion_gemma.py` (+1/-1)
  - 修改 `vllm/v1/worker/gpu/mm/encoder_runner.py` (+20/-17)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+18/-13)
  - 修改 `vllm/v1/worker/gpu/model_states/default.py` (+4/-0)
  - 修改 `vllm/v1/worker/gpu/model_states/interface.py` (+6/-2)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1) `vllm/v1/worker/gpu/mm/encoder_runner.py` 中 `gather_mm_embeddings` 方法的参数名从 `computed_prefill_lens` 改为 `num_computed_tokens`，vllm-ascend 的 `EncoderRunner` 实现若直接调用此方法需同步更新参数名。2) `vllm/v1/worker/gpu/model_states/interface.py` 中 `ModelState` 基类新增了 `dummy_inputs_embeds` 方法，vllm-ascend 的 `NPUModelRunner` 若继承 `GPUModelRunner` 需确认是否需要 override 此方法。3) `vllm/v1/worker/gpu/model_states/interface.py` 中 `gather_mm_embeddings` 的参数名从 `num_computed_prefill_tokens_np` 改为 `num_computed_tokens_np`，vllm-ascend 的 `NPUModelRunner` 若调用此方法需同步更新。
    - 建议测试区域: `vllm_ascend/worker/model_runner_v1.py`, `vllm_ascend/worker/test_encoder_runner.py`

- **[1d41009e](https://github.com/vllm-project/vllm/commit/1d41009e81eb6493f2c19e9d2a0d472564764e62)** 修复 ModelRunner V2 中 cross-attention block table 的尺寸计算问题。在 `vllm/v1/worker/gpu/model_runner.py` 中，`initialize_kv_cache` 方法在计算 `block_table_max_model_len` 时，除了考虑 `max_source_positions`，还加入了 `self.scheduler_config.max_num_encoder_input_tokens`，确保 cross-attention block table 能够索引 encoder tokens（如 Whisper 的 ~1500 tokens），这些 tokens 可能超过 decoder 的 `max_model_len`。风险较低，修复了明确的 bug。
  - 标签: `bugfix`, `low-risk`, `model-runner`, `attention`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+3/-2)
  - Ascend 影响: ✓ 无影响

- **[b94f212e](https://github.com/vllm-project/vllm/commit/b94f212e37f4ddf4b5e1cc96cd87217f36e3ec0c)** 重构 ModelState 初始化逻辑，消除代码重复。将 `DefaultModelState`、`EncoderDecoderModelState` 和 `DiffusionGemmaModelState` 中重复的初始化代码（设置 `vllm_config`、`model_config`、`scheduler_config`、`model`、`device`、`max_model_len`、`max_num_reqs`、`max_num_tokens`、`inputs_embeds_size`、`dtype`、`supports_mm_inputs`、`encoder_cache`、`encoder_runner` 等）提取到基类 `ModelState.__init__` 中。子类现在只需调用 `super().__init__()` 即可。风险较低，纯重构，不改变行为。
  - 标签: `refactor`, `low-risk`, `model-runner`
  - 变更文件:
  - 修改 `vllm/model_executor/models/diffusion_gemma.py` (+1/-27)
  - 修改 `vllm/v1/worker/gpu/model_states/default.py` (+1/-25)
  - 修改 `vllm/v1/worker/gpu/model_states/encoder_decoder.py` (+1/-19)
  - 修改 `vllm/v1/worker/gpu/model_states/interface.py` (+23/-6)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: `vllm/v1/worker/gpu/model_states/interface.py` 中 `ModelState` 基类的 `__init__` 方法从抽象方法变为具体实现，初始化了 `encoder_runner` 等属性。vllm-ascend 的 `NPUModelRunner` 若直接访问 `self.encoder_runner` 或 `self.supports_mm_inputs` 等属性，行为不变。但若 vllm-ascend 有自定义的 `ModelState` 子类，需确保调用 `super().__init__()`。

---

## 2026-06-26
### vllm
- **[37ce3492](https://github.com/vllm-project/vllm/commit/37ce34922f7f5e58241369511130cd99c1c50bfe)** 修复了 Triton MoE 中 NVFP4 模拟的 CUDA Graph 捕获失败问题。在 Nvfp4QuantizationEmulationTritonExperts 类中新增了 a1_scale 属性，返回 self.a1_gscale，并在 triton_moe.py 中将 moe_kernel_quantize_input 的调用从 self.a1_scale or self.a1_gscale 改为 self.a1_scale。
  - 标签: `bugfix`, `low-risk`, `model-runner`, `quantization`
  - 变更文件:
  - 修改 `vllm/model_executor/layers/fused_moe/experts/nvfp4_emulation_moe.py` (+5/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/experts/triton_moe.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

- **[c2507fb2](https://github.com/vllm-project/vllm/commit/c2507fb2937aa8c8e74bea15719d04fb6090befe)** 为 ROCm 平台的 bias-routed MoE 实现了共享专家融合（shared-expert fusion），并启用了 MiniMax-M3 模型的 mxfp8 支持。主要变更：1) FusedMoE 层新增 shared_expert_weight 参数，用于在融合共享专家时调整权重；2) FusedTopKBiasRouter 新增 num_fused_shared_experts 和 shared_expert_weight 参数，在路由计算后将共享专家作为额外的 routed-expert slot 追加；3) MiniMax-M3 模型在 ROCm 平台上通过 VLLM_ROCM_USE_AITER_FUSION_SHARED_EXPERTS 环境变量启用共享专家融合；4) mxfp8_native_moe 中修复了 binning 逻辑，使用 w13.shape[0] 而非 global_num_experts 来正确处理融合后的权重张量。
  - 标签: `feature`, `performance`, `medium-risk`, `model-runner`, `moe`
  - 变更文件:
  - 修改 `vllm/model_executor/layers/fused_moe/experts/mxfp8_native_moe.py` (+7/-1)
  - 修改 `vllm/model_executor/layers/fused_moe/layer.py` (+27/-16)
  - 修改 `vllm/model_executor/layers/fused_moe/router/fused_topk_bias_router.py` (+26/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/router/router_factory.py` (+3/-0)
  - 修改 `vllm/models/minimax_m3/amd/model.py` (+47/-3)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1. FusedMoE 层新增了 shared_expert_weight 参数，NPUModelRunner 在调用 FusedMoE 时需要传递此参数。2. FusedTopKBiasRouter 新增了 num_fused_shared_experts 和 shared_expert_weight 参数，Ascend 的 MoE 路由实现（如果有自定义路由）需要同步适配。3. create_fused_moe_router 函数新增了 shared_expert_weight 参数，所有调用该函数的地方需要适配。4. determine_expert_counts 函数中移除了对 rocm_aiter_ops.is_fusion_moe_shared_experts_enabled() 的独占依赖，改为同时支持 envs.VLLM_ROCM_USE_AITER_FUSION_SHARED_EXPERTS，Ascend 的 MoE 配置逻辑不受影响。

- **[8e394244](https://github.com/vllm-project/vllm/commit/8e394244a59afc67a37bf47dab0ab76bf5ce5885)** 为 MiniMax-M3-MXFP4 模型启用了 AITER MoE 后端。主要变更：1) FusedMoEConfig 新增 intermediate_pad 字段；2) rocm_aiter_moe.py 支持 SWIGLUOAI_UNINTERLEAVE 激活函数，并新增 activation_interleave 参数控制 gate_mode；3) MiniMax-M3 模型在调用 FusedMoE 时传递 intermediate_pad=0。
  - 标签: `feature`, `low-risk`, `model-runner`, `moe`
  - 变更文件:
  - 修改 `vllm/model_executor/layers/fused_moe/config.py` (+2/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/experts/rocm_aiter_moe.py` (+22/-8)
  - 修改 `vllm/model_executor/layers/fused_moe/layer.py` (+2/-0)
  - 修改 `vllm/models/minimax_m3/amd/model.py` (+1/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1. FusedMoEConfig 新增了 intermediate_pad 字段，NPUModelRunner 在创建 FusedMoEConfig 时需要适配。2. FusedMoE 函数新增了 intermediate_pad 参数，所有调用 FusedMoE 的地方需要传递此参数。3. MoEActivation 新增了 SWIGLUOAI_UNINTERLEAVE 枚举值，Ascend 的 MoE 激活函数处理逻辑需要检查是否需要支持此枚举。

- **[5b330417](https://github.com/vllm-project/vllm/commit/5b33041746b9b9ab45bdbd9b42cdd5d19357879a)** 修复了 whisper 测试中的两个问题：1) EncoderCache 新增 __len__ 方法；2) maybe_create_mm_pruner 中的空值检查从 not rope_state 改为 rope_state is None，从 not encoder_cache 改为 encoder_cache is None，从 not model_config.multimodal_config 改为 model_config.multimodal_config is None，以避免在空张量或空列表等 falsy 值上误判。
  - 标签: `bugfix`, `low-risk`, `model-runner`, `multimodal`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/mm/encoder_cache.py` (+3/-0)
  - 修改 `vllm/v1/worker/gpu/model_states/mm_pruning.py` (+3/-3)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1. EncoderCache 新增了 __len__ 方法，所有使用 EncoderCache 的代码（包括 Ascend 的 encoder 实现）可以调用 len() 获取缓存大小。2. maybe_create_mm_pruner 中的空值检查从 not 改为 is None，这改变了行为：之前空张量（falsy）会触发提前返回，现在只有 None 才会触发。Ascend 的 MM pruner 实现如果依赖旧行为需要适配。

- **[02a1f237](https://github.com/vllm-project/vllm/commit/02a1f23711c5bdbff81eb8a610dde39e1141d036)** 为 DFlash 实现了逐层 K-norm 的融合 RMSNorm。修改了 csrc 中的 rms_norm kernel，支持 2D 权重（[num_groups, hidden_size]），使得可以一次性对所有层的 K 进行 RMSNorm，而不是逐层循环。在 Qwen3DFlash 模型中，将 K-norm 权重堆叠为 [num_layers, head_dim] 的连续张量，并调用一次 ops.rms_norm 完成所有层的归一化。
  - 标签: `performance`, `low-risk`, `model-runner`, `spec-decode`
  - 变更文件:
  - 修改 `csrc/libtorch_stable/layernorm_kernels.cu` (+25/-8)
  - 新增 `tests/kernels/core/test_batched_weight_rms_norm.py` (+70/-0)
  - 修改 `vllm/model_executor/models/qwen3_dflash.py` (+13/-10)
  - Ascend 影响: ✓ 无影响

- **[652d962b](https://github.com/vllm-project/vllm/commit/652d962bc9df7e04959e84ce478c3a8d26fe52a7)** 为推测解码减少了 draft token 生成时的 TP 通信。新增 use_local_argmax_reduction 配置选项，当启用时，draft 模型的 greedy sample 通过调用 model.get_top_tokens() 在本地获取 argmax，而不是先通过 compute_logits 计算完整 logits 再 argmax，从而将通信量从 O(vocab_size) 降低到 O(2*tp_size)。同时增加了验证逻辑，确保该模式与 probabilistic 采样不兼容，且 draft 模型实现了 get_top_tokens 方法。
  - 标签: `performance`, `low-risk`, `spec-decode`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/spec_decode/speculator.py` (+34/-3)
  - Ascend 影响: ✓ 无影响

- **[5314665b](https://github.com/vllm-project/vllm/commit/5314665badcb93f798e117aacad8ce02f148cd73)** 为 DFlash 启用了注意力后端选择。在 load_dflash_model 中，将 speculative_config.attention_backend 传递给 draft 模型的 attention_config.backend，使得 draft 模型可以使用与目标模型不同的注意力后端。
  - 标签: `feature`, `low-risk`, `spec-decode`, `attention`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/utils.py` (+3/-1)
  - Ascend 影响: ✓ 无影响

- **[3daea7ce](https://github.com/vllm-project/vllm/commit/3daea7ceb990bff87e925b2f4b77325af052282f)** 修复了 Mamba 混合模型中 seq_lens_cpu_upper_bound 的传递问题。在 MambaHybridModelState.prepare_attn 方法中，将 seq_lens_cpu_upper_bound 参数传递给 prepare_attn 调用。
  - 标签: `bugfix`, `low-risk`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

- **[32bb3195](https://github.com/vllm-project/vllm/commit/32bb3195f0b93f6971781479591f7a6ee666e7dc)** 为大型 logprobs 请求限制了内存使用。在 compute_token_logprobs 函数中，将 _topk_log_softmax_kernel 的 PADDED_TOPK 参数替换为 TOPK_BLOCK_SIZE，并设置上限为 1024。当 num_logprobs 很大时，kernel 会分块处理，避免一次性分配过大的内存。
  - 标签: `performance`, `low-risk`, `sampler`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/sample/logprob.py` (+18/-10)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 1. compute_token_logprobs 函数中 _topk_log_softmax_kernel 的 PADDED_TOPK 参数被替换为 TOPK_BLOCK_SIZE，且新增了 _MAX_TOPK_BLOCK = 1024 上限。AscendSampler 如果实现了自己的 compute_token_logprobs 或使用了相同的 kernel，需要同步适配。2. _topk_log_softmax_kernel 的 kernel 参数从 PADDED_TOPK 改为 TOPK_BLOCK_SIZE，且内部逻辑改为循环分块处理。如果 Ascend 有自定义的 Triton kernel 实现，需要同步修改。
    - 建议测试区域: `vllm_ascend/sample/sampler.py`

- **[c53994e1](https://github.com/vllm-project/vllm/commit/c53994e1348bac3496aafb88e9e731124a00a8a7)** 在拒绝采样中使用 log1p 提高数值稳定性。将 rejection_sampler_utils.py 中的 tl.log(1 - ratio) 替换为 tldevice.log1p(-ratio)，当 ratio 接近 1 时，log1p 比 log(1 - x) 具有更高的数值精度。
  - 标签: `performance`, `low-risk`, `spec-decode`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py` (+7/-5)
  - Ascend 影响: ✓ 无影响

---

## 2026-06-25
### vllm-ascend
- **[b9a12d96](https://github.com/vllm-project/vllm-ascend/commit/b9a12d96bac03cb747b2d31e6e2081b5f38fe2b2)** 优化异步投机解码模式下seq_lens的CPU校正。之前通过额外的NPU->CPU拷贝seq_lens并同步事件来校正optimistic_seq_lens_cpu，现在直接使用已异步拷贝的valid_sampled_token_count_cpu在CPU上校正，避免不必要的NPU->CPU同步。新增correct_optimistic_seq_lens_cpu函数和_correct_optimistic_seq_lens_cpu方法，并添加单元测试。同时更新了310P的model_runner。风险中等，因为校正逻辑变更可能影响投机解码的精度，但新增的单元测试覆盖了主要场景。
  - 标签: `performance`, `bugfix`, `medium-risk`, `spec_decode`, `model-runner`
  - 变更文件:
  - 新增 `tests/ut/spec_decode/test_utils.py` (+186/-0)
  - 修改 `tests/ut/worker/a2/test_model_runner_v1.py` (+57/-0)
  - 修改 `vllm_ascend/_310p/model_runner_310p.py` (+9/-8)
  - 修改 `vllm_ascend/spec_decode/utils.py` (+42/-0)
  - 修改 `vllm_ascend/worker/model_runner_v1.py` (+59/-60)
  - Ascend 影响: ✓ 无影响

- **[5270d846](https://github.com/vllm-project/vllm-ascend/commit/5270d84675dc122273bb7ac16688046b6b208614)** 修复Qwen3.5在ACL Graph、MTP和DP同时启用时的精度问题。两个修复：1) dummy graph运行时未经过_prepare_inputs()，但GDN/Mamba attention metadata仍读取block_table，导致读取到stale block id。修复在_dummy_run中同步block_table。2) 当MTP+DP+ACL Graph时，captured的GDN spec conv1d graph task可能在无runtime spec sequence的rank上重放，导致cache_indices为空，kernel使用默认batch-indexed state writes损坏conv_state。修复在无spec sequence时传递-1作为cache_indices。风险中等，涉及GDN状态管理。
  - 标签: `bugfix`, `medium-risk`, `model-runner`, `spec_decode`, `ops`
  - 变更文件:
  - 修改 `vllm_ascend/ops/gdn.py` (+7/-0)
  - 修改 `vllm_ascend/worker/model_runner_v1.py` (+5/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-06-24
### vllm
- **[84c62e1c](https://github.com/vllm-project/vllm/commit/84c62e1cbdef4250fbfda83782fd250e07ad0256)** 该 commit 为多模态模型（特别是 Qwen2.5-VL、Qwen3-VL 等支持 EVS 的模型）添加了 Efficient Video Sampling（EVS）支持。核心变更包括：1) 新增 vllm/v1/worker/gpu/model_states/mm_pruning.py 文件，实现 MultiModalPruner 类，用于处理 M-RoPE 位置重计算和嵌入修剪；2) 修改 ModelState 接口（interface.py），新增 gather_mm_embeddings 默认方法，并将 get_mm_embeddings 方法签名增加 req_states 参数；3) 修改 DefaultModelState（default.py），集成 MultiModalPruner 的 recompute 和 strip 逻辑；4) 修改 GPUModelRunner（model_runner.py），简化 gather_mm_embeddings 调用，将参数传递改为直接传递 input_batch；5) 修改 Qwen2.5-VL 和 Qwen3-VL 模型的 recompute_mrope_positions 方法，支持 input_ids 为 torch.Tensor 类型；6) 修改 RopeState（rope.py），新增 read_prefill_positions 和 update_prefill_positions 方法用于读写分阶段 prefill 位置。该变更对多模态模型的视频处理性能有显著提升，但涉及多个接口变更，需要确保所有 ModelState 子类同步更新。
  - 标签: `feature`, `medium-risk`, `model-runner`, `multimodal`
  - 变更文件:
  - 修改 `vllm/model_executor/models/diffusion_gemma.py` (+9/-9)
  - 修改 `vllm/model_executor/models/interfaces.py` (+6/-5)
  - 修改 `vllm/model_executor/models/qwen2_5_vl.py` (+10/-6)
  - 修改 `vllm/model_executor/models/qwen3_vl.py` (+14/-10)
  - 修改 `vllm/v1/worker/gpu/mm/rope.py` (+17/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+4/-10)
  - 修改 `vllm/v1/worker/gpu/model_states/default.py` (+25/-8)
  - 修改 `vllm/v1/worker/gpu/model_states/encoder_decoder.py` (+4/-1)
  - 修改 `vllm/v1/worker/gpu/model_states/interface.py` (+21/-1)
  - 新增 `vllm/v1/worker/gpu/model_states/mm_pruning.py` (+135/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 影响 ModelState 接口（vllm/v1/worker/gpu/model_states/interface.py）中的 get_mm_embeddings 方法签名，新增 req_states 参数。vllm-ascend 的 NPUModelRunner 继承自 GPUModelRunner，其 get_mm_embeddings 方法在 default.py 中被重写，但 vllm-ascend 的 NPUModelRunner 也重写了 get_mm_embeddings 方法（在 vllm_ascend/worker/model_runner_v1.py 中），需要检查是否适配了新的 req_states 参数。同时，ModelState 接口新增了 gather_mm_embeddings 默认方法，vllm-ascend 的 DefaultModelState 重写了该方法，需要确认是否兼容。此外，RopeState 新增了 read_prefill_positions 和 update_prefill_positions 方法，vllm-ascend 如果使用了 RopeState 则需要同步更新。

- **[7ee4d220](https://github.com/vllm-project/vllm/commit/7ee4d220097db4b397e55fd4ad58caf6a7977c5b)** 修复 rejection sampler 中 placeholder draft token (-1) 的处理。在 rejection_greedy_sample_kernel 和 rejection_random_sample_kernel 中，添加了对 draft_token_id < 0 的检查，确保 placeholder token 被拒绝而不是被采样。同时修复了 _rejection_kernel 中可能的 OOB 指针访问。这是一个 Bug 修复，风险较低。
  - 标签: `bugfix`, `low-risk`, `spec-decode`, `sampler`
  - 变更文件:
  - 修改 `tests/v1/sample/test_rejection_sampler.py` (+33/-0)
  - 修改 `tests/v1/spec_decode/test_rejection_sampler_utils.py` (+29/-0)
  - 修改 `vllm/v1/sample/rejection_sampler.py` (+6/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py` (+7/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 影响 RejectionSampler 的 Triton kernel 和 rejection_sampler_utils 中的 _rejection_kernel。vllm-ascend 的 AscendSampler 需要同步更新 placeholder draft token 的处理逻辑。
    - 建议测试区域: `vllm_ascend/sample/`, `vllm_ascend/spec_decode/`

- **[e2bdc246](https://github.com/vllm-project/vllm/commit/e2bdc24612ab0b7bf7a1bc67c955fd244e8660c4)** 修复 ROCm 平台在 Ray driver 线程中使用 use_v2_model_runner 的问题。将 CUDA_VISIBLE_DEVICES 的环境变量检查改为根据平台选择 HIP_VISIBLE_DEVICES 或 CUDA_VISIBLE_DEVICES。这是一个跨平台兼容性修复，风险较低。
  - 标签: `bugfix`, `low-risk`, `rocm`
  - 变更文件:
  - 修改 `.buildkite/test_areas/distributed.yaml` (+13/-1)
  - 修改 `vllm/triton_utils/importing.py` (+10/-3)
  - Ascend 影响: ✓ 无影响

- **[0a3e2dbc](https://github.com/vllm-project/vllm/commit/0a3e2dbc09c8a70dfd18f728bb829bf29ffa7da6)** 在 MoE 中跳过 DP padding tokens。新增 VLLM_MOE_SKIP_PADDING 环境变量（默认关闭），当启用时，在 modular_kernel._prepare 和 DeepSeek V4 的 forward 中，将 padding tokens 的 expert id 设为 -1，使其被 MoE 内核跳过。同时修改了 InputBatch 和 CUDA Graph 捕获逻辑，添加 is_padding 标记。这是一个性能优化，风险中等。
  - 标签: `performance`, `medium-risk`, `moe`
  - 变更文件:
  - 修改 `tests/models/test_deepseek_v4_mega_moe.py` (+80/-1)
  - 修改 `vllm/envs.py` (+6/-0)
  - 修改 `vllm/forward_context.py` (+9/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/modular_kernel.py` (+17/-0)
  - 修改 `vllm/models/deepseek_v4/nvidia/model.py` (+10/-0)
  - 修改 `vllm/models/deepseek_v4/nvidia/ops/prepare_megamoe.py` (+11/-0)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+4/-0)
  - 修改 `vllm/v1/worker/gpu/input_batch.py` (+7/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+10/-0)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[ed8e8b77](https://github.com/vllm-project/vllm-ascend/commit/ed8e8b77c00362ed55d40107e41cd7f224006b81)** 修复PP+MTP流水线中的气泡问题，并修复PD分离场景下PP的验证。在PD分离+PP+MTP场景中，通过跳过P节点的broadcast来避免同步并消除气泡。同时修复了MooncakeConnector中PP感知的handshake metadata设置，以及PP模式下transfer engine的设备名称设置。潜在风险：跳过broadcast可能影响PP其他rank的数据同步，需要验证在非PD分离场景下的行为是否正确。
  - 标签: `bugfix`, `medium-risk`, `distributed`, `model-runner`
  - 变更文件:
  - 修改 `vllm_ascend/distributed/kv_transfer/kv_p2p/mooncake_connector.py` (+14/-1)
  - 修改 `vllm_ascend/worker/model_runner_v1.py` (+4/-3)
  - Ascend 影响: ✓ 无影响

- **[edcae83d](https://github.com/vllm-project/vllm-ascend/commit/edcae83da32af8e1f1b7b97c7e19e8114e0535a5)** 将vllm-ascend的默认vLLM版本从v0.22.1升级到v0.23.0。主要变更包括：更新所有Dockerfile中的VLLM_TAG、恢复release-tag CI测试、添加v2 model runner兼容性处理(在v0.23.0上自动回退到v1)、更新文档和README。潜在风险：版本升级可能引入与v0.23.0 API不兼容的问题，虽然已通过补丁和回退机制处理，但仍需全面测试。v2 model runner在v0.23.0上不支持，相关测试已标记skip。
  - 标签: `chore`, `high-risk`, `ci`
  - 变更文件（共 23 个）:
  - 修改 `.github/vllm-release-tag.commit` (+1/-1)
  - 修改 `.github/workflows/pr_e2e_command.yml` (+1/-4)
  - 修改 `.github/workflows/pr_test.yaml` (+1/-4)
  - 修改 `.github/workflows/schedule_update_estimated_times.yaml` (+10/-14)
  - 修改 `.github/workflows/schedule_vllm_e2e_test.yaml` (+2/-8)
  - 修改 `Dockerfile` (+1/-1)
  - 修改 `Dockerfile.310p` (+1/-1)
  - 修改 `Dockerfile.310p.openEuler` (+1/-1)
  - 修改 `Dockerfile.a3` (+1/-1)
  - 修改 `Dockerfile.a3.openEuler` (+1/-1)
  - ... 及其他 13 个文件
  - Ascend 影响: ✓ 无影响

---
