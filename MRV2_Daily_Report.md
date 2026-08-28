# MRV2 每日报告
生成时间: 2026-08-28 09:01:17
统计范围: 最近 30 天

**MRV2 定义**: `vllm/v1/worker/gpu/model_runner.py` 及其依赖的所有组件

MRV2 相关 commits 总数: 123

## 2026-08-27
### vllm
- **[b3af042a](https://github.com/vllm-project/vllm/commit/b3af042abd8fe5a297ec3ec72db276fd661a67b3)** ([#53869](https://github.com/vllm-project/vllm/pull/53869)) [修复] PIECEWISE 捕获时使用 PCP slot mappings
  - 标签: `bugfix`, `high-risk`, `mrv2`, `model-runner`, `cudagraph`, `pcp`, `tests`
  - 变更文件:
  - 修改 `tests/evals/gsm8k/configs/GLM-5.2-NVFP4-TP1-PCP4-EP.yaml` (+1/-1)
  - 修改 `tests/evals/gsm8k/configs/GLM-5.2-NVFP4-TP2-PCP2-EP.yaml` (+1/-1)
  - 修改 `tests/v1/cudagraph/test_cudagraph_manager.py` (+53/-0)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+8/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+1/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改 vllm/v1/worker/gpu/model_runner.py 与 vllm/v1/worker/gpu/cudagraph_utils.py，均为 vllm-ascend 核心覆盖路径。vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，ModelAclGraphManager 继承 ModelCudaGraphManager。PCP slot mappings 在 PIECEWISE 捕获路径的使用需在 Ascend ACL graph 机制下验证正确性。
    - 建议测试区域: `Ascend PCP + PIECEWISE ACL graph 捕获 slot mappings 正确性`, `GLM-5.2 PCP 端到端验证`, `ModelAclGraphManager PIECEWISE 捕获路径回归`

- **[5acc1c4e](https://github.com/vllm-project/vllm/commit/5acc1c4e4b8730298cbff7a4a7c68c814dc24fd7)** ([#53694](https://github.com/vllm-project/vllm/pull/53694)) [Spec Decode] 在 EAGLE/MTP draft prefill 前跳过 DP 同步
  - 标签: `feature`, `high-risk`, `mrv2`, `spec-decode`, `model-runner`, `distributed`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_model_runner_v2_eplb.py` (+1/-1)
  - 修改 `vllm/v1/worker/gpu/dp_utils.py` (+106/-18)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+11/-3)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` (+15/-4)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+9/-4)
  - 修改 `vllm/v1/worker/gpu/spec_decode/extract_hidden_states.py` (+5/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/multi_module_mtp/speculator.py` (+7/-3)
  - 修改 `vllm/v1/worker/gpu/spec_decode/speculator.py` (+2/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改 vllm/v1/worker/gpu/model_runner.py（vllm-ascend NPUModelRunner 继承）与 vllm/v1/worker/gpu/spec_decode/ 目录（vllm-ascend 有 v2/spec_decode 覆盖）。draft prefill 跳过 DP sync 的逻辑会传递到 Ascend 子类，需验证 Ascend HCCL 在跳过同步时的通信正确性，以及 Ascend spec decode 的 draft/verify 一致性。
    - 建议测试区域: `Ascend spec decode draft prefill 跳过 DP sync 正确性`, `多卡 DP 场景 draft/verify 一致性`, `vllm_ascend/worker/v2/spec_decode/autoregressive speculator 兼容性`

- **[94d96e24](https://github.com/vllm-project/vllm/commit/94d96e2446d68a949541f2a458a748e08ccbe717)** ([#53955](https://github.com/vllm-project/vllm/pull/53955)) [修复] 在 KV cache 分配前释放 CUDA graph profiling 显存
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `cudagraph`, `tests`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_model_runner_v2_cudagraph_profiling.py` (+67/-0)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+8/-4)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改 vllm/v1/worker/gpu/cudagraph_utils.py，vllm-ascend 的 ModelAclGraphManager 继承自 ModelCudaGraphManager。profiling 显存释放逻辑需在 Ascend ACL graph 机制下验证，避免 Ascend NPU 显存（HBM）在 profiling 后未及时释放影响 KV cache 分配。

### vllm-ascend
- **[72059e41](https://github.com/vllm-project/vllm-ascend/commit/72059e41b239e2ea469a0fb2d9eb0cb7ee4e3085)** ([#14878](https://github.com/vllm-project/vllm-ascend/pull/14878)) [Feature] 重新合入基础 MLA prefill context parallelism
  - 标签: `feature`, `high-risk`, `mrv2`, `mla`, `attention`, `pcp`, `tests`
  - 变更文件:
  - 修改 `tests/ut/attention/a2/test_mla_v1.py` (+147/-4)
  - 修改 `tests/ut/worker/test_attn_utils_v2.py` (+36/-0)
  - 修改 `vllm_ascend/attention/mla_v1.py` (+197/-8)
  - Ascend 影响: ✓ 无影响

- **[bed43af3](https://github.com/vllm-project/vllm-ascend/commit/bed43af3334e8c942bd2928532ccd87742cab74c)** ([#14668](https://github.com/vllm-project/vllm-ascend/pull/14668)) [Feature] 在 model runner v2 sample 路径支持 lmhead TP
  - 标签: `feature`, `high-risk`, `mrv2`, `distributed`, `model-runner`, `tests`
  - 变更文件:
  - 新增 `tests/ut/worker/test_model_runner_v2_finegrained_tp.py` (+238/-0)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+102/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-26
### vllm
- **[080a66a6](https://github.com/vllm-project/vllm/commit/080a66a69c6fd1fe464756f88ab958baad66ce69)** ([#53818](https://github.com/vllm-project/vllm/pull/53818)) [Bugfix][ROCm] 在当前 stream 上捕获 CUDA Graph
  - 标签: `bugfix`, `mrv2`, `high-risk`, `cuda-graph`, `model-runner`, `spec-decode`, `rocm`, `cudagraph-utils`
  - 变更文件:
  - 修改 `vllm/v1/spec_decode/gemma4.py` (+2/-1)
  - 修改 `vllm/v1/worker/encoder_cudagraph.py` (+5/-1)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+4/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改了 MRV2 核心文件 vllm/v1/worker/gpu/cudagraph_utils.py，vllm-ascend 的 ModelAclGraphManager 继承自 vllm 的 ModelCudaGraphManager，graph 捕获的 stream 选择逻辑会传递到 Ascend 子类。需评估 Ascend ACL Graph 捕获是否同样需要在当前 stream 上进行
    - 建议测试区域: `ModelAclGraphManager graph 捕获 stream 兼容性`, `ACL Graph 与 offloader copy stream 同步`

- **[b1fbbc2a](https://github.com/vllm-project/vllm/commit/b1fbbc2ade51e3826bc92e4733c9c692ee21d42d)** ([#53515](https://github.com/vllm-project/vllm/pull/53515)) BugFix(PCP): 为 PIECEWISE CUDA graphs 使用持久化输入缓冲区
  - 标签: `bugfix`, `mrv2`, `high-risk`, `cuda-graph`, `model-runner`, `pcp`, `tests`
  - 变更文件:
  - 新增 `tests/v1/worker/test_gpu_pcp_manager.py` (+109/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+15/-3)
  - 修改 `vllm/v1/worker/gpu/pcp_manager.py` (+71/-22)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改了 MRV2 核心文件 vllm/v1/worker/gpu/model_runner.py（vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner）与 pcp_manager.py。PCP 输入缓冲区持久化逻辑会传递到 Ascend 子类，需评估 vllm-ascend 在 PCP+ACL Graph 场景下的缓冲区管理
    - 建议测试区域: `vllm-ascend PCP 缓冲区持久化`, `NPUModelRunner PCP+ACL Graph 捕获`

- **[a447955a](https://github.com/vllm-project/vllm/commit/a447955acad919a6902d65f0af2d4f76c0335ed3)** ([#53773](https://github.com/vllm-project/vllm/pull/53773)) [Kimi Bug] 修复 k3 torch.AcceleratorError: 遇到 CUDA 非法显存访问
  - 标签: `bugfix`, `mrv2`, `high-risk`, `cuda-graph`, `model-runner`, `cudagraph-utils`, `kimi`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+2/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改了 MRV2 核心文件 vllm/v1/worker/gpu/cudagraph_utils.py，vllm-ascend 的 ModelAclGraphManager 继承该路径。需评估该防护逻辑在 Ascend ACL Graph 下是否同样适用
    - 建议测试区域: `vllm-ascend ACL Graph 非法显存访问防护`

### vllm-ascend
- **[f9945a89](https://github.com/vllm-project/vllm-ascend/commit/f9945a892774f475ff4827cf6713b6f3f9fda6a6)** ([#14801](https://github.com/vllm-project/vllm-ascend/pull/14801)) [BugFix][SpecDecode] 为 full graph 填充 draft 序列长度
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `acl-graph`, `model-runner`, `worker-v2`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+13/-6)
  - Ascend 影响: ✓ 无影响

- **[1d9cf248](https://github.com/vllm-project/vllm-ascend/commit/1d9cf2485de31b219a0770476ca3f7d5b2493793)** ([#14890](https://github.com/vllm-project/vllm-ascend/pull/14890)) [CI][BugFix] 降低 dspark 验收阈值
  - 标签: `chore`, `mrv2`, `low-risk`, `ci`, `tests`, `spec-decode`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/model_runner_v2/test_deepseek_v4.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

- **[ce8f64e5](https://github.com/vllm-project/vllm-ascend/commit/ce8f64e5617bbeb315e7b736fa8199a36457f5ae)** ([#15007](https://github.com/vllm-project/vllm-ascend/pull/15007)) [CI] 暂时跳过 DeepSeek V4 MTP eager 测试
  - 标签: `chore`, `mrv2`, `low-risk`, `ci`, `tests`, `spec-decode`, `mtp`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/model_runner_v2/test_deepseek_v4.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

- **[59a36f29](https://github.com/vllm-project/vllm-ascend/commit/59a36f29392eb6ad7bf9068933b997dd33761d46)** ([#14761](https://github.com/vllm-project/vllm-ascend/pull/14761)) [Feature][310P] 为 310P 适配 MRV2
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `worker-v2`, `hardware`, `310p`, `acl-graph`
  - 变更文件（共 15 个）:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+1/-0)
  - 新增 `tests/e2e/pull_request/four_card/_310p/test_model_runner_v2_310p.py` (+44/-0)
  - 新增 `tests/ut/_310p/test_model_runner_v2_310p.py` (+328/-0)
  - 修改 `vllm_ascend/_310p/attention/metadata_builder.py` (+12/-4)
  - 新增 `vllm_ascend/_310p/worker/__init__.py` (+3/-0)
  - 新增 `vllm_ascend/_310p/worker/v2/__init__.py` (+3/-0)
  - 新增 `vllm_ascend/_310p/worker/v2/block_table.py` (+169/-0)
  - 新增 `vllm_ascend/_310p/worker/v2/model_runner.py` (+668/-0)
  - 新增 `vllm_ascend/_310p/worker/v2/model_state.py` (+89/-0)
  - 新增 `vllm_ascend/_310p/worker/v2/sampler.py` (+66/-0)
  - ... 及其他 5 个文件
  - Ascend 影响: ✓ 无影响

- **[895d4755](https://github.com/vllm-project/vllm-ascend/commit/895d4755f8af0821d5ccb0c7272964d68bb71724)** ([#14791](https://github.com/vllm-project/vllm-ascend/pull/14791)) [BugFix] 从 draft prefill 元数据中过滤 target-only 注意力层
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `attention`, `worker-v2`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+27/-0)
  - Ascend 影响: ✓ 无影响

- **[e5365a66](https://github.com/vllm-project/vllm-ascend/commit/e5365a66d263bbf590b6d0cb23007a0c3b0d4eeb)** ([#14862](https://github.com/vllm-project/vllm-ascend/pull/14862)) [Feature][Bugfix] 新增 triton 算子补丁以规避上游失败
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `triton`, `ops`, `worker-v2`, `patch`
  - 变更文件:
  - 新增 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_num_nans.py` (+176/-0)
  - 新增 `vllm_ascend/ops/triton/v2/metrics/__init__.py` (+0/-0)
  - 新增 `vllm_ascend/ops/triton/v2/metrics/docs/num_nans.md` (+115/-0)
  - 新增 `vllm_ascend/ops/triton/v2/metrics/num_nans.py` (+39/-0)
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_triton.py` (+6/-3)
  - Ascend 影响: ✓ 无影响

- **[ff998aad](https://github.com/vllm-project/vllm-ascend/commit/ff998aad1434142a36a3176d3180b477a4f8d26b)** ([#14893](https://github.com/vllm-project/vllm-ascend/pull/14893)) [Test] 移除过时的 MRV2 slot-mapping 测试
  - 标签: `chore`, `mrv2`, `low-risk`, `tests`, `triton`
  - 变更文件:
  - 删除 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_compute_slot_mapping.py` (+0/-109)
  - Ascend 影响: ✓ 无影响

- **[2452b1fd](https://github.com/vllm-project/vllm-ascend/commit/2452b1fd06a348b11ad4e03548049f97c9caeb0d)** ([#14571](https://github.com/vllm-project/vllm-ascend/pull/14571)) [Doc] 新增 prefill 上下文并行指南
  - 标签: `docs`, `mrv2`, `low-risk`, `pcp`, `context-parallel`
  - 变更文件:
  - 修改 `docs/source/user_guide/feature_guide/context_parallel.md` (+62/-23)
  - Ascend 影响: ✓ 无影响

- **[aeb8e76d](https://github.com/vllm-project/vllm-ascend/commit/aeb8e76d35158ceab5fa4d0b8c6670f0928b6b3f)** ([#14649](https://github.com/vllm-project/vllm-ascend/pull/14649)) [BugFix][Mamba] 修复分阶段写 kernel 与重复的 is_prefilling 参数
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `mamba`, `attention`, `triton`, `worker-v2`
  - 变更文件:
  - 修改 `tests/ut/patch/worker/test_patch_mamba_utils_source.py` (+2/-2)
  - 新增 `vllm_ascend/ops/triton/mamba/precopy.py` (+226/-0)
  - 修改 `vllm_ascend/patch/worker/patch_mamba_utils.py` (+4/-1)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+5/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-25
### vllm
- **[41729fc5](https://github.com/vllm-project/vllm/commit/41729fc53b02cb09beda2a1ced690d021443be43)** ([#52388](https://github.com/vllm-project/vllm/pull/52388)) [K3 性能] 优化 K3 mamba 元数据准备，内核性能提升 6.6~7.6 倍
  - 标签: `performance`, `medium-risk`, `mrv2`, `mamba`, `kimi-k3`, `triton`
  - 变更文件:
  - 修改 `tests/models/kimi_k3/test_kda_metadata.py` (+37/-0)
  - 修改 `vllm/models/kimi_k3/nvidia/kda_metadata.py` (+18/-6)
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+18/-0)
  - 修改 `vllm/v1/worker/mamba_utils.py` (+114/-0)
  - Ascend 影响: ✓ 无影响

- **[d5cadcee](https://github.com/vllm-project/vllm/commit/d5cadcee8641a9fcec15facb5a9157d157daa207)** ([#52242](https://github.com/vllm-project/vllm/pull/52242)) [Feature][DSpark] Logprobs 自适应验证
  - 标签: `feature`, `medium-risk`, `mrv2`, `spec-decode`, `dspark`, `logprobs`
  - 变更文件:
  - 修改 `docs/features/speculative_decoding/adaptive_verification.md` (+1/-1)
  - 修改 `tests/v1/engine/test_output_processor.py` (+1/-1)
  - 修改 `tests/v1/test_outputs.py` (+19/-0)
  - 修改 `tests/v1/worker/test_gpu_rejection_sampler_chunking.py` (+1/-0)
  - 修改 `vllm/sampling_params.py` (+0/-14)
  - 修改 `vllm/v1/engine/logprobs.py` (+1/-1)
  - 修改 `vllm/v1/outputs.py` (+21/-4)
  - 修改 `vllm/v1/worker/gpu/sample/logprob.py` (+4/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler.py` (+12/-1)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 可能影响 - vllm-ascend 的 DSpark 推测解码（vllm_ascend/spec_decode/dspark_proposer.py）复用 vllm 的 rejection_sampler 与 outputs/logprobs 路径；adaptive verification 改变了验证采样行为，ascend dspark 需同步采样参数与输出字段。
    - 建议测试区域: `vllm_ascend/spec_decode/dspark_proposer.py`, `vllm_ascend/spec_decode/llm_base_proposer.py`, `Ascend spec decode rejection sampling 输出`

- **[c74dd2d2](https://github.com/vllm-project/vllm/commit/c74dd2d208389305e3a6ced992ee0632f939c0a0)** ([#53407](https://github.com/vllm-project/vllm/pull/53407)) [Bugfix] 将 uniform decode 派发到 padding 后的 FULL cudagraph
  - 标签: `bugfix`, `high-risk`, `mrv2`, `cuda-graph`, `cudagraph-utils`
  - 变更文件:
  - 修改 `tests/v1/cudagraph/test_cudagraph_manager.py` (+230/-0)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+17/-24)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 高度相关 - vllm-ascend 的 ModelAclGraphManager 继承自 vllm 的 CudaGraphManager 并覆盖关键方法；cudagraph_utils.py 是 MRV2 cudagraph 核心派发逻辑，uniform decode 派发到 padded FULL graph 的改动需验证 ACL graph 兼容性，Ascend 的 ACL graph 与 Cuda graph 机制差异可能导致派发行为不同。
    - 建议测试区域: `vllm_ascend/worker/v2/ ACL graph manager`, `Ascend cudagraph_utils 覆盖实现`, `MRV2 uniform decode + FULL graph 端到端`

- **[7ca33692](https://github.com/vllm-project/vllm/commit/7ca336929c169fee1210dd5293029d78811fba27)** ([#53608](https://github.com/vllm-project/vllm/pull/53608)) [Model] 移除十个已废弃模型架构
  - 标签: `refactor`, `medium-risk`, `mrv2`, `model`, `cleanup`
  - 变更文件（共 46 个）:
  - 修改 `docs/contributing/model/multimodal.md` (+0/-1)
  - 修改 `docs/models/pooling_models/embed.md` (+0/-1)
  - 修改 `docs/models/supported_models.md` (+0/-10)
  - 修改 `examples/generate/multimodal/audio_language_offline.py` (+0/-21)
  - 修改 `examples/generate/multimodal/encoder_decoder_multimodal_offline.py` (+0/-43)
  - 修改 `examples/generate/multimodal/vision_language_multi_image_offline.py` (+0/-48)
  - 修改 `examples/generate/multimodal/vision_language_offline.py` (+0/-151)
  - 删除 `examples/speech_to_text/lid/openai_lid_client.py` (+0/-193)
  - 修改 `requirements/test/nightly-torch.txt` (+1/-1)
  - 修改 `tests/config/base_model_arch_groundtruth.json` (+0/-17)
  - ... 及其他 36 个文件
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[37e38249](https://github.com/vllm-project/vllm-ascend/commit/37e382498c81fdbcfce8529ea1d53570e0d239a5)** ([#14853](https://github.com/vllm-project/vllm-ascend/pull/14853)) Revert "[Feature] 支持基础 MLA prefill 上下文并行"
  - 标签: `revert`, `medium-risk`, `mrv2`, `mla`, `attention`, `context-parallel`, `v2`
  - 变更文件:
  - 修改 `tests/ut/attention/a2/test_mla_v1.py` (+4/-147)
  - 修改 `tests/ut/worker/test_attn_utils_v2.py` (+0/-36)
  - 修改 `vllm_ascend/attention/mla_v1.py` (+8/-192)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+0/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-24
### vllm
- **[f620499e](https://github.com/vllm-project/vllm/commit/f620499ee3fe18131d71b02e1e8e5f1cf984cf1c)** ([#53336](https://github.com/vllm-project/vllm/pull/53336)) [Bugfix][Spec Decode] 为 FlashAttention 元数据重新应用 group geometry
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `spec-decode`, `attention`, `flash-attn`
  - 变更文件:
  - 修改 `tests/v1/attention/test_group_head_counts.py` (+53/-6)
  - 修改 `vllm/v1/attention/backends/flash_attn.py` (+6/-5)
  - 修改 `vllm/v1/attention/backends/utils.py` (+5/-1)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+6/-6)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 可能影响 - 该 commit 修改了 vllm/v1/worker/gpu/spec_decode/dflash/speculator.py（MRV2 spec_decode 核心路径），vllm-ascend 有自己的 spec_decode 实现（vllm_ascend/spec_decode/、vllm_ascend/worker/v2/spec_decode/），group geometry 元数据处理逻辑需验证 Ascend speculator 是否需要同步修复。vllm/v1/attention/backends/flash_attn.py 为平台特定（Ascend 不使用 flash_attn backend），但 utils.py 的改动可能被 Ascend attention backend 复用。
    - 建议测试区域: `vllm_ascend/worker/v2/spec_decode/`, `vllm_ascend/spec_decode/`, `Ascend attention backend group head counts 处理`

- **[79bb395e](https://github.com/vllm-project/vllm/commit/79bb395eea64dbfef99a55f010d2854db71f8571)** ([#53464](https://github.com/vllm-project/vllm/pull/53464)) [Pooling] 提升 BGE-M3 同步 pooling 吞吐量最高 3.13%
  - 标签: `performance`, `medium-risk`, `mrv2`, `pooling`, `model-runner`, `pool`
  - 变更文件:
  - 修改 `tests/model_executor/layers/test_pooler_methods.py` (+36/-0)
  - 修改 `tests/models/language/pooling/test_splade_sparse_pooler.py` (+3/-6)
  - 修改 `tests/v1/worker/test_gpu_input_batch.py` (+5/-11)
  - 修改 `vllm/model_executor/layers/pooler/common.py` (+1/-1)
  - 修改 `vllm/model_executor/layers/pooler/tokwise/methods.py` (+1/-1)
  - 修改 `vllm/model_executor/models/jina.py` (+25/-20)
  - 修改 `vllm/v1/pool/metadata.py` (+23/-5)
  - 修改 `vllm/v1/worker/gpu/pool/pooling_runner.py` (+8/-13)
  - 修改 `vllm/v1/worker/gpu_input_batch.py` (+4/-6)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-4)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 可能影响 - 该 commit 修改了 vllm/v1/worker/gpu_model_runner.py（MRV2 核心路径，vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner），pooling_runner 和 gpu_input_batch 的改动可能影响 Ascend 上的 pooling 行为。vllm-ascend 有自己的 pooling_runner 实现，但 metadata 和 input_batch 变更可能传递。
    - 建议测试区域: `vllm_ascend/worker/v2/model_runner.py`, `vllm_ascend/worker/v2/ 下 pooling 相关路径`, `Ascend pooling metadata 处理`

- **[0ecc2847](https://github.com/vllm-project/vllm/commit/0ecc284790e5403f74b899524ef82ecb69f83cb3)** ([#51031](https://github.com/vllm-project/vllm/pull/51031)) [Bugfix][Kernel] 处理 V2 DCP slot mapping 中的内核块大小
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `dcp`, `block-table`, `kv-cache`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_block_table.py` (+44/-0)
  - 修改 `vllm/v1/worker/gpu/block_table.py` (+29/-15)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm/v1/worker/gpu/block_table.py（vllm-ascend 覆盖路径之一），vllm-ascend 通过 block_table_patch 打补丁。DCP slot mapping 中 kernel block sizes 的处理需要 vllm-ascend 验证其 block table 补丁是否兼容。
    - 建议测试区域: `vllm_ascend/worker/v2/ 下 block_table 相关路径`, `vllm_ascend patch block_table`, `Ascend DCP slot mapping`

- **[a4d70bef](https://github.com/vllm-project/vllm/commit/a4d70bef3724edb068c8206804154065acaa4cd4)** ([#53306](https://github.com/vllm-project/vllm/pull/53306)) [Model Runner V2] 预留 CUDA graph 内存
  - 标签: `feature`, `high-risk`, `mrv2`, `model-runner`, `cuda-graph`, `cudagraph-utils`, `mamba`
  - 变更文件（共 13 个）:
  - 修改 `tests/test_config.py` (+35/-0)
  - 修改 `tests/v1/sample/test_logprobs.py` (+4/-3)
  - 新增 `tests/v1/worker/test_gpu_model_runner_v2_cudagraph_profiling.py` (+286/-0)
  - 修改 `vllm/model_executor/layers/mamba/gdn/kimi_gdn_linear_attn.py` (+4/-1)
  - 修改 `vllm/model_executor/layers/mamba/gdn/olmo_gdn_linear_attn.py` (+4/-1)
  - 修改 `vllm/model_executor/layers/mamba/gdn/qwen_gdn_linear_attn.py` (+16/-12)
  - 修改 `vllm/model_executor/layers/mamba/linear/bailing_linear_attn.py` (+2/-1)
  - 修改 `vllm/model_executor/layers/mamba/linear/minimax_linear_attn.py` (+2/-1)
  - 修改 `vllm/model_executor/layers/mamba/mamba_mixer.py` (+2/-1)
  - 修改 `vllm/model_executor/layers/mamba/mamba_mixer2.py` (+2/-1)
  - ... 及其他 3 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 大幅修改了 vllm/v1/worker/gpu/cudagraph_utils.py 和 vllm/v1/worker/gpu/model_runner.py（均为 vllm-ascend 覆盖路径）。vllm-ascend 的 ModelAclGraphManager 继承自 vllm 的 ModelCudaGraphManager，CUDA graph 内存预留逻辑（reserve memory）需要 ACL graph 机制验证兼容性。mamba 层接口变更也可能影响 Ascend 上的 mamba 模型。这是 Dynamic SD + Full Cuda Graph 组合的关键变更，需重点验证与 Ascend ACL graph 的兼容性。
    - 建议测试区域: `vllm_ascend/worker/v2/aclgraph_utils.py`, `vllm_ascend/worker/v2/model_runner.py`, `vllm_ascend/compilation/ 下 ACL graph 相关`, `Ascend mamba 层接口适配`

### vllm-ascend
- **[bf89d2c4](https://github.com/vllm-project/vllm-ascend/commit/bf89d2c46ec12be04fdd09d2aba4c71c9b3a4921)** ([#14286](https://github.com/vllm-project/vllm-ascend/pull/14286)) 在 model runner v2 中支持 profiling chunk
  - 标签: `feature`, `high-risk`, `mrv2`, `model-runner`, `profiling`, `worker`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/test_profiling_chunk_performance.py` (+6/-1)
  - 修改 `tests/ut/worker/a2/test_worker_v2.py` (+116/-0)
  - 新增 `tests/ut/worker/test_model_runner_v2.py` (+78/-0)
  - 修改 `vllm_ascend/core/profiling_chunk_predictor.py` (+44/-0)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+26/-8)
  - 修改 `vllm_ascend/worker/worker.py` (+33/-11)
  - Ascend 影响: ✓ 无影响

- **[581051a8](https://github.com/vllm-project/vllm-ascend/commit/581051a80a3568fd4487484bfb7b13a4a9d2abf5)** ([#14008](https://github.com/vllm-project/vllm-ascend/pull/14008)) [Feature] 支持基础 MLA prefill context parallelism
  - 标签: `feature`, `high-risk`, `mrv2`, `mla`, `attention`, `context-parallel`, `pcp`, `attn-utils`
  - 变更文件:
  - 修改 `tests/ut/attention/a2/test_mla_v1.py` (+147/-4)
  - 修改 `tests/ut/worker/test_attn_utils_v2.py` (+36/-0)
  - 修改 `vllm_ascend/attention/mla_v1.py` (+192/-8)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

- **[64958294](https://github.com/vllm-project/vllm-ascend/commit/649582947376908c69e4759c79fadd62ce898ac5)** ([#14746](https://github.com/vllm-project/vllm-ascend/pull/14746)) [Ci] main2main vllm 0821 同步
  - 标签: `chore`, `medium-risk`, `ci`, `spec-decode`, `attention`, `acl-graph`, `deepseek-mtp`, `mrv2`
  - 变更文件:
  - 修改 `.github/vllm-main-verified.commit` (+1/-1)
  - 修改 `tests/e2e/conftest.py` (+9/-1)
  - 修改 `tests/ut/core/test_profiling_chunk.py` (+6/-0)
  - 修改 `tests/ut/core/test_recompute_scheduler.py` (+4/-0)
  - 修改 `tests/ut/patch/platform/test_patch_structured_output.py` (+7/-4)
  - 修改 `vllm_ascend/attention/attention_v1.py` (+6/-2)
  - 修改 `vllm_ascend/compilation/acl_graph.py` (+27/-10)
  - 修改 `vllm_ascend/models/deepseek_mtp.py` (+7/-3)
  - 修改 `vllm_ascend/spec_decode/llm_base_proposer.py` (+11/-2)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dflash/speculator.py` (+300/-144)
  - Ascend 影响: ✓ 无影响

- **[6958febe](https://github.com/vllm-project/vllm-ascend/commit/6958febef951f663fc54bc51403ffb9638d5a1fe)** ([#14533](https://github.com/vllm-project/vllm-ascend/pull/14533)) [Feature] 为 MRV1 添加 DFlash2 推测解码
  - 标签: `feature`, `high-risk`, `spec-decode`, `dflash2`, `model-runner-v1`, `qwen3`
  - 变更文件:
  - 修改 `.github/workflows/misc/model_dataset_list.json` (+2/-0)
  - 修改 `.github/workflows/scripts/test_config.yaml` (+10/-0)
  - 修改 `tests/e2e/pull_request/two_card/spec_decode/test_spec_decode.py` (+91/-0)
  - 新增 `tests/ut/spec_decode/test_dflash2_proposer.py` (+227/-0)
  - 修改 `vllm_ascend/models/__init__.py` (+4/-0)
  - 新增 `vllm_ascend/models/qwen3_dflash2.py` (+309/-0)
  - 修改 `vllm_ascend/ops/triton/spec_decode/utils.py` (+36/-0)
  - 修改 `vllm_ascend/spec_decode/__init__.py` (+3/-0)
  - 新增 `vllm_ascend/spec_decode/dflash2_proposer.py` (+100/-0)
  - 修改 `vllm_ascend/spec_decode/llm_base_proposer.py` (+11/-1)
  - Ascend 影响: ✓ 无影响

- **[4c9cdea5](https://github.com/vllm-project/vllm-ascend/commit/4c9cdea56d349542775e677669b0702680887195)** ([#14493](https://github.com/vllm-project/vllm-ascend/pull/14493)) [BugFix] 修复 Graph input_batch 并移除冗余 attention buffers
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `input-batch`, `attention`, `sfa`, `acl-graph`
  - 变更文件:
  - 修改 `tests/ut/attention/a2/test_sfa_v1.py` (+0/-17)
  - 修改 `vllm_ascend/attention/sfa_v1.py` (+3/-32)
  - 修改 `vllm_ascend/worker/v2/input_batch.py` (+5/-3)
  - Ascend 影响: ✓ 无影响

- **[bb570591](https://github.com/vllm-project/vllm-ascend/commit/bb570591f0a95c186318ef044beb4efbf51a2653)** ([#14640](https://github.com/vllm-project/vllm-ascend/pull/14640)) [Bugfix] 修复 triton 算子 fill_logprob_token_idx 内部错误
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `triton`, `ops`, `sample`
  - 变更文件:
  - 新增 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_fill_logprob_token_ids_kernel.py` (+194/-0)
  - 新增 `vllm_ascend/ops/triton/v2/sample/docs/fill_logprob_token_ids.md` (+181/-0)
  - 新增 `vllm_ascend/ops/triton/v2/sample/fill_logprob_token_idx.py` (+54/-0)
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_triton.py` (+5/-0)
  - Ascend 影响: ✓ 无影响

- **[d0de46c7](https://github.com/vllm-project/vllm-ascend/commit/d0de46c794a301566288d8d70de7589505bcc8f8)** ([#14184](https://github.com/vllm-project/vllm-ascend/pull/14184)) [Feature] 在 MRV2 中支持 MTP 与流水线并行
  - 标签: `feature`, `high-risk`, `mrv2`, `mtp`, `spec-decode`, `pipeline-parallel`, `model-runner`
  - 变更文件:
  - 修改 `vllm_ascend/patch/__init__.py` (+16/-0)
  - 新增 `vllm_ascend/patch/worker/patch_v2/patch_spec_pp.py` (+93/-0)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+20/-1)
  - Ascend 影响: ✓ 无影响

- **[9794b38f](https://github.com/vllm-project/vllm-ascend/commit/9794b38fa7f5938165fbd96d2299e83326c5b077)** ([#14522](https://github.com/vllm-project/vllm-ascend/pull/14522)) [CI] 添加 DeepSeek V4 MTP 接受率 golden 基准
  - 标签: `ci`, `test`, `low-risk`, `deepseek-v4`, `mtp`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/model_runner_v2/test_deepseek_v4.py` (+25/-12)
  - Ascend 影响: ✓ 无影响

- **[bb4d264f](https://github.com/vllm-project/vllm-ascend/commit/bb4d264f8eeb8eff9073c2619153cbad4fe18b52)** ([#14310](https://github.com/vllm-project/vllm-ascend/pull/14310)) [Feature] 在 FullGraph 模式下支持 MTP 与 SFA
  - 标签: `feature`, `high-risk`, `mrv2`, `mtp`, `sfa`, `acl-graph`, `spec-decode`, `deepseek-mtp`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/eight_card/model_runner_v2/test_glm5_2.py` (+3/-3)
  - 修改 `tests/ut/spec_decode/test_eagle_aclgraph_source_regression.py` (+3/-3)
  - 修改 `vllm_ascend/models/deepseek_mtp.py` (+19/-1)
  - 修改 `vllm_ascend/patch/__init__.py` (+5/-7)
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_eagle_speculator.py` (+2/-2)
  - 修改 `vllm_ascend/worker/v2/README.md` (+2/-2)
  - 修改 `vllm_ascend/worker/v2/aclgraph_utils.py` (+6/-0)
  - 重命名 `vllm_ascend/worker/v2/spec_decode/autoregressive/aclgraph.py` (+42/-29)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+20/-26)
  - Ascend 影响: ✓ 无影响

- **[9a0cdb27](https://github.com/vllm-project/vllm-ascend/commit/9a0cdb27a656520048675ea24a30b83c716a93e3)** ([#14037](https://github.com/vllm-project/vllm-ascend/pull/14037)) [Feature] 支持 DSA prefill context parallelism
  - 标签: `feature`, `high-risk`, `mrv2`, `dsa`, `attention`, `context-parallel`, `pcp`, `deepseek-v4`, `attn-utils`, `model-states`
  - 变更文件（共 11 个）:
  - 修改 `tests/ut/attention/test_dsa_v1.py` (+350/-19)
  - 修改 `tests/ut/models/test_deepseek_v4_indexer.py` (+128/-1)
  - 修改 `tests/ut/worker/test_pcp_manager_v2.py` (+41/-0)
  - 修改 `vllm_ascend/attention/context_parallel/dsa_cp.py` (+391/-2)
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+109/-43)
  - 修改 `vllm_ascend/models/deepseek_v4/indexer.py` (+69/-14)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+14/-2)
  - 修改 `vllm_ascend/worker/v2/input_batch.py` (+3/-0)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+1/-1)
  - 修改 `vllm_ascend/worker/v2/model_states/default.py` (+16/-1)
  - ... 及其他 1 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-08-23
### vllm
- **[2f55ef25](https://github.com/vllm-project/vllm/commit/2f55ef254c70e110d637beeedf48238977ebb683)** [Model] Add Qwen3-Omni DSpark support (#52560)
  - 变更文件（共 11 个）:
  - 修改 `tests/model_executor/test_qwen3_omni.py` (+171/-1)
  - 修改 `tests/models/registry.py` (+7/-0)
  - 修改 `tests/test_config.py` (+121/-0)
  - 新增 `tests/transformers_utils/test_speculators_dspark_config.py` (+58/-0)
  - 修改 `vllm/config/speculative.py` (+302/-2)
  - 修改 `vllm/model_executor/models/qwen3_dflash.py` (+8/-8)
  - 修改 `vllm/model_executor/models/qwen3_dspark.py` (+20/-2)
  - 修改 `vllm/model_executor/models/qwen3_omni_moe_thinker.py` (+11/-1)
  - 修改 `vllm/model_executor/models/registry.py` (+1/-0)
  - 修改 `vllm/transformers_utils/configs/speculators/algos.py` (+17/-4)
  - ... 及其他 1 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-08-22
### vllm
- **[da329cc3](https://github.com/vllm-project/vllm/commit/da329cc303a5233e17fa3d553ce0a3d6ceea87a8)** ([#50272](https://github.com/vllm-project/vllm/pull/50272)) [Bugfix] 修复 short_conv (LFM2) 模型的推测解码问题
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `mamba`, `model-runner`
  - 变更文件:
  - 修改 `vllm/model_executor/layers/mamba/mamba_utils.py` (+2/-1)
  - 修改 `vllm/model_executor/layers/mamba/short_conv.py` (+33/-9)
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+6/-1)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+2/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm-ascend 在 vllm_ascend/worker/v2/model_states/mamba_hybrid.py 有自己的 mamba_hybrid 实现，且 MRV1 通过 NPUModelRunner 继承 gpu_model_runner.py。推测解码与 mamba hybrid 状态衔接的修复需在 Ascend 上验证一致性。
    - 建议测试区域: `Ascend mamba hybrid + 推测解码`, `vllm_ascend/worker/v2/model_states/mamba_hybrid.py 状态时序`

- **[7ca49fbe](https://github.com/vllm-project/vllm/commit/7ca49fbe4bab019e55d57cdc4b7fd3d55c67c1a6)** ([#53176](https://github.com/vllm-project/vllm/pull/53176)) [重构][多模态] 将 encoder-only 路径从共享 runner 中抽出
  - 标签: `refactor`, `mrv2`, `medium-risk`, `model-runner`, `multimodal`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_warmup_blocks.py` (+3/-2)
  - 修改 `vllm/config/vllm.py` (+11/-1)
  - 修改 `vllm/v1/core/sched/scheduler.py` (+2/-2)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+3/-33)
  - 修改 `vllm/v1/worker/gpu/warmup.py` (+1/-1)
  - 修改 `vllm/v1/worker/gpu_worker.py` (+8/-3)
  - 新增 `vllm/v1/worker/mm_encoder_model_runner.py` (+141/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改 vllm/v1/worker/gpu/model_runner.py（vllm-ascend MRV2 NPUModelRunner 继承）与 gpu_worker.py 装配路径。encoder-only runner 抽出后，vllm-ascend MRV2 需确认 NPUModelRunner 与新 mm_encoder_model_runner 的衔接是否需要适配。
    - 建议测试区域: `vllm-ascend MRV2 NPUModelRunner 与 mm_encoder_model_runner 衔接`, `多模态 warmup 回归`

- **[8bdc70ec](https://github.com/vllm-project/vllm/commit/8bdc70ec7b379279ec0152343239c2d50aced687)** ([#51718](https://github.com/vllm-project/vllm/pull/51718)) [6/N][KV-Cache 布局重构] 标准化 KV cache 布局
  - 标签: `refactor`, `mrv2`, `high-risk`, `kv-cache`, `attention`, `model-runner`, `distributed`, `kv-connector`
  - 变更文件（共 150 个）:
  - 修改 `.buildkite/test_areas/disaggregated.yaml` (+3/-0)
  - 修改 `benchmarks/attention_benchmarks/runner.py` (+47/-48)
  - 修改 `docs/assets/contributing/dockerfile-stages-dependency.png` (+0/-0)
  - 修改 `docs/features/mooncake_store_connector_usage.md` (+0/-1)
  - 修改 `docs/features/nixl_connector_compatibility.md` (+4/-4)
  - 修改 `docs/features/nixl_connector_usage.md` (+1/-9)
  - 修改 `rust/Cargo.lock` (+9/-9)
  - 修改 `tests/compile/passes/test_fusion_attn.py` (+32/-24)
  - 修改 `tests/compile/passes/test_mla_attn_quant_fusion.py` (+6/-19)
  - 修改 `tests/compile/passes/test_mla_rope_kvcache_cat_fusion.py` (+4/-19)
  - ... 及其他 140 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的多个核心覆盖路径：(1) vllm/v1/worker/gpu/model_runner.py - vllm-ascend MRV2 NPUModelRunner 继承，KV cache 布局协商需适配；(2) vllm/v1/worker/gpu/attn_utils.py - vllm-ascend 有自己的 attn_utils 实现，需适配统一布局；(3) vllm/v1/worker/gpu/spec_decode/dflash/speculator.py - vllm-ascend 有对应 dflash speculator，attn_vllm_config/布局变更需同步；(4) vllm/v1/attention/backend.py 与 selector.py - vllm-ascend 有自己的 attention backend，supports/get_supported_kv_cache_layouts 接口需实现；(5) vllm/v1/kv_cache_interface.py 与新增 kv_cache_layout.py - 共享数据结构，vllm-ascend 继承，布局协商需在 Ascend backend 落地；(6) vllm/model_executor/layers/attention/mla_attention.py - DeepSeek 等 MLA 模型在 Ascend 使用。vllm-ascend 必须实现统一 KV cache 布局协商接口并验证 Ascend attention backend 的布局支持。
    - 建议测试区域: `Ascend attention backend KV cache 布局协商接口实现`, `NPUModelRunner 布局协商`, `copy_kv_cache_blocks_inplace Ascend 存储拷贝语义`, `dflash speculator 布局适配`, `DeepSeek MLA KV cache 布局正确性`, `KV connector（nixl/mooncake）在 Ascend 的布局适配`

- **[9ff7041b](https://github.com/vllm-project/vllm/commit/9ff7041b55555976359fe8a67eef59f3a055a822)** ([#53002](https://github.com/vllm-project/vllm/pull/53002)) [Bugfix][推测解码] FlashAttention metadata 使用 group 几何
  - 标签: `bugfix`, `mrv2`, `low-risk`, `spec-decode`, `attention`
  - 变更文件:
  - 修改 `tests/v1/attention/test_group_head_counts.py` (+53/-6)
  - 修改 `vllm/v1/attention/backends/flash_attn.py` (+6/-5)
  - 修改 `vllm/v1/attention/backends/utils.py` (+5/-1)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+6/-6)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改 vllm/v1/worker/gpu/spec_decode/dflash/speculator.py，vllm-ascend 在 vllm_ascend/worker/v2/spec_decode/dflash/speculator.py 有对应实现；attn_vllm_config 构造方式变更（replace→copy.copy）需在 Ascend dflash speculator 上验证一致性。flash_attn.py/utils.py 为 NVIDIA FA 路径，Ascend 使用自有 attention backend，但 group 几何来源的修复思路Ascend backend 也应核对。
    - 建议测试区域: `Ascend dflash speculator attn_vllm_config 构造`, `Ascend attention backend group 几何来源核对`

### vllm-ascend
- **[175ef4d4](https://github.com/vllm-project/vllm-ascend/commit/175ef4d49c2072f9233619636f0309f4f88b4e2c)** ([#14131](https://github.com/vllm-project/vllm-ascend/pull/14131)) [CI] main2main 同步 vllm 0814 cdc4824
  - 标签: `ci`, `mrv2`, `medium-risk`, `model-runner`, `fused-moe`, `mamba`, `patch`
  - 变更文件（共 21 个）:
  - 修改 `.github/vllm-main-verified.commit` (+1/-1)
  - 修改 `tests/e2e/pull_request/two_card/lora/test_qwen3moe_lora.py` (+1/-0)
  - 修改 `tests/ut/kv_offload/test_native_cpu_offload.py` (+9/-0)
  - 修改 `tests/ut/ops/test_routed_experts.py` (+4/-0)
  - 修改 `tests/ut/patch/platform/test_patch_structured_output.py` (+17/-3)
  - 修改 `tests/ut/patch/worker/test_patch_mamba_utils_source.py` (+38/-2)
  - 修改 `tests/ut/patch/worker/test_patch_qwen3_5_mtp.py` (+14/-3)
  - 修改 `tests/ut/spec_decode/test_extract_hidden_states_proposer.py` (+18/-5)
  - 修改 `vllm_ascend/_310p/fused_moe/grouped_topk_router.py` (+8/-0)
  - 修改 `vllm_ascend/__init__.py` (+20/-29)
  - ... 及其他 11 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-08-21
### vllm
- **[b389ac29](https://github.com/vllm-project/vllm/commit/b389ac29465b33f9e9c534df221ea3c129e9793f)** ([#52816](https://github.com/vllm-project/vllm/pull/52816)) [Spec Decode] DFlash2：局部卷积 + 候选选择器
  - 标签: `feature`, `mrv2`, `high-risk`, `spec-decode`, `model-runner`, `attention`
  - 变更文件（共 14 个）:
  - 修改 `tests/models/registry.py` (+8/-0)
  - 修改 `tests/test_config.py` (+24/-0)
  - 新增 `tests/v1/spec_decode/test_dflash2.py` (+118/-0)
  - 修改 `tests/v1/spec_decode/test_dflash_causality.py` (+25/-1)
  - 修改 `vllm/config/vllm.py` (+17/-0)
  - 修改 `vllm/model_executor/layers/logits_processor.py` (+81/-0)
  - 修改 `vllm/model_executor/models/qwen3_dflash.py` (+11/-4)
  - 新增 `vllm/model_executor/models/qwen3_dflash2.py` (+290/-0)
  - 修改 `vllm/model_executor/models/registry.py` (+1/-0)
  - 修改 `vllm/v1/worker/gpu/sample/gumbel.py` (+52/-34)
  - ... 及其他 4 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 MRV2 核心路径 vllm/v1/worker/gpu/spec_decode/ 与 sample/gumbel.py。vllm-ascend NPUModelRunner 继承 GPUModelRunner，spec_decode 注册逻辑会传递到 Ascend 子类；DFlash2 speculator 为新算法，需评估是否在 Ascend 上启用及 gumbel sample 正确性
    - 建议测试区域: `DFlash2 推测解码在 Ascend 上的功能验证`, `NPUModelRunner speculator 注册回归`

- **[91a893de](https://github.com/vllm-project/vllm/commit/91a893de64722019ea2faf852e06cabe143b3490)** ([#52809](https://github.com/vllm-project/vllm/pull/52809)) [Bugfix][Spec Decode] 将 DSpark 后端继承限定到 DeepSeek V4
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `model`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/spec_decode/dspark/utils.py` (+34/-10)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 MRV2 核心路径 vllm/v1/worker/gpu/spec_decode/dspark/。vllm-ascend #14696 正在修复 MRV2 DSpark 推测解码，本变更限定 DSpark 后端继承范围会传递到 Ascend 子类，需确认 vllm-ascend DSpark 选择逻辑一致
    - 建议测试区域: `vllm-ascend MRV2 DSpark 推测解码回归`

### vllm-ascend
- **[4ce367a7](https://github.com/vllm-project/vllm-ascend/commit/4ce367a7d12db55c3dbe9b670eff52b2e14b3b9a)** ([#14696](https://github.com/vllm-project/vllm-ascend/pull/14696)) [BugFix] 修复 model runner v2 上的 DSpark 推测解码
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `attention`, `model`
  - 变更文件:
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+1/-1)
  - 修改 `vllm_ascend/models/deepseek_v4/model.py` (+4/-1)
  - Ascend 影响: ✓ 无影响

- **[d2818b08](https://github.com/vllm-project/vllm-ascend/commit/d2818b08d4284162f7671644303100475fd8aafa)** ([#14198](https://github.com/vllm-project/vllm-ascend/pull/14198)) [CI][E2E] 新增 Qwen3-32B V1/V2 性能迁移守卫
  - 标签: `test`, `medium-risk`, `e2e`, `performance`, `mrv2`, `ci`
  - 变更文件:
  - 修改 `.github/workflows/pr_test.yaml` (+4/-2)
  - 修改 `.github/workflows/scripts/select_tests.py` (+44/-0)
  - 修改 `.github/workflows/scripts/test_config.yaml` (+17/-0)
  - 新增 `tests/e2e/pull_request/four_card/qwen3_32b_v2_migration_common.py` (+329/-0)
  - 新增 `tests/e2e/pull_request/four_card/test_qwen3_32b_bf16_ll_performance.py` (+53/-0)
  - 新增 `tests/e2e/pull_request/four_card/test_qwen3_32b_w8a8_lc_performance.py` (+52/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-20
### vllm
- **[01af92e1](https://github.com/vllm-project/vllm/commit/01af92e175407231b1433b0aef01a1b9c983d955)** ([#49811](https://github.com/vllm-project/vllm/pull/49811)) [Feature][Model Runner V2] 支持 extract_hidden_states 推测解码
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `spec-decode`
  - 变更文件:
  - 修改 `tests/test_config.py` (+15/-0)
  - 新增 `tests/v1/worker/test_gpu_extract_hidden_states_speculator.py` (+132/-0)
  - 修改 `vllm/config/vllm.py` (+1/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+6/-1)
  - 修改 `vllm/v1/worker/gpu/spec_decode/__init__.py` (+7/-1)
  - 新增 `vllm/v1/worker/gpu/spec_decode/extract_hidden_states.py` (+153/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 MRV2 核心路径 vllm/v1/worker/gpu/model_runner.py 与 spec_decode/ 目录。vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，model_runner 中新增的 extract_hidden_states speculator 接入逻辑会传递到 Ascend 子类；spec_decode 目录为 MRV2 推测解码实现，vllm-ascend 需评估是否需要在 Ascend 上支持该推测解码算法及其 HCCL 通信正确性
    - 建议测试区域: `MRV2 extract_hidden_states 推测解码在 Ascend 上的功能验证`, `NPUModelRunner speculator 接入回归`

- **[a1c5b1fd](https://github.com/vllm-project/vllm/commit/a1c5b1fd9f6ef06a4fa236b7d48350115e5688b9)** ([#46701](https://github.com/vllm-project/vllm/pull/46701)) [Core][V1] 支持 trace_decode_token_ids 用于确定性 decode 重放
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `sampling`, `trace-replay`
  - 变更文件（共 13 个）:
  - 新增 `docs/serving/online_serving/trace_replay.md` (+60/-0)
  - 新增 `examples/generate/trace_replay_offline.py` (+195/-0)
  - 新增 `tests/v1/engine/test_input_processor_trace_replay.py` (+110/-0)
  - 新增 `tests/v1/sample/test_trace_replay_params.py` (+111/-0)
  - 新增 `tests/v1/worker/test_gpu_trace_replay.py` (+195/-0)
  - 修改 `vllm/config/model.py` (+7/-0)
  - 修改 `vllm/config/vllm.py` (+8/-0)
  - 修改 `vllm/engine/arg_utils.py` (+5/-0)
  - 修改 `vllm/sampling_params.py` (+72/-8)
  - 修改 `vllm/v1/engine/input_processor.py` (+40/-1)
  - ... 及其他 3 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 MRV2 核心路径 vllm/v1/worker/gpu/model_runner.py 与 sample/sampler.py。vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner，model_runner 中 trace 记录集成会传递到 Ascend 子类；sampler 与 sampling_params 新增字段影响采样路径。vllm-ascend 需评估 NPUModelRunner 是否需要重写 trace 集成、Ascend sampler 是否兼容 trace_replay
    - 建议测试区域: `MRV2 trace decode 重放在 Ascend 上的功能验证`, `NPUModelRunner trace 集成回归`, `Ascend sampler 与 sampling_params 新字段兼容性`

### vllm-ascend
- **[e3e8ba1e](https://github.com/vllm-project/vllm-ascend/commit/e3e8ba1e84a66193c0fb9ce701aa5991830876c9)** ([#14200](https://github.com/vllm-project/vllm-ascend/pull/14200)) [CI][E2E] 新增 Qwen3-32B V1/V2 精度迁移守卫
  - 标签: `test`, `medium-risk`, `ci`, `qwen`, `accuracy`, `mrv2`
  - 变更文件:
  - 修改 `.github/workflows/configs/nightly_config.yaml` (+18/-0)
  - 修改 `.github/workflows/schedule_nightly_test_a3.yaml` (+1/-0)
  - 修改 `.github/workflows/schedule_nightly_test_a3_560t.yaml` (+1/-0)
  - 新增 `tests/e2e/nightly/test_qwen3_32b_bf16_gpqa_accuracy.py` (+122/-0)
  - 新增 `tests/e2e/nightly/test_qwen3_32b_w8a8_aime2024_accuracy.py` (+121/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-19
### vllm
- **[08afae27](https://github.com/vllm-project/vllm/commit/08afae27863e884d68937f76e5bb87bba171c5de)** ([#48290](https://github.com/vllm-project/vllm/pull/48290)) [ModelRunner v2] 默认为 pooling 模型启用 MRV2
  - 标签: `feature`, `mrv2`, `medium-risk`, `model-runner`, `pooling`, `config`
  - 变更文件:
  - 修改 `tests/models/language/pooling/test_colbert.py` (+2/-2)
  - 修改 `tests/test_config.py` (+24/-1)
  - 修改 `vllm/config/vllm.py` (+0/-3)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/config/vllm.py MRV2 默认值变更会影响 Ascend MRV2 默认行为，Ascend 需评估 pooling 模型默认走 MRV2 是否符合预期

- **[a2257f95](https://github.com/vllm-project/vllm/commit/a2257f95b79287933defef5be40b74ce93053da3)** ([#51885](https://github.com/vllm-project/vllm/pull/51885)) [Elastic EP] 降低 eager 模式重配置停机时间
  - 标签: `feature`, `mrv2`, `high-risk`, `distributed`, `eplb`, `elastic-ep`, `model-runner`, `config`
  - 变更文件（共 12 个）:
  - 修改 `tests/distributed/test_eplb_execute.py` (+0/-122)
  - 修改 `tests/v1/worker/test_gpu_model_runner_v2_eplb.py` (+1/-2)
  - 修改 `vllm/config/parallel.py` (+1/-1)
  - 修改 `vllm/distributed/elastic_ep/elastic_execute.py` (+108/-54)
  - 修改 `vllm/distributed/elastic_ep/elastic_state.py` (+12/-37)
  - 修改 `vllm/distributed/eplb/eplb_communicator.py` (+12/-36)
  - 修改 `vllm/distributed/eplb/eplb_state.py` (+46/-25)
  - 修改 `vllm/distributed/parallel_state.py` (+7/-7)
  - 修改 `vllm/v1/worker/gpu/eplb_utils.py` (+0/-2)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+0/-2)
  - ... 及其他 2 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 Ascend 多个覆盖路径：(1) vllm/config/parallel.py - Ascend 依赖 ParallelConfig；(2) vllm/distributed/parallel_state.py - Ascend 继承分布式通信；(3) vllm/v1/worker/gpu/model_runner.py - vllm-ascend NPUModelRunner 继承 GPUModelRunner，EPLB/eager 重配置逻辑会传递到 Ascend 子类；(4) vllm/v1/worker/gpu/eplb_utils.py 与 gpu_worker.py - MRV2 worker 路径。Ascend 需评估 Elastic EP 重配置在 HCCL 下的正确性与停机时间优化是否生效
    - 建议测试区域: `Ascend Elastic EP eager 重配置验证`, `Ascend EPLB HCCL 通信验证`, `NPUModelRunner EPLB 重配置继承验证`

### vllm-ascend
- **[424e27e1](https://github.com/vllm-project/vllm-ascend/commit/424e27e1fd2b1c6e0d7fe659b489b87c1223a33c)** ([#13847](https://github.com/vllm-project/vllm-ascend/pull/13847)) [Feature][Bugfix] 在 Ascend 上支持并修复 Top-K/Top-P Triton kernel
  - 标签: `feature`, `mrv2`, `high-risk`, `triton`, `sampling`, `spec-decode`
  - 变更文件:
  - 新增 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_apply_top_k_top_p_triton.py` (+516/-0)
  - 新增 `vllm_ascend/ops/triton/v2/__init__.py` (+0/-0)
  - 新增 `vllm_ascend/ops/triton/v2/sample/__init__.py` (+0/-0)
  - 新增 `vllm_ascend/ops/triton/v2/sample/apply_top_k_top_p_triton.py` (+883/-0)
  - 新增 `vllm_ascend/ops/triton/v2/sample/docs/apply_top_k_top_p.md` (+95/-0)
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_triton.py` (+5/-0)
  - Ascend 影响: ✓ 无影响

- **[efc2dd9e](https://github.com/vllm-project/vllm-ascend/commit/efc2dd9e997fa99483f09f09a5cbc2d101b89c71)** ([#14023](https://github.com/vllm-project/vllm-ascend/pull/14023)) [Feature] 支持基础 GQA prefill context parallelism
  - 标签: `feature`, `mrv2`, `high-risk`, `attention`, `pcp`, `distributed`, `model-runner`
  - 变更文件:
  - 修改 `tests/ut/attention/a2/test_attention_v1.py` (+145/-1)
  - 修改 `tests/ut/spec_decode/test_speculators_vwn_eagle3.py` (+3/-3)
  - 修改 `tests/ut/worker/test_pcp_manager_v2.py` (+16/-52)
  - 修改 `vllm_ascend/attention/attention_v1.py` (+118/-2)
  - 修改 `vllm_ascend/attention/utils.py` (+6/-0)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+10/-14)
  - 修改 `vllm_ascend/worker/v2/pcp_manager.py` (+24/-32)
  - Ascend 影响: ✓ 无影响

- **[744bdce6](https://github.com/vllm-project/vllm-ascend/commit/744bdce6e7263274a7f3b25f3fd40991a5f2be1e)** ([#14433](https://github.com/vllm-project/vllm-ascend/pull/14433)) [Bugfix][Spec Decode] 修复 bad words kernel 中 draft token 偏移
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `sampling`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/sample/bad_words.py` (+3/-1)
  - Ascend 影响: ✓ 无影响

- **[4b19e8c9](https://github.com/vllm-project/vllm-ascend/commit/4b19e8c9f681a8fc1262a74cdbb7a1c4330baa50)** ([#14394](https://github.com/vllm-project/vllm-ascend/pull/14394)) [Bugfix] 修复 FULL_DECODE_ONLY 的图批次路由
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `model-runner`, `cudagraph`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+4/-1)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-18
### vllm-ascend
- **[27a94764](https://github.com/vllm-project/vllm-ascend/commit/27a94764b5ead50ed3e42ab52a257c2173032750)** ([#13470](https://github.com/vllm-project/vllm-ascend/pull/13470)) [Bugfix] 为投机解码支持概率拒绝采样
  - 标签: `bugfix`, `mrv2`, `high-risk`, `spec-decode`, `rejection-sampling`, `dflash`, `dspark`
  - 变更文件:
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_triton.py` (+3/-0)
  - 修改 `vllm_ascend/worker/v2/sample/gumbel.py` (+56/-45)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dflash/speculator.py` (+19/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dspark/speculator.py` (+21/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/rejection_sampler_utils.py` (+13/-2)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-17
### vllm
- **[70afdedc](https://github.com/vllm-project/vllm/commit/70afdedc1081d28c3eaae53bece8292298484c86)** ([#51855](https://github.com/vllm-project/vllm/pull/51855)) [K3] 为 Kimi-K3 支持 RecoverSSM
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `mamba`, `k3`, `recoverssm`
  - 变更文件（共 19 个）:
  - 修改 `tests/models/kimi_k3/test_kda.py` (+342/-0)
  - 修改 `tests/models/kimi_k3/test_kda_metadata.py` (+145/-4)
  - 修改 `tests/models/test_registry.py` (+3/-1)
  - 修改 `tests/test_config.py` (+47/-0)
  - 修改 `tests/v1/worker/test_mamba_hybrid_model_state.py` (+67/-0)
  - 修改 `tests/v1/worker/test_mamba_utils.py` (+36/-0)
  - 修改 `vllm/config/cache.py` (+4/-3)
  - 修改 `vllm/config/vllm.py` (+33/-8)
  - 修改 `vllm/model_executor/layers/mamba/abstract.py` (+5/-3)
  - 修改 `vllm/model_executor/layers/mamba/mamba_utils.py` (+30/-0)
  - ... 及其他 9 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改了 vllm/v1/worker/gpu/model_states/ 目录下的 mamba_hybrid.py 与 recoverssm.py，虽未直接命中 vllm-ascend 显式覆盖的 default.py，但该目录是 vllm-ascend MRV2 worker 继承链路的一部分。vllm-ascend 当前未支持 K3 模型， RecoverSSM 暂不直接影响 Ascend，但若未来 K3 上 Ascend，需评估 NPUModelRunner 是否需要为 RecoverSSM 适配状态恢复路径。

- **[6664d397](https://github.com/vllm-project/vllm/commit/6664d397bf091cb9371cba481d4efb8233436fe6)** ([#52329](https://github.com/vllm-project/vllm/pull/52329)) [Performance] 缓存 logits 处理的请求状态
  - 标签: `performance`, `mrv2`, `low-risk`, `sampler`, `logits-processing`, `model-runner`
  - 变更文件:
  - 新增 `tests/v1/worker/test_gpu_sampler_flags.py` (+90/-0)
  - 修改 `tests/v1/worker/test_gpu_thinking_budget.py` (+39/-0)
  - 修改 `vllm/v1/worker/gpu/sample/sampler.py` (+18/-19)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改 vllm/v1/worker/gpu/sample/sampler.py，该路径不在显式覆盖列表中，但 vllm-ascend 的 MRV2 v2/ worker 通过继承链路可能复用上游 sampler。缓存行为变更可能影响 Ascend MRV2 采样路径，建议回归 thinking budget 与 sampler flags 行为。

### vllm-ascend
- **[58d624ad](https://github.com/vllm-project/vllm-ascend/commit/58d624ad4d89584ac30a3322f4d52945c64780d7)** ([#14391](https://github.com/vllm-project/vllm-ascend/pull/14391)) [CI] 重新启用 DeepSeek V4 测试
  - 标签: `chore`, `low-risk`, `ci`, `deepseek-v4`, `mrv2`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/model_runner_v2/test_deepseek_v4.py` (+0/-1)
  - Ascend 影响: ✓ 无影响

- **[8fcb3bb9](https://github.com/vllm-project/vllm-ascend/commit/8fcb3bb9e84b85ebe0cc7f029f5fce087c0a992f)** ([#14105](https://github.com/vllm-project/vllm-ascend/pull/14105)) [Feature] 在 eager 模式下支持 MTP 与 SFA
  - 标签: `feature`, `mrv2`, `high-risk`, `spec-decode`, `mtp`, `sfa`, `model-runner`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+2/-0)
  - 新增 `tests/e2e/pull_request/eight_card/model_runner_v2/__init__.py` (+1/-0)
  - 新增 `tests/e2e/pull_request/eight_card/model_runner_v2/test_glm5_2.py` (+93/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+14/-8)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-16
### vllm
- **[4d2a68d6](https://github.com/vllm-project/vllm/commit/4d2a68d64d9e05921ed5c4099146e768a92d71d5)** ([#52436](https://github.com/vllm-project/vllm/pull/52436)) [修复][投机解码][结构化输出] DSpark：修复 draft 预算为零时语法位掩码映射错误
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `structured-output`, `model-runner`, `tests`
  - 变更文件:
  - 修改 `tests/v1/spec_decode/test_adaptive_verification.py` (+49/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+1/-0)
  - 修改 `vllm/v1/worker/gpu/structured_outputs.py` (+39/-15)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - (1) vllm/v1/worker/gpu/model_runner.py 命中 vllm-ascend 覆盖路径（vllm_ascend/worker/v2/model_runner.py 镜像继承上游 GPUModelRunner），构造 StructuredOutputsWorker 新增 num_bonus_tokens 参数，vllm-ascend 若覆写或自行实例化需同步；(2) vllm_ascend/worker/v2/structured_outputs.py 为 Ascend 自有 bitmask 实现（未见 _build_grammar_mapping/num_bonus_tokens），DSPark 是 Ascend 上常用投机解码方案（vllm_ascend/worker/v2/spec_decode/dspark/），零预算 compaction 场景若存在同类映射逻辑需移植修复
    - 建议测试区域: `DSpark + structured output 在 NPU 上的零预算回归`, `vllm_ascend/worker/v2/structured_outputs.py 映射逻辑与上游 _build_grammar_mapping 对齐评估`

- **[1b079c40](https://github.com/vllm-project/vllm/commit/1b079c40ff9d2598d837f4ed1fc08342fca4fd6e)** ([#52311](https://github.com/vllm-project/vllm/pull/52311)) [修复][Model Runner V2][投机解码] 修复 bad_words 草稿前缀匹配的差一错误
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `sampling`, `model-runner`, `tests`
  - 变更文件:
  - 新增 `tests/v1/worker/test_gpu_bad_words.py` (+105/-0)
  - 修改 `vllm/v1/worker/gpu/sample/bad_words.py` (+3/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响（需移植）- vllm_ascend/worker/v2/sample/bad_words.py 为上游 gpu/sample/bad_words.py 的 MRV2 镜像，经核对其第 116 行 from_spec_input 分支仍为修复前代码（缺少 +1 偏移），在 Ascend 上启用 MRV2 + 投机解码 + bad_words 时存在相同的掩码错位缺陷
    - 建议测试区域: `vllm_ascend/worker/v2/sample/bad_words.py 移植 +1 修复`, `Ascend 上 bad_words + 投机解码掩码正确性单测（参照 test_gpu_bad_words.py）`

- **[8efa13b7](https://github.com/vllm-project/vllm/commit/8efa13b700f1836657699cae2503dc2feab27fa0)** ([#52401](https://github.com/vllm-project/vllm/pull/52401)) [修复] DeepSeek V4 按 model runner 选择 eager CUDA graph 区域
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `deepseek-v4`, `cudagraph`, `config`, `tests`
  - 变更文件:
  - 修改 `tests/test_config.py` (+24/-37)
  - 修改 `vllm/config/vllm.py` (+7/-25)
  - 修改 `vllm/models/deepseek_v4/attention.py` (+65/-4)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - (1) vllm_ascend/models/deepseek_v4.py 从 vllm.models.deepseek_v4.attention 导入 DeepseekV4IndexerCache，该文件新增的 _prepare_and_attn_eager/_prepare_and_attn_fn 逻辑随导入路径生效；(2) default_v2_model_runner_architectures 仅对 ROCm 做例外，Ascend（非 ROCm）上 DSV4 将默认 MRV2，需确认 vllm-ascend 的 worker/v2 路径对 DSV4 的支持度与 ACLGraph 对 eager break 的兼容性；(3) 若 Ascend 上仍走 MRV1 + piecewise，宽 eager 区域分支会被启用
    - 建议测试区域: `Ascend 上 DSV4 默认（MRV2）运行正确性验证`, `DSV4 + Ascend ACLGraph eager break 兼容性验证`

### vllm-ascend
- **[dd6805d8](https://github.com/vllm-project/vllm-ascend/commit/dd6805d846bdac9474f3a4d59fdadb99beda8aca)** ([#14211](https://github.com/vllm-project/vllm-ascend/pull/14211)) [修复] 修复 DSA 预填充元数据传播
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `attention`, `dsa`, `spec-decode`, `tests`
  - 变更文件:
  - 修改 `tests/ut/worker/test_attn_utils_v2.py` (+6/-0)
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+1/-1)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+2/-0)
  - 修改 `vllm_ascend/worker/v2/model_states/default.py` (+2/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+10/-2)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-15
### vllm
- **[97388c44](https://github.com/vllm-project/vllm/commit/97388c44f9c608f83318e0c9540a536cd7de3e0d)** ([#51538](https://github.com/vllm-project/vllm/pull/51538)) [Bugfix] 使 DSV4 稀疏 MLA 在普通 decode、MTP 与 DSpark 场景下端到端可用
  - 标签: `bugfix`, `mrv2`, `high-risk`, `model-runner`, `spec-decode`, `attention`, `mla`, `kv-cache`, `workspace`, `deepseek`, `tests`
  - 变更文件（共 20 个）:
  - 修改 `csrc/libtorch_stable/cooperative_topk.cuh` (+4/-1)
  - 修改 `csrc/libtorch_stable/persistent_topk.cuh` (+20/-1)
  - 修改 `tests/kernels/attention/test_flashmla_sparse.py` (+118/-0)
  - 修改 `tests/kernels/moe/test_ocp_mx_moe.py` (+95/-0)
  - 修改 `tests/kernels/test_compressor_kv_cache.py` (+13/-0)
  - 修改 `tests/v1/attention/test_flashinfer_sparse_mla_sm120_api.py` (+33/-0)
  - 新增 `tests/v1/spec_decode/test_dflash_prepare_inputs.py` (+152/-0)
  - 新增 `tests/v1/worker/test_workspace.py` (+102/-0)
  - 修改 `vllm/model_executor/layers/fused_moe/experts/flashinfer_cutlass_moe.py` (+9/-18)
  - 修改 `vllm/models/deepseek_v4/amd/rocm.py` (+4/-4)
  - ... 及其他 10 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 vllm-ascend 覆盖路径 vllm/v1/worker/gpu/model_runner.py（vllm-ascend v2 NPUModelRunner 继承 GPUModelRunner，speculator load/capture/propose 包裹 use_workspace_lane 的改动会传递到 Ascend 子类），并修改 MRV2 核心目录 gpu/spec_decode/dflash/speculator.py 与公共基础设施 vllm/v1/worker/workspace.py（vllm-ascend worker 直接使用 init_workspace_manager，WorkspaceManager 新增 num_lanes 参数与 (ubatch, lane) 分配逻辑为行为变更）、vllm/v1/worker/gpu_worker.py 的 _num_workspace_lanes 初始化。vllm-ascend 已有 DSpark DeepSeek-V4 e2e 用例（tests/e2e/pull_request/four_card/spec_decode/test_dspark_deepseekv4.py），DSpark 在 Ascend 上启用时 target/draft workspace 隔离语义需重新验证；NPU 图模式（aclgraph）下 workspace resize/lane 切换行为与 CUDA graph 存在差异
    - 建议测试区域: `test_dspark_deepseekv4.py 回归`, `MRV2 workspace lane 在 NPU aclgraph 下的行为验证`, `DSpark target/draft workspace 隔离验证`, `speculator load/capture/propose lane 包裹在 NPUModelRunner 子类的兼容性`

- **[acb0f1dc](https://github.com/vllm-project/vllm/commit/acb0f1dcdb668d90bbbf50e57552d2f6f0987c87)** ([#52288](https://github.com/vllm-project/vllm/pull/52288)) [Bugfix][投机解码] DSpark：当投机配置未指定 attention backend 时继承目标模型的注意力后端
  - 标签: `bugfix`, `mrv2`, `low-risk`, `spec-decode`, `dspark`, `attention`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/spec_decode/dspark/utils.py` (+7/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改 MRV2 核心目录 vllm/v1/worker/gpu/spec_decode/dspark/utils.py。vllm-ascend 已有 DSpark e2e 用例（test_dspark_deepseekv4.py，启用 enable_dsa_cp 等 additional_config），draft 模型的 attention backend 继承逻辑变化会影响 Ascend 上 DSpark draft 的后端选择与加载路径

- **[615d4cfa](https://github.com/vllm-project/vllm/commit/615d4cfadeb3d5ea1df248eb59aa128af5dbd441)** ([#43107](https://github.com/vllm-project/vllm/pull/43107)) [Core] 在 CI 中检查 GPU 与 CPU 之间的同步
  - 标签: `feature`, `medium-risk`, `ci`, `instrumentation`, `gpu-sync`, `multimodal`, `distributed`, `sampler`, `lora`, `eplb`, `kv-transfer`, `tests`
  - 变更文件（共 44 个）:
  - 修改 `.buildkite/test_areas/plugins.yaml` (+6/-0)
  - 修改 `docker/Dockerfile` (+3/-0)
  - 修改 `docker/Dockerfile.rocm` (+3/-0)
  - 修改 `tests/models/multimodal/generation/test_mm_prefix_lm.py` (+4/-1)
  - 修改 `tests/v1/e2e/general/test_mamba_prefix_cache.py` (+28/-17)
  - 修改 `vllm/distributed/eplb/eplb_communicator.py` (+6/-4)
  - 修改 `vllm/distributed/eplb/eplb_state.py` (+21/-18)
  - 修改 `vllm/distributed/eplb/rebalance_execute.py` (+6/-2)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/example_connector.py` (+3/-1)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py` (+32/-27)
  - ... 及其他 34 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 不命中列出的 MRV2 覆盖路径，但修改的 vllm/v1/worker/gpu_model_runner.py（V1 runner，vllm-ascend v1 NPUModelRunner 的基类）、vllm/v1/worker/dp_utils.py（DP 同步路径，vllm-ascend 大量使用 DP/外部 DP）、vllm/distributed/eplb/*（vllm-ascend 支持 dynamic_eplb）、vllm/v1/sample/sampler.py、vllm/lora/worker_manager.py、vllm/v1/worker/encoder_cudagraph.py 均为 vllm-ascend 直接继承的通用路径；gpu_sync_allowed/VLLM_GPU_SYNC_CHECK 在 NPU（torch.npu 语义）下是否正常工作、DP Gloo/HCCL 路径是否误报需评估

- **[d6f17f3d](https://github.com/vllm-project/vllm/commit/d6f17f3d530efbd83a730d3d73e9f483726dfde1)** ([#52374](https://github.com/vllm-project/vllm/pull/52374)) 支持无注意力模型
  - 标签: `feature`, `mrv2`, `medium-risk`, `model-runner`, `model-states`, `mamba`, `hybrid`, `attention-free`, `tests`
  - 变更文件:
  - 修改 `tests/v1/e2e/general/test_mamba_prefix_cache.py` (+4/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+2/-1)
  - 修改 `vllm/v1/worker/gpu/model_states/__init__.py` (+1/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 vllm-ascend 覆盖路径 vllm/v1/worker/gpu/model_runner.py 与 gpu/model_states/ 目录（vllm-ascend 覆盖 model_states 并在 v2 NPUModelRunner 中继承该分发逻辑）。attention-free 路由到 MambaHybridModelState 影响 Ascend 侧线性注意力模型（Qwen3-Next/Qwen3.5-35B-A3B 等）的 V2 runner 状态管理；更关键的是上游混合/MoE 模型已默认使用 V2 runner，而 vllm-ascend 对 Qwen3.5-35B-A3B 的 MRV2 支持尚未完备（其 #13975 明确 skip），默认切换将迫使 vllm-ascend 加快 MRV2 适配或在平台层显式 pin V1
    - 建议测试区域: `混合/线性注意力模型 V2 runner 默认切换验证`, `MambaHybridModelState 路由回归（test_mtp_qwen3_next 类用例）`, `release_memory_cleanup 与 Ascend sleep mode 兼容性`

### vllm-ascend
- **[21d8dba4](https://github.com/vllm-project/vllm-ascend/commit/21d8dba46c8973da4d1523ee21a19aa373fe6384)** ([#13975](https://github.com/vllm-project/vllm-ascend/pull/13975)) [特性] 适配 model runner v2 的 routed-experts 捕获
  - 标签: `feature`, `mrv2`, `medium-risk`, `model-runner`, `moe`, `rlhf`, `eplb`, `tests`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+2/-2)
  - 新增 `tests/e2e/pull_request/two_card/rlhf/__init__.py` (+0/-0)
  - 新增 `tests/e2e/pull_request/two_card/rlhf/consistency/__init__.py` (+16/-0)
  - 新增 `tests/e2e/pull_request/two_card/rlhf/consistency/test_moe_routing_replay.py` (+65/-0)
  - 删除 `tests/e2e/pull_request/two_card/test_moe_routing_replay.py` (+0/-38)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+2/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-14
### vllm
- **[57bd0ed4](https://github.com/vllm-project/vllm/commit/57bd0ed441095b5c546707cabe25d3fa08b7f161)** ([#51704](https://github.com/vllm-project/vllm/pull/51704)) [5/N][KV-Cache 布局重构] 通过 customize_spec 机制将 KV 打包规格下沉到后端发布
  - 标签: `refactor`, `high-risk`, `mrv2`, `kv-cache`, `attention`, `model-runner`, `platform-interface`, `tests`
  - 变更文件（共 18 个）:
  - 修改 `tests/quantization/test_turboquant.py` (+15/-6)
  - 修改 `tests/v1/core/test_kv_cache_utils.py` (+10/-11)
  - 修改 `tests/v1/test_kv_cache_spec_registry.py` (+0/-11)
  - 修改 `tests/v1/worker/test_dsv4_packed_zeroer_geometry.py` (+1/-0)
  - 修改 `vllm/model_executor/layers/attention/attention.py` (+11/-26)
  - 修改 `vllm/model_executor/layers/attention/mla_attention.py` (+20/-1)
  - 修改 `vllm/models/deepseek_v4/attention.py` (+3/-0)
  - 修改 `vllm/models/kimi_k3/nvidia/mla.py` (+2/-0)
  - 修改 `vllm/platforms/interface.py` (+13/-13)
  - 修改 `vllm/v1/attention/backend.py` (+15/-1)
  - ... 及其他 8 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 严重影响 - 命中多个 vllm-ascend 核心覆盖路径：(1) vllm/v1/kv_cache_interface.py：vllm-ascend 的 vllm_ascend/core/kv_cache_interface.py、core/single_type_kv_cache_manager.py、attention/attention_v1.py、attention/dsa_v1.py 均导入其中 FullAttentionSpec/MLAAttentionSpec/AttentionSpec 等，spec 结构与打包逻辑重构（净删 80 行）可能要求 Ascend 后端实现 customize_spec 并同步适配层；(2) vllm/v1/attention/backend.py：vllm-ascend 十余处导入（attention_v1/mla_v1/sfa_v1/dsa_v1 等），接口扩展需确认兼容；(3) vllm/model_executor/layers/attention/mla_attention.py：vllm-ascend 的 mla_v1.py/sfa_v1.py 导入 MLAAttention/MLACommonMetadataBuilder，+20 行改动需同步；(4) mla/sparse_swa.py 的 DeepseekV4SWACache 被 vllm_ascend/models/deepseek_v4.py 使用；(5) vllm/v1/worker/gpu/attn_utils.py 与 gpu_model_runner.py 位于 MRV2 继承链（worker/v2/attn_utils.py、model_runner.py）；(6) platforms/interface.py 是 AscendPlatform 继承的平台基类
    - 建议测试区域: `Ascend attention backend customize_spec 适配与单测`, `DeepSeek V3.2/V4 MLA + sparse_swa 在 Ascend 的 KV 布局回归`, `vllm_ascend/core/kv_cache_interface.py 导入兼容性检查`, `MRV2（worker/v2）路径 KV cache 初始化回归`, `DSA（dsa_v1）spec 生成验证`

- **[66728feb](https://github.com/vllm-project/vllm/commit/66728feb1fbe0c6d32dcce2d4ce6e827712118c8)** ([#49852](https://github.com/vllm-project/vllm/pull/49852)) [多模态] 为 Model Runner V2 启用 encoder CUDA Graph
  - 标签: `feature`, `medium-risk`, `mrv2`, `model-runner`, `multimodal`, `cuda-graph`
  - 变更文件:
  - 修改 `vllm/v1/worker/encoder_cudagraph.py` (+4/-0)
  - 修改 `vllm/v1/worker/gpu/mm/encoder_runner.py` (+38/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+36/-24)
  - 修改 `vllm/v1/worker/gpu/model_states/interface.py` (+23/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - vllm_ascend/worker/v2/model_runner.py 继承 vllm.v1.worker.gpu.model_runner，vllm_ascend/worker/v2/aclgraph_utils.py 导入 gpu/cudagraph_utils、gpu/model_states.interface（ModelState）、gpu/input_batch（InputBuffers）；encoder 图捕获编排与 ModelState 接口扩展会传导到 Ascend MRV2（ACL graph）路径，需评估 NPU 上 encoder 图捕获支持
    - 建议测试区域: `Ascend MRV2 多模态（Qwen-VL 类）+ ACL graph 回归`, `vllm_ascend/worker/v2 对新 ModelState 接口的兼容`

- **[3c8676ae](https://github.com/vllm-project/vllm/commit/3c8676aebbd54ccf5d666b9c493d28badd3f970f)** ([#51650](https://github.com/vllm-project/vllm/pull/51650)) [PP][XPU] 异步调度下流水线并行采样 token 广播与计算重叠
  - 标签: `perf`, `medium-risk`, `distributed`, `pipeline-parallel`, `async-scheduling`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+11/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - vllm_ascend/worker/model_runner_v1.py 继承 vllm.v1.worker.gpu_model_runner.GPUModelRunner，PP 广播时序变化影响 Ascend PP 路径执行顺序（HCCL 广播），需回归验证
    - 建议测试区域: `Ascend PP 多卡一致性回归`, `async scheduling 开启时 PP 吞吐对比`

- **[6adad087](https://github.com/vllm-project/vllm/commit/6adad08767583f52eb4d2122111af0bf638ed5e6)** ([#51655](https://github.com/vllm-project/vllm/pull/51655)) 新增 Muse Glimmer 模型支持
  - 标签: `feature`, `medium-risk`, `mrv2`, `models`, `tool-use`, `reasoning`, `spec-decode`, `multimodal`, `tests`
  - 变更文件（共 21 个）:
  - 新增 `examples/tool_chat_template_muse_glimmer.jinja` (+1/-0)
  - 修改 `tests/models/registry.py` (+18/-0)
  - 修改 `tests/models/utils.py` (+7/-2)
  - 新增 `tests/tool_use/test_muse_glimmer.py` (+386/-0)
  - 新增 `tests/tool_use/test_muse_glimmer_parse_delta.py` (+187/-0)
  - 新增 `tests/transformers_utils/test_muse_glimmer_config.py` (+174/-0)
  - 修改 `vllm/config/speculative.py` (+5/-1)
  - 修改 `vllm/model_executor/models/interfaces.py` (+11/-10)
  - 新增 `vllm/model_executor/models/muse_glimmer.py` (+1649/-0)
  - 修改 `vllm/model_executor/models/qwen3_dflash.py` (+38/-1)
  - ... 及其他 11 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/worker/gpu/spec_decode/dflash/utils.py 与 vllm/v1/spec_decode/dflash.py 被 vllm-ascend 的 patch_v2/patch_dflash_speculator.py、vllm_ascend/worker/v2/spec_decode/dflash/speculator.py patch/继承，utils 变更需同步；新增模型本身为增量，Ascend 后续若支持 Muse Glimmer 需移植（含 processor 与 DFlash）
    - 建议测试区域: `vllm_ascend/worker/v2/spec_decode/dflash 与上游 utils.py 同步检查`, `Ascend DFlash 投机解码回归`

- **[827a2af8](https://github.com/vllm-project/vllm/commit/827a2af806c4e4ea7bcc280f57f793e6a5fcc676)** ([#48666](https://github.com/vllm-project/vllm/pull/48666)) [Kernel] Gemma-4 FA4 FP8 kernel
  - 标签: `feature`, `medium-risk`, `mrv2`, `attention`, `kernels`, `fa4`, `gemma`, `spec-decode`
  - 变更文件:
  - 修改 `cmake/external_projects/vllm_flash_attn.cmake` (+1/-1)
  - 修改 `vllm/model_executor/layers/attention/attention.py` (+11/-3)
  - 修改 `vllm/platforms/interface.py` (+3/-5)
  - 修改 `vllm/v1/attention/backend.py` (+14/-0)
  - 修改 `vllm/v1/attention/backends/fa_utils.py` (+3/-3)
  - 修改 `vllm/v1/attention/backends/flash_attn.py` (+57/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/gemma4/speculator.py` (+43/-12)
  - 修改 `vllm/vllm_flash_attn/flash_attn_interface.py` (+20/-3)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/attention/backend.py 的接口/能力扩展需确认 vllm-ascend 各 attention backend（attention_v1/mla_v1/sfa_v1/dsa_v1 等十余处导入）兼容（若新增方法无默认实现则需 Ascend 侧补齐）；platforms/interface.py 为 AscendPlatform 继承的基类；FA4/flash_attn/vllm_flash_attn 本身为 CUDA 专用不影响 NPU
    - 建议测试区域: `Ascend attention backend 对 v1/attention/backend.py 新增接口的兼容性检查`, `AscendPlatform 对 platforms/interface.py 变更的适配检查`

- **[f80b66f5](https://github.com/vllm-project/vllm/commit/f80b66f548d855a104c9b2a0527e6c0b1a31750c)** ([#50062](https://github.com/vllm-project/vllm/pull/50062)) [Model Runner V2][Spec Decode] 为多层 MTP 增加 KV cache 支持
  - 标签: `feature`, `high-risk`, `mrv2`, `kv-cache`, `spec-decode`, `scheduler`, `mtp`
  - 变更文件:
  - 修改 `tests/config/test_speculative_draft_hf_overrides.py` (+4/-2)
  - 修改 `tests/v1/core/test_scheduler.py` (+3/-1)
  - 修改 `vllm/config/speculative.py` (+1/-10)
  - 修改 `vllm/v1/core/kv_cache_coordinator.py` (+53/-3)
  - 修改 `vllm/v1/core/kv_cache_manager.py` (+2/-0)
  - 修改 `vllm/v1/core/kv_cache_utils.py` (+18/-0)
  - 修改 `vllm/v1/core/sched/scheduler.py` (+58/-8)
  - 修改 `vllm/v1/core/single_type_kv_cache_manager.py` (+19/-1)
  - 修改 `vllm/v1/kv_cache_interface.py` (+32/-7)
  - 修改 `vllm/v1/worker/gpu/spec_decode/__init__.py` (+6/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 严重影响 - vllm-ascend 的 recompute_scheduler/dyntra_lb_scheduler/batch_job_aware_scheduler 等直接继承 vllm.v1.core.sched.scheduler.Scheduler，scheduler.py +58/-8 的流程变化需同步定制调度器；vllm/v1/kv_cache_interface.py 被 vllm_ascend/core 与 attention 模块大量导入，+32/-7 接口扩展需适配；vllm/v1/worker/gpu/spec_decode/__init__.py 处于 vllm-ascend patch 链（patch_v2/patch_dflash_speculator）
    - 建议测试区域: `vllm_ascend/core 各定制 scheduler 与新 Scheduler 基类的兼容性`, `Ascend 上 multi-layer MTP（DFlash 类）KV cache 回归`, `vllm_ascend/core/kv_cache_interface.py 与上游接口对齐`

---

## 2026-08-13
### vllm
- **[f3c16389](https://github.com/vllm-project/vllm/commit/f3c1638927eee6ea31ad5a66e86e5b7ed6ebaa02)** ([#51653](https://github.com/vllm-project/vllm/pull/51653)) [ROCm] 在 ROCm 上为 Kimi-K3 启用 V2 model runner
  - 标签: `feature`, `low-risk`, `rocm`, `config`, `model-runner`
  - 变更文件:
  - 修改 `vllm/config/vllm.py` (+0/-16)
  - Ascend 影响: ✓ 无影响

- **[95c91444](https://github.com/vllm-project/vllm/commit/95c9144424060a3ec11090050318a5e702a70be2)** ([#42662](https://github.com/vllm-project/vllm/pull/42662)) [LoRA][Gemma4] 支持视觉塔 LoRA
  - 标签: `feature`, `mrv2`, `medium-risk`, `lora`, `multimodal`, `model`
  - 变更文件:
  - 修改 `.buildkite/test_areas/lora.yaml` (+1/-0)
  - 修改 `docs/models/supported_models.md` (+1/-1)
  - 修改 `tests/lora/conftest.py` (+5/-0)
  - 新增 `tests/lora/test_gemma4_tp.py` (+106/-0)
  - 修改 `tests/v1/worker/test_gpu_model_runner.py` (+6/-2)
  - 修改 `vllm/lora/model_manager.py` (+20/-6)
  - 修改 `vllm/model_executor/models/gemma4_mm.py` (+120/-14)
  - 修改 `vllm/model_executor/models/interfaces.py` (+23/-1)
  - 修改 `vllm/v1/worker/gpu/mm/lora.py` (+13/-11)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+14/-13)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改了 vllm/v1/worker/gpu_model_runner.py（旧 model runner 路径），vllm-ascend 通过 NPUModelRunner 继承该路径。视觉塔 LoRA 加载逻辑可能需要 vllm-ascend 适配。同时修改 vllm/v1/worker/gpu/mm/lora.py 属于 MRV2 新路径。
    - 建议测试区域: `Ascend 多模态 LoRA 加载验证`, `NPUModelRunner 视觉塔 LoRA 集成`

- **[50ba4bc6](https://github.com/vllm-project/vllm/commit/50ba4bc6b2cacd70c4711a1904dd7ad9740a578b)** ([#49577](https://github.com/vllm-project/vllm/pull/49577)) [Feature] Mask Replay 功能
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `sampling`, `config`, `entrypoints`
  - 变更文件（共 24 个）:
  - 新增 `docs/training/sampling_mask.md` (+113/-0)
  - 修改 `rust/src/engine-core-client/src/protocol/output.rs` (+3/-0)
  - 修改 `rust/src/engine-core-client/src/tests/client.rs` (+14/-0)
  - 修改 `rust/src/engine-core-client/src/tests/python_compat.py` (+25/-0)
  - 修改 `tests/entrypoints/scale_out/token_in_token_out/test_serving_tokens.py` (+44/-0)
  - 修改 `tests/v1/core/test_async_scheduler.py` (+1/-0)
  - 修改 `tests/v1/core/test_scheduler.py` (+1/-0)
  - 修改 `tests/v1/test_outputs.py` (+73/-0)
  - 修改 `vllm/config/model.py` (+3/-0)
  - 修改 `vllm/config/vllm.py` (+27/-0)
  - ... 及其他 14 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改了 vllm/v1/worker/gpu/model_runner.py（vllm-ascend 通过 NPUModelRunner 继承的核心路径）。Mask Replay 功能在 model runner 的采样流程中新增了掩码处理逻辑，vllm-ascend 需评估 NPUModelRunner 是否需要适配采样输出和掩码重放逻辑。同时修改了 vllm/v1/worker/gpu/sample/sampler.py 和 output.py，属于采样器核心路径。
    - 建议测试区域: `NPUModelRunner mask replay 采样验证`, `Ascend 采样器掩码处理测试`, `Mask Replay 端到端功能验证`

- **[373592ef](https://github.com/vllm-project/vllm/commit/373592ef57d4a19b057237fb015b0bd1382daa03)** ([#52092](https://github.com/vllm-project/vllm/pull/52092)) [CPU] 发布 triton-cpu wheel 并修复多处硬编码的 pin_memory=True
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `cpu`
  - 变更文件:
  - 修改 `.buildkite/hardware_tests/cpu.yaml` (+7/-22)
  - 修改 `docker/Dockerfile.cpu` (+30/-15)
  - 修改 `vllm/model_executor/models/granite_speech.py` (+3/-1)
  - 修改 `vllm/model_executor/models/qwen3_vl.py` (+2/-1)
  - 修改 `vllm/v1/worker/cpu/shm.py` (+1/-0)
  - 修改 `vllm/v1/worker/cpu_worker.py` (+3/-0)
  - 修改 `vllm/v1/worker/gpu/mm/encoder_runner.py` (+2/-1)
  - 修改 `vllm/v1/worker/gpu/structured_outputs.py` (+2/-1)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[b7bdfd59](https://github.com/vllm-project/vllm-ascend/commit/b7bdfd59f590f0c7a58a1818faa71728a86719ef)** ([#13958](https://github.com/vllm-project/vllm-ascend/pull/13958)) [Feature] MRV2 SFA 支持图模式
  - 标签: `feature`, `medium-risk`, `attention`, `mrv2`, `graph-mode`, `tests`
  - 变更文件:
  - 修改 `tests/ut/attention/a2/test_sfa_v1.py` (+15/-9)
  - 修改 `tests/ut/attention/test_sfa_cp.py` (+12/-8)
  - 修改 `vllm_ascend/attention/context_parallel/sfa_cp.py` (+12/-12)
  - 修改 `vllm_ascend/attention/indexer.py` (+4/-0)
  - 修改 `vllm_ascend/attention/sfa_v1.py` (+21/-4)
  - 修改 `vllm_ascend/worker/v2/aclgraph_utils.py` (+26/-10)
  - Ascend 影响: ✓ 无影响

- **[c04eb05c](https://github.com/vllm-project/vllm-ascend/commit/c04eb05cbbc04f90ca0bb863e5704b923cc2d080)** ([#14189](https://github.com/vllm-project/vllm-ascend/pull/14189)) [CI] 因 PR 冲突临时跳过 DeepSeek V4 测试
  - 标签: `ci`, `low-risk`, `mrv2`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/model_runner_v2/test_deepseek_v4.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-12
### vllm
- **[b1b75204](https://github.com/vllm-project/vllm/commit/b1b752042f622c692d5019c3ea122f2f7ee9d6ac)** ([#51841](https://github.com/vllm-project/vllm/pull/51841)) 避免 ViT 中的长时间阻塞 H2D 拷贝
  - 标签: `optimization`, `medium-risk`, `model-runner`, `multimodal`
  - 变更文件:
  - 修改 `vllm/model_executor/models/qwen3_vl.py` (+9/-1)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+14/-4)
  - Ascend 影响: ✓ 无影响

- **[02ac1785](https://github.com/vllm-project/vllm/commit/02ac17851dfb603c1ba788545200ae3e43a4f61b)** ([#51917](https://github.com/vllm-project/vllm/pull/51917)) [重构] 统一 uniform decode token count 辅助函数
  - 标签: `refactor`, `mrv2`, `medium-risk`, `model-runner`, `cudagraph`, `spec-decode`
  - 变更文件:
  - 修改 `tests/v1/spec_decode/test_dynamic_sd_cug.py` (+8/-5)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+1/-17)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+3/-2)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/model_runner.py（MRV2 model runner），这是 vllm-ascend 的核心覆盖路径。vllm-ascend 的 NPUModelRunner V2 继承 GPUModelRunner，cudagraph_utils.py 中的 get_uniform_token_count 被移除后，如果 vllm-ascend 的 V2 实现引用了该函数，会导致导入失败。需验证 vllm-ascend 的 worker/v2/ 路径是否引用了被移除的 get_uniform_token_count。
    - 建议测试区域: `vllm-ascend worker/v2/ 对 get_uniform_token_count 的引用检查`, `MRV2 cudagraph 捕获在 Ascend 上的功能验证`

- **[a53ad859](https://github.com/vllm-project/vllm/commit/a53ad859139ee37ef7c2c29716963abffd9cb486)** ([#51905](https://github.com/vllm-project/vllm/pull/51905)) [XPU][CI] 在 Intel GPU CI 中全局使用 VLLM_DISABLE_COMPILE_CACHE=1
  - 标签: `chore`, `low-risk`, `ci`, `xpu`
  - 变更文件:
  - 修改 `.buildkite/intel_jobs/basic_correctness.yaml` (+1/-2)
  - 修改 `.buildkite/intel_jobs/benchmarks_intel.yaml` (+1/-2)
  - 修改 `.buildkite/intel_jobs/model_executor_intel.yaml` (+1/-2)
  - 修改 `.buildkite/intel_jobs/model_runner_v2_intel.yaml` (+1/-2)
  - 修改 `.buildkite/intel_jobs/models_distributed_intel.yaml` (+1/-2)
  - 修改 `.buildkite/intel_jobs/samplers_intel.yaml` (+1/-2)
  - 修改 `.buildkite/intel_jobs/test-intel.yaml` (+1/-2)
  - 修改 `.buildkite/scripts/hardware_ci/run-intel-ci-test.sh` (+2/-2)
  - 修改 `.buildkite/scripts/hardware_ci/run-intel-test.sh` (+4/-1)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[de35b401](https://github.com/vllm-project/vllm-ascend/commit/de35b40196dbd6c21d075a31183982355149c9b0)** ([#13874](https://github.com/vllm-project/vllm-ascend/pull/13874)) [特性] 在 eager 模式下支持 MTP 与 DSA
  - 标签: `feature`, `mrv2`, `medium-risk`, `spec-decode`, `model`, `dsa`, `mtp`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+2/-1)
  - 新增 `tests/e2e/pull_request/four_card/model_runner_v2/__init__.py` (+1/-0)
  - 新增 `tests/e2e/pull_request/four_card/model_runner_v2/test_deepseek_v4.py` (+79/-0)
  - 修改 `vllm_ascend/models/deepseek_v4_mtp.py` (+3/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+33/-12)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-11
### vllm
- **[b64a2708](https://github.com/vllm-project/vllm/commit/b64a2708b06b6329420702bffce994543c1ec6d2)** ([#51447](https://github.com/vllm-project/vllm/pull/51447)) 在昂贵操作前绑定生成输入边界
  - 标签: `feature`, `medium-risk`, `mrv2`, `entrypoints`, `sampling`
  - 变更文件（共 11 个）:
  - 修改 `rust/src/server/src/routes/openai/utils/types.rs` (+47/-2)
  - 新增 `tests/test_request_input_bounds.py` (+273/-0)
  - 修改 `vllm/entrypoints/openai/chat_completion/protocol.py` (+3/-2)
  - 修改 `vllm/entrypoints/openai/completion/protocol.py` (+2/-1)
  - 修改 `vllm/entrypoints/openai/engine/protocol.py` (+6/-1)
  - 修改 `vllm/entrypoints/openai/responses/protocol.py` (+2/-2)
  - 修改 `vllm/envs.py` (+14/-0)
  - 修改 `vllm/sampling_params.py` (+33/-13)
  - 修改 `vllm/tokenizers/deepseek_v32_encoding.py` (+13/-3)
  - 修改 `vllm/tokenizers/deepseek_v4_encoding.py` (+15/-2)
  - ... 及其他 1 个文件
  - Ascend 影响: ✓ 无影响

- **[a311916a](https://github.com/vllm-project/vllm/commit/a311916a291c1fed3dbfb72e60f74cd778c8419d)** ([#46849](https://github.com/vllm-project/vllm/pull/46849)) [Spec] 将 AR speculator 多步 decode 融合回单个 CUDA graph
  - 标签: `feature`, `mrv2`, `high-risk`, `attention`, `spec-decode`, `mla`
  - 变更文件:
  - 修改 `docs/design/model_runner_v2.md` (+8/-0)
  - 修改 `tests/v1/worker/test_gpu_autoregressive_speculator.py` (+166/-0)
  - 修改 `vllm/models/deepseek_v4/amd/rocm.py` (+4/-0)
  - 修改 `vllm/v1/attention/backend.py` (+13/-0)
  - 修改 `vllm/v1/attention/backends/flash_attn.py` (+94/-42)
  - 修改 `vllm/v1/attention/backends/mla/sparse_swa.py` (+35/-0)
  - 修改 `vllm/v1/attention/backends/mla/triton_mla.py` (+5/-0)
  - 修改 `vllm/v1/attention/backends/triton_attn.py` (+5/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` (+151/-7)
  - 修改 `vllm/v1/worker/utils.py` (+11/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 覆盖路径 vllm/v1/attention/backend.py（+13），新增多步 decode attention 计算接口。vllm-ascend 有自己的 attention backend 实现，需在 Ascend backend 中实现相应接口以支持多步 decode 的 attention 计算。同时修改了 vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py（MRV2 核心文件），vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner，speculator 的 CUDA graph 融合逻辑需验证在 Ascend 上的兼容性。
    - 建议测试区域: `Ascend attention backend 多步 decode 接口实现`, `AR speculator graph 融合在 Ascend 上的正确性`, `MLA backend 多步 decode 场景验证`, `投机解码端到端功能验证`

- **[3e174bb7](https://github.com/vllm-project/vllm/commit/3e174bb73c70b677dd339c59c39d7460abc5d02d)** ([#47352](https://github.com/vllm-project/vllm/pull/47352)) [Model Runner V2][MTP] 在 draft 步骤间共享 topk index buffer
  - 标签: `performance`, `mrv2`, `medium-risk`, `spec-decode`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` (+27/-5)
  - 修改 `vllm/v1/worker/gpu/spec_decode/mtp/speculator.py` (+41/-1)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[7a25ef83](https://github.com/vllm-project/vllm-ascend/commit/7a25ef83a605f4709a9f67af12a9bc0f5051e705)** ([#12831](https://github.com/vllm-project/vllm-ascend/pull/12831)) [功能][KV传输] 添加 SFA PD RD2H 连接器用于 KV cache 卸载
  - 标签: `feature`, `high-risk`, `kv-transfer`, `attention`, `distributed`, `model-runner`, `tests`, `docs`
  - 变更文件（共 39 个）:
  - 新增 `docs/source/developer_guide/Design_Documents/sfa_remote_d2h_connector.md` (+248/-0)
  - 修改 `docs/source/user_guide/feature_guide/index.md` (+1/-1)
  - 新增 `docs/source/user_guide/feature_guide/layerwise_and_sparse_kv_cache_offloading.md` (+333/-0)
  - 修改 `docs/source/user_guide/feature_guide/layerwise_kv_pool.md` (+1/-1)
  - 删除 `docs/source/user_guide/feature_guide/layerwise_prefill_kv_offload.md` (+0/-207)
  - 删除 `docs/source/user_guide/feature_guide/sparse_kv_cache_offload.md` (+0/-113)
  - 修改 `examples/disaggregated_prefill_v1/load_balance_proxy_layerwise_server_example.py` (+113/-29)
  - 修改 `mkdocs.yml` (+3/-0)
  - 修改 `tests/ut/attention/a2/test_sfa_v1.py` (+5/-0)
  - 修改 `tests/ut/distributed/ascend_store/_mock_deps.py` (+21/-6)
  - ... 及其他 29 个文件
  - Ascend 影响: ✓ 无影响

- **[a47fbe26](https://github.com/vllm-project/vllm-ascend/commit/a47fbe2648c55fa757c81df727fd1c0b844025ac)** ([#13069](https://github.com/vllm-project/vllm-ascend/pull/13069)) [功能] SFA 模型 Runner V2 适配
  - 标签: `feature`, `high-risk`, `mrv2`, `model-runner`, `patch`, `attention`
  - 变更文件:
  - 修改 `vllm_ascend/patch/__init__.py` (+13/-0)
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_attn_utils.py` (+8/-0)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+180/-1)
  - Ascend 影响: ✓ 无影响

- **[0c935ead](https://github.com/vllm-project/vllm-ascend/commit/0c935eadd3e44876dbc99c442fef0c86a7faabdf)** ([#13729](https://github.com/vllm-project/vllm-ascend/pull/13729)) [Bug修复] 在 NPUModelRunner 中添加 potential max tokens 设置
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `model-runner`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-09
### vllm
- **[f18e10a7](https://github.com/vllm-project/vllm/commit/f18e10a7e1c1eb37e898c31989ff625d79791657)** ([#50892](https://github.com/vllm-project/vllm/pull/50892)) 将 Flashinfer 版本升级至 0.6.16.post3
  - 标签: `chore`, `medium-risk`, `flashinfer`, `dependency`, `benchmark`
  - 变更文件:
  - 修改 `docker/Dockerfile` (+1/-1)
  - 修改 `docker/versions.json` (+1/-1)
  - 修改 `requirements/cuda.txt` (+2/-2)
  - 修改 `vllm/model_executor/warmup/kernel_warmup.py` (+36/-51)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+11/-3)
  - Ascend 影响: ✓ 无影响

- **[9b0afeb4](https://github.com/vllm-project/vllm/commit/9b0afeb4f6c435a06d394f8a25209d4682a215af)** ([#51458](https://github.com/vllm-project/vllm/pull/51458)) [Perf] 避免更多不必要的 GPU<->CPU 同步
  - 标签: `perf`, `low-risk`, `gpu-sync`, `multimodal`
  - 变更文件（共 13 个）:
  - 修改 `tests/basic_correctness/test_basic_correctness.py` (+2/-1)
  - 修改 `tests/v1/e2e/general/test_mamba_prefix_cache.py` (+7/-7)
  - 修改 `tests/v1/logits_processors/utils.py` (+14/-6)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/utils.py` (+8/-3)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/example_connector.py` (+4/-3)
  - 修改 `vllm/lora/ops/triton_ops/fused_moe_lora_op.py` (+2/-2)
  - 修改 `vllm/model_executor/models/chameleon.py` (+32/-4)
  - 修改 `vllm/model_executor/models/gemma3n_mm.py` (+13/-4)
  - 修改 `vllm/model_executor/models/glm4_1v.py` (+11/-4)
  - 修改 `vllm/model_executor/models/qwen3_omni_moe_thinker.py` (+1/-1)
  - ... 及其他 3 个文件
  - Ascend 影响: ✓ 无影响

- **[d608dfab](https://github.com/vllm-project/vllm/commit/d608dfabfdba7e1496e5fef7c66d27c131f59432)** ([#51438](https://github.com/vllm-project/vllm/pull/51438)) [Bugfix] 在 V2 warmup 中预留 spec-decode lookahead blocks
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `warmup`, `scheduler`, `model-runner`
  - 变更文件:
  - 新增 `tests/v1/worker/test_gpu_warmup_blocks.py` (+361/-0)
  - 修改 `vllm/config/vllm.py` (+27/-0)
  - 修改 `vllm/v1/core/sched/scheduler.py` (+2/-16)
  - 修改 `vllm/v1/worker/gpu/warmup.py` (+59/-21)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-08
### vllm
- **[44351f81](https://github.com/vllm-project/vllm/commit/44351f81d58861edc873c7678c500a4f40834450)** ([##51410](https://github.com/vllm-project/vllm/pull/#51410)) [CI] 刷新混合模型 Model Runner V2 覆盖率
  - 标签: `chore`, `low-risk`, `ci`, `mtp`, `pipeline-parallel`
  - 变更文件:
  - 修改 `.buildkite/intel_jobs/model_runner_v2_intel.yaml` (+1/-0)
  - 修改 `.buildkite/test-amd.yaml` (+1/-1)
  - 修改 `.buildkite/test_areas/model_runner_v2.yaml` (+5/-1)
  - 修改 `.buildkite/test_areas/quantization.yaml` (+1/-7)
  - 修改 `tests/v1/e2e/spec_decode/mtp/test_mtp.py` (+0/-7)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-07
### vllm
- **[ae934ba8](https://github.com/vllm-project/vllm/commit/ae934ba8a5577c580c33e3489290ff7d8bf1f83e)** ([#48355](https://github.com/vllm-project/vllm/pull/48355)) [功能] 扩展 EPLB 支持到 Mistral Large 3 及更多 MoE backend
  - 标签: `feature`, `mrv2`, `medium-risk`, `eplb`, `quantization`, `model-executor`, `moe`
  - 变更文件（共 16 个）:
  - 新增 `tests/distributed/test_eplb_quant_scale_consistency.py` (+299/-0)
  - 修改 `tests/kernels/moe/test_flashinfer_cutedsl_nvfp4_moe.py` (+16/-15)
  - 修改 `tests/quantization/test_trtllm_nvfp4_hidden_dim_padding.py` (+6/-1)
  - 修改 `tests/v1/worker/test_gpu_model_runner_v2_eplb.py` (+6/-4)
  - 修改 `vllm/model_executor/layers/fused_moe/oracle/fp8.py` (+13/-2)
  - 修改 `vllm/model_executor/layers/fused_moe/oracle/nvfp4.py` (+5/-0)
  - 修改 `vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w4a4_nvfp4.py` (+16/-2)
  - 修改 `vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w8a8_fp8.py` (+3/-1)
  - 修改 `vllm/model_executor/layers/quantization/fp8.py` (+3/-1)
  - 修改 `vllm/model_executor/layers/quantization/modelopt.py` (+3/-1)
  - ... 及其他 6 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改了 vllm/v1/worker/gpu/eplb_utils.py（MRV2 路径）和 vllm/v1/worker/gpu_model_runner.py。EPLB 在 Ascend 上的 MoE 专家负载均衡行为需验证。同时修改了 vllm/model_executor/ 下多个量化 backend，需确认 Ascend 使用的量化 backend 是否受影响

- **[b706fd16](https://github.com/vllm-project/vllm/commit/b706fd1628b06c216a945176a9fedfa808324803)** ([#51337](https://github.com/vllm-project/vllm/pull/51337)) [CI][XPU] 通过 VLLM_DISABLE_COMPILE_CACHE=1 规避 Intel XPU CI 中的间歇性段错误
  - 标签: `ci`, `low-risk`, `xpu`
  - 变更文件:
  - 修改 `.buildkite/intel_jobs/basic_correctness.yaml` (+2/-1)
  - 修改 `.buildkite/intel_jobs/model_executor_intel.yaml` (+2/-1)
  - 修改 `.buildkite/intel_jobs/model_runner_v2_intel.yaml` (+2/-1)
  - 修改 `.buildkite/intel_jobs/models_distributed_intel.yaml` (+2/-1)
  - 修改 `.buildkite/intel_jobs/samplers_intel.yaml` (+2/-1)
  - Ascend 影响: ✓ 无影响

- **[dd856e48](https://github.com/vllm-project/vllm/commit/dd856e48bbf969e3f0e561e8c76f6e92c76e0795)** ([#51222](https://github.com/vllm-project/vllm/pull/51222)) [Bugfix][EPD][Model Runner V2] 为 encoder-only 实例跳过多模态 embedding gather
  - 标签: `bugfix`, `mrv2`, `high-risk`, `model-runner`, `multimodal`, `encoder`, `epd`
  - 变更文件:
  - 修改 `tests/v1/core/test_scheduler.py` (+31/-0)
  - 修改 `tests/v1/worker/test_encoder_runner.py` (+43/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+11/-3)
  - 修改 `vllm/v1/worker/gpu/model_states/default.py` (+1/-8)
  - 修改 `vllm/v1/worker/gpu/model_states/interface.py` (+15/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改了 vllm/v1/worker/gpu/model_runner.py 和 vllm/v1/worker/gpu/model_states/default.py，这两个文件是 vllm-ascend 的核心覆盖路径。vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner，encoder-only 实例的 mm embedding gather 跳过逻辑会传递到 Ascend 子类。model_states/default.py 的 gather 逻辑重构（移到 interface.py）需验证 NPUModelRunner 的 model states 是否受影响
    - 建议测试区域: `encoder-only 实例 mm embedding gather 跳过在 Ascend 上的正确性`, `EPD 分离场景多模态模型在 Ascend 上的正确性`, `NPUModelRunner model_states interface 适配验证`

- **[72c0d676](https://github.com/vllm-project/vllm/commit/72c0d6765793e4c7242c3586274af3e1a8aca170)** ([#46727](https://github.com/vllm-project/vllm/pull/46727)) [功能] 在 Model Runner V2 中支持 thinking_token_budget
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `sampling`, `reasoning`, `config`
  - 变更文件:
  - 新增 `benchmarks/kernels/benchmark_thinking_budget.py` (+365/-0)
  - 修改 `tests/entrypoints/openai/chat_completion/test_thinking_token_budget.py` (+3/-8)
  - 新增 `tests/v1/worker/test_gpu_thinking_budget.py` (+262/-0)
  - 修改 `vllm/config/reasoning.py` (+31/-13)
  - 修改 `vllm/config/vllm.py` (+0/-6)
  - 修改 `vllm/v1/engine/input_processor.py` (+9/-16)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+1/-0)
  - 修改 `vllm/v1/worker/gpu/sample/sampler.py` (+22/-0)
  - 新增 `vllm/v1/worker/gpu/sample/thinking_budget.py` (+428/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler.py` (+1/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改了 vllm/v1/worker/gpu/model_runner.py（vllm-ascend 核心覆盖路径，NPUModelRunner 继承 GPUModelRunner）和 vllm/config/reasoning.py（配置路径）。新增的 thinking_budget.py（428 行）位于 vllm/v1/worker/gpu/sample/ 路径下，thinking budget 的采样逻辑会传递到 Ascend 子类。sampler.py 的采样流程变更需验证在 Ascend 上的正确性
    - 建议测试区域: `thinking_token_budget 在 Ascend 上的采样正确性`, `推理模型 thinking budget 限制在 Ascend 上的效果`, `NPUModelRunner thinking_budget 初始化适配`, `spec_decode rejection sampler thinking budget 适配`

- **[b1e12d14](https://github.com/vllm-project/vllm/commit/b1e12d142d8c9533f857f8da13d8fc368e95a8cd)** ([#51304](https://github.com/vllm-project/vllm/pull/51304)) [V1] 异步将 logits 中的 NaN 计数拷贝到主机
  - 标签: `performance`, `medium-risk`, `model-runner`, `v1`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+52/-18)
  - Ascend 影响: ✓ 无影响

- **[27930df9](https://github.com/vllm-project/vllm/commit/27930df9c2bd14047be35ff2a986ca72fc65631a)** ([#50939](https://github.com/vllm-project/vllm/pull/50939)) [Model Runner V2] 修复 rejection sampler 中的 -1 占位 draft token ids
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `spec-decode`, `model-runner`, `sampling`
  - 变更文件:
  - 修改 `tests/v1/spec_decode/test_rejection_sampler_utils.py` (+122/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py` (+107/-74)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py 位于 vllm/v1/worker/gpu/ 路径下（MRV2 路径）。rejection sampler 的 -1 占位符处理逻辑在 Ascend 上也适用，需验证 spec decode 在 Ascend 上的正确性

### vllm-ascend
- **[08a68770](https://github.com/vllm-project/vllm-ascend/commit/08a68770b68debdb21c8fe7720a7d89797e6bdc8)** ([#13810](https://github.com/vllm-project/vllm-ascend/pull/13810)) [BugFix][Test] 恢复 NPU 内存辅助函数的导入
  - 标签: `bugfix`, `low-risk`, `tests`, `mrv2`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

- **[a6ae7f57](https://github.com/vllm-project/vllm-ascend/commit/a6ae7f57601e9bafdc18ec1e3a5035e53d5fad6f)** ([#13290](https://github.com/vllm-project/vllm-ascend/pull/13290)) 回退 "[Performance] 移除 DSA_CP 中 QLIMetadata builder 的 D2H 同步"
  - 标签: `bugfix`, `low-risk`, `attention`, `dsa-cp`, `tests`, `mrv2`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+1/-2)
  - 修改 `vllm_ascend/attention/context_parallel/dsa_cp.py` (+11/-11)
  - Ascend 影响: ✓ 无影响

- **[1bff043f](https://github.com/vllm-project/vllm-ascend/commit/1bff043fe717aaafeacf1051313ac9b8256311d0)** ([#13155](https://github.com/vllm-project/vllm-ascend/pull/13155)) [Feature] 在 ModelRunner V2 中支持 DSA
  - 标签: `feature`, `mrv2`, `high-risk`, `dsa`, `attention`, `kv-cache`, `model-runner`, `deepseek-v4`, `tests`
  - 变更文件（共 27 个）:
  - 修改 `tests/ut/_310p/fused_moe/test_shared_fused_moe_310.py` (+2/-0)
  - 修改 `tests/ut/models/test_deepseek_v4_moe.py` (+15/-0)
  - 修改 `tests/ut/ops/test_fused_moe.py` (+66/-3)
  - 修改 `tests/ut/test_ascend_forward_context.py` (+51/-0)
  - 新增 `tests/ut/worker/test_attn_utils_v2.py` (+306/-0)
  - 修改 `vllm_ascend/ascend_forward_context.py` (+0/-3)
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+14/-5)
  - 修改 `vllm_ascend/attention/mla_v1.py` (+3/-1)
  - 修改 `vllm_ascend/core/kv_cache_interface.py` (+11/-0)
  - 修改 `vllm_ascend/models/deepseek_v4.py` (+33/-11)
  - ... 及其他 17 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-08-06
### vllm
- **[81bc1969](https://github.com/vllm-project/vllm/commit/81bc196913653c9e06b957e39a606002a09db171)** ([#50910](https://github.com/vllm-project/vllm/pull/50910)) [Model Runner V2] 以模型 LM Head dtype 缓存 draft logits
  - 标签: `feature`, `high-risk`, `mrv2`, `spec-decode`, `model-runner`
  - 变更文件:
  - 修改 `tests/v1/spec_decode/test_rejection_sampler_utils.py` (+21/-7)
  - 修改 `tests/v1/worker/test_gpu_gumbel_sample.py` (+66/-0)
  - 修改 `vllm/v1/worker/gpu/sample/gumbel.py` (+33/-36)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dspark/speculator.py` (+2/-2)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py` (+44/-28)
  - 修改 `vllm/v1/worker/gpu/spec_decode/speculator.py` (+4/-3)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - vllm/v1/worker/gpu/ 为 MRV2 路径，vllm-ascend 通过 AscendEagleProposer/AscendRejectionSampler 等覆盖 spec decode；draft logits dtype 缓存逻辑需在 Ascend spec decode 实现中对齐验证
    - 建议测试区域: `Ascend Eagle/DFlash draft logits dtype 验证`, `Ascend rejection sampler dtype 一致性`

- **[b50fdebc](https://github.com/vllm-project/vllm/commit/b50fdebce0698c1f2d57ba7ff94211323655557e)** ([#39935](https://github.com/vllm-project/vllm/pull/39935)) [Bugfix] 修复 enable_lora=True 时 level-2 sleep/wake/reload
  - 标签: `bugfix`, `high-risk`, `lora`, `model-runner`, `kv-cache`
  - 变更文件（共 11 个）:
  - 修改 `docs/features/sleep_mode.md` (+1/-1)
  - 修改 `tests/basic_correctness/test_mem.py` (+93/-0)
  - 修改 `tests/lora/test_layers.py` (+47/-0)
  - 修改 `tests/lora/test_lora_manager.py` (+4/-0)
  - 修改 `tests/v1/worker/test_gpu_worker_weight_transfer.py` (+40/-0)
  - 修改 `vllm/lora/layers/base.py` (+13/-0)
  - 修改 `vllm/lora/layers/logits_processor.py` (+12/-0)
  - 修改 `vllm/lora/model_manager.py` (+2/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+18/-3)
  - 修改 `vllm/v1/worker/gpu_worker.py` (+6/-0)
  - ... 及其他 1 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - vllm/v1/worker/gpu_model_runner.py（GPUModelRunner）为 vllm-ascend NPUModelRunner 的父类，sleep/wake/reload 与 LoRA 状态管理变更会传递到 Ascend 子类；vllm-ascend 有 SleepWakeupManager，需验证 LoRA 启用时的一致性
    - 建议测试区域: `Ascend level-2 sleep/wake + LoRA 验证`, `NPUModelRunner LoRA 状态恢复`

- **[47a4e410](https://github.com/vllm-project/vllm/commit/47a4e410ba3e027a69ec34ca03b3dd313b4350d2)** ([#50183](https://github.com/vllm-project/vllm/pull/50183)) [Bugfix][Spec Decode] 修复 rejection sampler tl.argmax 的 NaN 处理
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `spec-decode`
  - 变更文件:
  - 修改 `tests/v1/spec_decode/test_rejection_sampler_utils.py` (+41/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils.py` (+10/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - vllm/v1/worker/gpu/spec_decode/ 为 MRV2 路径，vllm-ascend 有 AscendRejectionSampler 覆盖，NaN 处理需在 Ascend 实现中对齐
    - 建议测试区域: `Ascend rejection sampler NaN 处理`

- **[811622c4](https://github.com/vllm-project/vllm/commit/811622c410c2f1baf2fa7056ca19753264b95815)** ([#50066](https://github.com/vllm-project/vllm/pull/50066)) [Refactor][PCP] 使 PCPManager 构造可扩展
  - 标签: `refactor`, `medium-risk`, `mrv2`, `pcp`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+6/-0)
  - 修改 `vllm/v1/worker/gpu/pcp_manager.py` (+3/-2)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - vllm/v1/worker/gpu/model_runner.py 与 gpu/pcp_manager.py 为 MRV2 路径，vllm-ascend 有 pcp_manager_v2，PCPManager 构造可扩展性变更需验证 Ascend PCP 集成

### vllm-ascend
- **[0703581e](https://github.com/vllm-project/vllm-ascend/commit/0703581e8d530d2ae8079a740ec70843883add5f)** ([#12804](https://github.com/vllm-project/vllm-ascend/pull/12804)) [Feature][EPLB] 将上游 EPLB 与 Model Runner V2 集成
  - 标签: `feature`, `mrv2`, `high-risk`, `eplb`, `moe`, `distributed`, `model-runner`
  - 变更文件（共 50 个）:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+11/-0)
  - 修改 `docs/hooks/nav_titles.py` (+4/-0)
  - 新增 `docs/source/developer_guide/Design_Documents/model_runner_v2_eplb.md` (+167/-0)
  - 修改 `docs/source/user_guide/configuration/additional_config.md` (+22/-9)
  - 修改 `docs/source/user_guide/feature_guide/expert_parallelism_load_balancer.md` (+133/-14)
  - 修改 `docs/source/user_guide/support_matrix/feature_matrix.md` (+2/-2)
  - 修改 `docs/source/user_guide/support_matrix/supported_features.md` (+2/-1)
  - 修改 `mkdocs.yml` (+1/-0)
  - 修改 `tests/e2e/conftest.py` (+6/-3)
  - 新增 `tests/e2e/pull_request/four_card/test_qwen3_mrv2_eplb.py` (+92/-0)
  - ... 及其他 40 个文件
  - Ascend 影响: ✓ 无影响

- **[bc226d48](https://github.com/vllm-project/vllm-ascend/commit/bc226d4867f0d50ae6ca51a88bb4451c4393a049)** ([#13684](https://github.com/vllm-project/vllm-ascend/pull/13684)) [BugFix] 修复 DeepSeek Overlay C8 启用 MTP 加载重权重集时的错误
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `deepseek`, `mtp`
  - 变更文件:
  - 修改 `vllm_ascend/patch/__init__.py` (+11/-1)
  - 修改 `vllm_ascend/patch/worker/patch_deepseek_mtp.py` (+5/-0)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+1/-4)
  - Ascend 影响: ✓ 无影响

- **[798ed122](https://github.com/vllm-project/vllm-ascend/commit/798ed122a4d93fcdc4a228d1707aa6e7185c877a)** ([#13479](https://github.com/vllm-project/vllm-ascend/pull/13479)) [Misc] 移除 model runner v2 中的死代码
  - 标签: `refactor`, `mrv2`, `low-risk`, `model-runner`
  - 变更文件:
  - 修改 `vllm_ascend/attention/attention_v1.py` (+1/-5)
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+1/-5)
  - 修改 `vllm_ascend/attention/fa3_v1.py` (+1/-2)
  - 修改 `vllm_ascend/attention/mla_v1.py` (+1/-5)
  - 修改 `vllm_ascend/attention/sfa_v1.py` (+1/-5)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+0/-112)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-05
### vllm
- **[397094da](https://github.com/vllm-project/vllm/commit/397094da1768c7a6f29dfa4f70079d793ac747df)** ([#49990](https://github.com/vllm-project/vllm/pull/49990)) 通过 huggingface_hub 的 resolve_revision 在每次模型加载时解析 revision 为 commit_hash
  - 标签: `refactor`, `low-risk`, `config`, `model-loading`
  - 变更文件:
  - 修改 `requirements/common.txt` (+1/-0)
  - 修改 `requirements/test/cpu.txt` (+2/-1)
  - 修改 `requirements/test/cuda.txt` (+3/-1)
  - 修改 `requirements/test/rocm.txt` (+3/-1)
  - 修改 `requirements/test/xpu.txt` (+3/-1)
  - 修改 `vllm/config/model.py` (+27/-0)
  - 修改 `vllm/model_executor/models/ultravox.py` (+4/-2)
  - 修改 `vllm/transformers_utils/repo_utils.py` (+38/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+3/-0)
  - Ascend 影响: ✓ 无影响

- **[12292d94](https://github.com/vllm-project/vllm/commit/12292d94b25869be2af6b6d4f8eea6c2445e935f)** ([#50323](https://github.com/vllm-project/vllm/pull/50323)) [CI] 在 logits 中出现 NaN 时检测并失败 evals
  - 标签: `feature`, `mrv2`, `medium-risk`, `model-runner`, `ci`, `tests`
  - 变更文件:
  - 修改 `tests/basic_correctness/test_basic_correctness.py` (+31/-0)
  - 修改 `tests/v1/worker/test_gpu_model_runner.py` (+2/-1)
  - 修改 `vllm/envs.py` (+7/-0)
  - 修改 `vllm/v1/worker/gpu/async_utils.py` (+4/-0)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+3/-1)
  - 修改 `vllm/v1/worker/utils.py` (+13/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/async_utils.py (MRV2 核心路径) 和 vllm/v1/worker/utils.py (通用 worker 工具)。vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner，NaN 检测钩子会传递到 Ascend 子类。需验证 NaN 检测在 Ascend 上的行为是否正确，特别是 Ascend 上 logits 的 dtype 和数值范围可能不同于 NVIDIA GPU。

---

## 2026-08-04
### vllm
- **[4f819f80](https://github.com/vllm-project/vllm/commit/4f819f801b7702e39d9588cc9f2ecd28560b31f5)** ([#38390](https://github.com/vllm-project/vllm/pull/38390)) E/P/D 分离部署支持
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `kv-cache`, `distributed`, `disaggregation`
  - 变更文件:
  - 修改 `examples/disaggregated/disaggregated_encoder/disagg_1e1pd_example.sh` (+1/-1)
  - 修改 `vllm/config/vllm.py` (+18/-4)
  - 修改 `vllm/v1/worker/gpu/block_table.py` (+6/-0)
  - 新增 `vllm/v1/worker/gpu/ec_connector.py` (+85/-0)
  - 修改 `vllm/v1/worker/gpu/mm/encoder_runner.py` (+2/-0)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+30/-3)
  - 修改 `vllm/v1/worker/gpu/warmup.py` (+3/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 修改了 vllm-ascend 的核心覆盖路径：(1) vllm/v1/worker/gpu/model_runner.py - vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，新增的 is_encoder_only 字段、ec_connector 集成与 encoder-only 分支会传递到 Ascend 子类；(2) vllm/v1/worker/gpu/block_table.py - vllm-ascend 通过 block_table_patch 打补丁，新增的 num_kv_cache_groups==0 短路逻辑需验证在 Ascend 上 encoder-only 场景的正确性。vllm-ascend 需评估 NPUModelRunner 在 E/P/D 分离部署下的行为，以及 ec_connector 在 Ascend 通信库下的可用性。
    - 建议测试区域: `NPUModelRunner is_encoder_only 分支验证`, `Ascend encoder-only worker block_table 短路逻辑`, `E/P/D 分离部署在 Ascend 上的端到端验证`

- **[5789897a](https://github.com/vllm-project/vllm/commit/5789897aa40fbab6bdfcffaa9e83da64939286fb)** ([#49969](https://github.com/vllm-project/vllm/pull/49969)) [Spec Decode] 新增 top-k DSpark Markov 投影
  - 标签: `feature`, `mrv2`, `medium-risk`, `spec-decode`, `dspark`, `qwen3`
  - 变更文件:
  - 新增 `tests/v1/spec_decode/test_dspark_topk.py` (+58/-0)
  - 修改 `vllm/config/speculative.py` (+59/-1)
  - 修改 `vllm/model_executor/models/qwen3_dspark.py` (+39/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dspark/speculator.py` (+79/-25)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 变更文件命中 vllm/v1/worker/gpu/spec_decode/ 子路径（MRV2 核心目录）。若 vllm-ascend 启用 DSpark 推测解码，speculator 的 top-k 采样路径与 Markov 投影需在 Ascend 上验证。该优化要求 draft TP=1，需确认 Ascend 部署配置兼容。

- **[59b2fdfc](https://github.com/vllm-project/vllm/commit/59b2fdfc4e237794c2b26f0781054ced73f5b8df)** ([#48250](https://github.com/vllm-project/vllm/pull/48250)) 在 Transformers modeling backend 中正确支持 MLA
  - 标签: `feature`, `medium-risk`, `mla`, `transformers`, `model-runner`
  - 变更文件:
  - 新增 `tests/models/transformers/fusers/test_mla.py` (+161/-0)
  - 修改 `tests/models/transformers/test_backend.py` (+42/-11)
  - 修改 `vllm/config/model.py` (+7/-1)
  - 修改 `vllm/model_executor/models/transformers/__init__.py` (+34/-3)
  - 修改 `vllm/model_executor/models/transformers/base.py` (+104/-33)
  - 修改 `vllm/model_executor/models/transformers/fuser.py` (+5/-4)
  - 修改 `vllm/model_executor/models/transformers/fusers/__init__.py` (+2/-0)
  - 新增 `vllm/model_executor/models/transformers/fusers/mla.py` (+325/-0)
  - 修改 `vllm/model_executor/models/transformers/fx_utils.py` (+19/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-03
### vllm
- **[dd11df04](https://github.com/vllm-project/vllm/commit/dd11df04f3b7046c40f13e586ac38a3725bc3c03)** ([#49389](https://github.com/vllm-project/vllm/pull/49389)) [Misc] 移除已废弃的 calculate_kv_scales 运行时 KV 缩放计算
  - 标签: `refactor`, `medium-risk`, `kv-cache`, `quantization`, `attention`, `mla`
  - 变更文件（共 19 个）:
  - 修改 `.buildkite/test-amd.yaml` (+1/-1)
  - 修改 `.buildkite/test_areas/compile.yaml` (+0/-3)
  - 修改 `.buildkite/test_areas/pytorch.yaml` (+1/-2)
  - 修改 `docs/design/metrics.md` (+1/-1)
  - 修改 `docs/features/quantization/quantized_kvcache.md` (+3/-32)
  - 修改 `tests/compile/fullgraph/test_full_graph.py` (+0/-32)
  - 修改 `tests/models/quantization/test_per_token_kv_cache.py` (+0/-4)
  - 修改 `tests/quantization/test_fp8.py` (+8/-20)
  - 修改 `tests/quantization/test_per_token_kv_cache.py` (+0/-1)
  - 修改 `vllm/config/cache.py` (+0/-17)
  - ... 及其他 9 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/model_executor/layers/attention/mla_attention.py（vllm-ascend 覆盖路径），移除了 MLAAttention 类的 calculate_kv_scales 属性、calc_kv_scales 方法、q_range/k_range/v_range 初始化以及 forward 中的 maybe_calc_kv_scales 调用。DeepSeek V3/R1 等 MLA 模型在 Ascend 上使用 MLAAttention，若 vllm-ascend 的 MLA 实现引用了 calculate_kv_scales 或 calc_kv_scales 接口，需要同步移除相关引用以避免 AttributeError
    - 建议测试区域: `DeepSeek V3/R1 FP8 KV cache 在 Ascend 上的功能验证`, `vllm-ascend MLAAttention 实现中 calculate_kv_scales 引用清理`

---

## 2026-08-01
### vllm
- **[652ba592](https://github.com/vllm-project/vllm/commit/652ba59229499eb65fc4115b7feadeddf9bcb75d)** ([#50574](https://github.com/vllm-project/vllm/pull/50574)) [Model Runner V2] 启用编码器 token 嵌入
  - 标签: `feature`, `mrv2`, `medium-risk`, `model-runner`, `pooling`, `late-interaction`
  - 变更文件:
  - 修改 `tests/models/language/pooling/test_colbert.py` (+13/-2)
  - 修改 `tests/models/language/pooling/test_splade_sparse_pooler.py` (+67/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+6/-0)
  - 修改 `vllm/v1/worker/gpu/pool/pooling_runner.py` (+20/-4)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/model_runner.py 中的 GPUModelRunner 类，vllm-ascend 的 NPUModelRunner 继承该类。新增的 reset_encoder_cache 中 pooling_runner.clear() 调用和 finish_requests 中 pooling_runner.on_requests_finished() 调用会传递到 Ascend 子类。如果 vllm-ascend 使用 pooling 功能（ColBERT/SPLADE 等晚期交互模型），需验证 NPUModelRunner 的 encoder cache 清理和请求完成流程是否正确处理 pooling_runner 的状态。pooling_runner.py 的变更（新增 LateInteractionRunner 和 token_embed 任务）也可能影响 Ascend 上的 pooling 推理。
    - 建议测试区域: `ColBERT token_embed 在 Ascend 上的功能验证`, `NPUModelRunner reset_encoder_cache 中 pooling_runner.clear() 行为`, `NPUModelRunner finish_requests 中 pooling_runner.on_requests_finished() 行为`, `SPLADE sparse pooling 在 Ascend 上的正确性`

- **[fcdc7c2e](https://github.com/vllm-project/vllm/commit/fcdc7c2e9c9b75c923751ea7d2dd79ef66572c81)** ([#50330](https://github.com/vllm-project/vllm/pull/50330)) [CI] 按覆盖范围重新组织推测解码 E2E 测试
  - 标签: `chore`, `mrv2`, `low-risk`, `spec-decode`, `tests`, `ci`
  - 变更文件（共 39 个）:
  - 修改 `.buildkite/intel_jobs/engine_intel.yaml` (+4/-2)
  - 修改 `.buildkite/intel_jobs/model_runner_v2_intel.yaml` (+0/-1)
  - 修改 `.buildkite/test-amd.yaml` (+16/-23)
  - 修改 `.buildkite/test_areas/engine.yaml` (+5/-30)
  - 修改 `.buildkite/test_areas/misc.yaml` (+0/-27)
  - 修改 `.buildkite/test_areas/model_runner_v2.yaml` (+4/-3)
  - 修改 `.buildkite/test_areas/spec_decode.yaml` (+78/-32)
  - 修改 `tests/models/registry.py` (+2/-2)
  - 修改 `tests/utils.py` (+4/-1)
  - 修改 `tests/v1/e2e/general/test_kv_sharing_fast_prefill.py` (+1/-1)
  - ... 及其他 29 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/spec_decode/dspark/utils.py（DSpark 推测解码模型加载工具），新增 get_draft_quant_config 调用以修复 draft model 的 quant_config 被 post-init 恢复的问题。如果 vllm-ascend 支持 DSpark 推测解码（Kimi K3 等模型），此变更会影响 draft model 的量化配置加载。同时 gemma4_dspark.py 的因果掩码变更可能影响 Ascend 上的 DSpark 注意力计算。
    - 建议测试区域: `DSpark draft model quant config 在 Ascend 上的加载验证`, `Gemma4 DSpark 因果掩码在 Ascend 上的行为`

---

## 2026-07-31
### vllm
- **[a0cd2b69](https://github.com/vllm-project/vllm/commit/a0cd2b69b3dac2b43be02fc16ff940b856d6791b)** ([#50302](https://github.com/vllm-project/vllm/pull/50302)) [Bugfix] 统一将 block table 宽度对齐到 128 tokens
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `kv-cache`, `attention`, `model-runner`, `block-table`, `mla`, `tests`
  - 变更文件:
  - 修改 `tests/v1/attention/test_indexer_deepseek_v4_slot_mapping.py` (+4/-0)
  - 修改 `tests/v1/attention/test_mla_backends.py` (+3/-9)
  - 修改 `tests/v1/worker/test_gpu_model_runner.py` (+28/-0)
  - 修改 `vllm/v1/attention/backend.py` (+2/-0)
  - 修改 `vllm/v1/attention/backends/mla/indexer.py` (+3/-11)
  - 修改 `vllm/v1/worker/block_table.py` (+32/-4)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+6/-5)
  - 修改 `vllm/v1/worker/utils.py` (+12/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的多个核心覆盖路径：(1) vllm/v1/worker/gpu/model_runner.py - vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，block table 宽度计算逻辑的变更会传递到 Ascend 子类；(2) vllm/v1/worker/block_table.py - vllm-ascend 通过 block_table_patch 打补丁，新增的 get_block_table_width 函数和 MultiGroupBlockTable 中的对齐逻辑变更需验证；(3) vllm/v1/attention/backend.py - 新增的 requires_block_table_width 接口需在 Ascend attention backend 中评估是否需要实现。vllm-ascend 需验证 block table 宽度对齐在 Ascend 上的正确性，特别是 MLA 模型和 Mamba 模型的差异处理。
    - 建议测试区域: `Ascend block table 宽度对齐验证`, `MLA indexer block_table_width 在 Ascend 上的正确性`, `Mamba 模型 block table 不对齐在 Ascend 上的验证`, `NPUModelRunner 中 get_block_table_width 调用路径验证`

- **[b2fb83e7](https://github.com/vllm-project/vllm/commit/b2fb83e7ffbc30a1aa4667b1dad7ca3e2c342bcf)** ([#50148](https://github.com/vllm-project/vllm/pull/50148)) [Attention] 为 AttentionMetadataBuilder 类型提示使用 KVCacheSpec
  - 标签: `refactor`, `low-risk`, `attention`, `mrv2`, `mla`, `kv-cache`
  - 变更文件（共 14 个）:
  - 修改 `vllm/model_executor/layers/attention/chunked_local_attention.py` (+1/-2)
  - 修改 `vllm/model_executor/layers/attention/mla_attention.py` (+2/-0)
  - 修改 `vllm/v1/attention/backend.py` (+3/-3)
  - 修改 `vllm/v1/attention/backends/flash_attn.py` (+2/-2)
  - 修改 `vllm/v1/attention/backends/flashinfer.py` (+3/-1)
  - 修改 `vllm/v1/attention/backends/gdn_attn.py` (+3/-3)
  - 修改 `vllm/v1/attention/backends/hpc_attn.py` (+2/-2)
  - 修改 `vllm/v1/attention/backends/linear_attn.py` (+5/-5)
  - 修改 `vllm/v1/attention/backends/mamba2_attn.py` (+2/-2)
  - 修改 `vllm/v1/attention/backends/mamba_attn.py` (+3/-3)
  - ... 及其他 4 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm-ascend 的核心覆盖路径：(1) vllm/v1/attention/backend.py - AttentionMetadataBuilder 基类接口变更，vllm-ascend 的 attention backend 需确保与新的 KVCacheSpec 类型提示兼容；(2) vllm/v1/worker/gpu/attn_utils.py - vllm-ascend 有自己的 attn_utils 实现，cast 移除需确认 Ascend 路径不受影响；(3) vllm/model_executor/layers/attention/mla_attention.py - DeepSeek 等 MLA 模型在 Ascend 上使用，新增的 kv_cache_spec 类型声明需验证。由于是类型提示级别变更，实际运行时影响较小，但 vllm-ascend 需确认其 attention backend 子类与基类接口一致。

- **[0f173945](https://github.com/vllm-project/vllm/commit/0f17394564fa2fccd332cf63321314884c15ee37)** ([#50293](https://github.com/vllm-project/vllm/pull/50293)) [Model Runner V2] 启用 encoder token 分类任务
  - 标签: `feature`, `mrv2`, `medium-risk`, `model-runner`, `pooling`, `tests`
  - 变更文件:
  - 修改 `tests/models/language/pooling/test_splade_sparse_pooler.py` (+41/-0)
  - 修改 `tests/models/language/pooling/test_token_classification.py` (+16/-6)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+3/-1)
  - 修改 `vllm/v1/worker/gpu/pool/pooling_runner.py` (+31/-12)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/model_runner.py（GPUModelRunner.get_supported_tasks 调用 PoolingRunner.get_supported_tasks 时新增传入 self.model_config），vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner，该签名变更会传递到 Ascend 子类。PoolingRunner 的 _get_enabled_tasks 基于 attn_type 启用 token_classify，若 vllm-ascend 支持 encoder-only 模型则需验证该任务在 Ascend 上的正确性。
    - 建议测试区域: `Ascend encoder-only 模型 token 分类 MRV2 路径`, `NPUModelRunner get_supported_tasks 签名兼容性`, `decoder 模型 token_classify 过滤在 Ascend 上的行为`

---

## 2026-07-30
### vllm
- **[aeeb36b1](https://github.com/vllm-project/vllm/commit/aeeb36b1f17145975c6713242f2447bb8b98782b)** ([#50000](https://github.com/vllm-project/vllm/pull/50000)) [新模型] Kimi K3
  - 标签: `feature`, `mrv2`, `high-risk`, `new-model`, `kimi-k3`, `mla`, `moe`, `spec-decode`, `attention`, `distributed`, `tests`
  - 变更文件（共 82 个）:
  - 修改 `cmake/external_projects/deepgemm.cmake` (+3/-3)
  - 修改 `docs/models/supported_models.md` (+1/-0)
  - 修改 `pyproject.toml` (+2/-0)
  - 修改 `requirements/cuda.txt` (+2/-2)
  - 修改 `requirements/test/cuda.txt` (+1/-1)
  - 修改 `tests/kernels/moe/test_deepgemm.py` (+32/-0)
  - 修改 `tests/models/registry.py` (+18/-0)
  - 新增 `tests/models/test_dspark_mla.py` (+143/-0)
  - 修改 `tests/test_config.py` (+20/-0)
  - 新增 `tests/transformers_utils/test_dspark_mla_config.py` (+165/-0)
  - ... 及其他 72 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 vllm/model_executor/layers/attention/mla_attention.py 与 vllm/config/parallel.py 核心覆盖路径，并修改 MRV2 路径 vllm/v1/worker/gpu/spec_decode/dflash/speculator.py。Kimi K3 使用 MLA + DeepGMM MoE + dspark/dflash 推测解码，vllm-ascend 若要支持 Kimi K3 需实现 Ascend 版 MLA backend、MoE 算子与 dspark speculator，并适配 config/parallel.py 新增配置。
    - 建议测试区域: `Kimi K3 Ascend 可行性评估`, `Ascend MLA backend 与 mla_attention.py 回归`, `dspark speculator Ascend 适配`, `config/parallel.py 新增配置对 Ascend 并行的影响`

---
