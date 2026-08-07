# 上游优化表 - 设计实现模板

> 本文档定义「上游 bugfix & 优化 → 下游迁移」分析表的规范化设计，包括 Schema、AI 生成约束、落地路径。
> 目标：让 AI 能稳定、可复现地生成结构化迁移分析表，供 vllm-ascend 团队决策使用。

---

## 一、设计目标与原则

| 原则 | 说明 |
|------|------|
| **可落地** | 表格每一行都对应一个明确的工程动作（cherry-pick / patch 对齐 / 借鉴 / 跳过），不是空谈 |
| **可追溯** | 每个 commit 链接到上游 PR、文件路径、架构上下文，可回查 |
| **可过滤** | 支持按优先级、模块、迁移策略、风险等多维度筛选 |
| **可自动化** | Schema 化 + Prompt 约束，让 LLM 批量生成，人工只做 P0 复核 |
| **上下文驱动** | 基于 `architecture.json` 的接口面和影响规则，不靠猜 |

---

## 二、Schema 设计

### 2.1 单条记录 Schema（JSON）

```json
{
  "sha": "b50fdebc",
  "full_sha": "b50fdebcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "date": "2026-08-06",
  "repo": "vllm-project/vllm",
  "title": "[Bugfix] Fix level-2 sleep/wake/reload with enable_lora=True",
  "pr_number": "39935",
  "pr_url": "https://github.com/vllm-project/vllm/pull/39935",

  "category": "core-engine",
  "change_type": "bugfix",
  "optimization_point": "修复 level-2 sleep/wake/reload 与 LoRA 的状态一致性",
  "affected_files": [
    "vllm/v1/worker/gpu_model_runner.py",
    "vllm/v1/worker/lora_model_runner_mixin.py"
  ],

  "ascend_value": "high",
  "ascend_value_reason": "gpu_model_runner.py 是 NPUModelRunner 父类，修改自动传递",

  "migration_method": "cherry-pick",
  "migration_steps": [
    "确认 NPUModelRunner 未覆盖被修改的方法",
    "验证 SleepWakeupManager 与 LoRA 协同",
    "添加 sleep/wake + LoRA 回归测试"
  ],
  "patch_conflict": true,
  "patch_conflict_detail": "distributed_parallel_state_patch 可能涉及 sleep 逻辑",

  "priority": "P0",
  "priority_reason": "直接影响功能正确性，涉及 11 个文件",
  "effort_estimate": "M",
  "risk_level": "high-risk",

  "test_verification": [
    "Ascend level-2 sleep/wake + LoRA 验证",
    "NPUModelRunner LoRA 状态恢复"
  ],
  "status": "pending",
  "assignee": "",

  "key_files": "vllm/v1/worker/gpu_model_runner.py"
}
```

### 2.2 字段约束与枚举值

| 字段 | 类型 | 必填 | 枚举值 / 约束 | 说明 |
|------|------|------|---------------|------|
| `sha` | string | ✅ | 8 位短 SHA | commit 标识 |
| `full_sha` | string | ✅ | 40 位完整 SHA | 用于链接 |
| `date` | string | ✅ | `YYYY-MM-DD` | commit 日期 |
| `repo` | string | ✅ | `vllm-project/vllm` \| `vllm-project/vllm-ascend` | 仓库 |
| `title` | string | ✅ | 首行 message | commit 标题 |
| `pr_number` | string | ⚠️ | 数字或空 | PR 号（从 message 提取） |
| `pr_url` | string | ✅ | URL | PR 链接 |
| `category` | enum | ✅ | 见 §2.3 | 模块分类 |
| `change_type` | enum | ✅ | `bugfix` \| `performance` \| `feature` \| `refactor` | 变更类型 |
| `optimization_point` | string | ✅ | ≤100 字 | 优化点一句话描述 |
| `affected_files` | array | ✅ | ≥1 项 | 受影响文件路径 |
| `ascend_value` | enum | ✅ | `high` \| `medium` \| `low` \| `none` | 对 Ascend 的价值 |
| `ascend_value_reason` | string | ✅ | ≤80 字 | 价值判断理由（基于架构上下文，非猜测） |
| `migration_method` | enum | ✅ | 见 §2.4 | 迁移策略 |
| `migration_steps` | array | ⚠️ | 当 method ≠ skip 时 ≥1 项 | 具体操作步骤 |
| `patch_conflict` | bool | ✅ | true/false | 是否与 Ascend patch 冲突 |
| `patch_conflict_detail` | string | ⚠️ | 当 conflict=true 时必填 | 冲突详情 |
| `priority` | enum | ✅ | `P0` \| `P1` \| `P2` \| `P3` \| `skip` | 优先级 |
| `priority_reason` | string | ✅ | ≤60 字 | 优先级判定理由 |
| `effort_estimate` | enum | ✅ | `S`(≤1天) \| `M`(1-3天) \| `L`(>3天) | 工作量估算 |
| `risk_level` | enum | ✅ | `high-risk` \| `medium-risk` \| `low-risk` | 风险等级 |
| `test_verification` | array | ⚠️ | 当 priority ≤ P2 时 ≥1 项 | 需验证的测试场景 |
| `status` | enum | ✅ | `pending` \| `in-progress` \| `done` \| `skipped` | 落地状态 |
| `assignee` | string | ✅ | 可空 | 负责人 |
| `key_files` | string | ✅ | 逗号分隔 | 关键文件路径（表格展示用） |

### 2.3 `category` 枚举（模块分类）

| 值 | 含义 | 典型路径 |
|----|------|---------|
| `core-engine` | 核心引擎与模型 Runner | `vllm/v1/worker/gpu_model_runner.py`, `vllm/engine/` |
| `attention-kv-cache` | Attention / KV Cache | `vllm/v1/attention/`, `vllm/v1/core/kv_cache*` |
| `model-architecture` | 模型架构 | `vllm/model_executor/models/`, `vllm/models/` |
| `moe-fusion` | MoE / 融合优化 | `vllm/model_executor/layers/fused_moe/` |
| `operator-kernel` | 算子 / Kernel | `csrc/`, `vllm/_custom_ops.py` |
| `distributed` | 分布式 / 并行 | `vllm/distributed/` |
| `spec-decode` | 推测解码 | `vllm/v1/worker/gpu/spec_decode/` |
| `kv-offload` | KV Offload | `vllm/v1/kv_offload/` |
| `quantization` | 量化 | `vllm/model_executor/layers/quantization/` |
| `lora` | LoRA | `vllm/lora/` |
| `multimodal` | 多模态 | `vllm/multimodal/` |
| `config` | 配置 | `vllm/config/` |
| `scheduler` | 调度器 | `vllm/v1/core/sched/` |
| `test-ci` | 测试 / CI | `tests/`, `.buildkite/` |
| `other` | 其他 | - |

### 2.4 `migration_method` 枚举（迁移策略）

| 值 | 含义 | 适用条件 | 成本 |
|----|------|---------|------|
| `cherry-pick` | 直接摘樱桃 | 公共路径，Ascend 无 patch 覆盖 | ✅ 低 |
| `patch-sync` | Patch 对齐 | Ascend 通过 patch 覆盖的路径 | ⚠️ 中 |
| `idea-copy` | 逻辑借鉴 | 平台特化但思路通用，需用 Ascend 算子重写 | ⚠️ 高 |
| `config-align` | 配置/接口对齐 | 配置默认值、新增参数、API 调整 | ✅ 低 |
| `auto-inherit` | 自动继承 | 父类方法，未被 patch 覆盖 | ✅ 零 |
| `skip` | 跳过 | CUDA/ROCm 专用，Ascend 无对应场景 | ✅ 零 |

### 2.5 `priority` 判定矩阵

| 条件 | 优先级 |
|------|--------|
| `ascend_value=high` 且 `patch_conflict=true` | **P0** |
| `ascend_value=high` 且 `change_type=bugfix` | **P0** |
| `ascend_value=high` 且 `change_type=performance` | **P1** |
| `ascend_value=medium` 且 `patch_conflict=true` | **P1** |
| `ascend_value=medium` 且 `patch_conflict=false` | **P2** |
| `ascend_value=low` | **P3** |
| `ascend_value=none` | **skip** |

---

## 三、AI 生成表格的要求与约束

### 3.1 Prompt 约束规则

| 规则编号 | 约束 | 违反后果 |
|---------|------|---------|
| R1 | **必须基于 `architecture.json` 上下文判断**，不得凭 commit 标题猜测 | 输出被标记为 `low-confidence` |
| R2 | **`ascend_value` 判定必须引用接口面规则**（必然影响/可能影响/绝不影响路径） | 记录被过滤 |
| R3 | **`migration_method` 必须与 `patch_impact_map` 一致** | 记录被标记需人工复核 |
| R4 | **`optimization_point` ≤100 字**，必须包含动词+对象+效果 | 截断处理 |
| R5 | **`migration_steps` 每步必须可执行**（含具体文件/模块/验证方法） | 标记为 `low-confidence` |
| R6 | **禁止输出"可能""也许""不确定"等模糊词**，不确定时填 `low-confidence: true` | 降级处理 |
| R7 | **`skip` 必须给出跳过理由**（CUDA 专用/ROCm 专用/无对应场景） | 记录被退回 |
| R8 | **`pr_number` 必须从 message 中正则提取**，提取不到填 `null` | - |
| R9 | **输出必须为合法 JSON**，不得包含注释、多余文本 | 整批重试 |
| R10 | **`patch_conflict` 判定依据 `patch_impact_map`**，不在映射表中的路径填 `false` | - |

### 3.2 判定流程（AI 必须遵循）

```
对每个 commit:
  1. 提取 affected_files（从 commits 数据）
  2. 查 architecture.json 的 patch_impact_map:
     - 命中 → patch_conflict=true, ascend_value ≥ medium
     - 未命中但属于公共路径 → ascend_value 视情况, patch_conflict=false
     - 命中 not_used_by_ascend → ascend_value=none, migration_method=skip
  3. 判断 change_type（bugfix/performance/feature/refactor）
  4. 根据 §2.5 矩阵确定 priority
  5. 根据 migration_method 生成 migration_steps
  6. 生成 test_verification（P0/P1/P2 必填）
```

### 3.3 输出格式约束

```json
{
  "period": "2026-07-08 ~ 2026-08-06",
  "generated_at": "2026-08-07T10:00:00+08:00",
  "total_commits": 350,
  "analyzed_commits": 22,
  "skipped_commits": 328,
  "summary": {
    "P0": 2,
    "P1": 4,
    "P2": 7,
    "P3": 5,
    "skip": 9
  },
  "records": [
    { ... 单条记录，见 §2.1 ... }
  ]
}
```

### 3.4 质量校验（后处理）

生成后脚本自动校验：
1. **Schema 校验**：所有必填字段存在，枚举值合法
2. **引用完整性**：`sha` 在 commits 数据中存在
3. **一致性校验**：`priority` 与 `ascend_value`/`patch_conflict` 符合矩阵
4. **去重**：同一 `full_sha` 只保留一条
5. **跳过理由**：`migration_method=skip` 时 `ascend_value_reason` 非空

---

## 四、落地路径分析

### 4.1 系统集成架构

```
┌─────────────────────────────────────────────────────────┐
│                    现有数据管道                           │
│  fetch_commits.py → commits/*.json                      │
│  analyze_commits.py → analysis/*.json (含 ascend_impact)│
│  architecture.json (接口面 + patch_impact_map)          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              新增：优化表生成管道                          │
│                                                         │
│  1. collect_candidates.py                               │
│     ├─ 读取 commits + analysis                          │
│     ├─ 过滤 bugfix/performance 类型                      │
│     └─ 输出 candidate_commits.json                      │
│                                                         │
│  2. generate_optimization_table.py                      │
│     ├─ 加载 architecture.json (patch_impact_map)        │
│     ├─ 构造 Prompt（§3.1 约束 + §2 Schema）             │
│     ├─ 调用 LLM（batch, 每批 10 commits）                │
│     ├─ 后处理校验（§3.4）                                │
│     └─ 输出 optimization_table.json                     │
│                                                         │
│  3. export_table.py                                     │
│     ├─ JSON → Excel（多 Sheet, §五）                     │
│     ├─ JSON → CSV                                       │
│     └─ JSON → Markdown（可读报告）                       │
│                                                         │
│  4. update_schedule.py                                  │
│     └─ 定时任务：每日 10:00 增量更新                      │
└─────────────────────────────────────────────────────────┘
```

### 4.2 分阶段实施路径

| 阶段 | 内容 | 交付物 | 验收标准 |
|------|------|--------|---------|
| **阶段 1：Schema + Prompt** | 定义 Schema、编写 Prompt 模板 | `schema.json` + `prompt_template.txt` | LLM 输出通过 Schema 校验 |
| **阶段 2：生成脚本** | 实现 collect + generate + validate | `generate_optimization_table.py` | 对 30 天数据生成 ≤30s |
| **阶段 3：导出** | JSON → Excel/CSV/Markdown | `export_table.py` | Excel 可筛选、P0 高亮 |
| **阶段 4：定时化** | 每日增量更新 + 周报汇总 | Schedule 任务 | 每日自动生成，无人工干预 |
| **阶段 5：反馈闭环** | 人工标注 status，回流到训练 | `status_tracker.json` | P0 复核率 100% |

### 4.3 与现有系统的复用关系

| 现有能力 | 复用方式 |
|---------|---------|
| `analyze_commits.py` 的 `ascend_impact` | 作为 `ascend_value` 和 `patch_conflict` 的初判输入 |
| `architecture.json` 的 `patch_impact_map` | 作为 `migration_method` 和 `patch_conflict` 的判定依据 |
| `triage_ascend()` 的路径规则 | 作为 `skip` 的快速判定（auto-false 路径直接 skip） |
| `.env` 中的 `LLM_API_KEY` | 复用 LLM 调用基础设施 |
| `generate_mrv2_report.py` 的文件路径匹配 | 复用 `category` 分类逻辑 |

---

## 五、Excel 导出模板设计

| Sheet | 内容 | 特色 |
|-------|------|------|
| **优化点总表** | 所有 records | 自动筛选、优先级颜色高亮（P0 红、P1 橙、P2 黄） |
| **P0 行动清单** | 仅 priority=P0 | 含 migration_steps 和 test_verification |
| **迁移策略说明** | 5 种 method 说明 | 静态参考表 |
| **跳过清单** | migration_method=skip | 含跳过理由，便于回查 |
| **统计看板** | 按 category/priority 汇总 | 透视表 + 图表 |

---

## 六、文件清单

| 文件 | 用途 |
|------|------|
| `templates/optimization_schema.json` | JSON Schema 定义（机器可读） |
| `templates/optimization_prompt.txt` | LLM Prompt 模板 |
| `scripts/generate_optimization_table.py` | 生成脚本（collect + generate + validate） |
| `scripts/export_optimization_table.py` | 导出脚本（JSON → Excel/CSV/MD） |

---

*本模板为 vllm-report 项目的上游优化分析标准化设计，可作为同类「上游→下游迁移」分析场景的通用模板*
