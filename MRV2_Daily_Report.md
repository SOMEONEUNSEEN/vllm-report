# MRV2 每日报告
生成时间: 2026-08-17 09:03:11
统计范围: 最近 30 天

**MRV2 定义**: `vllm/v1/worker/gpu/model_runner.py` 及其依赖的所有组件

MRV2 相关 commits 总数: 99

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
