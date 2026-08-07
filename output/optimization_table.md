# 上游优化迁移分析表

> 生成时间: 2026-08-07T10:51:09.560251+08:00
> 统计周期: 最近 30 天
> 总 commits: 326 | 已分析: 281 | 跳过: 45

## 汇总
| 优先级 | 数量 |
|--------|------|
| P0 (必须处理) | 0 |
| P1 (高价值) | 0 |
| P2 (中期跟进) | 116 |
| P3 (长期参考) | 165 |
| skip (跳过) | 45 |

## P2 优先级 (116 个)
| SHA | 日期 | 分类 | 优化内容 | 迁移策略 | 工作量 | 关键文件 |
|-----|------|------|---------|---------|--------|---------|
| 2afa3f7e | 2026-07-08 | moe-fusion | 【变更概述】[Perf] 新增：Minimax M3 - 支持 cross-layer allred | auto-inherit | S | vllm/model_executor/layers/fused_moe/lay |
| 80eb01e9 | 2026-07-08 | model-architecture | 【变更概述】[Bugfix] 更新：DSV4 TP16 garbage output
【PR号】#4 | auto-inherit | S | vllm/models/deepseek_v4/attention.py, vl |
| 2c17d33f | 2026-07-09 | attention-kv-cache | 【变更概述】[Bugfix] 更新：ROCm Change AttentionCGSuppoort  | auto-inherit | S | vllm/v1/attention/backends/mla/triton_ml |
| 95d6d6f4 | 2026-07-09 | test-ci | 【变更概述】[Bugfix] 更新：Use int8 workspace FlashInfer ML | auto-inherit | S | tests/kernels/attention/test_flashinfer_ |
| 56da398d | 2026-07-09 | model-architecture | 【变更概述】修复：修复 embed scaling + CUDA graphs Transforme | auto-inherit | S | vllm/model_executor/models/transformers/ |
| 49abadae | 2026-07-09 | attention-kv-cache | 【变更概述】[ROCm] 修复：Bugfix 修复 empty-tensor max crash A | idea-copy | L | vllm/v1/attention/backends/rocm_aiter_fa |
| 300e3379 | 2026-07-10 | model-architecture | 【变更概述】[Perf] 更新：fuse more rmsnorm all-reduce qwen3 | auto-inherit | S | vllm/model_executor/layers/mamba/gdn/qwe |
| b0dec2a1 | 2026-07-10 | attention-kv-cache | 【变更概述】[ROCM] 优化：DSV32][Perf][MTP Enable UNIFORM_BA | idea-copy | L | vllm/v1/attention/backends/mla/rocm_aite |
| a02984ed | 2026-07-12 | model-architecture | 【变更概述】[Perf] 更新：Qwen Replace MoE all-reduce reduce | auto-inherit | S | vllm/model_executor/layers/mamba/gdn/qwe |
| 481e481b | 2026-07-12 | test-ci | 【变更概述】【MRV2】[2/N] 修复：核心 支持 partial prefix 缓存 hit h | config-align | M | tests/v1/core/prefix_cache/test_partial_ |
| 56a357ed | 2026-07-13 | test-ci | 【变更概述】[Bugfix] [KV Cache] 更新：Don't route uniform-p | auto-inherit | S | tests/v1/core/test_kv_cache_utils.py, vl |
| 36484e46 | 2026-07-13 | model-architecture | 【变更概述】[BugFix] 更新：Restore full tokens Qwen MTP Whe | auto-inherit | S | vllm/model_executor/models/qwen3_5_mtp.p |
| 8c5dafcd | 2026-07-13 | test-ci | 【变更概述】[Bugfix] [UT] 修复：修复 EagleMiniCPMForCausalLM  | auto-inherit | S | tests/models/registry.py, vllm/model_exe |
| 1ff94296 | 2026-07-14 | config | 【变更概述】[CI Bug] 更新：Fully solve accuracy issue DSv3. | config-align | S | vllm/config/parallel.py, vllm/model_exec |
| 793cf79c | 2026-07-14 | test-ci | 【变更概述】[Bugfix] [Security] 修复：修复 concurrent sparse  | auto-inherit | S | tests/renderers/test_sparse_tensor_concu |
| 9a21f0d1 | 2026-07-14 | model-architecture | 【变更概述】[BugFix] 更新：Initialize model_config Qwen3-VL | auto-inherit | S | vllm/model_executor/models/qwen3_vl_moe. |
| 26587f95 | 2026-07-14 | core-engine | 【变更概述】【MRV2】[BugFix] 【MRV2】[ModelRunner V2] 【MRV2】 | idea-copy | L | vllm/v1/worker/gpu/cudagraph_utils.py, v |
| adce0681 | 2026-07-15 | test-ci | 【变更概述】[ROCm] [CI] 修复：修复 test_common.py
【PR号】#48676 | auto-inherit | S | tests/conftest.py, vllm/model_executor/m |
| 442c421e | 2026-07-15 | model-architecture | 【变更概述】[Perf] 更新：移除 redundant repeat copy dsv4 1.8% | auto-inherit | S | vllm/model_executor/kernels/mhc/tilelang |
| 3ca242d1 | 2026-07-15 | test-ci | 【变更概述】【MRV2】[Bugfix] 【MRV2】[R3] 【MRV2】更新：Exclude d | cherry-pick | S | tests/model_executor/test_routed_experts |
| 313d01f5 | 2026-07-15 | test-ci | 【变更概述】[CI] [Bugfix] 修复：修复 FlashAttention reported  | auto-inherit | S | docs/design/attention_backends.md, tests |
| b8168e33 | 2026-07-16 | test-ci | 【变更概述】[ROCm] [Perf] [DSV4] 更新：Enable 拆分 sparse dec | idea-copy | L | tests/kernels/attention/test_rocm_triton |
| 6a9f24aa | 2026-07-16 | core-engine | 【变更概述】【MRV2】[ROCm] 【MRV2】[CI] 【MRV2】修复：修复 CUDA gra | cherry-pick | S | vllm/v1/worker/gpu_model_runner.py |
| 2db39c70 | 2026-07-16 | model-architecture | 【变更概述】[Bugfix] [Spec Decode] 修复：修复 eagle3 first-la | auto-inherit | S | vllm/model_executor/models/llama_eagle3. |
| 3c1bc1fc | 2026-07-16 | attention-kv-cache | 【变更概述】[ROCm] [Perf] 优化：优化 sparse 注意力 prefill 内核 De | idea-copy | L | vllm/v1/attention/ops/rocm_aiter_mla_spa |
| 3a5e88e6 | 2026-07-16 | config | 【变更概述】[Bugfix] 修复：修复 local speculators dots name f | config-align | S | vllm/config/speculative.py |
| eb33ff34 | 2026-07-16 | test-ci | 【变更概述】[ROCm] [Perf] 更新：DSv4 two-stage compressor 内 | auto-inherit | S | tests/kernels/test_compressor_kv_cache.p |
| b7950e79 | 2026-07-16 | core-engine | 【变更概述】【MRV2】[Bugfix] 【MRV2】更新：Initialize draft CUD | cherry-pick | S | vllm/v1/worker/gpu_model_runner.py |
| 41ea2dd4 | 2026-07-18 | test-ci | 【变更概述】★★★ MRV2 重点 commit ★★★
修复 prompt_logprobs 未遵 | config-align | M | tests/v1/sample/test_logprobs.py, vllm/c |
| bf578e1a | 2026-07-18 | test-ci | 【变更概述】修复 GLM-4V（glm4_1v.py）在视频 dummy profiling（预分配 | auto-inherit | S | tests/models/multimodal/processing/test_ |
| efed8a1e | 2026-07-18 | attention-kv-cache | 【变更概述】优化 ROCm gfx950 上 DSV4 sparse decode reductio | idea-copy | L | vllm/v1/attention/ops/rocm_aiter_mla_spa |
| e6d1310b | 2026-07-19 | test-ci | 【变更概述】修复 pooling 参数被移除后的校验问题。当用户传入已被废弃的 pooling 参数 | config-align | M | tests/test_pooling_params.py, vllm/confi |
| 7c2acd38 | 2026-07-19 | model-architecture | 【变更概述】修复 Qwen3-VL 与 Qwen2.5-Omni 在处理视频提示时未遵循 max_p | auto-inherit | S | vllm/model_executor/models/qwen2_5_omni_ |
| e9424389 | 2026-07-19 | attention-kv-cache | 【变更概述】为 ROCm 平台的 DeepSeek V3.2 sparse MLA decode 添 | idea-copy | L | vllm/v1/attention/backends/mla/rocm_aite |
| 0a5069e4 | 2026-07-20 | test-ci | 【变更概述】修复 Gemma4 模型在 ModelOpt 混合精度量化时 MoE 专家权重路径映射错 | auto-inherit | S | tests/quantization/test_modelopt.py, vll |
| 4d30c510 | 2026-07-21 | test-ci | 【变更概述】修复 Cosmos3 Edge 多模态模型的 checkpoint 权重过滤、视频加载和 | auto-inherit | S | tests/models/multimodal/processing/test_ |
| 3e0c8875 | 2026-07-21 | model-architecture | 【变更概述】修复 Ovis2.5 多模态模型在 transformers v5 下的特殊 token | auto-inherit | S | vllm/model_executor/models/ovis2_5.py, v |
| 8def3cdd | 2026-07-21 | model-architecture | 【变更概述】修复 LFM2 模型 ShortConv 投影层未接收 quant_config 导致量 | auto-inherit | S | vllm/model_executor/layers/mamba/short_c |
| 2e2e626b | 2026-07-21 | test-ci | 【变更概述】修复 get_max_concurrency_for_kv_cache_config 中 | auto-inherit | S | tests/v1/core/test_kv_cache_utils.py, vl |
| 37e370fe | 2026-07-22 | test-ci | 【变更概述】为 DeepSeek V4 压缩器（compressor）添加 c128 边界检测机制， | auto-inherit | S | tests/kernels/test_compressor_kv_cache.p |
| 060b5f61 | 2026-07-22 | test-ci | 【变更概述】修复 MLA（Multi-Head Latent Attention）在 PCP（Pre | auto-inherit | S | tests/evals/gsm8k/configs/GLM-5.2-NVFP4- |
| ba189290 | 2026-07-22 | test-ci | 【变更概述】修复 MTP（Multi-Token Prediction）投机解码在权重传输（weig | auto-inherit | S | tests/model_executor/model_loader/test_m |
| c8db00b1 | 2026-07-23 | model-architecture | 【变更概述】修复 GPTQ 量化模式下 Qwen3.5 MTP（Multi-Token Predic | auto-inherit | S | vllm/model_executor/models/qwen3_5_mtp.p |
| 80c76839 | 2026-07-23 | multimodal | 【变更概述】将多模态 embeds（图像/视频/音频嵌入）的加载操作从主事件循环中分离，改为延迟异步 | auto-inherit | S | vllm/entrypoints/chat_utils.py, vllm/mul |
| 76bf5524 | 2026-07-23 | model-architecture | 【变更概述】修复 DeepSeek-V4 DSpark draft 模型的共享专家（shared e | auto-inherit | S | vllm/models/deepseek_v4/nvidia/dspark.py |
| 9a698f32 | 2026-07-23 | model-architecture | 【变更概述】优化 Inkling 模型的结果处理，避免临时张量分配以减少内存开销，防止在较小显存配置 | auto-inherit | S | vllm/models/inkling/nvidia/mlp.py, vllm/ |
| 4080263b | 2026-07-23 | test-ci | 【变更概述】移除 Inkling 模型 scale planning 中对 SciPy 的依赖，改用 | auto-inherit | S | tests/models/inkling/test_contract_valid |
| d02df748 | 2026-07-24 | test-ci | 【变更概述】修复 MediaConnector 解析 base64 data URL 时未遵循 RF | auto-inherit | S | tests/multimodal/media/test_connector.py |
| dd72658e | 2026-07-24 | operator-kernel | 【变更概述】【MRV2 关键 commit】为 GLM-5.2（DeepSeek V3.2 架构）在 | idea-copy | L | CMakeLists.txt, csrc/libtorch_stable/bf1 |
| 7bdf8cc3 | 2026-07-24 | model-architecture | 【变更概述】修复 hy_v3（Humming）模型在 layer.has_bias 为 None 时 | auto-inherit | S | vllm/model_executor/models/hy_v3.py |
| 33ef67e9 | 2026-07-25 | model-architecture | 【变更概述】提升 MOSS-TD（MOSS Transcribe Diarize，语音转写与说话人分 | auto-inherit | S | vllm/model_executor/models/moss_transcri |
| d1a8ba63 | 2026-07-25 | model-architecture | 【变更概述】修复 MiniMax-M3 模型在 Triton kernel 中 token-majo | auto-inherit | S | vllm/models/minimax_m3/common/indexer.py |
| fe514576 | 2026-07-25 | test-ci | 【变更概述】修复 prefix-LM 模型（如 GLM 系列）在纯文本服务时注意力后端被错误排除的问 | config-align | M | tests/config/test_multimodal_config.py,  |
| 0da6e7f3 | 2026-07-26 | test-ci | 【变更概述】修复 CompilationConfig 和 CustomOp 对矛盾自定义算子指令（c | config-align | S | tests/compile/test_config.py, vllm/confi |
| 8d28b48d | 2026-07-26 | test-ci | 【变更概述】将多模态（MM）预处理从共享的 renderer 线程池 executor 隔离到独立的 | config-align | S | tests/test_config.py, vllm/config/model. |
| 30b07140 | 2026-07-26 | model-architecture | 【变更概述】优化 DeepSeek-OCR-2（基于 DeepEncoder2 架构）的首 toke | auto-inherit | S | vllm/model_executor/models/deepencoder2. |
| 1240c74c | 2026-07-26 | test-ci | 【变更概述】修复 ColQwen3.5（ColBERT 式 late-interaction 检索模 | auto-inherit | S | tests/models/multimodal/pooling/test_col |
| 04502dec | 2026-07-27 | test-ci | 【变更概述】优化多模态视频哈希机制，将视频哈希方式从帧数据哈希改为按源字节（source bytes | auto-inherit | S | tests/multimodal/test_hasher.py, vllm/mu |
| ef9975d0 | 2026-07-27 | model-architecture | 【变更概述】移除 DiffusionGemma 模型不正确的流水线并行（PP）支持声明。移除 Sup | auto-inherit | S | vllm/model_executor/models/diffusion_gem |
| a89015c6 | 2026-07-27 | attention-kv-cache | 【变更概述】将 triton_merge_attn_states.py 中 merge_attn_s | auto-inherit | S | vllm/v1/attention/ops/triton_merge_attn_ |
| 8061dc26 | 2026-07-27 | test-ci | 【变更概述】修复 DeepSeek V4 sparse MLA 预热时 compress_ratio | auto-inherit | S | tests/v1/attention/test_indexer_deepseek |
| 50aa8304 | 2026-07-27 | test-ci | 【变更概述】【MRV2 commit】修复 MRV2 中 dummy 请求创建时将余数 token  | auto-inherit | S | tests/v1/worker/test_gpu_input_batch_v2. |
| f0553889 | 2026-07-27 | test-ci | 【变更概述】修复 XPU 平台 sparse MLA 内核中全掩码索引块导致 NaN 中毒的问题。使 | auto-inherit | S | tests/kernels/attention/test_xpu_mla_spa |
| 62d8db7c | 2026-07-28 | model-architecture | 【变更概述】补充 Kimi-K3 模型目录缺失的 __init__.py 文件，修复导入错误。
【P | auto-inherit | S | vllm/models/kimi_k3/__init__.py, vllm/mo |
| 90245f41 | 2026-07-28 | multimodal | 【变更概述】【MRV2 相关】修复 CPU MRV2 上多模态推理的问题。修改 vllm/v1/wo | auto-inherit | S | vllm/multimodal/inputs.py, vllm/v1/worke |
| d223c900 | 2026-07-28 | model-architecture | 【变更概述】修复 transformers backend 中 value padding 逻辑，仅 | auto-inherit | S | vllm/model_executor/models/transformers/ |
| fbb1ef68 | 2026-07-28 | model-architecture | 【变更概述】修复 DeepseekV4FP8 Quark MXFP4 量化在遇到列表值权重时的崩溃问 | auto-inherit | S | vllm/models/deepseek_v4/quant_config.py |
| 02b6ecf0 | 2026-07-28 | attention-kv-cache | 【变更概述】优化 ROCm sparse MLA decode 热循环，消除逐 decode 的 F | idea-copy | L | vllm/v1/attention/ops/rocm_aiter_mla_spa |
| 381b6916 | 2026-07-29 | test-ci | 【变更概述】修复 Kimi K3 的 KDA（Kernel Delta Attention）在 RO | auto-inherit | S | .buildkite/test-amd.yaml, vllm/models/ki |
| d6247d71 | 2026-07-29 | test-ci | 【变更概述】将 DSpark（Qwen3-DSpark）的 Markov head 在各 TP ra | auto-inherit | S | tests/v1/sample/test_head_dtype.py, vllm |
| aeaa50a7 | 2026-07-29 | test-ci | 【变更概述】修复多模态缓存哈希未包含媒体 IO 配置（如图片/视频处理参数）的 bug，导致不同 I | auto-inherit | S | tests/multimodal/test_hasher.py, vllm/mu |
| 32e657e6 | 2026-07-29 | test-ci | 【变更概述】修复 Eagle 投机解码 draft 模型 max_position_embeddin | config-align | M | tests/config/test_speculative_draft_max_ |
| 65a1a165 | 2026-07-29 | operator-kernel | 【变更概述】修复 CPU 平台 FP8 attention 的 scratchpad 大小计算问题。 | idea-copy | L | csrc/cpu/cpu_attn.cpp, csrc/cpu/torch_bi |
| 837eae64 | 2026-07-30 | test-ci | 【变更概述】DeepSeek V4 性能优化，移除 flashmla sparse prefill  | auto-inherit | S | tests/kernels/attention/test_flashmla_sp |
| 904fae8b | 2026-07-30 | model-architecture | 【变更概述】DeepSeek V4 显存优化，修复 pipeline parallel 场景下 _m | auto-inherit | S | vllm/models/deepseek_v4/amd/model.py, vl |
| 5b958907 | 2026-07-30 | test-ci | 【变更概述】修复 FlexAttention 编码器场景下 block-mask 编译爆炸问题，避免 | config-align | M | tests/entrypoints/pooling/embed/test_onl |
| b8891661 | 2026-07-30 | test-ci | 【变更概述】Triton prefix-prefill 算子支持 cached K/V（key/va | auto-inherit | S | tests/kernels/attention/test_prefix_pref |
| a0cd2b69 | 2026-07-31 | test-ci | 【变更概述】【MRV2 commit】将 block table 宽度的 128-token 对齐逻 | auto-inherit | S | tests/v1/attention/test_indexer_deepseek |
| df71917c | 2026-07-31 | operator-kernel | 【变更概述】【DSv4 性能优化】为 DeepSeek V4 的 attention eager b | idea-copy | L | csrc/libtorch_stable/fused_deepseek_v4_q |
| 92643d68 | 2026-07-31 | model-architecture | 【变更概述】为 Kimi K3 DSpark（推测解码）模型实现 all-reduce + resi | auto-inherit | S | vllm/models/common/ops/__init__.py, vllm |
| 17beffd5 | 2026-07-31 | test-ci | 【变更概述】明确 split_audio 函数要求单声道（1D）音频输入，并增加多声道输入的显式校验 | auto-inherit | S | docs/features/multimodal_inputs.md, test |
| f727951d | 2026-07-31 | test-ci | 【变更概述】重新合入（re-land）MiniMax M3 的默认视频处理器修复。在 vllm/mo | auto-inherit | S | tests/multimodal/test_video.py, vllm/mod |
| 10e6b400 | 2026-07-31 | test-ci | 【变更概述】修复 CPU attention backend 中冗余的 KV cache 写入问题。 | auto-inherit | S | .buildkite/scripts/hardware_ci/run-cpu-t |
| 3ee2bd13 | 2026-07-31 | model-architecture | 【变更概述】修复 HunyuanVL 模型图像边界 token 重复的问题。此前 dummy 输入仅 | auto-inherit | S | vllm/model_executor/models/hunyuan_visio |
| bebf9180 | 2026-07-31 | test-ci | 【变更概述】为 JinaEmbeddingsV5Model 新增 JinaEmbeddingsV5M | auto-inherit | S | tests/models/language/pooling/test_jina_ |
| f1899b2f | 2026-07-31 | test-ci | 【变更概述】修复 ROCm AITER MLA 在 MTP（Multi-Token Predicti | idea-copy | L | tests/v1/attention/test_rocm_aiter_mla_m |
| 77469c90 | 2026-08-01 | test-ci | 【变更概述】修复 ROCm 平台 AITER MLA 注意力后端在小头（small-head）验证场 | idea-copy | L | tests/kernels/attention/test_rocm_aiter_ |
| f7097a92 | 2026-08-01 | model-architecture | 【变更概述】修复导入 vllm.models.common.ops 时意外初始化 CUDA 的问题。 | auto-inherit | S | vllm/models/common/ops/__init__.py, vllm |
| 68ca6fd0 | 2026-08-03 | config | 【变更概述】移除 SpeculativeConfig 中针对 DSpark 投机解码方法的错误启动断 | config-align | S | vllm/config/speculative.py |
| 89ac407e | 2026-08-03 | test-ci | 【变更概述】优化多模态占位符（placeholder）和 token 匹配扫描的性能。重构 vllm | auto-inherit | S | tests/multimodal/test_processing.py, vll |
| d83eb0b3 | 2026-08-03 | test-ci | 【变更概述】安全修复：将 NVIDIA DeepStream 视频处理管线正确分类为 GPU 后端， | auto-inherit | S | tests/multimodal/media/test_video.py, vl |
| 4635cc3e | 2026-08-03 | moe-fusion | 【变更概述】为 Kimi-K3 Latent-MoE 的 fused path 新增基于 token | auto-inherit | S | vllm/model_executor/layers/fused_moe/run |
| 7c40d61e | 2026-08-04 | model-architecture | 【变更概述】修复多模态 embeddings 展平逻辑，原先只处理 3D，现扩展到 >2D 的任意维 | auto-inherit | S | vllm/model_executor/models/transformers/ |
| 5f2ee2fa | 2026-08-04 | attention-kv-cache | 【变更概述】将 KV cache 容量日志打印时机调整到 block-size 解析完成之后，确保打 | auto-inherit | S | vllm/v1/core/kv_cache_utils.py, vllm/v1/ |
| 6a9fdf0d | 2026-08-04 | test-ci | 【变更概述】修复多模态 checkpoint 下序列分类（seq-cls）num_labels 未从 | auto-inherit | S | tests/models/test_adapters.py, vllm/mode |
| 41ba11b8 | 2026-08-04 | operator-kernel | 【变更概述】修复 Kimi K3 AttnRes dispatch 的 packed rows 与算 | idea-copy | L | csrc/libtorch_stable/kimi_k3/attn_res_ke |
| 6a9109d8 | 2026-08-04 | test-ci | 【变更概述】修复 Qwen3-Omni 在 use_audio_in_video=True 时处理无 | auto-inherit | S | tests/models/multimodal/processing/test_ |
| beca88e5 | 2026-08-05 | model-architecture | 【变更概述】修复 Kimi-K3 模型在启用专家并行（EP）时 moe_intermediate 层 | auto-inherit | S | vllm/models/kimi_k3/nvidia/model.py |
| f5cd862d | 2026-08-05 | model-architecture | 【变更概述】修复 Kimi-K3 模型在 ROCm 平台上的两个问题：(1) 混合批次时 KDA 算 | auto-inherit | S | vllm/models/kimi_k3/amd/kda.py, vllm/mod |
| 4719a9b8 | 2026-08-05 | model-architecture | 【变更概述】修复 EAGLE3 DeepSeek draft 模型在非 YaRN RoPE 配置下的 | auto-inherit | S | vllm/model_executor/models/deepseek_eagl |
| 7794b1e0 | 2026-08-05 | model-architecture | 【变更概述】修复 Qwen3 多模态模型在无视觉输入时仍尝试处理 deepstack buffers | auto-inherit | S | vllm/model_executor/models/qwen3_omni_mo |
| eb3dce97 | 2026-08-05 | test-ci | 【变更概述】修复 Gemma3n/Gemma4 模型处理变长音频批次时的 padding 问题。修改 | auto-inherit | S | tests/models/multimodal/generation/test_ |
| c416f157 | 2026-08-05 | model-architecture | 【变更概述】修复 Kimi-K3 模型在禁用上下文并行（CP）时 MLA 注意力的处理问题。修改 k | auto-inherit | S | vllm/models/kimi_k3/nvidia/mla.py |
| 33c50587 | 2026-08-05 | model-architecture | 【变更概述】恢复 Inkling 模型 MTP（Multi-Token Prediction）在 R | auto-inherit | S | vllm/models/inkling/amd/mtp.py |
| 5fba75ae | 2026-08-06 | model-architecture | 【变更概述】为 Kimi-K3 的 nvidia model 补充缺失的 fused_qkv_a_p | auto-inherit | S | vllm/models/kimi_k3/nvidia/model.py |
| ad528025 | 2026-08-06 | model-architecture | 【变更概述】DeepSeek-V3.2/GLM 在 MTP（Multi-Token Predicti | idea-copy | L | vllm/models/deepseek_v32/amd/rocm.py, vl |
| 2dfb8ba5 | 2026-08-06 | operator-kernel | 【变更概述】为 DeepSeek Sparse Attention（DSA）decode kerne | idea-copy | L | csrc/libtorch_stable/quantization/fp4/nv |
| febea17f | 2026-08-06 | test-ci | 【变更概述】修复原生 Qwen3.5 纯文本 checkpoint 加载时的权重前缀映射问题，确保权 | auto-inherit | S | tests/models/registry.py, vllm/model_exe |
| 53704616 | 2026-08-06 | test-ci | 【变更概述】修复混合架构（hybrid）模型在 hidden-state 提取场景下的前缀缓存命中错 | auto-inherit | S | tests/v1/core/test_kv_cache_utils.py, vl |
| c0202c56 | 2026-08-06 | test-ci | 【变更概述】为使用 draft model 的推测解码自动启用异步调度（async scheduli | config-align | S | tests/test_config.py, tests/v1/e2e/spec_ |
| 82171711 | 2026-08-06 | test-ci | 【变更概述】当 pooling 模型存在 WeightsMapper 时跳过 weight-pref | auto-inherit | S | tests/models/test_adapters.py, vllm/mode |
| f84df12c | 2026-08-06 | test-ci | 【变更概述】修复 Transformers v5 下 MiniCPM-V 的占位符替换与图像处理器加 | auto-inherit | S | tests/models/multimodal/processing/test_ |
| d54b58cc | 2026-08-06 | distributed | 【变更概述】将 host cache 清理由平台特定调用改为 torch.accelerator.e | cherry-pick | S | vllm/distributed/parallel_state.py |
| f85c1d2f | 2026-08-06 | model-architecture | 【变更概述】移除 Kimi-K3 nvidia model 中 megamoe 路径的冗余 add  | auto-inherit | S | vllm/models/kimi_k3/nvidia/model.py |
| b50fdebc | 2026-08-06 | test-ci | 【变更概述】修复 level-2 sleep/wake/reload 在 enable_lora=T | cherry-pick | M | docs/features/sleep_mode.md, tests/basic |
| 8cfa01cd | 2026-08-06 | test-ci | 【变更概述】修复 Dense 模型多节点数据并行（DP）rescope 问题，修改 config/p | config-align | S | tests/test_config.py, vllm/config/parall |

## P3 优先级 (165 个)
| SHA | 日期 | 分类 | 优化内容 | 迁移策略 | 工作量 | 关键文件 |
|-----|------|------|---------|---------|--------|---------|
| d35eba30 | 2026-07-08 | test-ci | 【变更概述】[Bugfix] 更新：Avoid leaking Pydantic repr tool | auto-inherit | S | tests/entrypoints/openai/chat_completion |
| 5d5fab00 | 2026-07-08 | test-ci | 【变更概述】[Bugfix] 修复：前端 修复 http_requests_total metric | auto-inherit | S | tests/entrypoints/serve/instrumentator/t |
| bc44f9fe | 2026-07-09 | moe-fusion | 【变更概述】[ROCm] 修复：CI][MoE 修复 double-transpose 融合 w3  | auto-inherit | S | vllm/model_executor/layers/fused_moe/rou |
| 6cf7b26b | 2026-07-09 | moe-fusion | 【变更概述】[docs] 修复：修复 文档 build
【PR号】#48008
【变更类型】此提交为 | auto-inherit | S | vllm/model_executor/layers/fused_moe/lay |
| 089e4128 | 2026-07-09 | test-ci | 【变更概述】[Perf] 更新：Integrate TRTLLM BF16 MoE Modular  | auto-inherit | S | tests/kernels/moe/test_trtllm_bf16_moe.p |
| d1f1d867 | 2026-07-09 | test-ci | 【变更概述】[Bugfix] 更新：Re-enable benchmarking librispee | auto-inherit | S | tests/benchmarks/test_audio_dataset.py,  |
| 88e5e2c5 | 2026-07-10 | test-ci | 【变更概述】[CI/Build] 修复：AMD 修复 ROCm OOM eagle_correctn | auto-inherit | S | tests/v1/e2e/spec_decode/test_spec_decod |
| 766469a4 | 2026-07-10 | other | 【变更概述】[ROCm] 修复：Revert Part `[ROCm 修复 pooling star | auto-inherit | S | vllm/v1/worker/gpu_worker.py |
| ed908cf0 | 2026-07-11 | test-ci | 【变更概述】[Bugfix] 修复：修复 thinking_token_budget not enf | auto-inherit | S | tests/v1/logits_processors/test_correctn |
| 735def4f | 2026-07-11 | other | 【变更概述】[Bugfix] 修复：修复 FlashMLA dense fp8 metadata c | auto-inherit | S | cmake/external_projects/flashmla.cmake |
| 5f8e73cb | 2026-07-12 | test-ci | 【变更概述】[Bugfix] 更新：保护 mixed-dtype AllReduce RMSNorm | auto-inherit | S | tests/compile/passes/distributed/test_fu |
| 9a48eef8 | 2026-07-12 | test-ci | 【变更概述】[Bugfix] 新增：LoRA 支持 ark_linear base layer _g | auto-inherit | S | tests/lora/test_layers_utils.py, vllm/lo |
| b3cfca99 | 2026-07-13 | other | 【变更概述】[Mypy Fix] 更新：拆分 Mypy 工作
【PR号】#48490
【变更类型】此 | auto-inherit | S | tools/pre_commit/mypy.py |
| 2595d5ce | 2026-07-13 | moe-fusion | 【变更概述】[Model] 优化：优化 Qwen3.5 H20
【PR号】#48350
【变更类型】 | auto-inherit | S | vllm/model_executor/layers/fused_moe/con |
| 4c81772e | 2026-07-13 | distributed | 【变更概述】[Bugfix] [KV Offloading] 修复：修复 stale transfe | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| af453e56 | 2026-07-14 | test-ci | 【变更概述】[Bugfix] 更新：Gemma4 parser classify channel-l | auto-inherit | S | tests/parser/engine/test_gemma4_streamin |
| 32aef443 | 2026-07-14 | test-ci | 【变更概述】[Bugfix] 更新：Include inline per-token-head sc | auto-inherit | S | tests/v1/core/test_kv_cache_utils.py, vl |
| 038ec293 | 2026-07-14 | test-ci | 【变更概述】[Bugfix] 更新：Return 400 instead 500 when 多模态  | auto-inherit | S | tests/renderers/test_process_multi_modal |
| c9a788ee | 2026-07-14 | other | 【变更概述】修复：fix(security guard lm-format-enforcer reg | auto-inherit | S | vllm/v1/structured_output/backend_lm_for |
| dcf4072d | 2026-07-14 | other | 【变更概述】[Perf] [ROCm] 修复：修复 GDN KKT warmup regressio | auto-inherit | S | vllm/model_executor/layers/fla/ops/chunk |
| fec64fea | 2026-07-14 | other | 【变更概述】[BugFix] 更新：Correct OTEL span start time Dyn | auto-inherit | S | vllm/compilation/backends.py |
| 550218b1 | 2026-07-14 | test-ci | 【变更概述】[Bugfix] [Frontend] 更新：Flush engine reasonin | auto-inherit | S | tests/parser/test_streaming.py, vllm/par |
| 1b30ae4c | 2026-07-15 | other | 【变更概述】[Rust Frontend] 修复：修复 flaky `tls_handshake_t | auto-inherit | S | rust/.config/nextest.toml, rust/src/serv |
| 66b6c684 | 2026-07-15 | distributed | 【变更概述】[PD] [Bugfix] 修复：修复 validation 缓存 shape attn | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| c0302d94 | 2026-07-15 | test-ci | 【变更概述】[Bugfix] 修复：修复 parallel_tool_calls=null cras | auto-inherit | S | tests/tool_use/test_responses_request_va |
| 313fae3e | 2026-07-15 | other | 【变更概述】[Bugfix] 修复：修复 GLM5 config
【PR号】#48711
【变更类型 | auto-inherit | S | vllm/transformers_utils/config.py |
| 7aab6e26 | 2026-07-15 | test-ci | 【变更概述】[ROCm] [Bugfix] 更新：Enable fp32 head_dtype to | auto-inherit | S | tests/v1/sample/test_head_dtype.py, vllm |
| 3b39fd28 | 2026-07-15 | test-ci | 【变更概述】[Bugfix] [Spec Decode] 新增：支持 heterogeneous Q | auto-inherit | S | tests/compile/passes/test_qk_norm_rope_f |
| 64721312 | 2026-07-15 | other | 【变更概述】[Bugfix] 更新：Set kv_quant_mode generic MLA KV | auto-inherit | S | vllm/model_executor/layers/attention/mla |
| 0bd6b85a | 2026-07-15 | test-ci | 【变更概述】[Bugfix] 更新：Preserve unloaded non-persistent | auto-inherit | S | tests/model_executor/model_loader/test_r |
| 520a20ba | 2026-07-15 | test-ci | 【变更概述】[Bugfix] 新增：MoRIIO toy P/D proxy 添加 /health
 | auto-inherit | S | examples/disaggregated/disaggregated_ser |
| 32e632df | 2026-07-15 | other | 【变更概述】[Reasoning] 优化：优化 TPOT thinking budget when  | auto-inherit | S | vllm/v1/sample/rejection_sampler.py, vll |
| b2f7d256 | 2026-07-15 | other | 【变更概述】[Bugfix] 更新：Make MLA+SWA check layer's 后端 no | auto-inherit | S | vllm/model_executor/layers/attention/att |
| 75bdad40 | 2026-07-16 | test-ci | 【变更概述】[Bug] [Quantization] 修复：修复 humming is_layer_ | auto-inherit | S | tests/quantization/test_humming_ignore.p |
| d08eebad | 2026-07-16 | test-ci | 【变更概述】[Perf] [MoE] 更新：Write FlashInfer combine int | auto-inherit | S | tests/distributed/test_mnnvl_alltoall.py |
| 530852f9 | 2026-07-16 | test-ci | 【变更概述】[KV Connector] 修复：修复 PD async scheduling rac | auto-inherit | S | tests/v1/kv_connector/unit/test_nixl_con |
| 12f2c515 | 2026-07-16 | distributed | 【变更概述】[Bugfix] 修复：修复 卸载 set_ overflow packed non-u | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| 59b964f3 | 2026-07-16 | test-ci | 【变更概述】修复：fix(lora validate LoRA rank is positive P | auto-inherit | S | tests/lora/test_peft_helper.py, vllm/lor |
| df8a0900 | 2026-07-16 | other | 【变更概述】[BugFix] 更新：Don't apply weight batch-invaria | auto-inherit | S | vllm/model_executor/layers/batch_invaria |
| 0becb748 | 2026-07-16 | other | 【变更概述】[BugFix] [MLA] 新增：支持 kv_cache_dtype_skip_lay | auto-inherit | S | vllm/model_executor/layers/attention/mla |
| 2dab187f | 2026-07-16 | operator-kernel | 【变更概述】[Perf] 优化：优化 `fused_topk_bias` DSv4 1.5~2x 内 | idea-copy | L | csrc/libtorch_stable/moe/topk_softplus_s |
| 2bd89576 | 2026-07-16 | quantization | 【变更概述】[Bugfix] [NVFP4 MoE] 更新：Pad gated intermedia | auto-inherit | S | vllm/model_executor/layers/quantization/ |
| 43cd3402 | 2026-07-16 | other | 【变更概述】[Fix] 更新：Align OpenAI vllm_xargs value types | auto-inherit | S | vllm/entrypoints/openai/completion/proto |
| 1d99f0f4 | 2026-07-16 | test-ci | 【变更概述】[ROCm] [BugFix] 更新：Triton W4A16 handling GPT | auto-inherit | S | tests/kernels/quantization/test_triton_w |
| c7ce03bc | 2026-07-18 | other | 【变更概述】升级 tml-fa4（FlashAttention 4 外部依赖）版本以适配 cutla | auto-inherit | S | cmake/external_projects/tml_fa4.cmake |
| d96aee09 | 2026-07-18 | other | 【变更概述】修复 replicated 权重和 disable_tp 场景下权重重新加载时 tp_r | auto-inherit | S | vllm/model_executor/layers/linear.py, vl |
| c71a583a | 2026-07-18 | other | 【变更概述】对 hybrid（Mamba/SSM）模型 _copy_mamba_state_bloc | auto-inherit | S | vllm/v1/worker/mamba_utils.py |
| f12b80c6 | 2026-07-18 | test-ci | 【变更概述】修复 ROCm 平台 GPT-OSS 模型使用 Quark MXFP4 量化时 MoE  | auto-inherit | S | tests/kernels/moe/test_ocp_mx_moe.py, vl |
| da64db78 | 2026-07-18 | moe-fusion | 【变更概述】优化 TrtLlmLoRAExperts（TensorRT-LLM 风格的 LoRA M | auto-inherit | S | vllm/model_executor/layers/fused_moe/exp |
| 425c4eaf | 2026-07-18 | test-ci | 【变更概述】优化采样路径：apply_sampling_params 不再强制将 logits 上转 | auto-inherit | S | tests/v1/sample/test_topk_topp_sampler.p |
| fae54301 | 2026-07-18 | other | 【变更概述】将 beam-search 离线入口的 beam 拍平从 sum（O(n²)）改为 it | auto-inherit | S | vllm/entrypoints/generate/beam_search/of |
| b5433b6f | 2026-07-18 | operator-kernel | 【变更概述】为 DeepSeek-V4（DSV4）的 MoE routing 引入专用 CUDA k | idea-copy | L | csrc/libtorch_stable/moe/topk_softplus_s |
| c4cd2bd5 | 2026-07-18 | test-ci | 【变更概述】修复 MoRIIO toy P/D（Prefill/Decode 分离）代理服务器在 D | auto-inherit | S | examples/disaggregated/disaggregated_ser |
| 11d29151 | 2026-07-18 | test-ci | 【变更概述】修复 MiniMax M2、Qwen3、MiniCPM5 XML 工具解析器在解析参数值 | auto-inherit | S | tests/parser/engine/test_qwen3.py, tests |
| 8ce53a61 | 2026-07-20 | other | 【变更概述】修复量化 + 滑动窗口混合 KV 缓存场景下，新分配的 KV 块未零初始化导致 deco | auto-inherit | S | vllm/v1/kv_cache_interface.py |
| 530ee36a | 2026-07-20 | test-ci | 【变更概述】修复 OpenAI 兼容接口中非数字 logprobs 值导致 HTTP 500 错误的 | auto-inherit | S | tests/entrypoints/openai/chat_completion |
| 8950394e | 2026-07-21 | test-ci | 【变更概述】修复当 KV connector 延迟请求时 prefix-cache 命中指标被重复计 | auto-inherit | S | tests/v1/core/test_scheduler.py, tests/v |
| 7bb49be4 | 2026-07-21 | other | 【变更概述】修复 FA4 JIT 预热阶段 MLA 模型回退处理的边界问题。修改 fa4_cuted | auto-inherit | S | vllm/model_executor/warmup/fa4_cutedsl_w |
| f890e1db | 2026-07-21 | test-ci | 【变更概述】【MRV2 相关】修复 MRV2 中 FULL CUDA graph 捕获前未设置 gr | idea-copy | L | tests/v1/cudagraph/test_cudagraph_manage |
| 1134545b | 2026-07-21 | test-ci | 【变更概述】【MRV2 相关】回退 PR #48641，恢复在 apply_sampling_par | auto-inherit | S | tests/v1/sample/test_topk_topp_sampler.p |
| 94ed0bf4 | 2026-07-21 | test-ci | 【变更概述】修复 KV Offloading connector 在处理已排队但未分配 KV blo | auto-inherit | S | tests/v1/kv_connector/unit/offloading_co |
| 58b2012a | 2026-07-21 | test-ci | 【变更概述】修复 CuMem（CUDA 内存管理）slept-L1 碎片化统计问题。修改 mem_u | auto-inherit | S | tests/models/language/pooling/test_rewar |
| 53c2f20d | 2026-07-22 | moe-fusion | 【变更概述】修复 ROCm 平台 EPLB（Expert-Level Load Balancing） | auto-inherit | S | vllm/model_executor/layers/fused_moe/unq |
| 2dc5a72e | 2026-07-22 | other | 【变更概述】修复异步渲染路径中视觉 chunk UUID 未重建的问题。在 HfRenderer 中 | auto-inherit | S | vllm/renderers/hf.py |
| d6dbdb9b | 2026-07-22 | operator-kernel | 【变更概述】为 XPU 平台添加 topk_softplus_sqrt 算子参数不匹配的临时规避方案 | auto-inherit | S | vllm/_custom_ops.py |
| 06da482f | 2026-07-22 | operator-kernel | 【变更概述】为 XPU 平台添加 topk_softmax 算子参数不匹配的临时规避方案（Worka | auto-inherit | S | vllm/_custom_ops.py |
| 7c21548c | 2026-07-22 | distributed | 【变更概述】修复 NIXL KV connector 在混合 MLA+Mamba（SSM）模型异构  | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| 1ad84fea | 2026-07-23 | test-ci | 【变更概述】修复投机解码中 stop string 检测的边界问题。当多个 stop string  | auto-inherit | S | tests/detokenizer/test_check_stop_string |
| 12213c67 | 2026-07-23 | test-ci | 【变更概述】修复结构化输出语法编译失败时导致引擎崩溃的问题。此前当 XGrammar/LLGuida | auto-inherit | S | tests/v1/core/test_async_scheduler.py, t |
| 10c75477 | 2026-07-23 | test-ci | 【变更概述】修复共享内存广播（shm_broadcast）机制中空闲 reader 无限等待与读取槽 | auto-inherit | S | tests/distributed/test_shm_broadcast.py, |
| a76df87d | 2026-07-23 | test-ci | 【变更概述】修复 MooncakeStore KV 连接器在存储边界上外部命中（external h | auto-inherit | S | tests/v1/kv_connector/unit/test_mooncake |
| a4904ba9 | 2026-07-23 | test-ci | 【变更概述】将 MooncakeStore KV 连接器在 KV 加载路径上的 prepare_va | auto-inherit | S | tests/v1/kv_connector/unit/test_mooncake |
| b07ec92f | 2026-07-23 | test-ci | 【变更概述】修复 NVFP4 量化 MoE（Mixture of Experts）中共享 scale | auto-inherit | S | tests/quantization/test_trtllm_nvfp4_hid |
| 229e01e9 | 2026-07-23 | test-ci | 【变更概述】修复混合模型（hybrid models，如包含不同 attention 类型的层）在使 | auto-inherit | S | tests/v1/core/test_scheduler.py, vllm/v1 |
| 149daf0d | 2026-07-23 | test-ci | 【变更概述】修复 torch.compile 缓存命中问题。此前路径派生的环境变量（如安装路径）被纳 | auto-inherit | S | tests/config/test_config_utils.py, vllm/ |
| 917fdb5b | 2026-07-23 | other | 【变更概述】修复使用 FlashInferFp8DeepGEMMDynamicBlockScaled | auto-inherit | S | vllm/model_executor/warmup/deep_gemm_war |
| 8eac21a6 | 2026-07-24 | test-ci | 【变更概述】修复 ROCm AITER 融合 AllReduce+RMSNorm 的 token_n | auto-inherit | S | tests/compile/fusions_e2e/test_tp2_ar_rm |
| a454a1dd | 2026-07-24 | test-ci | 【变更概述】修复 #39896 引入的回归：--skip-tokenizer-init 与 --da | auto-inherit | S | tests/benchmarks/test_skip_tokenizer_ini |
| 163ecba3 | 2026-07-24 | other | 【变更概述】修复 layerwise reload 时线性 bias 被错误重载导致权重损坏。bia | auto-inherit | S | vllm/model_executor/model_loader/reload/ |
| 589a5b88 | 2026-07-24 | test-ci | 【变更概述】修复 PD 分离部署 NixlPush KV 连接器 writer 线程同步握手阻塞管线 | auto-inherit | S | docs/design/nixl_kv_push_connector.md, t |
| 275556c3 | 2026-07-24 | test-ci | 【变更概述】修复 packed KV cache specs 在混合精度下未被正确检测的问题，修改  | auto-inherit | S | tests/v1/core/test_kv_cache_utils.py, vl |
| 1423569f | 2026-07-25 | test-ci | 【变更概述】修复 Jamba 和 InternLM2 工具解析器在流式输出时丢弃部分参数的 bug， | auto-inherit | S | tests/tool_parsers/test_internlm2_tool_p |
| a82f1b38 | 2026-07-25 | other | 【变更概述】性能优化：当 prefix caching 关闭时，跳过 free_blocks 中的  | auto-inherit | S | vllm/v1/core/block_pool.py |
| 70052fb9 | 2026-07-25 | test-ci | 【变更概述】修复 Mooncake store worker 中 TP 分片的 Mamba stat | auto-inherit | S | tests/v1/kv_connector/unit/test_mooncake |
| 7154856f | 2026-07-26 | distributed | 【变更概述】修复 KV cache 在接收端布局后处理（kv_postprocess_layout_ | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| 3f1d4096 | 2026-07-26 | distributed | 【变更概述】修复 OffloadingConnectorScheduler 中 num_tokens | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| 55596792 | 2026-07-26 | distributed | 【变更概述】修复 OffloadingConnectorScheduler 中 sliding wi | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| 7a29a3c5 | 2026-07-26 | test-ci | 【变更概述】修复 KV 卸载持久化缓存（FileMapper）的命名空间未区分 V1（paralle | auto-inherit | S | tests/v1/kv_offload/test_file_mapper.py, |
| 48ebd6f2 | 2026-07-26 | other | 【变更概述】修复 KVConnector 在 per-token-head 量化模式下启用跨层 KV | auto-inherit | S | vllm/v1/worker/kv_connector_model_runner |
| d2ca3002 | 2026-07-27 | other | 【变更概述】【MRV2 commit】在 MRV2 采样器中跳过不必要的 FP32 logits 物 | auto-inherit | S | vllm/v1/worker/gpu/sample/sampler.py |
| 27d7061e | 2026-07-27 | test-ci | 【变更概述】修复 JinaRankingIOProcessor 在在线请求构建时丢失 truncat | auto-inherit | S | tests/entrypoints/pooling/scoring/test_j |
| 56c96b0d | 2026-07-27 | other | 【变更概述】为 LL BF16 Router GEMM 添加 SM100F（Blackwell）和  | auto-inherit | S | vllm/model_executor/kernels/linear/cute_ |
| 59a6b041 | 2026-07-27 | test-ci | 【变更概述】修复 DP 内部负载均衡（LB）的多个问题：(1) 移除 Rust 前端 routing | auto-inherit | S | rust/src/engine-core-client/src/client/s |
| 96fa3f42 | 2026-07-27 | other | 【变更概述】在 kernel_warmup 中为 ll_bf16 router GEMM 预热添加  | auto-inherit | S | vllm/model_executor/warmup/kernel_warmup |
| 30fbd055 | 2026-07-27 | test-ci | 【变更概述】修复 ReplaySSM Triton 内核在 ROCm 上不支持 tf32x3 的问题 | auto-inherit | S | .buildkite/test-amd.yaml, vllm/model_exe |
| 394beb63 | 2026-07-27 | test-ci | 【变更概述】修复 ROCm 平台 CPU KV cache 加载使用 Triton 内核的问题。RO | auto-inherit | S | tests/v1/kv_offload/cpu/test_gpu_worker. |
| eb290ab6 | 2026-07-27 | test-ci | 【变更概述】修复 CPU 平台 MoE grouped-gemm 内核在 TP 分片后 interm | auto-inherit | S | tests/kernels/moe/test_cpu_fused_moe.py, |
| cbc3a872 | 2026-07-27 | other | 【变更概述】修复 HF tokenizer 在双格式 Mistral 仓库中选择错误 tokeniz | auto-inherit | S | vllm/tokenizers/registry.py |
| 544cb724 | 2026-07-27 | operator-kernel | 【变更概述】优化 CPU 平台投机解码的 GDN 卷积路径。重构 conv.cpp 和 gdn_at | idea-copy | L | csrc/cpu/sgl-kernels/conv.cpp, csrc/cpu/ |
| 53397fbf | 2026-07-27 | test-ci | 【变更概述】修复 KV Offload P2P 传输中重连到已回收 peer 时 EngineCor | auto-inherit | S | tests/v1/kv_offload/tiering/p2p/test_zmq |
| 49f31d7c | 2026-07-27 | test-ci | 【变更概述】修复 ROCm 平台 vllm_c RMSNorm 内核输出非连续张量的问题。
【PR号 | auto-inherit | S | tests/kernels/ir/test_layernorm.py, vllm |
| 74d3b799 | 2026-07-27 | other | 【变更概述】修复 mHC block-M prenorm GEMM 中跨行规约进位错误。
【PR号】 | auto-inherit | S | vllm/model_executor/kernels/mhc/tilelang |
| 439f3362 | 2026-07-27 | other | 【变更概述】【MRV2 commit】修复 MRV2 mamba_hybrid.py 中的 GPU< | auto-inherit | S | vllm/v1/worker/gpu/model_states/mamba_hy |
| 30217b0e | 2026-07-28 | test-ci | 【变更概述】修复 P2P KV Offload 会话中 serve 状态管理问题，将 serve 状 | auto-inherit | S | tests/v1/kv_offload/tiering/p2p/test_man |
| 1e81853a | 2026-07-28 | test-ci | 【变更概述】修复 Mamba 模型在 DCP（Decode Context Parallelism） | auto-inherit | S | tests/v1/kv_connector/unit/offloading_co |
| 98e91a96 | 2026-07-28 | distributed | 【变更概述】优化 NIXL Push 模式 D->P 握手流程，跳过多余的 add_remote_a | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| 948107ac | 2026-07-28 | test-ci | 【变更概述】增强 Intel INC 量化方案的 extra_config 处理，修复 layer  | auto-inherit | S | tests/quantization/test_auto_round.py, v |
| b09688a6 | 2026-07-28 | other | 【变更概述】修复 speculative decode 在 level-2 sleep（GPU 休眠 | auto-inherit | S | vllm/v1/worker/gpu_worker.py |
| 03a2d033 | 2026-07-28 | other | 【变更概述】修复权重加载时未在所有平台上遵循 cgroup 内存限制的问题，统一内存限制检测逻辑。
 | auto-inherit | S | vllm/model_executor/model_loader/weight_ |
| f472ab0a | 2026-07-28 | test-ci | 【变更概述】移除 ROCm 平台的 triton per group 量化逻辑，清理 input_q | auto-inherit | S | tests/compile/passes/distributed/test_fu |
| 52c3c4a4 | 2026-07-28 | test-ci | 【变更概述】修复 OBJ（对象存储）KV Offload 在清理期间作业完成状态丢失的问题。
【PR | auto-inherit | S | tests/v1/kv_offload/tiering/test_obj_tie |
| a8f29608 | 2026-07-28 | test-ci | 【变更概述】使 KV Offload 的紧凑二级标识（compact secondary ident | auto-inherit | S | tests/v1/kv_offload/test_file_mapper.py, |
| 33fe71a4 | 2026-07-28 | test-ci | 【变更概述】回退 AMD MXFP4 MoE backend 的 TRITON_UNFUSED 回退 | auto-inherit | S | tests/kernels/moe/test_ocp_mx_moe.py, te |
| 12068918 | 2026-07-28 | distributed | 【变更概述】修复 ROCm MoRI-IO KV Connector 在 WRITE 模式下远程 T | auto-inherit | S | vllm/distributed/kv_transfer/kv_connecto |
| a0c092ee | 2026-07-29 | test-ci | 【变更概述】修复异步调度（AsyncScheduler）下请求被抢占时 num_output_pla | auto-inherit | S | tests/v1/core/test_async_scheduler.py, t |
| e0cfa52d | 2026-07-29 | other | 【变更概述】修复语音转文字（speech-to-text）接口中 transcription 与 t | auto-inherit | S | vllm/entrypoints/speech_to_text/base/ser |
| 72297d85 | 2026-07-29 | other | 【变更概述】将 XPU 平台上无权重（weightless）的 RMSNorm 路由到 _C 扩展分 | auto-inherit | S | vllm/kernels/xpu_ops.py |
| db7a79cb | 2026-07-29 | operator-kernel | 【变更概述】修复 s390x（IBM Z 架构）构建问题并更新 dockerfile 中的 torc | idea-copy | L | csrc/cpu/cpu_types_vxe.hpp, docker/Docke |
| 59e831c0 | 2026-07-30 | test-ci | 【变更概述】新增编译 pass：将 Transformers 的 Residual Add 与 RM | auto-inherit | S | tests/compile/passes/test_rmsnorm_reshap |
| e04a30a7 | 2026-07-30 | test-ci | 【变更概述】前端 chat_utils 延迟初始化媒体连接器，避免不必要的初始化开销。
【PR号】# | auto-inherit | S | tests/entrypoints/unit_tests/test_chat_u |
| 4e582c5b | 2026-07-30 | test-ci | 【变更概述】P/D 分离场景下，将 KV lease 截止时间从全局时钟重算到 worker 本地时 | auto-inherit | S | tests/v1/kv_connector/unit/test_nixl_con |
| 437e0b7f | 2026-07-30 | test-ci | 【变更概述】修复 P/D 分离下的抢占竞态条件。修改核心 vllm/v1/core/sched/sc | auto-inherit | S | tests/v1/core/test_async_scheduler.py, t |
| b28c178f | 2026-07-30 | other | 【变更概述】修复 Quark 量化模型在推测解码场景下 FusedMoE 触发的 Assertion | auto-inherit | S | (无文件变更信息) |
| 48aa8d8d | 2026-07-30 | test-ci | 【变更概述】修复多进程执行器中陈旧 RPC deadline 变成无限等待的问题，修改 shm_br | auto-inherit | S | tests/v1/executor/test_multiproc_executo |
| 94e9ef07 | 2026-07-31 | test-ci | 【变更概述】修复融合 MoE（Fused MoE）权重加载中对量化 scale 转置的问题。此前 R | auto-inherit | S | tests/kernels/moe/test_moe_weight_loadin |
| 5233368d | 2026-07-31 | moe-fusion | 【变更概述】为 ROCm gfx942 平台添加 MXFP4 仿真回退路径。当 AITER MXFP | auto-inherit | S | vllm/model_executor/layers/fused_moe/exp |
| 0b5b49dd | 2026-07-31 | test-ci | 【变更概述】将 vllm/entrypoints/chat_utils.py 中多处面向用户的 Va | auto-inherit | S | tests/entrypoints/unit_tests/test_chat_u |
| f5ffc59b | 2026-07-31 | other | 【变更概述】修复 renderer 预热（warmup）流程，将其从 OpenAIServingCh | auto-inherit | S | vllm/entrypoints/generate/api_router.py, |
| 1d8be5cb | 2026-07-31 | other | 【变更概述】将 deepseek_v4_fp8 加入 XPUPlatform 的 supported | auto-inherit | S | vllm/platforms/xpu.py |
| ef0d084b | 2026-07-31 | other | 【变更概述】修复 XPU FP8 block-scaled GEMM kernel 的 scale  | auto-inherit | S | vllm/model_executor/kernels/linear/scale |
| 4689c7dd | 2026-07-31 | other | 【变更概述】为 AMD Instinct MI325X 显卡新增 selective_state_u | auto-inherit | S | vllm/model_executor/layers/mamba/ops/con |
| d91f7af7 | 2026-07-31 | test-ci | 【变更概述】修复 ROCm DeepEP 的 FP8 dispatch 量化上界问题。将 DeepE | idea-copy | L | docker/Dockerfile.rocm, tests/kernels/mo |
| ab98034d | 2026-07-31 | test-ci | 【变更概述】修复 Kimi K3 工具调用 ID 在多轮会话中重复的问题。此前解析器根据 XTML  | auto-inherit | S | rust/src/chat/src/renderer/kimi_k3/encod |
| 0bff0ce5 | 2026-07-31 | test-ci | 【变更概述】修复 DeepGEMM MoE 在 Kimi K3 配置下的 ep_gather 内核问 | auto-inherit | S | tests/kernels/moe/test_deepgemm.py, vllm |
| 39f55ffd | 2026-08-01 | other | 【变更概述】将 AsyncLLM 中原始提示词（raw prompt）的预处理（tokenizati | auto-inherit | S | vllm/v1/engine/async_llm.py, vllm/v1/eng |
| 6c91de36 | 2026-08-01 | other | 【变更概述】修复推理解析器（reasoning parser）未将 model_config 转发给 | auto-inherit | S | vllm/parser/abstract_parser.py |
| ec40f6a8 | 2026-08-03 | other | 【变更概述】修复 CPU-only 主机上 torch.compile 因调用 torch.acce | auto-inherit | S | vllm/v1/worker/cpu/shm.py, vllm/v1/worke |
| 2755489a | 2026-08-03 | test-ci | 【变更概述】修复 INC（Intel Neural Compressor）w4a4 量化模型的问题。 | auto-inherit | S | tests/quantization/test_auto_round.py, v |
| f5bb701f | 2026-08-03 | test-ci | 【变更概述】在 Anthropic API 兼容入口点约束 cache_salt 为非空。修改 vl | auto-inherit | S | tests/entrypoints/anthropic/test_anthrop |
| 5e35a6f4 | 2026-08-03 | other | 【变更概述】当编译模式为 CompilationMode.NONE 时跳过 CPU model ru | auto-inherit | S | vllm/v1/worker/cpu_model_runner.py |
| 5c4fe4b1 | 2026-08-03 | test-ci | 【变更概述】修复 Mooncake KV Connector 在合并的 store 组间未正确传播  | auto-inherit | S | tests/v1/kv_connector/unit/test_mooncake |
| 7b50d2c0 | 2026-08-04 | moe-fusion | 【变更概述】重构 vllm/model_executor/layers/fused_moe/all2 | auto-inherit | S | vllm/model_executor/layers/fused_moe/all |
| 199644d4 | 2026-08-04 | test-ci | 【变更概述】修复 sparse MLA 在 masked MHA 路径下 workspace 未正确 | auto-inherit | S | tests/v1/attention/test_sparse_mla_backe |
| 24c939c4 | 2026-08-04 | other | 【变更概述】修复 XPU 平台 collect_env.py 中 oneccl 版本信息采集问题。
 | auto-inherit | S | vllm/collect_env.py |
| a1657a02 | 2026-08-04 | other | 【变更概述】修复 DeepGEMM 在 CUDA 12.9 下 FP8 头文件可见性问题，调整 cm | auto-inherit | S | cmake/external_projects/deepgemm.cmake,  |
| adbf08d9 | 2026-08-04 | test-ci | 【变更概述】优化 Kimi K3 reasoning parser 在 decode 路径上的推理结 | auto-inherit | S | tests/reasoning/test_kimi_k3_reasoning_p |
| 385d4c08 | 2026-08-04 | test-ci | 【变更概述】修复 ROCm AITER triton MOE routing 的 memory ac | auto-inherit | S | tests/models/quantization/test_gpt_oss.p |
| 413e70d5 | 2026-08-04 | moe-fusion | 【变更概述】新增 NVIDIA H20 平台 E=256,N=512 的 fused MoE 性能配 | auto-inherit | S | vllm/model_executor/layers/fused_moe/con |
| 08b8613b | 2026-08-05 | test-ci | 【变更概述】修复 MiniMax-M3 模型使用 NVFP4 量化时 flashinfer cutl | auto-inherit | S | tests/kernels/moe/test_flashinfer_moe.py |
| cd930c8e | 2026-08-05 | other | 【变更概述】修复 MLA（Multi-Head Latent Attention）在 Marlin  | auto-inherit | S | vllm/model_executor/layers/attention/mla |
| b92352ca | 2026-08-05 | test-ci | 【变更概述】优化 CPU KV Offload 的 ARC（Adaptive Replacement | auto-inherit | S | tests/v1/kv_offload/cpu/test_manager.py, |
| 999dd8b4 | 2026-08-05 | other | 【变更概述】为 XPU 平台添加 is_current_stream_capturing 的别名，指 | auto-inherit | S | vllm/v1/worker/xpu_model_runner.py |
| 50c51682 | 2026-08-05 | test-ci | 【变更概述】修复 EC（Encoder-Connector）Connector 在图像编码完成前错误 | auto-inherit | S | examples/disaggregated/disaggregated_enc |
| 2cb3ff88 | 2026-08-05 | quantization | 【变更概述】修复 compressed_tensors w8a16_fp8 量化方案中 KV sca | auto-inherit | S | vllm/model_executor/layers/quantization/ |
| ffee3246 | 2026-08-05 | test-ci | 【变更概述】修复 Mooncake KV Connector 使用局部 DP index 而非全局  | auto-inherit | S | tests/v1/kv_connector/unit/test_mooncake |
| 62a86318 | 2026-08-06 | other | 【变更概述】修复 VocabParallelEmbedding 的 extra_repr 方法中字段 | auto-inherit | S | vllm/model_executor/layers/vocab_paralle |
| 46e6a83c | 2026-08-06 | kv-offload | 【变更概述】修复 KV Offload（CPU/tiering）在初始化失败后未正确清理资源的问题， | auto-inherit | S | vllm/v1/kv_offload/cpu/spec.py, vllm/v1/ |
| ef2615c2 | 2026-08-06 | test-ci | 【变更概述】当系统不支持 MADV_POPULATE_WRITE 时，KV offload 的 sh | auto-inherit | S | tests/v1/kv_offload/cpu/test_shared_offl |
| 872fd597 | 2026-08-06 | moe-fusion | 【变更概述】在 unquantized MoE oracle 的 LoRA gate 逻辑中增加激活 | auto-inherit | S | vllm/model_executor/layers/fused_moe/ora |
| 9c226684 | 2026-08-06 | test-ci | 【变更概述】修复在线 NVFP4 专家打包过程中的精度损失问题，调整 nvfp4.py 打包逻辑。
 | auto-inherit | S | tests/quantization/test_online.py, vllm/ |
| 7e724dca | 2026-08-06 | test-ci | 【变更概述】修复 ROCm AITER all-reduce 融合 pass 的覆盖范围问题，调整  | auto-inherit | S | tests/compile/passes/distributed/test_fu |
| 2e35c529 | 2026-08-06 | test-ci | 【变更概述】修复 FlashInfer CUTLASS 路径下 MXFP4 MoE 专家的转换逻辑， | auto-inherit | S | tests/kernels/moe/test_ocp_mx_moe.py, vl |
| 9f316996 | 2026-08-06 | moe-fusion | 【变更概述】对齐 TRTLLM MXFP4 MoE 的 autotune buckets 配置。
【 | auto-inherit | S | vllm/model_executor/layers/fused_moe/exp |
| 47a4e410 | 2026-08-06 | test-ci | 【变更概述】【MRV2 相关】修复 MRV2 rejection sampler 中 tl.argm | auto-inherit | S | tests/v1/spec_decode/test_rejection_samp |
| 7c77868c | 2026-08-06 | test-ci | 【变更概述】修复非门控 MoE 的 w13 权重按 shard count 进行 sizing 与迭 | auto-inherit | S | tests/quantization/test_auto_gptq.py, te |
