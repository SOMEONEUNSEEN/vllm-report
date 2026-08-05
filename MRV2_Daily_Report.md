# MRV2 每日报告
生成时间: 2026-08-05 09:01:58
统计范围: 最近 30 天

**MRV2 定义**: `vllm/v1/worker/gpu/model_runner.py` 及其依赖的所有组件

MRV2 相关 commits 总数: 101

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

## 2026-07-29
### vllm
- **[43eaefba](https://github.com/vllm-project/vllm/commit/43eaefba5a5dbccb71d2404e4bf28e21bb74fce6)** ([#48791](https://github.com/vllm-project/vllm/pull/48791)) [ModelRunner V2] 为 embedding 和分类模型启用序列池化
  - 标签: `feature`, `mrv2`, `medium-risk`, `model-runner`, `pooling`
  - 变更文件:
  - 修改 `tests/models/language/pooling/test_all_pooling_plus_chunked_prefill.py` (+44/-1)
  - 修改 `tests/models/language/pooling/test_classification.py` (+57/-0)
  - 修改 `tests/models/language/pooling/test_embedding.py` (+76/-0)
  - 修改 `tests/models/language/pooling/test_splade_sparse_pooler.py` (+75/-0)
  - 修改 `tests/v1/streaming_input/test_gpu_model_runner_v2_streaming.py` (+1/-0)
  - 修改 `vllm/v1/worker/gpu/async_utils.py` (+27/-14)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+13/-3)
  - 修改 `vllm/v1/worker/gpu/model_states/encoder_only.py` (+49/-1)
  - 修改 `vllm/v1/worker/gpu/pool/pooling_runner.py` (+162/-17)
  - 修改 `vllm/v1/worker/gpu/warmup.py` (+5/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改 vllm/v1/worker/gpu/model_runner.py（vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner）及 gpu/pool/pooling_runner.py、gpu/model_states/encoder_only.py。若 vllm-ascend 支持 MRV2 与 pooling 模型，需验证 NPUModelRunner 子类中池化流程与 encoder_only 状态适配；若 vllm-ascend 暂未启用 MRV2 则影响有限

- **[f51193b9](https://github.com/vllm-project/vllm/commit/f51193b9aefe665904d793ca782002320224d27a)** ([#49291](https://github.com/vllm-project/vllm/pull/49291)) [Kernel][Mamba] 为 align-mode DS-conv 状态迁移在 num_accepted_tokens > 1 时提供融合内核支持
  - 标签: `feature`, `mrv2`, `medium-risk`, `mamba`, `model-runner`
  - 变更文件:
  - 修改 `tests/kernels/mamba/test_precopy_mamba_align.py` (+257/-20)
  - 修改 `tests/v1/e2e/general/test_mamba_prefix_cache.py` (+38/-6)
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+5/-12)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+1/-0)
  - 修改 `vllm/v1/worker/mamba_utils.py` (+108/-26)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改 vllm/v1/worker/gpu_model_runner.py（旧路径，vllm-ascend 的 NPUModelRunner 曾继承）与 gpu/model_states/mamba_hybrid.py（MRV2 路径）、mamba_utils.py。若 vllm-ascend 支持 Mamba 混合模型与投机解码，需验证 Ascend 上多 token DS-conv 状态迁移融合逻辑的正确性；mamba_utils 是通用工具路径

### vllm-ascend
- **[2a607f09](https://github.com/vllm-project/vllm-ascend/commit/2a607f094951ea55eda2bd26486ccd9d27940633)** ([#12195](https://github.com/vllm-project/vllm-ascend/pull/12195)) [BugFix] 修复 eager 模式下的数据并行问题
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `platform`, `distributed`
  - 变更文件:
  - 修改 `vllm_ascend/platform.py` (+9/-5)
  - Ascend 影响: ✓ 无影响

- **[0838ce8d](https://github.com/vllm-project/vllm-ascend/commit/0838ce8d099a09176cb7aa669f3ea36187b6d396)** ([#12731](https://github.com/vllm-project/vllm-ascend/pull/12731)) [Misc] 将 V2 Model Runner 与上游对齐
  - 标签: `refactor`, `mrv2`, `medium-risk`, `model-runner`, `spec-decode`, `sampler`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+40/-34)
  - 修改 `vllm_ascend/worker/worker.py` (+1/-0)
  - Ascend 影响: ✓ 无影响

- **[261a3e9f](https://github.com/vllm-project/vllm-ascend/commit/261a3e9f9ef0276ef36e5a57b3759c071c86a4fb)** ([#12648](https://github.com/vllm-project/vllm-ascend/pull/12648)) [Misc] 与上游同步 0724 续
  - 标签: `refactor`, `mrv2`, `medium-risk`, `spec-decode`, `distributed`, `config`
  - 变更文件:
  - 修改 `.github/vllm-main-verified.commit` (+1/-1)
  - 修改 `vllm_ascend/_310p/model_runner_310p.py` (+5/-1)
  - 修改 `vllm_ascend/core/recompute_scheduler.py` (+6/-1)
  - 修改 `vllm_ascend/worker/v2/attn_utils.py` (+5/-2)
  - 修改 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+16/-8)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dflash/aclgraph.py` (+4/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dflash/speculator.py` (+9/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/dspark/speculator.py` (+14/-1)
  - 修改 `vllm_ascend/worker/v2/spec_decode/eagle/aclgraph.py` (+6/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/mtp/speculator.py` (+18/-3)
  - Ascend 影响: ✓ 无影响

- **[f731be8a](https://github.com/vllm-project/vllm-ascend/commit/f731be8a5f0741228ef87a800167f23257f2dde8)** ([#12981](https://github.com/vllm-project/vllm-ascend/pull/12981)) [Feature] GQA C8 ModelRunnerV2 适配
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `attention`
  - 变更文件:
  - 修改 `vllm_ascend/attention/attention_v1.py` (+7/-4)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-28
### vllm
- **[0d0504b5](https://github.com/vllm-project/vllm/commit/0d0504b54c73119ed643c80b4ed56ef3cf80e209)** ([#49903](https://github.com/vllm-project/vllm/pull/49903)) [Core] 在首个请求前预热 runner 拥有的 Triton 内核
  - 标签: `feature`, `mrv2`, `medium-risk`, `model-runner`, `warmup`, `kernels`
  - 变更文件:
  - 修改 `tests/v1/worker/test_kv_block_zeroer.py` (+65/-1)
  - 修改 `vllm/model_executor/warmup/kernel_warmup.py` (+10/-6)
  - 修改 `vllm/model_executor/warmup/qwen_triton_warmup.py` (+0/-114)
  - 修改 `vllm/model_executor/warmup/v1_block_table_warmup.py` (+14/-28)
  - 修改 `vllm/v1/worker/gpu/warmup.py` (+85/-36)
  - 修改 `vllm/v1/worker/mamba_utils.py` (+3/-3)
  - 修改 `vllm/v1/worker/utils.py` (+6/-1)
  - Ascend 影响: ✓ 无影响

- **[90245f41](https://github.com/vllm-project/vllm/commit/90245f4190a35593a625e4bc349485c39c774d39)** ([#50073](https://github.com/vllm-project/vllm/pull/50073)) [Bugfix] 修复 CPU MRV2 上的多模态支持
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `multimodal`, `model-states`, `cpu`
  - 变更文件:
  - 修改 `vllm/multimodal/inputs.py` (+2/-0)
  - 修改 `vllm/v1/worker/cpu/shm.py` (+12/-0)
  - 修改 `vllm/v1/worker/gpu/model_states/encoder_decoder.py` (+4/-1)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/model_states/encoder_decoder.py，该文件位于 vllm-ascend 覆盖的 model_states/ 目录。vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner，若 Ascend 上使用 MRV2 + 多模态，encoder_decoder 的多模态输入处理逻辑需验证。

- **[60417b4b](https://github.com/vllm-project/vllm/commit/60417b4b744c371453eddcf5c8fa0f184418c957)** ([#50034](https://github.com/vllm-project/vllm/pull/50034)) [Core][PCP] 当 PCP 启用时选择 MRV2
  - 标签: `feature`, `mrv2`, `medium-risk`, `config`, `pcp`
  - 变更文件:
  - 修改 `vllm/config/vllm.py` (+9/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改 vllm/config/vllm.py 的运行时选择逻辑。PCP 启用时强制选择 MRV2，vllm-ascend 的 NPUModelRunner 基于 MRV2，此配置联动可能影响 Ascend 上 PCP 的使用。需验证 Ascend 上 PCP+MRV2 的行为。

- **[272abd5f](https://github.com/vllm-project/vllm/commit/272abd5f486967f1fb9db7ca7504f8c34235ef50)** ([#47920](https://github.com/vllm-project/vllm/pull/47920)) [Tests][Spec Decode] 添加 gemma4 MTP 接受率测试
  - 标签: `test`, `mrv2`, `low-risk`, `spec-decode`, `gemma4`
  - 变更文件:
  - 修改 `.buildkite/test_areas/spec_decode.yaml` (+12/-0)
  - 修改 `tests/v1/e2e/spec_decode/test_spec_decode.py` (+73/-42)
  - 修改 `vllm/v1/spec_decode/gemma4.py` (+24/-0)
  - 修改 `vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py` (+11/-6)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py，该文件位于 MRV2 的 gpu/spec_decode/ 目录。vllm-ascend 若使用 MRV2 spec decode，需验证 speculator 变更不影响 Ascend 上的推测解码。

---

## 2026-07-27
### vllm
- **[d2ca3002](https://github.com/vllm-project/vllm/commit/d2ca3002d93314a08bbddf9c6eb6ee78b1343407)** ([#47711](https://github.com/vllm-project/vllm/pull/47711)) [性能] 跳过无操作的 FP32 logits 物化
  - 标签: `performance`, `mrv2`, `medium-risk`, `model-runner`, `sampler`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/sample/sampler.py` (+21/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/worker/gpu/sample/sampler.py 是 MRV2 GPU 采样器核心路径，vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner 并使用同一 Sampler。跳过 FP32 logits 物化的优化会传递到 Ascend 平台

- **[29fdeab2](https://github.com/vllm-project/vllm/commit/29fdeab2548fdb5cd61ec3613e5e72200c695ef0)** ([#49422](https://github.com/vllm-project/vllm/pull/49422)) [XPU][CI] 在 Intel GPU CI 中添加更多测试用例
  - 标签: `chore`, `low-risk`, `xpu`, `ci`, `tests`
  - 变更文件:
  - 新增 `.buildkite/intel_jobs/benchmarks_intel.yaml` (+26/-0)
  - 修改 `.buildkite/intel_jobs/engine_intel.yaml` (+76/-0)
  - 新增 `.buildkite/intel_jobs/model_executor_intel.yaml` (+33/-0)
  - 修改 `.buildkite/intel_jobs/model_runner_v2_intel.yaml` (+55/-1)
  - 新增 `.buildkite/intel_jobs/samplers_intel.yaml` (+29/-0)
  - Ascend 影响: ✓ 无影响

- **[439f3362](https://github.com/vllm-project/vllm/commit/439f336212227833e126526d3c5f3ef3968dfbf5)** ([#49736](https://github.com/vllm-project/vllm/pull/49736)) [核心] 修复 MRV2 mamba_hybrid.py 中的 GPU<->CPU 同步
  - 标签: `bugfix`, `mrv2`, `low-risk`, `model-runner`, `mamba`, `model-states`
  - 变更文件:
  - 修改 `vllm/v1/worker/gpu/model_states/mamba_hybrid.py` (+4/-4)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/worker/gpu/model_states/mamba_hybrid.py 是 MRV2 GPU model_states 路径，vllm-ascend 的 NPUModelRunner 可能继承 MambaHybridModelState

- **[50aa8304](https://github.com/vllm-project/vllm/commit/50aa83048219b70a3a68adf2fc8cd860ccc3e238)** ([#49751](https://github.com/vllm-project/vllm/pull/49751)) [BugFix] 不要创建超过 max_model_len 的 dummy 请求
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `model-runner`, `input-batch`, `cudagraph`
  - 变更文件:
  - 新增 `tests/v1/worker/test_gpu_input_batch_v2.py` (+52/-0)
  - 修改 `vllm/v1/worker/gpu/input_batch.py` (+9/-4)
  - 修改 `vllm/v1/worker/gpu/lora_utils.py` (+5/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+6/-2)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm/v1/worker/gpu/model_runner.py（vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner），dummy 请求创建逻辑的变更会影响 Ascend 上的 CUDA graph 捕获
    - 建议测试区域: `Ascend CUDA graph 捕获 dummy 请求 seq_len 验证`, `NPUModelRunner dummy 请求 token 分布正确性`

- **[fdaa0d9e](https://github.com/vllm-project/vllm/commit/fdaa0d9e59238b6884f9515fa3245dea118edc66)** ([#49331](https://github.com/vllm-project/vllm/pull/49331)) [ModelRunner V2] 支持 encoder-only attention
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `attention`, `encoder-only`, `model-states`
  - 变更文件:
  - 修改 `tests/models/language/pooling/test_embedding.py` (+54/-0)
  - 修改 `vllm/v1/worker/gpu/attn_utils.py` (+12/-0)
  - 修改 `vllm/v1/worker/gpu/block_table.py` (+1/-1)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+3/-0)
  - 修改 `vllm/v1/worker/gpu/model_states/__init__.py` (+7/-1)
  - 新增 `vllm/v1/worker/gpu/model_states/encoder_only.py` (+182/-0)
  - 修改 `vllm/v1/worker/gpu/model_states/interface.py` (+10/-0)
  - 修改 `vllm/v1/worker/gpu/warmup.py` (+7/-2)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的多个核心覆盖路径：(1) vllm/v1/worker/gpu/attn_utils.py - vllm-ascend 有自己的 attn_utils 实现，encoder-only attention 支持需在 Ascend backend 中实现；(2) vllm/v1/worker/gpu/block_table.py - vllm-ascend 通过 block_table_patch 打补丁；(3) vllm/v1/worker/gpu/model_runner.py - vllm-ascend 的 NPUModelRunner 继承 GPUModelRunner，EncoderOnlyModelState 选择逻辑会传递到 Ascend。vllm-ascend 必须评估是否需要在 Ascend attention backend 中实现 encoder-only 支持
    - 建议测试区域: `Ascend encoder-only/pooling 模型端到端推理`, `Ascend attention backend encoder-only 支持`, `NPUModelRunner EncoderOnlyModelState 集成验证`, `block_table_patch 在 encoder-only 模式下的行为`

### vllm-ascend
- **[80431747](https://github.com/vllm-project/vllm-ascend/commit/804317471ca4406451b04f3eb2b3cec431117f79)** ([#12944](https://github.com/vllm-project/vllm-ascend/pull/12944)) [BugFix] 避免 ACL graph replay 的全局同步
  - 标签: `bugfix`, `mrv2`, `medium-risk`, `model-runner`, `aclgraph`
  - 变更文件:
  - 修改 `vllm_ascend/worker/v2/aclgraph_utils.py` (+6/-1)
  - 修改 `vllm_ascend/worker/v2/model_runner.py` (+0/-5)
  - Ascend 影响: ✓ 无影响

- **[1ae2a6e9](https://github.com/vllm-project/vllm-ascend/commit/1ae2a6e9583db3627ac19049a8ad3217fa863e45)** ([#12810](https://github.com/vllm-project/vllm-ascend/pull/12810)) [Feature] 在 MRV2 中支持 MTP eager 模式
  - 标签: `feature`, `mrv2`, `high-risk`, `model-runner`, `spec-decode`, `mtp`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+43/-0)
  - 修改 `vllm_ascend/worker/v2/input_batch.py` (+6/-4)
  - 修改 `vllm_ascend/worker/v2/spec_decode/__init__.py` (+10/-0)
  - 新增 `vllm_ascend/worker/v2/spec_decode/autoregressive/__init__.py` (+6/-0)
  - 新增 `vllm_ascend/worker/v2/spec_decode/autoregressive/speculator.py` (+420/-0)
  - 修改 `vllm_ascend/worker/v2/spec_decode/eagle/speculator.py` (+5/-385)
  - 新增 `vllm_ascend/worker/v2/spec_decode/mtp/__init__.py` (+16/-0)
  - 新增 `vllm_ascend/worker/v2/spec_decode/mtp/speculator.py` (+89/-0)
  - Ascend 影响: ✓ 无影响

---

## 2026-07-26
### vllm
- **[7a29a3c5](https://github.com/vllm-project/vllm/commit/7a29a3c54cc338b0103005978f38764e40299572)** ([#49440](https://github.com/vllm-project/vllm/pull/49440)) [Bugfix][KV Offload] 按 model runner 命名空间隔离持久化缓存
  - 标签: `bugfix`, `low-risk`, `kv-cache`, `kv-offload`
  - 变更文件:
  - 修改 `tests/v1/kv_offload/test_file_mapper.py` (+20/-1)
  - 修改 `vllm/v1/kv_offload/file_mapper.py` (+2/-0)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - vllm/v1/kv_offload/file_mapper.py 是 KV 卸载持久化缓存的通用路径，vllm-ascend 使用 KV 卸载持久化缓存时会经过此路径。命名空间分离修复影响 Ascend 上 V1/V2 runner 的缓存路径映射

---

## 2026-07-25
### vllm
- **[0b0bd2b5](https://github.com/vllm-project/vllm/commit/0b0bd2b5f6a7f15ef59621efe6e535b54c6348f9)** ([#44428](https://github.com/vllm-project/vllm/pull/44428)) [Feature] 为 DP+EP 外部负载均衡部署添加（简化版）容错框架
  - 标签: `feature`, `mrv2`, `high-risk`, `fault-tolerance`, `distributed`, `model-runner`, `entrypoints`, `engine`, `tests`
  - 变更文件（共 27 个）:
  - 新增 `.buildkite/test_areas/fault_tolerance.yaml` (+26/-0)
  - 修改 `tests/test_config.py` (+10/-0)
  - 新增 `tests/v1/fault_tolerance/__init__.py` (+2/-0)
  - 新增 `tests/v1/fault_tolerance/test_fault_tolerance_e2e.py` (+378/-0)
  - 修改 `vllm/config/__init__.py` (+3/-0)
  - 新增 `vllm/config/fault_tolerance.py` (+18/-0)
  - 修改 `vllm/config/parallel.py` (+19/-0)
  - 修改 `vllm/distributed/device_communicators/all2all.py` (+26/-1)
  - 修改 `vllm/distributed/device_communicators/base_device_communicator.py` (+21/-1)
  - 修改 `vllm/engine/arg_utils.py` (+31/-0)
  - ... 及其他 17 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 直接影响 - 该 commit 修改了 vllm-ascend 的核心覆盖路径：(1) vllm/v1/worker/gpu/model_runner.py - vllm-ascend 通过 NPUModelRunner 继承 GPUModelRunner，新增的容错钩子（+8）会传递到 Ascend 子类；(2) vllm/config/parallel.py - vllm-ascend 覆盖并行配置，弹性 EP 与容错相关校验需评估；(3) vllm/v1/worker/gpu_worker.py 与 vllm/v1/engine/core*.py - worker/engine 生命周期改动可能影响 Ascend worker。vllm-ascend 需评估 NPUModelRunner 是否需要接入容错哨兵、弹性 EP 在 HCCL 通信下的恢复行为。
    - 建议测试区域: `Ascend NPUModelRunner 容错钩子兼容性`, `弹性 EP + HCCL 通信恢复`, `gpu_worker_sentinel 在 NPU 上的健康检查`, `DP+EP 容错 e2e（Ascend）`

- **[213f681f](https://github.com/vllm-project/vllm/commit/213f681f8117b9026ca8189583d2855d70104401)** ([#49768](https://github.com/vllm-project/vllm/pull/49768)) 回退 "[Perf][GLM-5.2] Blackwell 解码优化"
  - 标签: `refactor`, `mrv2`, `medium-risk`, `spec-decode`, `mla`, `deepseek`, `kernels`, `revert`
  - 变更文件（共 29 个）:
  - 修改 `CMakeLists.txt` (+0/-17)
  - 删除 `csrc/libtorch_stable/bf16_skinny_gemm.cu` (+0/-262)
  - 删除 `csrc/libtorch_stable/bf16_skinny_gemm_entry.cu` (+0/-170)
  - 修改 `csrc/libtorch_stable/dsv3_fused_a_gemm.cu` (+36/-112)
  - 修改 `csrc/libtorch_stable/quantization/fp4/nvfp4_quant_kernels.cu` (+10/-42)
  - 修改 `csrc/libtorch_stable/torch_bindings.cpp` (+0/-4)
  - 删除 `recipes/glm5.2-ll-b300-tp8-mtp5.md` (+0/-41)
  - 删除 `tests/kernels/test_bf16_skinny_gemm.py` (+0/-70)
  - 修改 `tests/kernels/test_fused_deepseek_v32_norm_rope.py` (+0/-77)
  - 修改 `tests/models/registry.py` (+0/-4)
  - ... 及其他 19 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该回退修改了 MRV2 spec_decode 核心路径 vllm/v1/worker/gpu/spec_decode/{autoregressive,mtp}/speculator.py 与 vllm/v1/spec_decode/llm_base_proposer.py，vllm-ascend 通过 vllm_ascend/spec_decode/llm_base_proposer.py 覆盖该路径（见当日 vllm-ascend #12777）；同时回退 MLA sparse attention（vllm/v1/attention/backends/mla/），DeepSeek V3.2 在 Ascend 上使用 MLA。vllm-ascend 需评估 speculator API 回退是否影响其覆盖实现，以及 MLA sparse attention 回退对 Ascend MLA 的影响。注意：回退的是 NVIDIA 专用优化，Ascend 不直接使用这些 CUDA kernel，但共享的 spec_decode/MLA 接口可能需同步。
    - 建议测试区域: `Ascend MTP speculator 与回退后 vllm 接口兼容性`, `DeepSeek V3.2 MLA 在 Ascend 上的注意力正确性`, `vllm_ascend/spec_decode/llm_base_proposer.py 与回退后父类兼容性`

### vllm-ascend
- **[5f8c0e8f](https://github.com/vllm-project/vllm-ascend/commit/5f8c0e8fece7fa87f9dc2346b7782ff654a019a1)** ([#12728](https://github.com/vllm-project/vllm-ascend/pull/12728)) [DOC][CI] 将 PCP 相关文档下线
  - 标签: `docs`, `low-risk`, `pcp`, `ci`
  - 变更文件（共 18 个）:
  - 修改 `.github/workflows/configs/nightly_config.yaml` (+0/-6)
  - 修改 `.github/workflows/configs/weekly_config.yaml` (+0/-3)
  - 修改 `docs/hooks/nav_titles.py` (+0/-8)
  - 修改 `docs/source/developer_guide/Design_Documents/context_parallel.md` (+42/-110)
  - 修改 `docs/source/developer_guide/contribution/nightly_ci_test.md` (+0/-1)
  - 修改 `docs/source/tutorials/features/dynamic_chunked_pipeline_parallel.md` (+0/-1)
  - 删除 `docs/source/tutorials/features/long_sequence_context_parallel_multi_node.md` (+0/-335)
  - 删除 `docs/source/tutorials/features/long_sequence_context_parallel_single_node.md` (+0/-153)
  - 修改 `docs/source/tutorials/models/DeepSeek-V3.1.md` (+2/-2)
  - 修改 `docs/source/tutorials/models/MiniMax-M2.md` (+0/-19)
  - ... 及其他 8 个文件
  - Ascend 影响: ✓ 无影响

---

## 2026-07-24
### vllm
- **[7b40fb96](https://github.com/vllm-project/vllm/commit/7b40fb96450e1deef40ebc383ff549bea35b9b8f)** ([#49247](https://github.com/vllm-project/vllm/pull/49247)) [UX] 拒绝不兼容的嵌套运行时覆盖
  - 标签: `refactor`, `low-risk`, `config`, `model-runner`
  - 变更文件:
  - 修改 `tests/test_config.py` (+18/-3)
  - 修改 `tests/v1/worker/test_gpu_model_runner.py` (+1/-1)
  - 修改 `vllm/config/utils.py` (+31/-15)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+6/-4)
  - Ascend 影响: ✓ 无影响

- **[833483f3](https://github.com/vllm-project/vllm/commit/833483f3578a2c4766977d0fe431bd32a01ce250)** ([#48218](https://github.com/vllm-project/vllm/pull/48218)) 编码器缓存扩展钩子
  - 标签: `feature`, `medium-risk`, `model-runner`, `multimodal`, `encoder-cache`, `scheduler`
  - 变更文件:
  - 修改 `tests/v1/worker/test_gpu_model_runner_mm_gather.py` (+1/-0)
  - 修改 `vllm/config/__init__.py` (+3/-0)
  - 新增 `vllm/config/ec_manager_config.py` (+29/-0)
  - 修改 `vllm/config/vllm.py` (+5/-0)
  - 修改 `vllm/v1/core/encoder_cache_manager.py` (+4/-0)
  - 修改 `vllm/v1/core/sched/output.py` (+4/-1)
  - 修改 `vllm/v1/core/sched/scheduler.py` (+10/-6)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+50/-8)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - GPUModelRunner 新增 _on_request_state_removed/_process_encoder_cache_scheduler_output/_cache_encoder_output/_get_encoder_output_from_cache 等可重写钩子，NPUModelRunner 继承自此，多模态编码器缓存路径会经过这些钩子；EncoderCacheManagerConfig 经 VllmConfig 注入，Ascend 可借此扩展自定义管理器。需验证 Ascend 多模态编码器缓存生命周期不变。

- **[dd72658e](https://github.com/vllm-project/vllm/commit/dd72658e7db0c6a674f473f6f9f0f5c2ebe7e523)** ([#48597](https://github.com/vllm-project/vllm/pull/48597)) [Perf][GLM-5.2] Blackwell 解码优化
  - 标签: `feature`, `mrv2`, `high-risk`, `performance`, `spec-decode`, `mla`, `blackwell`, `model-runner`, `kernels`
  - 变更文件（共 29 个）:
  - 修改 `CMakeLists.txt` (+17/-0)
  - 新增 `csrc/libtorch_stable/bf16_skinny_gemm.cu` (+262/-0)
  - 新增 `csrc/libtorch_stable/bf16_skinny_gemm_entry.cu` (+170/-0)
  - 修改 `csrc/libtorch_stable/dsv3_fused_a_gemm.cu` (+112/-36)
  - 修改 `csrc/libtorch_stable/quantization/fp4/nvfp4_quant_kernels.cu` (+42/-10)
  - 修改 `csrc/libtorch_stable/torch_bindings.cpp` (+4/-0)
  - 新增 `recipes/glm5.2-ll-b300-tp8-mtp5.md` (+41/-0)
  - 新增 `tests/kernels/test_bf16_skinny_gemm.py` (+70/-0)
  - 修改 `tests/kernels/test_fused_deepseek_v32_norm_rope.py` (+77/-0)
  - 修改 `tests/models/registry.py` (+4/-0)
  - ... 及其他 19 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 修改 MRV2 spec decode 基类 vllm/v1/worker/gpu/spec_decode/autoregressive/speculator.py、mtp/speculator.py 与 vllm/v1/spec_decode/llm_base_proposer.py，vllm-ascend 的 dspark/eagle spec decode 继承或参考这些基类；MLA flashinfer_mla_sparse.py 属 MLA 路径。CUDA 内核为 NVIDIA 专用，但 speculator 基类接口变更需 Ascend 侧对齐回归。

---

## 2026-07-23
### vllm
- **[ac36a7a1](https://github.com/vllm-project/vllm/commit/ac36a7a1e7eb8f03f9ec2b6bf643f1002b205794)** ([#48630](https://github.com/vllm-project/vllm/pull/48630)) [Spec Decode] 通过分块避免拒绝采样器 OOM
  - 标签: `feature`, `mrv2`, `high-risk`, `spec-decode`, `model-runner`, `sampler`, `tests`
  - 变更文件（共 12 个）:
  - 修改 `tests/v1/spec_decode/test_rejection_sampler_utils.py` (+62/-0)
  - 修改 `tests/v1/test_outputs.py` (+26/-1)
  - 新增 `tests/v1/worker/test_gpu_rejection_sampler_chunking.py` (+109/-0)
  - 修改 `vllm/config/model.py` (+4/-0)
  - 修改 `vllm/v1/outputs.py` (+27/-0)
  - 修改 `vllm/v1/sample/ops/topk_topp_sampler.py` (+8/-12)
  - 修改 `vllm/v1/sample/rejection_sampler.py` (+2/-4)
  - 修改 `vllm/v1/worker/gpu/sample/prompt_logprob.py` (+1/-9)
  - 修改 `vllm/v1/worker/gpu/sample/sampler.py` (+3/-6)
  - 修改 `vllm/v1/worker/gpu/spec_decode/rejection_sampler.py` (+142/-31)
  - ... 及其他 2 个文件
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu_model_runner.py（vllm-ascend 的 NPUModelRunner 继承自 GPUModelRunner）以及 vllm/v1/worker/gpu/spec_decode/ 与 gpu/sample/ 路径。vllm-ascend 有自己的 spec_decode 实现（vllm_ascend/spec_decode/llm_base_proposer.py），但 rejection sampler 的分块逻辑若在父类 GPUModelRunner 中执行，可能传递到 Ascend 子类。需验证：(1) NPUModelRunner 的采样流程是否触发分块逻辑；(2) Ascend 上 rejection sampler 的内存行为是否符合预期；(3) 分块配置参数对 Ascend 的适用性。
    - 建议测试区域: `Ascend 投机解码 rejection sampler 分块行为`, `NPUModelRunner 采样流程分块兼容性`, `大 batch 投机解码 NPU 内存占用`

- **[521aa80f](https://github.com/vllm-project/vllm/commit/521aa80f719bb11bf973d2d51873ca966afe373d)** ([#48399](https://github.com/vllm-project/vllm/pull/48399)) [Core] 简化 KVBlockZeroen 索引张量处理
  - 标签: `refactor`, `mrv2`, `low-risk`, `model-runner`, `kv-cache`
  - 变更文件:
  - 修改 `tests/v1/worker/test_kv_block_zeroer.py` (+4/-7)
  - 修改 `vllm/v1/worker/gpu/model_runner.py` (+1/-3)
  - 修改 `vllm/v1/worker/gpu_model_runner.py` (+0/-2)
  - 修改 `vllm/v1/worker/utils.py` (+1/-43)
  - Ascend 影响: ⚠️ 影响 Ascend
    - 影响描述: 潜在影响 - 该 commit 修改了 vllm/v1/worker/gpu/model_runner.py，vllm-ascend 的 NPUModelRunner 继承自 GPUModelRunner。KVBlockZeroen 的索引张量处理简化可能影响 Ascend 上的 KV cache 块清零行为。需验证 NPUModelRunner 子类是否依赖原有的索引张量处理方式。

### vllm-ascend
- **[c88d7a0a](https://github.com/vllm-project/vllm-ascend/commit/c88d7a0a2473329377c9bb2d15429a2145d9ac4f)** ([#12536](https://github.com/vllm-project/vllm-ascend/pull/12536)) [性能] 移除 DSA_CP 的 QLIMetadata builder 中的 D2H 同步
  - 标签: `perf`, `low-risk`, `attention`, `context-parallel`
  - 变更文件:
  - 修改 `tests/e2e/pull_request/one_card/model_runner_v2/test_basic.py` (+2/-1)
  - 修改 `vllm_ascend/attention/context_parallel/dsa_cp.py` (+11/-11)
  - Ascend 影响: ✓ 无影响

---

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
