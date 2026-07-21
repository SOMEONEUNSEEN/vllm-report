# MRV2 每日报告
生成时间: 2026-07-21 09:37:36
统计范围: 最近 7 天

**MRV2 定义**: `vllm/v1/worker/gpu/model_runner.py` 及其依赖的所有组件

MRV2 相关 commits 总数: 22

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
