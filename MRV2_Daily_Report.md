# MRV2 每日报告
生成时间: 2026-09-09 09:03:24
统计范围: 最近 30 天

**MRV2 定义**: `vllm/v1/worker/gpu/model_runner.py` 及其依赖的所有组件

MRV2 相关 commits 总数: 157

## 2026-09-08
### vllm
- **[6b15bea0](https://github.com/vllm-project/vllm/commit/6b15bea080ac64c9e123982b48cbbffe34957ec0)** ([#53941](https://github.com/vllm-project/vllm/pull/53941)) [重构] 移除 utils dead code (#53941)
  - 标签: `refactor`, `medium-risk`, `model-runner`, `attention`, `distributed`, `kv-cache`, `tests`, `multimodal`, `context-parallel`
  - 变更文件（共 15 个）:
  - 修改 `tests/models/multimodal/generation/test_memory_leak.py` (+2/-1)
  - 修改 `vllm/compilation/passes/fx_utils.py` (+0/-10)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/lmcache_integration/utils.py` (+0/-74)
  - 修改 `vllm/model_executor/layers/utils.py` (+0/-8)
  - 修改 `vllm/model_executor/model_loader/weight_utils.py` (+0/-15)
  - 修改 `vllm/utils/flashinfer.py` (+0/-38)
  - 修改 `vllm/utils/hpc.py` (+0/-41)
  - 修改 `vllm/utils/mem_utils.py` (+0/-5)
  - 修改 `vllm/utils/torch_utils.py` (+0/-9)
  - 修改 `vllm/v1/attention/backends/utils.py` (+1/-14)
  - ... 及其他 5 个文件
  - Ascend 影响: ✓ 无影响

- **[07950d47](https://github.com/vllm-project/vllm/commit/07950d47347f7fff41f98616096fd10349171e3d)** ([#55774](https://github.com/vllm-project/vllm/pull/55774)) [Kimi Bug] 修复 kimi k3 startup cuda graph issue 使用 recoverSSM (#55774)
  - 标签: `bugfix`, `low-risk`, `mrv2`, `model-runner`, `tests`, `mamba`, `cudagraph`, `kimi`
  - 变更文件:
  - 修改 `tests/v1/cudagraph/test_cudagraph_manager.py` (+10/-1)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+5/-1)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[57e3c205](https://github.com/vllm-project/vllm-ascend/commit/57e3c205c8be34d5c08572c1d1d934a5ebcb58b2)** ([#16011](https://github.com/vllm-project/vllm-ascend/pull/16011)) [Bugfix]修复 mtp graph senario in a5 device (#16011)
  - 标签: `bugfix`, `low-risk`, `mrv2`, `tests`, `spec-decode`
  - 变更文件:
  - 新增 `tests/ut/spec_decode/test_autoregressive_draft_metadata.py` (+51/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+6/-3)
  - Ascend 影响: ✓ 无影响

- **[b51d788c](https://github.com/vllm-project/vllm-ascend/commit/b51d788c8d4693221735cd1b58e7aedb2d40a963)** ([#15656](https://github.com/vllm-project/vllm-ascend/pull/15656)) [Bugfix][SpecDecode] 同步 unstream fixes 到 MRV2 rejecti在 sampling (#15656)
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `tests`, `spec-decode`, `sampling`
  - 变更文件:
  - 修改 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_rejection_sample_v2.py` (+117/-0)
  - 修改 `vllm_ascend/ops/triton/v2/spec_decode/resample.py` (+24/-4)
  - 修改 `vllm_ascend/worker/v2/sample/gumbel.py` (+3/-3)
  - 修改 `vllm_ascend/worker/v2/spec_decode/rejection_sampler_utils.py` (+16/-2)
  - Ascend 影响: ✓ 无影响

- **[1823e572](https://github.com/vllm-project/vllm-ascend/commit/1823e5720d0d225665b5e9ea352e295b7f665222)** ([#15895](https://github.com/vllm-project/vllm-ascend/pull/15895)) [Bug修复]Fix backend input string path 为 sfa. (#15895)
  - 标签: `bugfix`, `low-risk`, `mrv2`, `attention`, `dsa-sfa`
  - 变更文件:
  - 修改 `vllm_ascend/attention/indexer.py` (+1/-1)
  - 修改 `vllm_ascend/attention/sfa_v1.py` (+1/-1)
  - Ascend 影响: ✓ 无影响

- **[d12d0381](https://github.com/vllm-project/vllm-ascend/commit/d12d03818faa62ffd40b28b45297defdf6d8e702)** ([#15633](https://github.com/vllm-project/vllm-ascend/pull/15633)) [Bugfix] 修复 eplb v2 使用 unquant type (#15633)
  - 标签: `bugfix`, `low-risk`, `mrv2`, `quantization`, `moe`, `eplb`
  - 变更文件:
  - 修改 `vllm_ascend/ops/fused_moe/routed_experts.py` (+13/-5)
  - Ascend 影响: ✓ 无影响

- **[d8870515](https://github.com/vllm-project/vllm-ascend/commit/d88705159109f66e24b96421c522e55dc3c3ba11)** ([#15954](https://github.com/vllm-project/vllm-ascend/pull/15954)) [Bugfix] Keep DFlash/DSpark DP metadata 在 CPU 期间 graph replay (#15954)
  - 标签: `bugfix`, `low-risk`, `mrv2`, `spec-decode`, `cudagraph`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/spec_decode/dflash/aclgraph.py` (+3/-1)
  - Ascend 影响: ✓ 无影响

- **[bddca22d](https://github.com/vllm-project/vllm-ascend/commit/bddca22da347068037de66731a197b5f81671331)** ([#15817](https://github.com/vllm-project/vllm-ascend/pull/15817)) [Bugfix] 约束 slot mapping block table staging (#15817)
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `kv-cache`, `tests`
  - 变更文件:
  - 修改 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_compute_slot_mapping.py` (+61/-0)
  - 修改 `vllm_ascend/ops/triton/v2/block_table/compute_slot_mappings.py` (+16/-9)
  - 修改 `vllm_ascend/ops/triton/v2/block_table/docs/compute_slot_mappings.md` (+14/-7)
  - 修改 `vllm_ascend/worker/v2/block_table.py` (+8/-0)
  - Ascend 影响: ✓ 无影响

- **[6e6aad57](https://github.com/vllm-project/vllm-ascend/commit/6e6aad57e29a24aed1fe4367b8e3120cde23c8c9)** ([#15573](https://github.com/vllm-project/vllm-ascend/pull/15573)) [Feature] 优化 resample_kernel 使用 150x speed up (#15573)
  - 标签: `feature`, `high-risk`, `mrv2`, `tests`, `spec-decode`, `sampling`
  - 变更文件:
  - 修改 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_resample.py` (+707/-587)
  - 删除 `vllm_ascend/ops/triton/docs/resample.md` (+0/-223)
  - 新增 `vllm_ascend/ops/triton/docs/v2/spec_decode/resample.md` (+266/-0)
  - 新增 `vllm_ascend/ops/triton/v2/spec_decode/__init__.py` (+0/-0)
  - 新增 `vllm_ascend/ops/triton/v2/spec_decode/resample.py` (+399/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/rejection_sampler_utils.py` (+9/-203)
  - Ascend 影响: ✓ 无影响

---

## 2026-09-07
### vllm
- **[6fbb00b1](https://github.com/vllm-project/vllm/commit/6fbb00b18874e27ba7d7adc0a3b8e93fee763ab1)** ([#41567](https://github.com/vllm-project/vllm/pull/41567)) [EPD] 新增 ECMooncakeConnector 用于基于 Mooncake TransferEngine 的 encoder cache
  - 标签: `feature`, `mrv2`, `high-risk`, `ec-transfer`, `epd`, `mooncake`, `encoder-cache`, `distributed`
  - 变更文件（共 30 个）:
  - 修改 `.buildkite/test_areas/disaggregated_mooncake.yaml` (+54/-0)
  - 修改 `examples/disaggregated/disaggregated_encoder/disagg_epd_proxy.py` (+336/-95)
  - 修改 `tests/v1/core/test_encoder_cache_manager.py` (+32/-0)
  - 修改 `tests/v1/core/test_scheduler.py` (+89/-3)
  - 修改 `tests/v1/ec_connector/integration/README.md` (+212/-170)
  - 新增 `tests/v1/ec_connector/integration/run_epd_mooncake_ec_full_pipeline.sh` (+289/-0)
  - 修改 `tests/v1/ec_connector/integration/test_epd_correctness.py` (+88/-23)
  - 新增 `tests/v1/ec_connector/unit/test_epd_proxy_retry.py` (+172/-0)
  - 修改 `tests/v1/ec_connector/unit/test_epd_proxy_round_robin.py` (+48/-2)
  - 修改 `tests/v1/ec_connector/unit/test_worker_ec_connector.py` (+26/-0)
  - ... 及其他 20 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 为 MRV2 commit，触及 vllm/v1/worker/gpu/ec_connector.py 与 vllm/v1/worker/gpu_worker.py（vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner 并覆盖 gpu_worker 路径）。新增的 ec_connector_model_runner_mixin 与 gpu/ec_connector.py 会传递到 Ascend worker 路径，vllm-ascend 需评估 EC connector 在 NPUModelRunner 中的集成，以及 Mooncake TransferEngine 在 Ascend 通信（HCCL）下的可行性与正确性；vllm/v1/core/sched/scheduler.py 的 EC 调度接入也会影响 Ascend 调度路径
    - 建议测试区域: `NPUModelRunner ec_connector 集成`, `Mooncake TransferEngine 在 Ascend 上的传输正确性`, `EC 调度与 core scheduler 交互`, `EPD 分离式架构 Ascend 端到端`

### vllm-ascend
- **[8bd1d5a7](https://github.com/vllm-project/vllm-ascend/commit/8bd1d5a79c4a6268ed6f08bf0b097919cc15665a)** ([#15863](https://github.com/vllm-project/vllm-ascend/pull/15863)) [Performance] 跳过恒等 EAGLE3 词表重映射
  - 标签: `performance`, `low-risk`, `mrv2`, `spec-decode`, `eagle3`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+23/-0)
  - Ascend 影响: ✓ 无影响

- **[c0b5b5ed](https://github.com/vllm-project/vllm-ascend/commit/c0b5b5ed304e2c742e2d858b04be9ba3e7990bc5)** ([#15873](https://github.com/vllm-project/vllm-ascend/pull/15873)) [BugFix][Spec Decode] 在 MRV2 中支持 draft enforce_eager
  - 标签: `bugfix`, `low-risk`, `mrv2`, `spec-decode`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+2/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dflash/speculator.py` (+2/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dspark/speculator.py` (+2/-0)
  - Ascend 影响: ✓ 无影响

- **[fd815467](https://github.com/vllm-project/vllm-ascend/commit/fd815467c221ee600137f6bdd53fe354d5e7c999)** ([#14872](https://github.com/vllm-project/vllm-ascend/pull/14872)) [CI] main2main vllm 0828 升级
  - 标签: `ci`, `high-risk`, `mrv2`, `upgrade`, `main2main`
  - 变更文件（共 86 个）:
  - 修改 `.github/vllm-main-verified.commit` (+1/-1)
  - 修改 `tests/e2e/conftest.py` (+3/-9)
  - 修改 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_num_nans.py` (+0/-10)
  - 修改 `tests/e2e/pull_request/four_card/context_parallel/test_accuracy_v2.py` (+12/-5)
  - 修改 `tests/e2e/pull_request/one_card/test_model_runner_v1_with_device.py` (+16/-1)
  - 修改 `tests/e2e/pull_request/two_card/rlhf/consistency/test_moe_routing_replay.py` (+0/-3)
  - 修改 `tests/ut/_310p/test_model_runner_310p.py` (+4/-0)
  - 修改 `tests/ut/_310p/test_model_runner_v2_310p.py` (+149/-7)
  - 修改 `tests/ut/attention/test_dsa_v1.py` (+44/-4)
  - 修改 `tests/ut/core/test_profiling_chunk.py` (+1/-8)
  - ... 及其他 76 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-09-05
### vllm
- **[d87a440f](https://github.com/vllm-project/vllm/commit/d87a440f88e28e5b37f9b1e22ce214d0426d5352)** ([#50514](https://github.com/vllm-project/vllm/pull/50514)) [Core] 支持 eagle3 投机解码与流水线并行的组合
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `spec-decode`, `attention`, `distributed`
  - 变更文件（共 27 个）:
  - 修改 `tests/model_executor/test_qwen3_omni.py` (+3/-3)
  - 修改 `tests/models/kimi_k3/test_aux_attn_res_stream.py` (+14/-16)
  - 新增 `tests/v1/e2e/spec_decode/eagle/test_eagle3_pp.py` (+59/-0)
  - 新增 `tests/v1/worker/test_eagle3_aux_hidden_states_pp.py` (+26/-0)
  - 新增 `tests/v1/worker/test_spec_decode_embed_sharing_pp.py` (+110/-0)
  - 修改 `vllm/config/speculative.py` (+1/-1)
  - 修改 `vllm/config/vllm.py` (+0/-6)
  - 修改 `vllm/model_executor/models/deepseek_eagle3.py` (+1/-3)
  - 修改 `vllm/model_executor/models/interfaces.py` (+58/-1)
  - 修改 `vllm/model_executor/models/laguna_dflash.py` (+1/-3)
  - ... 及其他 17 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的核心覆盖路径 vllm/v1/worker/gpu/model_runner.py。vllm-ascend 的 MRV2 实现位于 vllm_ascend/worker/v2/，NPU 侧的 ModelRunner 继承/复用 GPU model_runner，新增的 spec decode + PP 调度逻辑、aux hidden states 传递与 embed sharing 会传导到 Ascend 子类。vllm-ascend 需评估 Eagle3 + PP 在 NPU（HCCL 通信）下的正确性，以及 v2/spec_decode/autoregressive 路径与上游 model_runner 的接口一致性。
    - 建议测试区域: `Ascend MRV2 Eagle3 spec decode + PP 端到端验证`, `aux hidden states 跨 stage HCCL 传递正确性`, `v2/spec_decode/autoregressive 与上游接口兼容性`, `DeepSeek/Qwen3 Eagle3 NPU 多卡 PP 场景`

- **[8277c42e](https://github.com/vllm-project/vllm/commit/8277c42e4c74c5dd604f29b6d938a3456658f247)** ([#55202](https://github.com/vllm-project/vllm/pull/55202)) [Perf] 在更多位置确保异步 H2D 拷贝使用 pinned 内存
  - 标签: `perf`, `medium-risk`, `attention`, `model-runner`, `distributed`, `kv-cache`
  - 变更文件（共 21 个）:
  - 修改 `tests/kernels/attention/test_flashinfer.py` (+2/-0)
  - 修改 `vllm/distributed/eplb/eplb_state.py` (+10/-1)
  - 修改 `vllm/distributed/kv_transfer/kv_connector/v1/example_hidden_states_connector.py` (+6/-4)
  - 修改 `vllm/model_executor/layers/attention/mla_attention.py` (+8/-2)
  - 修改 `vllm/model_executor/layers/fused_moe/modular_kernel.py` (+5/-1)
  - 修改 `vllm/model_executor/models/cosmos3_edge.py` (+2/-4)
  - 修改 `vllm/model_executor/models/ernie45_vl.py` (+4/-4)
  - 修改 `vllm/model_executor/models/glm_ocr.py` (+6/-2)
  - 修改 `vllm/model_executor/models/isaac.py` (+9/-3)
  - 修改 `vllm/model_executor/models/keye.py` (+41/-16)
  - ... 及其他 11 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的覆盖路径 vllm/model_executor/layers/attention/mla_attention.py。DeepSeek V3/R1 在 Ascend 上使用 MLA，mla_attention 中异步 H2D 拷贝的 pinned 内存处理会传导到 Ascend 的 MLA 推理路径。Ascend 的 H2D 语义与 CUDA 不同（NPU 显存与 host 间拷贝机制差异），需评估 pinned 等价机制在 NPU 上的正确性与收益。
    - 建议测试区域: `DeepSeek V3/R1 MLA Ascend 异步拷贝正确性`, `NPU host-device pinned 等价机制验证`, `多模态模型 Ascend 异步 H2D 路径`

### vllm-ascend
- **[9afd6a92](https://github.com/vllm-project/vllm-ascend/commit/9afd6a925d3eb336b41649cf1bfa8a9f746e64ce)** ([#15706](https://github.com/vllm-project/vllm-ascend/pull/15706)) [Feature] 支持 DSA PCP 与 MTP 组合
  - 标签: `feature`, `mrv2`, `high-risk`, `attention`, `distributed`, `context-parallel`, `spec-decode`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+3/-1)
  - 修改 `docs/source/user_guide/feature_guide/context_parallel.md` (+1/-1)
  - 修改 `tests/e2e/pull_request/four_card/context_parallel/test_accuracy_v2.py` (+0/-63)
  - 新增 `tests/e2e/pull_request/four_card/context_parallel/test_deepseek_v4.py` (+151/-0)
  - 修改 `tests/ut/attention/test_dsa_v1.py` (+24/-0)
  - 修改 `tests/ut/worker/test_mtp_pcp_speculator_v2.py` (+21/-4)
  - 修改 `vllm_ascend/attention/context_parallel/dsa_cp.py` (+27/-15)
  - 修改 `vllm_ascend/attention/utils.py` (+0/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/aclgraph.py` (+5/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+27/-13)
  - Ascend 影响: ✓ 无影响

---

## 2026-09-04
### vllm
- **[8f816a3f](https://github.com/vllm-project/vllm/commit/8f816a3f665489d7f0d222115d4f72ebab01076b)** ([#52358](https://github.com/vllm-project/vllm/pull/52358)) [Metrics] Support `CUDAGraphStat` in MRV2
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `cudagraph`, `metrics`, `tests`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_model_runner_v2_eplb.py` (+1/-0)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+12/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+9/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm/v1/worker/gpu/model_runner.py（vllm-ascend NPUModelRunner 继承 GPUModelRunner）和 vllm/v1/worker/gpu/cudagraph_utils.py。新增的 CUDAGraphStat 统计逻辑会传递到 NPUModelRunner。vllm-ascend 需评估 ACL Graph 场景下的统计行为是否兼容。
    - 建议测试区域: `ACL Graph 统计指标兼容性`, `NPUModelRunner CUDAGraphStat 继承验证`

- **[560ef78b](https://github.com/vllm-project/vllm/commit/560ef78bfe734ea894f8a866e50406574021b9f5)** ([#54901](https://github.com/vllm-project/vllm/pull/54901)) [Perf][Model Runner V2] Compact sampling masks on GPU instead of unpacking the full-vocab bitmask on CPU
  - 标签: `performance`, `mrv2`, `high-risk`, `model-runner`, `sampling`, `gpu`, `tests`
  - 变更文件:
  - 修改 `tests/entrypoints/scale_out/token_in_token_out/test_serving_tokens.py` (+7/-1)
  - 修改 `tests/test_config.py` (+16/-0)
  - 修改 `tests/v1/core/test_scheduler.py` (+47/-0)
  - 修改 `tests/v1/test_outputs.py` (+31/-37)
  - 修改 `vllm/config/vllm.py` (+7/-0)
  - 修改 `vllm/v1/engine/output_processor.py` (+3/-2)
  - 修改 `vllm/v1/outputs.py` (+12/-27)
  - 修改 `vllm/v1/worker/gpu/async_utils.py` (+1/-1)
  - 修改 `vllm/v1/worker/gpu/sample/output.py` (+60/-38)
  - 修改 `vllm/v1/worker/gpu/sample/sampler.py` (+3/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/sample/sampler.py 和 sample/output.py，这些文件虽不在 vllm-ascend 的直接覆盖路径列表中，但 NPUModelRunner 继承 GPUModelRunner 的采样逻辑。将 mask 压缩从 CPU 移到 GPU 的优化可能在 NPU 上需要适配（NPU 的 bitmask 操作可能与 GPU 不同）。
    - 建议测试区域: `NPU sampling mask 压缩正确性`, `NPUModelRunner 采样继承验证`

### vllm-ascend
- **[4a4503b9](https://github.com/vllm-project/vllm-ascend/commit/4a4503b9e448e2b2f6ab778d669f74381f075653)** ([#15269](https://github.com/vllm-project/vllm-ascend/pull/15269)) [Feature]Support full graph mode for DSV4 DSpark
  - 标签: `feature`, `mrv2`, `high-risk`, `dsa`, `deepseek-v4`, `full-graph`, `attention`, `spec-decode`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/model_runner_v2/test_deepseek_v4.py` (+13/-1)
  - 修改 `vllm_ascend/attention/context_parallel/dsa_cp.py` (+1/-0)
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+35/-3)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+4/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-09-03
### vllm
- **[ee0a4c46](https://github.com/vllm-project/vllm/commit/ee0a4c46ae771af034ae676d44e932469586e7be)** ([#55111](https://github.com/vllm-project/vllm/pull/55111)) [Bugfix] 在多节点 world size 校验中计入 PCP (#55111)
  - 标签: `bugfix`, `medium-risk`, `mrv2`, `pcp`, `distributed`, `config`, `tests`
  - 变更文件:
  - 修改 `tests/engine/test_arg_utils.py` (+19/-0)
  - 修改 `vllm/engine/arg_utils.py` (+6/-8)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm-ascend 正在积极支持 PCP（见 ascend #14960/#15524/#15482/#15390），PCP 多节点 world size 校验逻辑同样适用于 ascend 的 PCP 部署，需确认 ascend 多节点 PCP 启动校验一致

- **[facd9a74](https://github.com/vllm-project/vllm/commit/facd9a74a1cd1b9fed324cdc2cceb8d54fdad3d0)** ([#54856](https://github.com/vllm-project/vllm/pull/54856)) [Spec Decode] 当所有 speculator 为均匀解码时跳过 DP 同步 (#54856)
  - 标签: `perf`, `medium-risk`, `mrv2`, `spec-decode`, `distributed`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/dp_utils.py` (+13/-1)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` (+7/-1)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+8/-5)
  - 修改 `vllm/v1/worker/gpu/spec_decode/speculator.py` (+20/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm-ascend 有自有的 MRV2 spec decode（vllm_ascend/worker/v2/spec_decode/），DP 同步跳过逻辑需在 ascend 的 speculator/rejection sampler 中对齐，HCCL 通信下 uniform 判定需验证
    - 建议测试区域: `ascend MRV2 spec decode DP 一致性`, `ascend speculator uniform 解码判定`

### vllm-ascend
- **[35463578](https://github.com/vllm-project/vllm-ascend/commit/3546357838389aa7201d9b44e234f831e98b2fd4)** ([#14960](https://github.com/vllm-project/vllm-ascend/pull/14960)) [Feature] 在 PCP 下支持 MTP 与 Eagle3 投机解码 (#14960)
  - 标签: `feature`, `high-risk`, `mrv2`, `spec-decode`, `pcp`, `model-runner`, `tests`
  - 变更文件（共 15 个）:
  - 修改 `.github/workflows/configs/nightly_config.yaml` (+12/-0)
  - 修改 `docs/source/user_guide/feature_guide/context_parallel.md` (+48/-2)
  - 新增 `tests/e2e/nightly/single_node/models/configs/Eagle3-Qwen3-8B-BF16-PCP.yaml` (+53/-0)
  - 新增 `tests/e2e/nightly/single_node/models/configs/MTPX-DeepSeek-R1-0528-W8A8-PCP.yaml` (+54/-0)
  - 修改 `tests/e2e/pull_request/four_card/context_parallel/test_accuracy_v2.py` (+107/-1)
  - 修改 `tests/ut/test_platform.py` (+2/-0)
  - 修改 `tests/ut/worker/test_model_runner_v2.py` (+50/-1)
  - 新增 `tests/ut/worker/test_mtp_pcp_speculator_v2.py` (+348/-0)
  - 修改 `tests/ut/worker/test_pcp_manager_v2.py` (+296/-0)
  - 修改 `vllm_ascend/platform.py` (+3/-0)
  - ... 及其他 5 个文件
  - Ascend 影响: ✓ 无影响

- **[637417db](https://github.com/vllm-project/vllm-ascend/commit/637417dbd59b14b1db5f8e0390eef982b96be282)** ([#15556](https://github.com/vllm-project/vllm-ascend/pull/15556)) [Feature][Spec Decode] MRV2 支持合成拒绝采样 (#15556)
  - 标签: `feature`, `medium-risk`, `mrv2`, `spec-decode`, `tests`
  - 变更文件:
  - 修改 `docs/source/user_guide/feature_guide/speculative_decoding.md` (+6/-1)
  - 新增 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_rejection_sample_v2.py` (+155/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/rejection_sampler_utils.py` (+35/-12)
  - Ascend 影响: ✓ 无影响

- **[94354a5c](https://github.com/vllm-project/vllm-ascend/commit/94354a5cc166c2cd3b910a54ed57813131f66a45)** ([#15390](https://github.com/vllm-project/vllm-ascend/pull/15390)) [Refactor][Attention] 统一 MRV2 PCP MLA 元数据与实现 (#15390)
  - 标签: `refactor`, `medium-risk`, `mrv2`, `pcp`, `attention`, `mla`, `tests`
  - 变更文件:
  - 修改 `tests/ut/attention/test_mla_v1.py` (+151/-46)
  - 修改 `vllm_ascend/attention/mla_v1.py` (+119/-173)
  - Ascend 影响: ✓ 无影响

- **[93a17d68](https://github.com/vllm-project/vllm-ascend/commit/93a17d680f98df46bd29564344eca15547b0cd6c)** ([#15524](https://github.com/vllm-project/vllm-ascend/pull/15524)) [Feature] 支持 PCP 与 pp 组合 (#15524)
  - 标签: `feature`, `medium-risk`, `mrv2`, `pcp`, `pipeline-parallel`, `model-runner`, `tests`
  - 变更文件:
  - 修改 `tests/ut/worker/test_pcp_manager_v2.py` (+55/-3)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+10/-0)
  - 修改 `vllm_ascend/worker/v2/pcp_manager.py` (+8/-2)
  - Ascend 影响: ✓ 无影响

- **[86bca2f1](https://github.com/vllm-project/vllm-ascend/commit/86bca2f14435afc0036e0df60110dbbdc7e267b2)** ([#15212](https://github.com/vllm-project/vllm-ascend/pull/15212)) [Performance][Kernel] 在 Ascend 上优化 V2 slot 映射 (#15212)
  - 标签: `perf`, `medium-risk`, `mrv2`, `kernel`, `block-table`, `triton`, `tests`
  - 变更文件:
  - 新增 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_compute_slot_mapping.py` (+125/-0)
  - 新增 `vllm_ascend/ops/triton/v2/block_table/__init__.py` (+0/-0)
  - 新增 `vllm_ascend/ops/triton/v2/block_table/compute_slot_mappings.py` (+74/-0)
  - 新增 `vllm_ascend/ops/triton/v2/block_table/docs/compute_slot_mappings.md` (+133/-0)
  - 修改 `vllm_ascend/worker/v2/block_table.py` (+43/-0)
  - Ascend 影响: ✓ 无影响

- **[69efc63d](https://github.com/vllm-project/vllm-ascend/commit/69efc63d57762244c1e7ef5bb16a0c83adf982e5)** ([#15482](https://github.com/vllm-project/vllm-ascend/pull/15482)) [Feature] 支持 DSA PCP 与 ACLGraph 组合 (#15482)
  - 标签: `feature`, `high-risk`, `mrv2`, `pcp`, `aclgraph`, `attention`, `model-runner`, `tests`
  - 变更文件（共 12 个）:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+1/-1)
  - 修改 `docs/source/user_guide/feature_guide/context_parallel.md` (+5/-5)
  - 修改 `tests/e2e/coverage_taxonomy.py` (+1/-0)
  - 修改 `tests/e2e/pull_request/four_card/context_parallel/test_accuracy_v2.py` (+81/-23)
  - 修改 `tests/ut/attention/test_dsa_v1.py` (+174/-10)
  - 修改 `tests/ut/worker/test_attn_utils_v2.py` (+54/-5)
  - 修改 `tests/ut/worker/test_pcp_manager_v2.py` (+22/-27)
  - 修改 `vllm_ascend/attention/context_parallel/dsa_cp.py` (+123/-35)
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+6/-4)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+28/-25)
  - ... 及其他 2 个文件
  - Ascend 影响: ✓ 无影响

- **[8e79911c](https://github.com/vllm-project/vllm-ascend/commit/8e79911c25dcd749bafaf1ab90a9891e188c1de5)** ([#15406](https://github.com/vllm-project/vllm-ascend/pull/15406)) [Feature][310P] 在 310P 上为 Qwen3&3.5 适配 MRv2 Prefix Cache (#15406)
  - 标签: `feature`, `medium-risk`, `mrv2`, `prefix-cache`, `310p`, `model-runner`, `tests`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/_310p/test_model_runner_v2_310p.py` (+76/-4)
  - 修改 `tests/ut/_310p/test_model_runner_v2_310p.py` (+7/-0)
  - 修改 `vllm_ascend/_310p/worker/v2/model_runner.py` (+152/-17)
  - 修改 `vllm_ascend/_310p/worker/v2/model_state.py` (+109/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-09-02
### vllm
- **[1c26e57d](https://github.com/vllm-project/vllm/commit/1c26e57d3c7b480bae4e67898784b6b976a4a515)** ([#54782](https://github.com/vllm-project/vllm/pull/54782)) 对不可用的分段 CUDA graph 抛出异常
  - 标签: `bugfix`, `medium-risk`, `cuda-graph`, `model-runner`, `mrv2`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+20/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 有影响 - 命中 vllm-ascend 覆盖路径: vllm/v1/worker/gpu/cudagraph_utils.py
    - 建议测试区域: `MRV2 cudagraph_utils 回归`

### vllm-ascend
- **[8e288b1c](https://github.com/vllm-project/vllm-ascend/commit/8e288b1c67921b1e1f94ef49042b0000a11979cd)** ([#15593](https://github.com/vllm-project/vllm-ascend/pull/15593)) 回退 "[Test][CI] update skip_tests"
  - 标签: `chore`, `low-risk`, `ci`, `tests`
  - 变更文件:
  - 修改 `.github/workflows/scripts/select_tests.py` (+13/-5)
  - 修改 `.github/workflows/scripts/test_config.yaml` (+11/-29)
  - 修改 `.github/workflows/scripts/update_estimated_times.py` (+7/-5)
  - 修改 `tests/e2e/pull_request/four_card/context_parallel/test_accuracy_v2.py` (+3/-0)
  - 修改 `tests/e2e/pull_request/four_card/spec_decode/test_mtp_step3p5.py` (+1/-0)
  - 修改 `tests/e2e/pull_request/one_card/_310p/test_classification_310p.py` (+2/-0)
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_uva.py` (+1/-0)
  - 修改 `tests/e2e/pull_request/two_card/aclgraph/test_aclgraph_capture_replay.py` (+1/-0)
  - 修改 `tests/e2e/pull_request/two_card/lora/test_llama32_lora_tp2.py` (+1/-0)
  - 修改 `tests/e2e/pull_request/two_card/test_qwen3_performance.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

- **[14784edc](https://github.com/vllm-project/vllm-ascend/commit/14784edc8f3be4d92dee0b000775c117dfddfe19)** ([#15493](https://github.com/vllm-project/vllm-ascend/pull/15493)) 更新 skip_tests
  - 标签: `chore`, `low-risk`, `ci`, `tests`
  - 变更文件:
  - 修改 `.github/workflows/scripts/select_tests.py` (+5/-13)
  - 修改 `.github/workflows/scripts/test_config.yaml` (+29/-11)
  - 修改 `.github/workflows/scripts/update_estimated_times.py` (+5/-7)
  - 修改 `tests/e2e/pull_request/four_card/context_parallel/test_accuracy_v2.py` (+0/-3)
  - 修改 `tests/e2e/pull_request/four_card/spec_decode/test_mtp_step3p5.py` (+0/-1)
  - 修改 `tests/e2e/pull_request/one_card/_310p/test_classification_310p.py` (+0/-2)
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_uva.py` (+0/-1)
  - 修改 `tests/e2e/pull_request/two_card/aclgraph/test_aclgraph_capture_replay.py` (+0/-1)
  - 修改 `tests/e2e/pull_request/two_card/lora/test_llama32_lora_tp2.py` (+0/-1)
  - 修改 `tests/e2e/pull_request/two_card/test_qwen3_performance.py` (+0/-1)
  - Ascend 影响: ✓ 无影响

- **[730f1337](https://github.com/vllm-project/vllm-ascend/commit/730f1337b2341ed166b34f99aeb314efda2876b2)** ([#15264](https://github.com/vllm-project/vllm-ascend/pull/15264)) 将 SFA PCP graph 精度测试移至四卡
  - 标签: `chore`, `low-risk`, `ci`, `tests`, `mrv2`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+1/-1)
  - 修改 `tests/e2e/pull_request/eight_card/model_runner_v2/test_glm5_2.py` (+1/-49)
  - 修改 `tests/e2e/pull_request/four_card/context_parallel/test_accuracy_v2.py` (+56/-1)
  - Ascend 影响: ✓ 无影响

- **[35e7c6d8](https://github.com/vllm-project/vllm-ascend/commit/35e7c6d8bf7cd1065604e66f99ec16525e096beb)** ([#15405](https://github.com/vllm-project/vllm-ascend/pull/15405)) 修复 PP 下混合注意力模型的全图参数更新
  - 标签: `bugfix`, `medium-risk`, `model-runner`, `mrv2`, `tests`
  - 变更文件:
  - 修改 `tests/ut/models/minimax_m3/test_msa_m3.py` (+27/-0)
  - 修改 `vllm_ascend/models/minimax_m3/msa_m3.py` (+36/-0)
  - Ascend 影响: ✓ 无影响

- **[4e6fb74b](https://github.com/vllm-project/vllm-ascend/commit/4e6fb74b23d3f66a5dc1b20219dce04aa66e6941)** ([#15118](https://github.com/vllm-project/vllm-ascend/pull/15118)) 为 rejection sampling 禁用 AutoBlockify
  - 标签: `bugfix`, `low-risk`, `spec-decode`, `mrv2`, `tests`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/four_card/model_runner_v2/test_deepseek_v4.py` (+0/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/rejection_sampler_utils.py` (+6/-0)
  - Ascend 影响: ✓ 无影响

- **[95933b18](https://github.com/vllm-project/vllm-ascend/commit/95933b1849d5cd61356c0a6b87391589b252ea6b)** ([#15177](https://github.com/vllm-project/vllm-ascend/pull/15177)) 为 MRV2 resample 内核添加数值测试和算子文档
  - 标签: `chore`, `low-risk`, `tests`, `doc`, `ops`, `mrv2`
  - 变更文件:
  - 新增 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_resample.py` (+725/-0)
  - 新增 `vllm_ascend/ops/triton/docs/resample.md` (+223/-0)
  - Ascend 影响: ✓ 无影响

- **[89df31d7](https://github.com/vllm-project/vllm-ascend/commit/89df31d7ed27658101d84ac0c3968163b2bee29a)** ([#15210](https://github.com/vllm-project/vllm-ascend/pull/15210)) 支持 GLM5.2 rotation v2 Dspark
  - 标签: `feature`, `high-risk`, `spec-decode`, `mrv2`, `deepseek`, `tests`
  - 变更文件（共 11 个）:
  - 修改 `tests/e2e/coverage_taxonomy.py` (+1/-0)
  - 修改 `tests/e2e/pull_request/eight_card/model_runner_v2/test_glm5_2.py` (+59/-43)
  - 修改 `tests/ut/quantization/test_modelslim_config.py` (+1/-2)
  - 新增 `tests/ut/spec_decode/test_dspark_speculator.py` (+100/-0)
  - 修改 `vllm_ascend/models/deepseek_v4/dspark.py` (+1/-1)
  - 修改 `vllm_ascend/models/kimi_k3.py` (+1/-1)
  - 修改 `vllm_ascend/models/kimi_k3_dspark.py` (+6/-6)
  - 修改 `vllm_ascend/models/llama_eagle3.py` (+5/-27)
  - 修改 `vllm_ascend/models/qwen3_dspark.py` (+3/-3)
  - 修改 `vllm_ascend/utils.py` (+29/-0)
  - ... 及其他 1 个文件
  - Ascend 影响: ✓ 无影响

- **[8a4ea147](https://github.com/vllm-project/vllm-ascend/commit/8a4ea1478b2eefcc516ce687674c7bef3db1f0eb)** ([#15391](https://github.com/vllm-project/vllm-ascend/pull/15391)) 统一 MRV2 PCP GQA 元数据和实现
  - 标签: `refactor`, `medium-risk`, `attention`, `mrv2`, `platform`, `tests`
  - 变更文件:
  - 修改 `tests/ut/_310p/attention/test_attention_v1_310.py` (+7/-0)
  - 修改 `tests/ut/attention/test_attention_v1.py` (+55/-71)
  - 修改 `tests/ut/spec_decode/test_speculators_vwn_eagle3.py` (+0/-1)
  - 修改 `tests/ut/test_platform.py` (+83/-0)
  - 修改 `tests/ut/worker/test_pcp_manager_v2.py` (+7/-0)
  - 修改 `vllm_ascend/attention/attention_v1.py` (+94/-119)
  - 修改 `vllm_ascend/platform.py` (+18/-2)
  - 修改 `vllm_ascend/worker/v2/pcp_manager.py` (+0/-2)
  - Ascend 影响: ✓ 无影响

---

## 2026-09-01
### vllm
- **[adebc41b](https://github.com/vllm-project/vllm/commit/adebc41b7e9f1085d3f73434e23beb76883b9eb4)** ([#52506](https://github.com/vllm-project/vllm/pull/52506)) [Mamba] 新增 FlashInfer ReplaySSM backend
  - 标签: `feature`, `high-risk`, `attention`, `config`, `kv-cache`, `mamba`, `model-executor`, `model-runner`, `tests`, `warmup`, `mrv2`
  - 变更文件（共 19 个）:
  - 修改 `tests/kernels/mamba/test_ssu_dispatch.py` (+70/-2)
  - 新增 `tests/model_executor/test_replayssm_warmup.py` (+150/-0)
  - 修改 `tests/v1/attention/test_replayssm_metadata_builder.py` (+46/-12)
  - 修改 `tests/v1/e2e/test_replayssm_decode.py` (+37/-2)
  - 修改 `tests/v1/worker/test_kv_cache_allocation_scope.py` (+2/-2)
  - 修改 `tests/v1/worker/test_utils.py` (+57/-0)
  - 修改 `vllm/config/cache.py` (+6/-5)
  - 修改 `vllm/config/vllm.py` (+17/-2)
  - 修改 `vllm/model_executor/layers/mamba/mamba_mixer2.py` (+148/-37)
  - 修改 `vllm/model_executor/layers/mamba/mamba_utils.py` (+14/-8)
  - ... 及其他 9 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 MRV2 核心覆盖路径（vllm/v1/worker/gpu/model_runner.py、vllm/v1/worker/gpu/attn_utils.py），vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，需评估适配
    - 建议测试区域: `NPUModelRunner 继承路径`, `Ascend attention utils`

- **[e16b5e51](https://github.com/vllm-project/vllm/commit/e16b5e518db8ed54a9c82dd825d3a3d5502ef13e)** ([#50175](https://github.com/vllm-project/vllm/pull/50175)) [Feature] 迁移 generic MLA metadata 与 indexing kernels
  - 标签: `feature`, `high-risk`, `attention`, `deepseek`, `doc`, `eplb`, `mla`, `model-executor`, `model-runner`, `tests`, `warmup`, `mrv2`
  - 变更文件（共 17 个）:
  - 修改 `docs/contributing/jit_kernel_warmup.md` (+10/-8)
  - 修改 `tests/model_executor/layers/test_fused_shared_expert.py` (+1/-0)
  - 修改 `tests/model_executor/test_jit_warmup.py` (+29/-0)
  - 修改 `tests/v1/attention/test_indexer_deepseek_v4_slot_mapping.py` (+43/-2)
  - 修改 `tests/v1/worker/test_gpu_model_runner_v2_eplb.py` (+2/-0)
  - 修改 `vllm/model_executor/layers/attention/mla_attention.py` (+47/-0)
  - 修改 `vllm/model_executor/warmup/jit_warmup.py` (+5/-1)
  - 修改 `vllm/model_executor/warmup/jit_warmup_triton_helper.py` (+90/-10)
  - 修改 `vllm/model_executor/warmup/kernel_warmup.py` (+0/-4)
  - 删除 `vllm/model_executor/warmup/sparse_mla_triton_warmup.py` (+0/-111)
  - ... 及其他 7 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 MRV2 核心覆盖路径（vllm/v1/worker/gpu/model_runner.py、vllm/model_executor/layers/attention/mla_attention.py），vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，需评估适配
    - 建议测试区域: `NPUModelRunner 继承路径`, `MLA on Ascend`

- **[c28feab9](https://github.com/vllm-project/vllm/commit/c28feab98919739ae6d2041c31c94a3b11718590)** ([#54646](https://github.com/vllm-project/vllm/pull/54646)) [Core] 冻结 gc during V2 CG capture; skip per-descriptor cleanup
  - 标签: `feature`, `high-risk`, `model-runner`, `mrv2`
  - 变更文件:
  - 修改 `vllm/compilation/breakable_cudagraph.py` (+7/-9)
  - 修改 `vllm/utils/gc_utils.py` (+29/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+40/-36)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+2/-23)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 MRV2 核心覆盖路径（vllm/v1/worker/gpu/model_runner.py），vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，需评估适配
    - 建议测试区域: `NPUModelRunner 继承路径`

- **[6bafc049](https://github.com/vllm-project/vllm/commit/6bafc049aae6c26e210162630914ee9177a4b586)** ([#54436](https://github.com/vllm-project/vllm/pull/54436)) [Bugfix] Never drop decoding request 从 sampled-token broadcast
  - 标签: `bugfix`, `high-risk`, `model-runner`, `pcp`, `pipeline-parallel`, `tests`, `mrv2`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_batch_shard.py` (+0/-1)
  - 新增 `tests/v1/worker/test_pp_utils.py` (+83/-0)
  - 修改 `vllm/v1/worker/gpu/input_batch.py` (+0/-4)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+0/-6)
  - 修改 `vllm/v1/worker/gpu/pcp_manager.py` (+0/-3)
  - 修改 `vllm/v1/worker/gpu/pp_utils.py` (+4/-8)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 命中 MRV2 核心覆盖路径（vllm/v1/worker/gpu/model_runner.py），vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，需评估适配
    - 建议测试区域: `NPUModelRunner 继承路径`

### vllm-ascend
- **[8b72fdb9](https://github.com/vllm-project/vllm-ascend/commit/8b72fdb97b2b0d8eccaf6ac7ac414a151e09810e)** ([#14822](https://github.com/vllm-project/vllm-ascend/pull/14822)) [Feature] 支持 Eagle3 与 DSpark 使用 PP
  - 标签: `feature`, `high-risk`, `ci`, `config`, `deepseek`, `pipeline-parallel`, `spec-decode`, `tests`, `mrv2`
  - 变更文件（共 11 个）:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+1/-0)
  - 新增 `tests/e2e/pull_request/eight_card/model_runner_v2/test_spec_pp_accuracy.py` (+122/-0)
  - 修改 `vllm_ascend/models/deepseek_v4/model.py` (+26/-6)
  - 修改 `vllm_ascend/models/minimax_m3/minimax_m3.py` (+30/-7)
  - 修改 `vllm_ascend/patch/platform/patch_pp_mtp.py` (+7/-5)
  - 修改 `vllm_ascend/patch/platform/patch_use_v2_model_runner.py` (+12/-0)
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_dspark.py` (+31/-1)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+16/-4)
  - 新增 `vllm_ascend/worker/v2/pp_utils.py` (+196/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+5/-0)
  - ... 及其他 1 个文件
  - Ascend 影响: ✓ 无影响

- **[6528d90f](https://github.com/vllm-project/vllm-ascend/commit/6528d90fa3e53258938a7ef2ceb0c617f26029a1)** ([#15304](https://github.com/vllm-project/vllm-ascend/pull/15304)) [CI] 新增 Qwen3-8B-eagle3-DSD E2E
  - 标签: `chore`, `low-risk`, `ci`, `config`, `tests`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+1/-0)
  - 新增 `tests/e2e/pull_request/one_card/model_runner_v2/test_qwen3_8B.py` (+89/-0)
  - 修改 `tests/e2e/pull_request/utils.py` (+2/-1)
  - Ascend 影响: ✓ 无影响

- **[e8f47fc1](https://github.com/vllm-project/vllm-ascend/commit/e8f47fc11c81f3eb3efeb9b40400db8b0fa6eef3)** ([#15155](https://github.com/vllm-project/vllm-ascend/pull/15155)) [Feature] 支持 SFA DCP 在 model runner v2
  - 标签: `feature`, `high-risk`, `ci`, `config`, `sfa`, `tests`, `mrv2`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+1/-0)
  - 新增 `tests/e2e/pull_request/four_card/context_parallel/test_accuracy_v2.py` (+154/-0)
  - 修改 `tests/ut/attention/test_sfa_cp.py` (+2/-0)
  - 修改 `tests/ut/worker/test_attn_utils_v2.py` (+59/-2)
  - 修改 `vllm_ascend/attention/context_parallel/sfa_cp.py` (+3/-0)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+14/-1)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+27/-4)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-31
### vllm
- **[e126687a](https://github.com/vllm-project/vllm/commit/e126687a9a828d513c01a07cd69f025f27d63280)** ([#53896](https://github.com/vllm-project/vllm/pull/53896)) [Model] 支持 Qwen3.8-Flash-Next 模型
  - 标签: `feature`, `mrv2`, `high-risk`, `model`, `qwen4-exp`, `moe`, `mamba`, `kv-cache`, `scheduler`, `attention`, `distributed`, `tests`
  - 变更文件（共 124 个）:
  - 修改 `.buildkite/test_areas/lm_eval.yaml` (+36/-0)
  - 修改 `.buildkite/test_areas/models_basic.yaml` (+37/-0)
  - 修改 `.buildkite/test_areas/spec_decode.yaml` (+1/-0)
  - 修改 `csrc/libtorch_stable/gdn/fused_gdn_decode_kernel.cu` (+26/-10)
  - 修改 `csrc/libtorch_stable/ops.h` (+1/-1)
  - 修改 `csrc/libtorch_stable/torch_bindings.cpp` (+2/-1)
  - 修改 `tests/config/test_config_utils.py` (+19/-0)
  - 修改 `tests/config/test_speculative_draft_hf_overrides.py` (+52/-1)
  - 修改 `tests/distributed/test_custom_all_reduce.py` (+23/-0)
  - 新增 `tests/evals/qwen4_exp/README.md` (+14/-0)
  - ... 及其他 114 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的核心覆盖路径：vllm/v1/worker/gpu/model_runner.py（vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner）、vllm/v1/worker/gpu/block_table.py（vllm-ascend 通过 block_table_patch 覆盖）、vllm/v1/worker/gpu/model_states/mamba_hybrid.py 与 warmup.py（vllm-ascend 覆盖 model_states 路径）。新增的 qwen4_exp 模型若需在 Ascend 上支持，NPUModelRunner 的 warmup、block_table、mamba_hybrid state 集成需评估适配。此外 KV cache 管理器与 scheduler 对 Mamba 的适配也需在 Ascend 验证。
    - 建议测试区域: `NPUModelRunner 对 model_runner.py 新接口的兼容`, `block_table_patch 与新 block_table.py 一致性`, `mamba_hybrid state 在 Ascend 的集成`, `warmup 路径在 Ascend 的回归`, `qwen4_exp 模型 Ascend 可行性评估`

### vllm-ascend
- **[f8c81e37](https://github.com/vllm-project/vllm-ascend/commit/f8c81e3795e067f3892a312e2d7435d607a587c0)** ([#14525](https://github.com/vllm-project/vllm-ascend/pull/14525)) [Feature] 在 A2/A3 上优化 triton ops grammar_bitmask
  - 标签: `feature`, `mrv2`, `medium-risk`, `triton`, `structured-outputs`, `grammar`, `a2`, `a3`, `tests`
  - 变更文件:
  - 新增 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_apply_grammar_bitmask_triton.py` (+95/-0)
  - 新增 `vllm_ascend/ops/triton/v2/apply_grammar_bitmask.py` (+110/-0)
  - 新增 `vllm_ascend/ops/triton/v2/docs/apply_grammar_bitmask.md` (+188/-0)
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_triton.py` (+3/-3)
  - 删除 `vllm_ascend/worker/v2/structured_outputs.py` (+0/-68)
  - Ascend 影响: ✓ 无影响

- **[a8501e3d](https://github.com/vllm-project/vllm-ascend/commit/a8501e3d21d84e1cbf9087ab5a848531b9bdb0ae)** ([#15376](https://github.com/vllm-project/vllm-ascend/pull/15376)) [Refactor][Device][5/N] 将注意力与量化迁移到硬件 profile
  - 标签: `refactor`, `mrv2`, `medium-risk`, `attention`, `quantization`, `hardware-profile`, `device`, `v1`, `v2`, `tests`
  - 变更文件（共 16 个）:
  - 修改 `tests/ut/attention/a2/test_attention_v1.py` (+5/-1)
  - 修改 `tests/ut/attention/a2/test_mla_v1.py` (+8/-11)
  - 修改 `tests/ut/device/test_hardware_profile.py` (+8/-0)
  - 修改 `tests/ut/quantization/test_utils.py` (+22/-11)
  - 修改 `tests/ut/worker/test_attn_utils_v2.py` (+4/-3)
  - 修改 `vllm_ascend/attention/attention_v1.py` (+3/-2)
  - 修改 `vllm_ascend/attention/context_parallel/dsa_cp.py` (+8/-6)
  - 修改 `vllm_ascend/attention/dsa_v1.py` (+5/-5)
  - 修改 `vllm_ascend/attention/mla_v1.py` (+18/-18)
  - 修改 `vllm_ascend/attention/sfa_v1.py` (+2/-3)
  - ... 及其他 6 个文件
  - Ascend 影响: ✓ 无影响

- **[cde915d2](https://github.com/vllm-project/vllm-ascend/commit/cde915d2b56edb6483cef7fd77b9bfbeb03cb059)** ([#15354](https://github.com/vllm-project/vllm-ascend/pull/15354)) [BugFix] 隔离 Eagle draft 的并行配置
  - 标签: `bugfix`, `mrv2`, `low-risk`, `spec-decode`, `eagle`, `worker`, `v2`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/spec_decode/eagle/speculator.py` (+17/-2)
  - Ascend 影响: ✓ 无影响

- **[40f9834e](https://github.com/vllm-project/vllm-ascend/commit/40f9834ee82aadfa4656ec65e5bd84f4d6241b5f)** ([#14342](https://github.com/vllm-project/vllm-ascend/pull/14342)) [BugFix][310P] 修复 310P 上 MTP overlay prefixcache 精度问题
  - 标签: `bugfix`, `low-risk`, `310p`, `mtp`, `prefix-cache`, `model-runner`
  - 变更文件:
  - 修改 `tests/ut/_310p/test_mamba_align_fallback_310p_source.py` (+2/-0)
  - 修改 `tests/ut/_310p/test_model_runner_310p.py` (+2/-0)
  - 修改 `vllm_ascend/_310p/model_runner_310p.py` (+3/-10)
  - 修改 `vllm_ascend/patch/worker/patch_mamba_utils.py` (+4/-1)
  - Ascend 影响: ✓ 无影响

- **[88538de8](https://github.com/vllm-project/vllm-ascend/commit/88538de84b09638249f9774ed82b1739ff74f8f4)** ([#15259](https://github.com/vllm-project/vllm-ascend/pull/15259)) [BugFix] 修复流水线并行下的专家传输
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `eplb`, `pipeline-parallelism`, `moe`, `distributed`
  - 变更文件:
  - 修改 `tests/ut/distributed/eplb/test_communicator.py` (+32/-1)
  - 修改 `vllm_ascend/distributed/eplb/communicator.py` (+37/-0)
  - Ascend 影响: ✓ 无影响

- **[75133ed7](https://github.com/vllm-project/vllm-ascend/commit/75133ed739e1ea62e4bc6ef8c76ec5b7963bc278)** ([#15006](https://github.com/vllm-project/vllm-ascend/pull/15006)) [Feature][310P] 在 310P 上为 Qwen3-VL+Qwen3.5 适配 MRv2
  - 标签: `feature`, `mrv2`, `high-risk`, `310p`, `qwen3-vl`, `qwen3.5`, `multimodal`, `worker`, `v2`, `quantization`, `tests`
  - 变更文件（共 13 个）:
  - 修改 `tests/e2e/pull_request/four_card/_310p/test_model_runner_v2_310p.py` (+18/-0)
  - 新增 `tests/ut/_310p/ops/test_qwen3vl_310.py` (+17/-0)
  - 修改 `tests/ut/_310p/quantization/test_w8a8_dynamic_310.py` (+16/-26)
  - 修改 `tests/ut/_310p/test_model_runner_v2_310p.py` (+137/-1)
  - 修改 `vllm_ascend/_310p/ops/fla/gdn_310.py` (+20/-17)
  - 修改 `vllm_ascend/_310p/quantization/methods/w8a8_dynamic.py` (+4/-0)
  - 新增 `vllm_ascend/_310p/worker/v2/kv_block_zeroer.py` (+38/-0)
  - 修改 `vllm_ascend/_310p/worker/v2/model_runner.py` (+141/-54)
  - 修改 `vllm_ascend/_310p/worker/v2/model_state.py` (+120/-22)
  - 新增 `vllm_ascend/_310p/worker/v2/rope.py` (+113/-0)
  - ... 及其他 3 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-08-30
### vllm
- **[5e71a11e](https://github.com/vllm-project/vllm/commit/5e71a11eb2b595ede15ecc39c7dddca38e03deb5)** ([#54326](https://github.com/vllm-project/vllm/pull/54326)) [CI] 为 L4 GPU 测试步骤标注 device: l4 以支持 EKS 迁移
  - 标签: `ci`, `low-risk`, `ci-infra`
  - 变更文件（共 13 个）:
  - 修改 `.buildkite/test_areas/crcr_report.yaml` (+2/-1)
  - 修改 `.buildkite/test_areas/disaggregated.yaml` (+10/-0)
  - 修改 `.buildkite/test_areas/distributed.yaml` (+9/-0)
  - 修改 `.buildkite/test_areas/engine.yaml` (+1/-0)
  - 修改 `.buildkite/test_areas/expert_parallelism.yaml` (+1/-0)
  - 修改 `.buildkite/test_areas/lora.yaml` (+1/-0)
  - 修改 `.buildkite/test_areas/misc.yaml` (+2/-0)
  - 修改 `.buildkite/test_areas/model_runner_v2.yaml` (+2/-0)
  - 修改 `.buildkite/test_areas/models_distributed.yaml` (+1/-0)
  - 修改 `.buildkite/test_areas/plugins.yaml` (+2/-0)
  - ... 及其他 3 个文件
  - Ascend 影响: ✓ 无影响

- **[b383e163](https://github.com/vllm-project/vllm/commit/b383e163961650c663ad2062544ecbee1b56afc8)** ([#54044](https://github.com/vllm-project/vllm/pull/54044)) [Bugfix] 在 profiling teardown 时重置缓存的 Mamba align metadata
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `model-runner`, `cudagraph`, `mamba`, `tests`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_model_runner_v2_cudagraph_profiling.py` (+36/-0)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+8/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/worker/gpu/cudagraph_utils.py 不在 vllm-ascend 的显式覆盖路径列表中，但 vllm-ascend 的 ModelAclGraphManager 继承自 vllm 的 ModelCudaGraphManager，profiling teardown 重置 Mamba align metadata 的逻辑可能传导到 Ascend 的 ACL graph capture 流程。若 Ascend 上启用 Mamba/SSM 模型并使用 cudagraph profiling，需验证 teardown 清理路径在 ACL graph 下生效。
    - 建议测试区域: `Ascend ACL graph profiling teardown 后 Mamba align metadata 重置验证`, `Mamba 模型在 Ascend 上 cudagraph capture 正确性回归`

- **[dbf662c9](https://github.com/vllm-project/vllm/commit/dbf662c9e810ef4c3f466c7c4b2b3282ba889622)** ([#51171](https://github.com/vllm-project/vllm/pull/51171)) [ROCm][MLA] 让 AITER MLA 投机解码达到 FULL cudagraph
  - 标签: `perf`, `medium-risk`, `attention`, `mla`, `rocm`, `spec-decode`, `cudagraph`, `tests`
  - 变更文件:
  - 修改 `tests/kernels/attention/test_rocm_aiter_mla_causal_verify_mask.py` (+48/-71)
  - 修改 `tests/v1/attention/test_rocm_aiter_mla_mtp_split.py` (+48/-2)
  - 修改 `vllm/v1/attention/backends/mla/rocm_aiter_mla.py` (+55/-54)
  - 修改 `vllm/v1/attention/backends/mla/triton_mla.py` (+30/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-29
### vllm
- **[cacc429f](https://github.com/vllm-project/vllm/commit/cacc429f62c3738c9c95093e9bd410e96103221a)** ([#50920](https://github.com/vllm-project/vllm/pull/50920)) [ROCm][CI] Stage E 门控
  - 标签: `chore`, `low-risk`, `rocm`, `ci`, `buildkite`
  - 变更文件:
  - 修改 `.buildkite/test_areas/compile.yaml` (+43/-0)
  - 修改 `.buildkite/test_areas/cuda.yaml` (+25/-0)
  - 修改 `.buildkite/test_areas/docker.yaml` (+16/-0)
  - 修改 `.buildkite/test_areas/e2e_integration.yaml` (+20/-0)
  - 修改 `.buildkite/test_areas/kernels.yaml` (+14/-0)
  - 修改 `.buildkite/test_areas/lm_eval.yaml` (+16/-0)
  - 修改 `.buildkite/test_areas/model_runner_v2.yaml` (+16/-0)
  - 修改 `.buildkite/test_areas/models_basic.yaml` (+8/-0)
  - 修改 `.buildkite/test_areas/models_language.yaml` (+33/-0)
  - 修改 `.buildkite/test_areas/rust_frontend.yaml` (+43/-0)
  - Ascend 影响: ✓ 无影响

- **[d3d79ffc](https://github.com/vllm-project/vllm/commit/d3d79ffc1e036a3263ba8497a3596a4767caf799)** ([#50488](https://github.com/vllm-project/vllm/pull/50488)) [Bugfix][Spec Decode] 默认捕获最宽的均匀解码批次
  - 标签: `bugfix`, `mrv2`, `high-risk`, `spec-decode`, `cudagraph`, `model-runner`, `compilation`, `tests`
  - 变更文件:
  - 修改 `tests/compile/test_config.py` (+441/-0)
  - 修改 `tests/v1/cudagraph/test_cudagraph_manager.py` (+8/-10)
  - 修改 `tests/v1/spec_decode/test_dynamic_sd_cug.py` (+35/-4)
  - 修改 `vllm/config/compilation.py` (+3/-1)
  - 修改 `vllm/config/vllm.py` (+122/-6)
  - 修改 `vllm/v1/worker/gpu/cudagraph_utils.py` (+12/-9)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改 vllm/v1/worker/gpu/cudagraph_utils.py，该文件属于 MRV2 Cuda Graph 核心路径。vllm-ascend 的 ModelAclGraphManager 继承自 vllm 的 ModelCudaGraphManager，推测解码的均匀批次捕获策略可能传递到 Ascend 的 ACL Graph 捕获逻辑。需评估“最宽均匀解码批次”策略在 Ascend NPU + ACL Graph 下的正确性与 graph 复用行为。
    - 建议测试区域: `Ascend ACL Graph + 动态推测解码批次捕获`, `widest uniform decode batch 在 NPU 上的复用`, `Dynamic SD + Full Cuda Graph 在 Ascend 的兼容性`

- **[fb680251](https://github.com/vllm-project/vllm/commit/fb6802513850d387e13ec231a0d3aa11d2754414)** ([#54162](https://github.com/vllm-project/vllm/pull/54162)) [Bugfix] 进程内引擎关闭时释放模型与 KV cache
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `engine`, `kv-cache`, `model-runner`, `tests`
  - 变更文件:
  - 新增 `tests/models/test_language_model_cache_is_weak.py` (+59/-0)
  - 新增 `tests/v1/engine/test_llm_engine_finalizer_is_weak.py` (+74/-0)
  - 修改 `vllm/model_executor/models/interfaces.py` (+4/-1)
  - 修改 `vllm/v1/engine/llm_engine.py` (+5/-2)
  - Ascend 影响: ✓ 无影响

- **[6d4562c5](https://github.com/vllm-project/vllm/commit/6d4562c59b97b4e35d459ff9389e71b6fe4995de)** ([#54277](https://github.com/vllm-project/vllm/pull/54277)) [Attention][DCP] 为 DSpark 推测起草启用 FlashInfer MLA
  - 标签: `feature`, `mrv2`, `medium-risk`, `attention`, `mla`, `spec-decode`, `dcp`, `flashinfer`, `tests`
  - 变更文件:
  - 修改 `tests/v1/attention/test_flashinfer_mla_dcp.py` (+33/-8)
  - 修改 `tests/v1/attention/test_mla_backends.py` (+2/-2)
  - 修改 `tests/v1/attention/test_mla_noncausal.py` (+3/-2)
  - 修改 `tests/v1/spec_decode/test_eagle_draft_attn_metadata.py` (+33/-0)
  - 修改 `vllm/v1/attention/backends/mla/flashinfer_mla.py` (+7/-2)
  - 修改 `vllm/v1/kv_cache_interface.py` (+6/-3)
  - 修改 `vllm/v1/worker/gpu/spec_decode/dflash/speculator.py` (+1/-11)
  - 修改 `vllm/v1/worker/gpu/spec_decode/speculator.py` (+13/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改 vllm/v1/worker/gpu/spec_decode/speculator.py 与 dflash/speculator.py，属 MRV2 spec_decode 核心路径，Ascend 推测解码路径会消费该 speculator。但 FlashInfer MLA 后端本身为 NVIDIA 专用，不直接用于 Ascend；需关注 speculator 接口变更是否影响 Ascend 推测解码起草器。
    - 建议测试区域: `Ascend 推测解码 speculator 接口适配`, `DSpark/draft speculator 在 NPU 上的行为`

- **[b2f68583](https://github.com/vllm-project/vllm/commit/b2f685834a6456197e7033966fdef52a23f1abcd)** ([#54160](https://github.com/vllm-project/vllm/pull/54160)) [Hy4] 支持 Hy4-preview 模型
  - 标签: `feature`, `mrv2`, `high-risk`, `model`, `hy4`, `rust`, `speculative`, `moe`, `mla`, `tests`
  - 变更文件（共 47 个）:
  - 修改 `docs/models/supported_models.md` (+2/-1)
  - 修改 `rust/src/chat/src/lib.rs` (+2/-2)
  - 修改 `rust/src/chat/src/parser/reasoning/mod.rs` (+3/-0)
  - 修改 `rust/src/chat/src/parser/tool/mod.rs` (+3/-0)
  - 修改 `rust/src/chat/src/parser/tool/tests.rs` (+4/-0)
  - 修改 `rust/src/chat/src/parser/unified.rs` (+34/-2)
  - 重命名 `rust/src/parser/src/reasoning/hy.rs` (+7/-7)
  - 修改 `rust/src/parser/src/reasoning/mod.rs` (+2/-2)
  - 重命名 `rust/src/parser/src/tool/hy.rs` (+250/-118)
  - 重命名 `rust/src/parser/src/tool/hy/structural_tag.rs` (+86/-23)
  - ... 及其他 37 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 有限影响 - 大部分文件为 NVIDIA 专用（vllm/models/hy_v4/nvidia/*）与 Rust 前端，Ascend 不直接使用。但 vllm/v1/worker/gpu/spec_decode/speculator.py 为 MRV2 共享路径，Ascend 推测解码消费该 speculator，需确认接口未破坏 Ascend 起草器。Hy4 模型本身暂无 Ascend 实现。
    - 建议测试区域: `Ascend speculator 接口兼容性`, `Hy4 模型未来 Ascend 移植评估`

- **[6c18a546](https://github.com/vllm-project/vllm/commit/6c18a5464852d9ddf4c59df8ec278ce1683a917e)** ([#54299](https://github.com/vllm-project/vllm/pull/54299)) [性能] 避免对非 pinned CPU tensor 的 H2D 拷贝
  - 标签: `perf`, `mrv2`, `medium-risk`, `multimodal`, `encoder-runner`, `attention`, `flashinfer`, `tests`
  - 变更文件（共 14 个）:
  - 修改 `vllm/model_executor/layers/pooler/tokwise/methods.py` (+2/-1)
  - 修改 `vllm/model_executor/model_loader/utils.py` (+11/-10)
  - 修改 `vllm/model_executor/models/ernie45_vl.py` (+3/-5)
  - 修改 `vllm/model_executor/models/glm4_1v.py` (+3/-3)
  - 修改 `vllm/model_executor/models/idefics2_vision_model.py` (+4/-1)
  - 修改 `vllm/model_executor/models/phi4mm_audio.py` (+3/-6)
  - 修改 `vllm/model_executor/models/qwen2_5_vl.py` (+5/-7)
  - 修改 `vllm/model_executor/models/qwen2_vl.py` (+3/-3)
  - 修改 `vllm/model_executor/models/qwen3_asr.py` (+3/-2)
  - 修改 `vllm/model_executor/models/qwen3_omni_moe_thinker.py` (+7/-7)
  - ... 及其他 4 个文件
  - Ascend 影响: ✓ 无影响

- **[68c52b5a](https://github.com/vllm-project/vllm/commit/68c52b5a937fe63c7a315739ad468f9d30fd483b)** ([#36255](https://github.com/vllm-project/vllm/pull/36255)) 修复：改进 token_ids_cpu swap 仅拷贝有效索引
  - 标签: `bugfix`, `low-risk`, `tpu`, `input-batch`, `model-runner`
  - 变更文件:
  - 修改 `vllm/v1/worker/tpu_input_batch.py` (+4/-4)
  - Ascend 影响: ✓ 无影响

### vllm-ascend
- **[28bf3a2e](https://github.com/vllm-project/vllm-ascend/commit/28bf3a2e8e8db396ee5dcfa6812626eee2d394ab)** ([#14100](https://github.com/vllm-project/vllm-ascend/pull/14100)) [Misc] 对齐 MRV2 公共代码逻辑与上游
  - 标签: `refactor`, `mrv2`, `medium-risk`, `model-runner`, `v2`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+31/-40)
  - Ascend 影响: ✓ 无影响

- **[843dd09a](https://github.com/vllm-project/vllm-ascend/commit/843dd09a9b315c21789d5d2663a7d15b2a0dca77)** ([#14887](https://github.com/vllm-project/vllm-ascend/pull/14887)) [重构][删除] 用当前 triton 实现替换上游 mrv2 apply_top_k_top_p 补丁
  - 标签: `refactor`, `mrv2`, `medium-risk`, `triton`, `ops`, `v2`
  - 变更文件:
  - 删除 `tests/e2e/nightly/single_node/ops/singlecard_ops/triton/test_apply_top_k_top_p_triton.py` (+0/-516)
  - 删除 `vllm_ascend/ops/triton/v2/sample/apply_top_k_top_p_triton.py` (+0/-883)
  - 删除 `vllm_ascend/ops/triton/v2/sample/docs/apply_top_k_top_p.md` (+0/-95)
  - 修改 `vllm_ascend/patch/worker/patch_v2/patch_triton.py` (+3/-3)
  - 新增 `vllm_ascend/worker/v2/sample/apply_top_k_top_p.py` (+14/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-08-28
### vllm-ascend
- **[d37529f4](https://github.com/vllm-project/vllm-ascend/commit/d37529f4df49e9da7a50123f4f810e4657e57013)** ([#14099](https://github.com/vllm-project/vllm-ascend/pull/14099)) [Feature][EPLB] 为 Model Runner V2 添加异步 EPLB 支持
  - 标签: `feature`, `mrv2`, `medium-risk`, `eplb`, `distributed`, `worker-v2`, `fused-moe`
  - 变更文件（共 36 个）:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+11/-3)
  - 修改 `docs/hooks/nav_titles.py` (+3/-3)
  - 重命名 `docs/source/developer_guide/Design_Documents/model_runner_v1_eplb.md` (+3/-1)
  - 修改 `docs/source/developer_guide/Design_Documents/model_runner_v2_eplb.md` (+36/-33)
  - 重命名 `docs/source/locale/zh_CN/LC_MESSAGES/developer_guide/Design_Documents/model_runner_v1_eplb.po` (+15/-2)
  - 修改 `docs/source/locale/zh_CN/LC_MESSAGES/developer_guide/Design_Documents/model_runner_v2_eplb.po` (+54/-59)
  - 修改 `docs/source/locale/zh_CN/LC_MESSAGES/user_guide/configuration/additional_config.po` (+3/-3)
  - 修改 `docs/source/locale/zh_CN/LC_MESSAGES/user_guide/feature_guide/expert_parallelism_load_balancer.po` (+28/-30)
  - 修改 `docs/source/locale/zh_CN/LC_MESSAGES/user_guide/support_matrix/supported_features.po` (+3/-2)
  - 修改 `docs/source/user_guide/configuration/additional_config.md` (+2/-2)
  - ... 及其他 26 个文件
  - Ascend 影响: ✓ 无影响

- **[2617fb6a](https://github.com/vllm-project/vllm-ascend/commit/2617fb6abf541145ea7f12d1dd39c757f1180b66)** ([#14026](https://github.com/vllm-project/vllm-ascend/pull/14026)) [Feature] SFA/MRV2 PCP 支持
  - 标签: `feature`, `mrv2`, `high-risk`, `pcp`, `attention`, `worker-v2`, `sfa`, `context-parallel`
  - 变更文件（共 16 个）:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+1/-1)
  - 修改 `tests/e2e/coverage_taxonomy.py` (+2/-0)
  - 修改 `tests/e2e/pull_request/eight_card/model_runner_v2/test_glm5_2.py` (+47/-0)
  - 修改 `tests/ut/attention/a2/test_sfa_v1.py` (+4/-0)
  - 修改 `tests/ut/attention/test_sfa_cp.py` (+81/-0)
  - 修改 `tests/ut/quantization/test_modelslim_config.py` (+2/-1)
  - 修改 `tests/ut/worker/test_attn_utils_v2.py` (+1/-0)
  - 修改 `tests/ut/worker/test_model_runner_v2.py` (+21/-0)
  - 修改 `tests/ut/worker/test_pcp_manager_v2.py` (+82/-27)
  - 修改 `vllm_ascend/attention/context_parallel/sfa_cp.py` (+62/-1)
  - ... 及其他 6 个文件
  - Ascend 影响: ✓ 无影响

- **[eb078d56](https://github.com/vllm-project/vllm-ascend/commit/eb078d56c3914d99abc99c337cd0b9277546834d)** ([#14981](https://github.com/vllm-project/vllm-ascend/pull/14981)) [Test][Mamba] 为 Mamba/混合模型添加 e2e 测试
  - 标签: `test`, `mrv2`, `low-risk`, `tests`, `mamba`, `model-runner-v2`
  - 变更文件:
  - 修改 `.github/workflows/scripts/test_config.yaml` (+1/-0)
  - 新增 `tests/e2e/pull_request/two_card/model_runner_v2/test_mamba_hybrid.py` (+72/-0)
  - Ascend 影响: ✓ 无影响

---

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
