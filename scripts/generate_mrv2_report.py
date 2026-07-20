#!/usr/bin/env python3
import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "MRV2_Daily_Report.md")


def get_date_range(days: int = 30) -> List[str]:
    dates = []
    today = datetime.now()
    for i in range(days):
        date = today - timedelta(days=i)
        dates.append(date.strftime("%Y-%m-%d"))
    return dates


# MRV2 核心文件路径（基于 vllm/v1/worker/gpu/model_runner.py 的 import）
MRV2_CORE_PATHS = [
    # 核心文件
    "vllm/v1/worker/gpu/model_runner.py",
    "vllm/v1/worker/gpu_model_runner.py",  # MRV1 对比文件

    # GPU worker 组件
    "vllm/v1/worker/gpu/async_utils.py",
    "vllm/v1/worker/gpu/attn_utils.py",
    "vllm/v1/worker/gpu/block_table.py",
    "vllm/v1/worker/gpu/buffer_utils.py",
    "vllm/v1/worker/gpu/cp_utils.py",
    "vllm/v1/worker/gpu/cudagraph_utils.py",
    "vllm/v1/worker/gpu/dp_utils.py",
    "vllm/v1/worker/gpu/eplb_utils.py",
    "vllm/v1/worker/gpu/input_batch.py",
    "vllm/v1/worker/gpu/kv_connector.py",
    "vllm/v1/worker/gpu/lora_utils.py",
    "vllm/v1/worker/gpu/pp_utils.py",
    "vllm/v1/worker/gpu/shutdown.py",
    "vllm/v1/worker/gpu/states.py",
    "vllm/v1/worker/gpu/structured_outputs.py",

    # mm 子目录
    "vllm/v1/worker/gpu/mm/encoder_cache.py",
    "vllm/v1/worker/gpu/mm/lora.py",

    # model_states 子目录
    "vllm/v1/worker/gpu/model_states/",

    # pool 子目录
    "vllm/v1/worker/gpu/pool/pooling_runner.py",

    # sample 子目录
    "vllm/v1/worker/gpu/sample/",

    # spec_decode 子目录
    "vllm/v1/worker/gpu/spec_decode/",
]

# MRV2 相关关键词（用于 commit message 匹配）
MRV2_KEYWORDS = [
    "MRV2",
    "Model Runner V2",
    "use_v2_model_runner",
    "VLLM_USE_V2_MODEL_RUNNER",
    "v2 model runner",
    "model_runner_v2",
]


def is_mrv2_file(filepath: str) -> bool:
    """检查文件路径是否属于 MRV2 核心组件"""
    for path in MRV2_CORE_PATHS:
        if path.endswith("/"):
            if filepath.startswith(path):
                return True
        elif filepath == path or filepath.startswith(path.replace(".py", "")):
            return True
    return False


def is_mrv2_commit(commit: Dict[str, Any]) -> bool:
    comment = commit.get("comment", "")
    tags = commit.get("tags", [])
    tag_str = " ".join(tags).lower()

    # 排除 MRV1 相关
    if "mrv1" in tag_str or "model_runner_v1" in comment.lower():
        return False
    if "【MRV1】" in comment:
        return False

    # 获取 commit 的文件列表
    files = commit.get("files", [])
    if isinstance(files, list):
        file_paths = [f.get("filename", "") if isinstance(f, dict) else str(f) for f in files]
    else:
        file_paths = []

    # 策略1: 文件路径匹配（最准确）
    for filepath in file_paths:
        if is_mrv2_file(filepath):
            return True

    # 策略2: commit message 关键词匹配
    for keyword in MRV2_KEYWORDS:
        if keyword.lower() in comment.lower():
            return True

    # 策略3: 标签匹配
    if "mrv2" in tag_str or "model-runner" in tag_str:
        # 排除自动生成的空内容
        auto_generated_phrases = [
            "常规维护变更",
            "新功能实现，扩展项目能力",
            "修复已知问题",
            "CI配置变更",
        ]
        has_real_content = not any(phrase in comment for phrase in auto_generated_phrases)
        if has_real_content:
            return True

    return False


def collect_mrv2_commits() -> Dict[str, List[Dict[str, Any]]]:
    mrv2_commits: Dict[str, List[Dict[str, Any]]] = {}
    repos = ["vllm", "vllm-ascend"]

    for repo in repos:
        commits_dir = os.path.join(DATA_DIR, repo, "commits")
        analysis_dir = os.path.join(DATA_DIR, repo, "analysis")

        for date in get_date_range(7):
            # 读取 commits 数据（包含 files 字段）
            commits_path = os.path.join(commits_dir, f"{date}.json")
            if not os.path.exists(commits_path):
                continue

            try:
                with open(commits_path, "r", encoding="utf-8") as f:
                    commits_data = json.load(f)
            except Exception:
                continue

            # 读取 analysis 数据（包含 tags, ascend_impact 等）
            analysis_path = os.path.join(analysis_dir, f"{date}.json")
            analysis_map: Dict[str, Dict] = {}
            if os.path.exists(analysis_path):
                try:
                    with open(analysis_path, "r", encoding="utf-8") as f:
                        analysis_data = json.load(f)
                    for ac in analysis_data.get("commits", []):
                        analysis_map[ac.get("sha", "")] = ac
                except Exception:
                    pass

            # 遍历 commits（有 files 信息），用 analysis 补充 tags 和 impact
            for commit in commits_data.get("commits", []):
                sha = commit.get("sha", "")
                analysis = analysis_map.get(sha, {})

                # 合并 commits 和 analysis 的信息
                merged = {
                    "sha": sha,
                    "message": commit.get("message", ""),
                    "files": commit.get("files", []),
                    "comment": analysis.get("comment", commit.get("message", "")),
                    "title_en": analysis.get("title_en", ""),
                    "title_zh": analysis.get("title_zh", ""),
                    "pr_number": analysis.get("pr_number", ""),
                    "tags": analysis.get("tags", []),
                    "ascend_impact": analysis.get("ascend_impact", {}),
                    "repo": repo,
                    "analysis_date": date,
                }

                if is_mrv2_commit(merged):
                    if date not in mrv2_commits:
                        mrv2_commits[date] = []
                    mrv2_commits[date].append(merged)

    return mrv2_commits


def clean_title(title: str) -> str:
    """清理标题中重复的 MRV2 标签和冗余空格"""
    if not title:
        return title
    # 去掉所有 【MRV2】 标记
    title = re.sub(r"【MRV2】", "", title)
    # 去掉英文 [MRV2] 标记
    title = re.sub(r"\[MRV2\]", "", title, flags=re.IGNORECASE)
    # 合并连续空格
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def extract_pr_number(comment: str) -> str:
    """从 comment 中提取 PR 号"""
    match = re.search(r"【PR号】#(\d+)", comment)
    if match:
        return match.group(1)
    return ""


def format_files(files: List[Any]) -> List[str]:
    """将文件变更列表格式化为缩进行"""
    lines = []
    for f in files:
        if isinstance(f, dict):
            filename = f.get("filename", "")
            status = f.get("status", "modified")
            additions = f.get("additions", 0)
            deletions = f.get("deletions", 0)
            status_zh = {"added": "新增", "modified": "修改", "removed": "删除", "renamed": "重命名"}.get(status, "修改")
            lines.append(f"  - {status_zh} `{filename}` (+{additions}/-{deletions})")
        else:
            lines.append(f"  - {f}")
    return lines


def dedup_tags(tags: List[str]) -> List[str]:
    """标签去重，保持顺序"""
    seen = set()
    result = []
    for tag in tags:
        t = tag.strip().lower()
        if t and t not in seen:
            seen.add(t)
            result.append(tag.strip())
    return result


def format_commit(commit: Dict[str, Any]) -> List[str]:
    """格式化单个 commit 的 Markdown 行列表"""
    sha = commit["sha"][:8]
    repo = commit["repo"]
    repo_url = f"https://github.com/vllm-project/{repo}"

    # 优先使用整理后的 title，fallback 到原始 comment 的第一行
    title = clean_title(commit.get("title_zh", "")) or clean_title(commit.get("title_en", ""))
    if not title:
        title = commit.get("comment", "").split("\n")[0]
        title = clean_title(title)

    pr_number = commit.get("pr_number", "") or extract_pr_number(commit.get("comment", ""))
    pr_link = f" ([#{pr_number}]({repo_url}/pull/{pr_number}))" if pr_number else ""

    lines = []
    lines.append(f"- **[{sha}]({repo_url}/commit/{commit['sha']})**{pr_link} {title}")

    # 标签
    tags = dedup_tags(commit.get("tags", []))
    if tags:
        lines.append(f"  - 标签: {', '.join(f'`{t}`' for t in tags)}")

    # 文件变更（最多展示 10 个，超出折叠）
    files = commit.get("files", [])
    if files:
        file_lines = format_files(files)
        if len(file_lines) <= 10:
            lines.append("  - 变更文件:")
            lines.extend(file_lines)
        else:
            lines.append(f"  - 变更文件（共 {len(file_lines)} 个）:")
            lines.extend(file_lines[:10])
            lines.append(f"  - ... 及其他 {len(file_lines) - 10} 个文件")

    # Ascend 影响
    impact = commit.get("ascend_impact", {})
    affected = "⚠️ 影响 Ascend" if impact.get("ascend_affected") else "✓ 无影响"
    lines.append(f"  - Ascend 影响: {affected}")
    if impact.get("ascend_affected"):
        functionality = impact.get("functionality", "").strip()
        if functionality:
            lines.append(f"    - 影响描述: {functionality}")
        if impact.get("needs_test_update"):
            areas = impact.get("suggested_test_areas", [])
            if areas:
                lines.append(f"    - 建议测试区域: {', '.join(f'`{a}`' for a in areas)}")

    return lines


def generate_report(mrv2_commits: Dict[str, List[Dict[str, Any]]]) -> str:
    sorted_dates = sorted(mrv2_commits.keys(), reverse=True)

    sections = []
    sections.append("# MRV2 每日报告")
    sections.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sections.append("统计范围: 最近 7 天")
    sections.append("")
    sections.append("**MRV2 定义**: `vllm/v1/worker/gpu/model_runner.py` 及其依赖的所有组件")
    sections.append("")
    sections.append(f"MRV2 相关 commits 总数: {sum(len(cs) for cs in mrv2_commits.values())}")
    sections.append("")

    for date in sorted_dates:
        commits = mrv2_commits[date]
        if not commits:
            continue

        sections.append(f"## {date}")

        vllm_commits = [c for c in commits if c["repo"] == "vllm"]
        ascend_commits = [c for c in commits if c["repo"] == "vllm-ascend"]

        if vllm_commits:
            sections.append("### vllm")
            for commit in vllm_commits:
                sections.extend(format_commit(commit))
                sections.append("")

        if ascend_commits:
            sections.append("### vllm-ascend")
            for commit in ascend_commits:
                sections.extend(format_commit(commit))
                sections.append("")

        sections.append("---")
        sections.append("")

    return "\n".join(sections)


def main():
    mrv2_commits = collect_mrv2_commits()
    report = generate_report(mrv2_commits)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"报告已生成: {REPORT_PATH}")
    print(f"包含 {len(mrv2_commits)} 天的 MRV2 相关 commits")


if __name__ == "__main__":
    main()
