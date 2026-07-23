import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

translations = {
    "[Bugfix][Multimodal] Fix Qwen3-Omni use_audio_in_video with mixed image/video inputs (#46213)":
        "[Bugfix][多模态] 修复 Qwen3-Omni 在混合图像/视频输入下的 use_audio_in_video 问题",
    "[Perf] Optimize `clamp` to `clamp_` (#48143)":
        "[性能] 将 clamp 优化为 clamp_",
    "[Spec Decode][DSpark] Add Gemma4-12B DSpark draft model (#47216)":
        "[Spec Decode][DSpark] 添加 Gemma4-12B DSpark draft 模型",
    "[Model] Add PW CUDA graph support for Inkling [2/N] (#48822)":
        "[Model] 为 Inkling 添加 PW CUDA graph 支持 [2/N]",
    "[Misc] Use meta tensor for KV cache stride calculation (#47316)":
        "[其他] 使用 meta tensor 进行 KV cache stride 计算",
    "[BugFix] Fix packed HND KV cache reshape for FlashAttention (#47314)":
        "[Bugfix] 修复 FlashAttention 的 packed HND KV cache reshape 问题",
    "[Model] Add LongCat-Flash-Lite (n-gram embedding) (#47857)":
        "[Model] 添加 LongCat-Flash-Lite（n-gram embedding）",
    "[Bugfix][Model Runner V2] Order uniform decodes first so spec decodes aren't misclassified as prefills (#47381)":
        "[Bugfix][Model Runner V2] 将 uniform decodes 优先排序，避免 spec decodes 被误分类为 prefills",
    "[Bugfix] Fix race condition in KVBlockZeroer (#48085)":
        "[Bugfix] 修复 KVBlockZeroer 中的竞态条件",
    "[Spec Decode] Support hybrid (SWA + full attention) DFlash drafters (#47914)":
        "[Spec Decode] 支持混合（SWA + full attention）DFlash drafters",
    "[Bugfix] Fix mamba+dflash for MRV2 (#47698)":
        "[Bugfix] 修复 MRV2 的 mamba+dflash 问题",
    "[Bugfix] Fix PD disagg + MTP correctness for Qwen3.5(GDN) (#47466)":
        "[Bugfix] 修复 Qwen3.5(GDN) 的 PD disagg + MTP 正确性问题",
    "Disable dynamic speculative decoding when DP is enabled (#45963)":
        "当启用 DP 时禁用动态投机解码",
    "[Perf] Use blocking CUDA events to avoid busy polling cuda driver lock (#47081)":
        "[性能] 使用阻塞式 CUDA events 避免忙轮询 cuda driver lock",
    "[ROCm] Align mixed encoder-decoder KV cache views in V2 runner (#47685)":
        "[ROCm] 在 V2 runner 中对齐混合 encoder-decoder KV cache views",
    "[XPU] Fix PP accuracy on XPU device (#47253)":
        "[XPU] 修复 XPU 设备上的 PP 精度问题",
    "Revert \"[Platform] Replace `torch.cuda.Event` with `torch.Event` (#47140)\" (#47668)":
        "回退 \"[Platform] 用 torch.Event 替换 torch.cuda.Event\"",
    "[XPU] Fix Eagle3 initialization on XPU (#43957)":
        "[XPU] 修复 XPU 上的 Eagle3 初始化问题",
    "[MRV2] Enable mm prefix bidi attention support on MRV2 (#46942)":
        "[MRV2] 在 MRV2 上启用 mm prefix bidi attention 支持",
    "[Bugfix][TurboQuant] Preserve KV cache dtype in backend shape (#47609)":
        "[Bugfix][TurboQuant] 在后端形状中保留 KV cache dtype",
    "[Bugfix][Structured Output][Spec Decode] Constrain bitmask and trim grammar advance at the reasoning boundary (#44297)":
        "[Bugfix][结构化输出][Spec Decode] 在推理边界约束 bitmask 和修剪语法 advance",
    "[MRV2][SD] Make Dynamic SD comatible with Full Cuda Graphs (#45953)":
        "[MRV2][SD] 使动态 SD 与 Full Cuda Graphs 兼容",
    "Support nvfp4 kv with kv-cache-dtype-skip-layers sliding_window (#42890)":
        "支持 nvfp4 kv 与 kv-cache-dtype-skip-layers sliding_window",
    "[ModelRunner V2][BugFix] Free all model refs on shutdown (#47483)":
        "[ModelRunner V2][BugFix] 关闭时释放所有模型引用",
    "Add Laguna XS.2.1 DFlash drafter support (#46853)":
        "添加 Laguna XS.2.1 DFlash drafter 支持",
    "[Bugfix][Model Runner V2][Spec Decode] Fix int32 offset overflow in block verification kernels (#47383)":
        "[Bugfix][Model Runner V2][Spec Decode] 修复 block verification kernels 中的 int32 偏移溢出",
    "[ModelRunner V2] Fix Mamba2 crash on non-spec-decode (#47428)":
        "[ModelRunner V2] 修复非 spec-decode 时的 Mamba2 崩溃",
    "[Feature] Universal speculative decoding for heterogeneous vocabularies (TLI) (#38174)":
        "[Feature] 异构词汇表的通用投机解码（TLI）",
    "[BugFix][Spec Decode] Compact shared topk indices buffer after first MTP draft step (#47238)":
        "[BugFix][Spec Decode] 在首个 MTP draft step 后压缩共享的 topk indices buffer",
    "[Spec Decode] DSpark speculators checkpoint support (#47093)":
        "[Spec Decode] DSpark speculators checkpoint 支持",
    "[Spec Decode] DSpark (#46995)":
        "[Spec Decode] DSpark",
    "Weight sync refactor + move sparse nccl engine (#44353)":
        "权重同步重构 + 移动稀疏 nccl engine",
    "[Platform] Replace `torch.cuda.Event` with `torch.Event` (#47140)":
        "[Platform] 用 torch.Event 替换 torch.cuda.Event",
    "[BugFix] Gate MRV2 mixed sparse-MLA warmup on `max_num_seqs` > 1 (#47050)":
        "[BugFix] 在 max_num_seqs > 1 时启用 MRV2 mixed sparse-MLA warmup",
    "[Model Runner V2][Spec Decode] Implement block verification for rejection sampling (#46781)":
        "[Model Runner V2][Spec Decode] 为 rejection sampling 实现 block verification",
    "[Platform] Replace `torch.cuda.mem_get_info` with `torch.accelerator.get_memory_info` (#44825)":
        "[Platform] 用 torch.accelerator.get_memory_info 替换 torch.cuda.mem_get_info",
    "[Model Runner V2] support mamba hybrid models align prefix cache (#42406)":
        "[Model Runner V2] 支持 mamba hybrid models align prefix cache",
    "[EPLB] Mask padding in EPLB load recording (#38128)":
        "[EPLB] 在 EPLB load recording 中 mask padding",
    "[Spec Decode] Avoid redundant hidden-states gather in draft prefill (#46968)":
        "[Spec Decode] 避免 draft prefill 中冗余的 hidden-states gather",
    "[Model] Support Unlimited OCR (#46564)":
        "[Model] 支持 Unlimited OCR",
    "[Model Runner V2][Spec Decode] Handle tuple hidden states from MTP draft models (#46786)":
        "[Model Runner V2][Spec Decode] 处理 MTP draft models 的 tuple hidden states",
    "[Model Runner V2][Spec Decode] Use fp32 uniform threshold for acceptance (#46878)":
        "[Model Runner V2][Spec Decode] 使用 fp32 uniform threshold 进行验收",
    "[ModelRunner V2] Support realtime embeddings (#46762)":
        "[ModelRunner V2] 支持实时 embeddings",
    "[ModelRunner V2] Fix cross-attention block table sizing (#46753)":
        "[ModelRunner V2] 修复 cross-attention block table sizing",
    "[ModelRunner V2] Deduplicate ModelState init logic (#46776)":
        "[ModelRunner V2] 去重 ModelState 初始化逻辑",
    "[ModelRunner V2] Fix whisper test (#46773)":
        "[ModelRunner V2] 修复 whisper 测试",
    "[Model Runner V2][Spec Decode] Reduce TP communication for draft token generation (#46448)":
        "[Model Runner V2][Spec Decode] 减少 draft token 生成的 TP 通信",
    "[Model Runner V2][DFlash] Enable dflash attention backend selection (#46770)":
        "[Model Runner V2][DFlash] 启用 dflash attention backend selection",
    "[Bugfix][MRV2] Forward seq_lens_cpu_upper_bound for mamba hybrid models (#46759)":
        "[Bugfix][MRV2] 为 mamba hybrid models 转发 seq_lens_cpu_upper_bound",
    "[ModelRunner V2] Bound memory for large logprobs requests (#46746)":
        "[ModelRunner V2] 为大型 logprobs 请求限制内存",
    "[Model Runner V2][Spec Decode] Use log1p to compute residual during rejection sampling (#46665)":
        "[Model Runner V2][Spec Decode] 使用 log1p 在 rejection sampling 期间计算残差",
    "[CPU][Spec Decode] Enable DFlash SD for CPU (#44029)":
        "[CPU][Spec Decode] 为 CPU 启用 DFlash SD",
    "[Model Runner V2][MM] Support EVS (#46535)":
        "[Model Runner V2][MM] 支持 EVS",
    "[Bugfix][Spec Decode] Fix probabilistic sampling for parallel drafting (#45956)":
        "[Bugfix][Spec Decode] 修复并行 drafting 的概率采样问题",
    "[Spec Decode] Reject placeholder (-1) draft tokens in rejection sampler (#46533)":
        "[Spec Decode] 在 rejection sampler 中拒绝占位符 (-1) draft tokens",
    "[Optimization] Skip DP padding tokens in MoE (#46428)":
        "[优化] 在 MoE 中跳过 DP padding tokens",
    "[Bugfix][Model Runner V2] Preserve all allowed_token_ids in the logit bias kernel (#46245)":
        "[Bugfix][Model Runner V2] 在 logit bias kernel 中保留所有 allowed_token_ids",
    "[Hardware][AMD][CI] Fix Spec Decode Eagle test group (#46018)":
        "[Hardware][AMD][CI] 修复 Spec Decode Eagle 测试组",
    "[Spec Decode] Add Qwen3 architecture support for EAGLE3 (#43132)":
        "[Spec Decode] 为 EAGLE3 添加 Qwen3 架构支持",
    "[Spec Decode] Support mixed KV page sizes for DFlash (#45181)":
        "[Spec Decode] 支持 DFlash 的混合 KV page sizes",
    "[Bugfix][Model Runner V2] Fix min_tokens off-by-one in the V2 GPU sampler (#46243)":
        "[Bugfix][Model Runner V2] 修复 V2 GPU sampler 中 min_tokens 的 off-by-one 问题",
    "[Core] Ensure memory is pinned prior to async h2d copy (#45424)":
        "[Core] 在异步 h2d copy 之前确保内存被 pinned",
    "[bugfix]Indexer init skip and MTP TopK share for iteration (#45895)":
        "[bugfix] Indexer 初始化跳过和 MTP TopK 迭代共享",
    "[CPU] Skip Triton kernel monkey-patches when Triton-CPU is available (#44991)":
        "[CPU] 当 Triton-CPU 可用时跳过 Triton kernel monkey-patches",
    "[CI/Build][Bugfix] Fix SD LoRA  (#45941)":
        "[CI/Build][Bugfix] 修复 SD LoRA",
    "[ModelRunnerV2] Various model/config compatibility fixes (#45868)":
        "[ModelRunnerV2] 各种模型/配置兼容性修复",
    "[Bugfix][V1] Split V2 model-runner attention groups on num_heads_q (#45564)":
        "[Bugfix][V1] 在 num_heads_q 上分割 V2 model-runner attention groups",
    "[Perf] Use bisect for mm feature lookup in model runner v2 (#45566)":
        "[性能] 在 model runner v2 中使用 bisect 进行 mm feature 查找",
    "[V1][Spec Decode] Add Dynamic SD (#32374)":
        "[V1][Spec Decode] 添加动态 SD",
    "[Core] Simplify MRV2 async output handling (#45442)":
        "[Core] 简化 MRV2 异步输出处理",
    "[Model Runner V2] Fix `openai.InternalServerError: Error code: 500 - 'list index out of range'` (#45467)":
        "[Model Runner V2] 修复 'list index out of range' 错误",
    "[Bug] Migrate Reset cache for both v2 and v1 model runner (#42759)":
        "[Bug] 为 v2 和 v1 model runner 迁移 Reset cache",
    "[Model] Add DiffusionGemma Support (#45163)":
        "[Model] 添加 DiffusionGemma 支持",
    "Hidden states extraction improvements (#43805)":
        "隐藏状态提取改进",
    "[Model Runner V2] Fix v2 `AttributeError: 'CohereASRDecoder' object has no attribute 'embed_input_ids'` (#44568)":
        "[Model Runner V2] 修复 CohereASRDecoder 缺少 embed_input_ids 属性的问题",
    "[MRV2][Spec Decode] DFlash (#44586)":
        "[MRV2][Spec Decode] DFlash",
    "[SpecDecode] Reduce TP communication for large-vocab draft models speculative decoding (#39419)":
        "[SpecDecode] 减少大词汇量 draft models 投机解码的 TP 通信",
    "[Core][Model] Gemma4: Unified FA4 for all layers + FlashAttention mm_prefix support (#42175)":
        "[Core][Model] Gemma4: 所有层统一 FA4 + FlashAttention mm_prefix 支持",
    "[feature] add index share feature for DSA MTP (#44420)":
        "[feature] 为 DSA MTP 添加索引共享功能",
    "[BUG] Fix FP64 Gumbel precision coverage (#43150)":
        "[BUG] 修复 FP64 Gumbel 精度覆盖问题",
}

wb = load_workbook('vllm_commits_export.xlsx')

for sheet_name in ['Commits', 'High Risk']:
    ws = wb[sheet_name]
    for row in range(2, ws.max_row + 1):
        en_title = ws.cell(row=row, column=3).value
        if en_title and en_title in translations:
            ws.cell(row=row, column=3).value = translations[en_title]

wb.save('vllm_commits_export.xlsx')
print(f"Translated {len(translations)} titles")
