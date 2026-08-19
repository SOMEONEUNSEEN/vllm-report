# 上游优化表 - 设计实现模板

> 本文档定义「上游 bugfix & 优化 → 下游迁移」分析表的规范化设计，包括 Schema、AI 生成约束、落地路径。
> 目标：让 AI 能稳定、可复现地生成结构化迁移分析表，供 vllm-ascend 团队决策使用。

**版本**：v2.0（2026-08-19）
**变更摘要**：v2 新增 `commit_url`/`upstream_status`/`merged_at`/`author`/`labels`/`patch_matched_keys`/`ascend_impact_ref`/`related_prs`/`blocking_issues`/`review_notes`/`confidence_reason` 字段，修复 `pr_url` 与 commit URL 不一致问题，增强条件约束（skip 一致性、P0 复核必填），补充错误处理、数据质量指标、监控告警、dashboard 集成章节。

---

## 一、设计目标与原则

| 原则 | 说明 |
|------|------|
| **可落地** | 表格每一行都对应一个明确的工程动作（cherry-pick / patch 对齐 / 借鉴 / 跳过），不是空谈 |
| **可追溯** | 每个 commit 链接到上游 PR、commit URL、文件路径、架构上下文，可回查 |
| **可过滤** | 支持按优先级、模块、迁移策略、风险、作者、标签等多维度筛选 |
| **可自动化** | Schema 化 + Prompt 约束，让 LLM 批量生成，人工只做 P0 复核 |
| **上下文驱动** | 基于 `architecture.json` 的接口面和影响规则，不靠猜 |
| **可反馈** | `review_notes`/`status`/`blocking_issues` 形成人工反馈闭环 |
| **低置信度透明** | `low_confidence` + `confidence_reason` 让 AI 不确定时显式标注 |

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
  "commit_url": "https://github.com/vllm-project/vllm/commit/b50fdebcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "upstream_status": "merged",
  "merged_at": "2026-08-06T10:00:00Z",
  "author": { "name": "John Doe", "email": "john@example.com" },
  "labels": ["bug", "lora"],

  "category": "core-engine",
  "change_type": "bugfix",
  "optimization_point": "修复 level-2 sleep/wake 与 LoRA 的状态一致性",
  "affected_files": [
    "vllm/v1/worker/gpu_model_runner.py",
    "vllm/v1/worker/lora_model_runner_mixin.py"
  ],

  "ascend_value": "high",
  "ascend_value_reason": "gpu_model_runner.py 是 NPUModelRunner 父类，修改自动传递",
  "ascend_impact_ref": {
    "ascend_affected": true,
    "functionality": "影响 sleep/wake 状态管理",
    "source": "2026-08-06"
  },

  "migration_method": "cherry-pick",
  "migration_steps": [
    "确认 NPUModelRunner 未覆盖被修改的方法",
    "验证 SleepWakeupManager 与 LoRA 协同",
    "添加 sleep/wake + LoRA 回归测试"
  ],
  "patch_conflict": false,
  "patch_conflict_detail": "",
  "patch_matched_keys": [],

  "priority": "P0",
  "priority_reason": "ascend_value=high 且 change_type=bugfix",
  "effort_estimate": "M",
  "risk_level": "high-risk",

  "test_verification": [
    "Ascend level-2 sleep/wake + LoRA 验证",
    "NPUModelRunner LoRA 状态恢复"
  ],
  "status": "pending",
  "assignee": "",
  "key_files": "vllm/v1/worker/gpu_model_runner.py",

  "related_prs": [],
  "blocking_issues": [],
  "review_notes": null,
  "low_confidence": false,
  "confidence_reason": null
}
```

### 2.2 字段约束与枚举值

| 字段 | 类型 | 必填 | 枚举值 / 约束 | 说明 |
|------|------|------|---------------|------|
| `sha` | string | ✅ | `^[0-9a-f]{8}$` | 8 位短 SHA |
| `full_sha` | string | ✅ | `^[0-9a-f]{40}$` | 40 位完整 SHA |
| `date` | string | ✅ | `YYYY-MM-DD` | commit 日期 |
| `repo` | string | ✅ | `vllm-project/vllm` \| `vllm-project/vllm-ascend` | 仓库 |
| `title` | string | ✅ | ≤200 字 | commit 标题 |
| `pr_number` | string\|null | ⚠️ | 数字或 null | PR 号（从 message 提取） |
| `pr_url` | string\|null | ⚠️ | URI 或 null | PR 链接（`/pull/{pr_number}`） |
| `commit_url` | string | ✅ | URI | commit 链接（`/commit/{full_sha}`） |
| `upstream_status` | enum | ✅ | `merged`\|`open`\|`closed`\|`draft`\|`unknown` | 上游 PR 状态 |
| `merged_at` | string\|null | ⚠️ | ISO8601 或 null | 合入时间 |
| `author` | object | ⚠️ | `{name, email}` | commit 作者 |
| `labels` | array | ⚠️ | 字符串数组 | 上游 PR 标签 |
| `category` | enum | ✅ | 见 §2.3 | 模块分类 |
| `change_type` | enum | ✅ | `bugfix`\|`performance`\|`feature`\|`refactor` | 变更类型 |
| `optimization_point` | string | ✅ | ≤100 字 | 优化点一句话描述 |
| `affected_files` | array | ✅ | ≥1 项 | 受影响文件路径 |
| `ascend_value` | enum | ✅ | `high`\|`medium`\|`low`\|`none` | 对 Ascend 的价值 |
| `ascend_value_reason` | string | ✅ | ≤80 字 | 价值判断理由（基于架构上下文） |
| `ascend_impact_ref` | object\|null | ⚠️ | `{ascend_affected, functionality, source}` | 引用 analyze_commits 判定 |
| `migration_method` | enum | ✅ | 见 §2.4 | 迁移策略 |
| `migration_steps` | array | ⚠️ | 当 method ≠ skip 时 ≥1 项 | 具体操作步骤 |
| `patch_conflict` | bool | ✅ | true/false | 是否与 Ascend patch 冲突 |
| `patch_conflict_detail` | string | ⚠️ | 当 conflict=true 时必填 | 冲突详情 |
| `patch_matched_keys` | array | ⚠️ | 命中的 patch_impact_map key | 便于回查 |
| `priority` | enum | ✅ | `P0`\|`P1`\|`P2`\|`P3`\|`skip` | 优先级 |
| `priority_reason` | string | ✅ | ≤60 字 | 优先级判定理由 |
| `effort_estimate` | enum | ✅ | `S`(≤1天)\|`M`(1-3天)\|`L`(>3天) | 工作量估算 |
| `risk_level` | enum | ✅ | `high-risk`\|`medium-risk`\|`low-risk` | 风险等级 |
| `test_verification` | array | ⚠️ | 当 priority ≤ P2 时 ≥1 项 | 需验证的测试场景 |
| `status` | enum | ✅ | `pending`\|`in-progress`\|`done`\|`skipped`\|`blocked` | 落地状态 |
| `assignee` | string | ✅ | 可空 | 负责人 |
| `key_files` | string | ✅ | 逗号分隔 | 关键文件路径（表格展示用） |
| `related_prs` | array | ⚠️ | `[{pr_number, repo, relation}]` | 关联 PR |
| `blocking_issues` | array | ⚠️ | 字符串数组 | 阻塞问题 |
| `review_notes` | string\|null | ⚠️ | P0 必填 | 人工复核反馈 |
| `low_confidence` | bool | ✅ | 默认 false | AI 标记的低置信度 |
| `confidence_reason` | string\|null | ⚠️ | low_confidence=true 时必填 | 低置信度原因 |

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
| `patch-sync` | Patch 对齐 | Ascend 通过 patch 覆盖的路径（查 patch_impact_map） | ⚠️ 中 |
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

### 2.6 条件约束规则（allOf）

| 规则 | 条件 | 约束 |
|------|------|------|
| C1 | `migration_method ≠ skip` | `migration_steps` 必填 |
| C2 | `patch_conflict = true` | `patch_conflict_detail` 必填 |
| C3 | `priority ∈ {P0, P1, P2}` | `test_verification` 必填 |
| C4 | `migration_method = skip` | `ascend_value=none`, `priority=skip`, `ascend_value_reason` 非空 |
| C5 | `low_confidence = true` | `confidence_reason` 必填 |
| C6 | `priority = P0` | `review_notes` 必填（人工复核后填） |

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
| R6 | **禁止输出"可能""也许""不确定"等模糊词**，不确定时填 `low_confidence: true` | 降级处理 |
| R7 | **`skip` 必须给出跳过理由**（CUDA 专用/ROCm 专用/无对应场景） | 记录被退回 |
| R8 | **`pr_number` 必须从 message 中正则提取**，提取不到填 `null` | - |
| R9 | **输出必须为合法 JSON**，不得包含注释、多余文本 | 整批重试 |
| R10 | **`patch_conflict` 判定依据 `patch_impact_map`**，不在映射表中的路径填 `false` | - |
| R11 | **`pr_url` 与 `commit_url` 必须分开**，`pr_url` 指向 PR，`commit_url` 指向 commit | 字段重写 |
| R12 | **语言规范**：描述性字段中文，枚举值英文 | 重写 |
| R13 | **边界情况**：Merge commit/无 files/跨模块/文档 commit 按 Prompt §边界情况处理 | - |

### 3.2 判定流程（AI 必须遵循）

```
对每个 commit:
  1. 提取基础字段（sha, full_sha, date, title, pr_number, pr_url, commit_url, author, labels）
  2. 提取 affected_files（从 commits 数据 files[].filename）
  3. 判定 category（按 affected_files 路径匹配）
  4. 查 architecture.json:
     - 命中 patch_impact_map → patch_conflict=true, patch_matched_keys 填入, ascend_value ≥ medium
     - 命中 definitely_affected_paths → ascend_value=high/medium
     - 命中 potentially_affected_paths → ascend_value=medium/low
     - 命中 never_affected_paths → ascend_value=none, migration_method=skip
     - 公共路径未命中 patch → ascend_value 视情况, patch_conflict=false
  5. 判断 change_type（bugfix/performance/feature/refactor）
  6. 根据 §2.5 矩阵确定 priority
  7. 根据 migration_method 生成 migration_steps
  8. 生成 test_verification（P0/P1/P2 必填）
  9. 填写 ascend_impact_ref（如 analysis 数据存在）
  10. 检查 low_confidence（上下文不足时标记）
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

| 校验项 | 规则 | 失败处理 |
|--------|------|---------|
| **Schema 校验** | 所有必填字段存在，枚举值合法 | 记录丢弃，记入错误日志 |
| **引用完整性** | `sha` 在 commits 数据中存在 | 记录丢弃 |
| **一致性校验** | `priority` 与 `ascend_value`/`patch_conflict` 符合矩阵 | 降级 priority 或标记 low_confidence |
| **skip 一致性** | `migration_method=skip` 时 `ascend_value=none` 且 `priority=skip` | 自动修正 |
| **去重** | 同一 `full_sha` 只保留一条 | 保留首条，其余丢弃 |
| **跳过理由** | `migration_method=skip` 时 `ascend_value_reason` 非空 | 记录退回重试 |
| **P0 复核** | `priority=P0` 时 `review_notes` 非空（人工阶段） | 标记为待复核 |
| **低置信度** | `low_confidence=true` 时 `confidence_reason` 非空 | 自动修正 |
| **patch 匹配** | `patch_conflict=true` 时 `patch_matched_keys` 非空 | 自动补全 |

---

## 四、错误处理与重试机制

### 4.1 LLM 调用错误处理

| 错误类型 | 处理策略 |
|---------|---------|
| **JSON 解析失败** | 重试 1 次（temperature=0），仍失败则该批 commit 标记为 `parse_error`，跳过 |
| **Schema 校验失败** | 自动修正（如补全缺失字段），无法修正则标记 `low_confidence` |
| **LLM 超时** | 拆分为更小批次（5 commits/批），重试 1 次 |
| **LLM 限流** | 指数退避（2s, 4s, 8s），最多 3 次 |
| **上下文过长** | 截断 commits_json（保留前 10 条），分多批处理 |

### 4.2 数据完整性保障

```python
# 伪代码
def generate_with_retry(commits, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = call_llm(prompt)
            validated = validate_schema(result, schema)
            return validated
        except JSONParseError:
            if attempt == 0:
                # 第一次失败，降低 temperature 重试
                continue
            else:
                return mark_low_confidence(commits, "JSON 解析失败")
        except SchemaError as e:
            if auto_fixable(e):
                return auto_fix(result)
            else:
                return mark_low_confidence(commits, str(e))
    return mark_low_confidence(commits, "重试次数耗尽")
```

---

## 五、数据质量指标

### 5.1 生成质量看板

| 指标 | 计算方式 | 目标值 | 告警阈值 |
|------|---------|--------|---------|
| **Schema 通过率** | 通过校验记录数 / 总记录数 | ≥95% | <90% |
| **低置信度率** | `low_confidence=true` 记录数 / 总记录数 | ≤10% | >20% |
| **skip 合规率** | 合规 skip 记录 / 总 skip 记录 | ≥98% | <95% |
| **P0 覆盖率** | 有 `review_notes` 的 P0 / 总 P0 | 100% | <100% |
| **patch 匹配准确率** | `patch_matched_keys` 正确的记录 / 总 patch_conflict=true 记录 | ≥95% | <90% |
| **去重率** | 重复记录数 / 总记录数 | 0% | >0% |
| **字段完整率** | 非空必填字段数 / 应填字段数 | ≥98% | <95% |

### 5.2 质量告警

- **Schema 通过率 < 90%**：暂停自动生成，通知人工介入
- **低置信度率 > 20%**：检查 `architecture.json` 是否过期
- **P0 覆盖率 < 100%**：阻塞导出，待人工复核完成
- **skip 合规率 < 95%**：Prompt 需优化

---

## 六、各 migration_method 示例记录

### 6.1 cherry-pick（公共路径，无 patch 冲突）

适用：`vllm/v1/worker/gpu_model_runner.py` 等公共路径，Ascend 通过继承获取，无 patch 覆盖。

```json
{
  "sha": "b50fdebc",
  "migration_method": "cherry-pick",
  "patch_conflict": false,
  "patch_matched_keys": [],
  "ascend_value": "high",
  "ascend_value_reason": "gpu_model_runner.py 是 NPUModelRunner 父类，修改自动传递",
  "migration_steps": ["确认 NPUModelRunner 未覆盖被修改方法", "添加回归测试"]
}
```

### 6.2 patch-sync（命中 patch_impact_map）

适用：Ascend 通过 `vllm_ascend.patch.*_patch` 覆盖的路径。

```json
{
  "sha": "a1b2c3d4",
  "migration_method": "patch-sync",
  "patch_conflict": true,
  "patch_conflict_detail": "命中 vllm.distributed.parallel_state → vllm_ascend.patch.platform.distributed_parallel_state_patch",
  "patch_matched_keys": ["vllm.distributed.parallel_state"],
  "ascend_value": "high",
  "ascend_value_reason": "命中 patch_impact_map: vllm.distributed.parallel_state",
  "migration_steps": ["对比 distributed_parallel_state_patch 与上游差异", "移植优化逻辑到 HCCL 实现"]
}
```

### 6.3 idea-copy（平台特化但思路通用）

适用：CUDA 优化但思路可用于 Ascend，需用 Ascend 算子重写。

```json
{
  "sha": "c3d4e5f6",
  "migration_method": "idea-copy",
  "patch_conflict": false,
  "ascend_value": "medium",
  "ascend_value_reason": "CUDA kernel 优化思路通用，需用 Ascend 算子重写",
  "migration_steps": ["分析 CUDA kernel 优化思路", "用 Ascend C++ 算子实现等价逻辑", "性能对比验证"]
}
```

### 6.4 config-align（配置对齐）

适用：配置默认值、新增参数、API 调整。

```json
{
  "sha": "d4e5f6g7",
  "migration_method": "config-align",
  "patch_conflict": true,
  "patch_matched_keys": ["vllm.config"],
  "ascend_value": "medium",
  "ascend_value_reason": "命中 patch_impact_map: vllm.config",
  "migration_steps": ["对比 model_config_patch 与上游配置差异", "同步新增参数默认值"]
}
```

### 6.5 auto-inherit（自动继承）

适用：父类方法，未被 patch 覆盖，Ascend 自动继承。

```json
{
  "sha": "e5f6g7h8",
  "migration_method": "auto-inherit",
  "patch_conflict": false,
  "ascend_value": "low",
  "ascend_value_reason": "NPUModelRunner 继承 GPUModelRunner，方法自动获取",
  "migration_steps": ["验证继承链未被破坏", "确认无需覆盖"]
}
```

### 6.6 skip（跳过）

适用：CUDA/ROCm 专用，Ascend 无对应场景。

```json
{
  "sha": "f6g7h8i9",
  "migration_method": "skip",
  "patch_conflict": false,
  "ascend_value": "none",
  "ascend_value_reason": "FlashInfer 为 CUDA 专用库，Ascend 无对应实现",
  "migration_steps": [],
  "priority": "skip"
}
```

---

## 七、落地路径分析

### 7.1 系统集成架构

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
│              优化表生成管道（v2）                         │
│                                                         │
│  1. collect_candidates.py                               │
│     ├─ 读取 commits + analysis                          │
│     ├─ 过滤 bugfix/performance 类型                      │
│     ├─ 去重（按 full_sha）                                │
│     └─ 输出 candidate_commits.json                      │
│                                                         │
│  2. generate_optimization_table.py                      │
│     ├─ 加载 architecture.json (patch_impact_map)        │
│     ├─ 加载 analysis (ascend_impact) 作为参考            │
│     ├─ 构造 Prompt（§3.1 约束 + §2 Schema + few-shot）  │
│     ├─ 调用 LLM（batch, 每批 10 commits）                │
│     ├─ 错误处理与重试（§四）                              │
│     ├─ 后处理校验（§3.4）                                │
│     └─ 输出 optimization_table.json                     │
│                                                         │
│  3. export_table.py                                     │
│     ├─ JSON → Excel（多 Sheet, §八）                     │
│     ├─ JSON → CSV                                       │
│     ├─ JSON → Markdown（可读报告）                       │
│     └─ JSON → dashboard 数据格式                         │
│                                                         │
│  4. update_schedule.py                                  │
│     ├─ 定时任务：每日 10:00 增量更新                      │
│     ├─ 质量指标采集（§五）                                │
│     └─ 告警通知（§五.2）                                  │
└─────────────────────────────────────────────────────────┘
```

### 7.2 分阶段实施路径

| 阶段 | 内容 | 交付物 | 验收标准 |
|------|------|--------|---------|
| **阶段 1：Schema + Prompt** | 定义 Schema v2、编写 Prompt 模板 | `schema.json` + `prompt_template.txt` | LLM 输出通过 Schema 校验 |
| **阶段 2：生成脚本** | 实现 collect + generate + validate | `generate_optimization_table.py` | 对 30 天数据生成 ≤30s，Schema 通过率 ≥95% |
| **阶段 3：导出** | JSON → Excel/CSV/Markdown/Dashboard | `export_table.py` | Excel 可筛选、P0 高亮、Dashboard 可视化 |
| **阶段 4：定时化** | 每日增量更新 + 周报汇总 + 质量监控 | Schedule 任务 | 每日自动生成，无人工干预 |
| **阶段 5：反馈闭环** | 人工标注 status，回流到训练 | `status_tracker.json` | P0 复核率 100%，低置信度率 ≤10% |

### 7.3 与现有系统的复用关系

| 现有能力 | 复用方式 |
|---------|---------|
| `analyze_commits.py` 的 `ascend_impact` | 作为 `ascend_impact_ref` 的输入，引用 `ascend_affected` 和 `functionality` |
| `architecture.json` 的 `patch_impact_map` | 作为 `migration_method` 和 `patch_conflict` 的判定依据，填充 `patch_matched_keys` |
| `architecture.json` 的 `impact_judgment_rules` | 作为 `ascend_value` 的判定依据（definitely/potentially/never） |
| `triage_ascend()` 的路径规则 | 作为 `skip` 的快速判定（auto-false 路径直接 skip） |
| `.env` 中的 `LLM_API_KEY` | 复用 LLM 调用基础设施 |
| `generate_mrv2_report.py` 的文件路径匹配 | 复用 `category` 分类逻辑 |
| `export_commits_to_excel.py` 的导出逻辑 | 复用 Excel 导出框架，新增优化表专用 Sheet |

---

## 八、Excel 导出模板设计

| Sheet | 内容 | 特色 |
|-------|------|------|
| **优化点总表** | 所有 records | 自动筛选、优先级颜色高亮（P0 红、P1 橙、P2 黄）、作者/标签可筛选 |
| **P0 行动清单** | 仅 priority=P0 | 含 migration_steps、test_verification、blocking_issues、review_notes |
| **迁移策略说明** | 5 种 method 说明 + 示例 | 静态参考表 |
| **跳过清单** | migration_method=skip | 含跳过理由、patch_matched_keys，便于回查 |
| **统计看板** | 按 category/priority/author 汇总 | 透视表 + 图表 |
| **低置信度清单** | low_confidence=true | 含 confidence_reason，待人工复核 |
| **质量指标** | 生成质量看板数据 | §五的指标可视化 |

---

## 九、监控与告警

### 9.1 监控指标

| 指标 | 采集方式 | 告警条件 |
|------|---------|---------|
| **生成成功率** | 记录生成日志 | <95% |
| **Schema 通过率** | 后处理校验日志 | <90% |
| **低置信度率** | 统计 low_confidence | >20% |
| **P0 覆盖率** | 统计 review_notes | <100% |
| **生成耗时** | 计时日志 | >60s |
| **LLM 调用失败率** | 调用日志 | >5% |

### 9.2 告警渠道

- **飞书机器人**：P0 级告警实时推送
- **日志文件**：`output/optimization_table.log`
- **质量看板**：Dashboard 实时展示

---

## 十、Dashboard 集成

### 10.1 数据格式

优化表 JSON 转换为 Dashboard 兼容格式：

```json
{
  "date": "2026-08-07",
  "type": "optimization_table",
  "summary": {
    "total": 22,
    "P0": 2,
    "P1": 4,
    "P2": 7,
    "P3": 5,
    "skip": 9
  },
  "by_category": {
    "core-engine": 5,
    "distributed": 3,
    "attention-kv-cache": 2
  },
  "by_method": {
    "cherry-pick": 8,
    "patch-sync": 5,
    "skip": 9
  },
  "low_confidence_count": 2,
  "trend": {
    "P0_delta": 1,
    "total_delta": 5
  }
}
```

### 10.2 Dashboard 展示

- **优化表总览**：按优先级/模块/迁移策略分布
- **P0 行动看板**：待办、进行中、已完成
- **趋势图**：每日新增优化点数量
- **低置信度列表**：待人工复核

---

## 十一、反馈闭环

### 11.1 人工反馈流程

```
1. AI 生成 optimization_table.json
2. 人工复核 P0 记录，填写 review_notes
3. 更新 status（pending → in-progress → done/blocked）
4. 回流到 status_tracker.json
5. 定期分析低置信度记录，优化 Prompt
```

### 11.2 反馈数据结构

```json
{
  "feedback_date": "2026-08-07",
  "reviewer": "张三",
  "records": [
    {
      "sha": "b50fdebc",
      "original_priority": "P0",
      "adjusted_priority": "P1",
      "review_notes": "影响范围有限，降级为 P1",
      "status": "in-progress",
      "assignee": "李四"
    }
  ]
}
```

### 11.3 Prompt 优化迭代

- 每周分析低置信度记录的共性原因
- 更新 Prompt 的边界情况处理
- 更新 few-shot 示例
- 版本化 Prompt（`optimization_prompt_v{N}.txt`）

---

## 十二、文件清单

| 文件 | 用途 |
|------|------|
| `templates/optimization_schema.json` | JSON Schema 定义 v2（机器可读） |
| `templates/optimization_prompt.txt` | LLM Prompt 模板（含 few-shot） |
| `templates/UPSTREAM_OPTIMIZATION_TABLE_DESIGN.md` | 本设计文档 |
| `scripts/generate_optimization_table.py` | 生成脚本（collect + generate + validate） |
| `scripts/export_optimization_table.py` | 导出脚本（JSON → Excel/CSV/MD/Dashboard） |
| `output/optimization_table.json` | 生成产物 |
| `output/optimization_table.log` | 生成日志 |
| `output/status_tracker.json` | 人工反馈跟踪 |

---

## 十三、版本变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-08-07 | 初版 Schema、Prompt、设计文档 |
| v2.0 | 2026-08-19 | 新增 11 个字段（commit_url/upstream_status/merged_at/author/labels/patch_matched_keys/ascend_impact_ref/related_prs/blocking_issues/review_notes/confidence_reason）；修复 pr_url 与 commit URL 不一致；增强条件约束（C4-C6）；新增错误处理、质量指标、监控告警、Dashboard 集成、反馈闭环章节；补充各 migration_method 示例 |

---

*本模板为 vllm-report 项目的上游优化分析标准化设计，可作为同类「上游→下游迁移」分析场景的通用模板*
