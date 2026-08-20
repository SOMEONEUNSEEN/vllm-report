# 上游优化表 - 设计实现模板 (V3 智能体增强版)

> 本文档定义「上游 bugfix & 优化 → 下游迁移」分析表的规范化设计。
> **v3 变更摘要**：在 v2 的 SLA、监控体系基础上，引入思维链(CoT)、底层目录映射(`target_ascend_module`)，并新增了基于大模型智能体的 Auto-PR 代码同步机制和架构配置自进化(RAG)机制。

---

## 一、 设计目标与原则

| 原则 | 说明 |
|------|------|
| **可落地** | 表格每一行都对应一个明确的工程动作，不是空谈 |
| **可追溯** | 每个 commit 链接到上游 PR、commit URL、文件路径 |
| **可自动化** | Schema 化 + Prompt 约束，让 LLM 批量生成，人工只做 P0 复核 |
| **低置信度透明**| `low_confidence` 让 AI 不确定时显式标注 |
| **Agentic 驱动**| AI 具备直接通过 `migration_method` 发起 PR 合并请求的能力 |

*(注：第二至第十章节，即 Schema 定义、分类矩阵、告警监控及 Dashboard 结构，直接继承自 V2 版本，此处略写以节省篇幅，具体请参考 `optimization_schema_v3.json`。)*

---

## 十一、 智能反馈与自进化闭环 (Self-Evolving)

### 11.1 人工反馈流程
1. AI 生成 `optimization_table.json`。
2. 研发复核 P0 记录，并在 `review_notes` 中填写修正意见。
3. 状态扭转流：`pending` → `in-progress` → `done/blocked`。

### 11.2 Prompt 自动优化
利用收集到的 `confidence_reason`（低置信度原因），通过调度脚本每周将共性原因喂给大模型自身，让大模型输出改进后的 Prompt 增量策略，形成飞轮。

### 11.3 架构映射自进化 (Self-Evolving RAG) 🚀
当开发者在 `review_notes` 中指正了 AI 的某次 Patch 判定时（例如：“*此处不仅影响 X 模块，也影响了 Y 模块的 Patch*”）：
- 专门的回流脚本会提取该信息，**自动修改** `architecture.json` 中的 `patch_impact_map`。
- 保证下一次发生类似的模块变更时，AI 不会再犯同样的错误，实现知识库自学习。

---

## 十二、 文件与脚本清单

| 文件路径 | 核心用途 |
|------|------|
| `templates/optimization_schema_v3.json` | JSON Schema 结构定义 |
| `templates/optimization_prompt_v3.txt` | LLM Prompt 模板（包含 CoT 要求） |
| `scripts/generate_optimization_table.py`| 数据收集、大模型调用与 Schema 防御性重试 |
| `scripts/export_optimization_table.py` | 多模态导出（Excel/CSV/Markdown/Dashboard） |
| `scripts/agent_auto_pr.py` | 🚀 基于 JSON 记录自动生成并提交 PR 的智能体脚本 |
| `output/status_tracker.json` | 用于回流的人工反馈跟踪库 |

---

## 十三、 版本变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-08-07 | 初版 Schema、Prompt、设计文档 |
| v2.0 | 2026-08-19 | 新增 11 个关联/追踪字段，SLA 响应规范，错误告警大盘 |
| v3.0 | 2026-08-19 | 引入 CoT (`_thought_process`) 提升判定准确度；新增 `target_ascend_module` 映射；引入 Auto-PR 和 RAG 架构自演进能力 |

---

## 十四、 🚀 高阶演进：Agentic 自动化代码同步 (Auto-PR)

为了进一步压榨效率，v3 设计引入了自动化代码合入机制。基于每天生成的 JSON 表格：

1. **触发条件**：
   对于所有 `migration_method == "cherry-pick"` 且 `patch_conflict == false` 且 `priority ∈ ["P1", "P2"]` 的纯粹上游特性。
2. **Agent 动作**：
   * Agent 会基于 `target_ascend_module` 拉取 `vllm-ascend` 分支。
   * 调用 Git 接口：`git cherry-pick {full_sha}`。
   * **冲突解决**：若发生 Minor 冲突，Agent 通过 AST 解析尝试自动 Merge；若解决失败则立刻打回为 `blocked` 并通过 `review_notes` 请求人工介入。
   * **自动测试**：通过后，由 GitHub Action Bot 自动发起 PR，触发 NPU E2E 测试。
3. **最终流转**：
   研发人员不再需要手动去摘取上游代码，只需每天早上看一眼 Bot 提过来的 Pull Requests 进行 Code Review 和 Click Approve。