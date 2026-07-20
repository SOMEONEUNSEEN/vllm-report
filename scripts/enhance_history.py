#!/usr/bin/env python3
"""
原地改造历史分析文件，为每个 commit 添加：
- pr_number: PR号
- title_en: 英文标题
- title_zh: 中文标题
- comment: 详细中文分析（替换原 comment）
"""
import os
import sys
import re
import json
import tempfile
from datetime import datetime, timezone, timedelta

TZ_CN = timezone(timedelta(hours=8))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_json(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Failed to load {filepath}: {e}")
        return None


def save_json_atomic(filepath, data):
    dirpath = os.path.dirname(filepath)
    os.makedirs(dirpath, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=dirpath, suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, filepath)
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise e


def extract_pr_number(message):
    """Extract PR number from commit message like 'title (#1234)'."""
    match = re.search(r'\(#(\d+)\)', message)
    if match:
        return match.group(1)
    match = re.search(r'PR[#:\s]+(\d+)', message, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def infer_tags(title, files):
    """Infer tags from commit message and file paths."""
    tags = []
    title_lower = title.lower()

    if any(w in title_lower for w in ["fix", "bug", "hotfix"]):
        tags.append("bugfix")
    elif any(w in title_lower for w in ["feat", "add", "support", "implement"]):
        tags.append("feature")
    elif any(w in title_lower for w in ["refactor", "cleanup", "rename", "restruct"]):
        tags.append("refactor")
    elif any(w in title_lower for w in ["perf", "optimize", "speed", "throughput"]):
        tags.append("performance")
    elif any(w in title_lower for w in ["test", "ci", "chore", "bump", "upgrade", "workflow"]):
        tags.append("chore")
    elif any(w in title_lower for w in ["doc", "readme"]):
        tags.append("docs")

    if "mrv2" in title_lower or "model runner v2" in title_lower:
        tags.append("mrv2")

    for f in files:
        filename = f.get("filename", "")
        if any(p in filename for p in ["vllm/v2/", "/v2/", "model_runner_v2", "model_runner/v2", "model_runner.py"]):
            tags.append("mrv2")
            break

    # 风险级别推断
    high_risk_keywords = ["breaking", "api change", "interface change", "signature change",
                          "major refactor", "remove", "delete"]
    medium_risk_keywords = ["refactor", "optimize", "performance", "change", "update"]

    risk = "low-risk"
    if any(w in title_lower for w in high_risk_keywords):
        risk = "high-risk"
    elif any(w in title_lower for w in medium_risk_keywords):
        risk = "medium-risk"
    else:
        for f in files:
            filename = f.get("filename", "")
            if any(p in filename for p in [
                "platforms/interface.py",
                "worker/worker_base.py",
                "worker/gpu_model_runner.py",
                "attention/backend.py",
                "sample/sampler.py",
                "compilation/compiler_interface.py",
            ]):
                risk = "high-risk"
                break

    tags.append(risk)
    return tags


def translate_title_to_chinese(title_en, files):
    """Translate commit title to Chinese based on patterns and keywords."""
    title_lower = title_en.lower()

    has_mrv2 = any("model_runner" in f.get("filename", "").lower() or
                   "gpu_model_runner" in f.get("filename", "").lower() or
                   "/v2/" in f.get("filename", "").lower()
                   for f in files)

    # 处理 [Tag] 前缀
    if title_lower.startswith("["):
        end_idx = title_en.find("]")
        if end_idx != -1:
            tag = title_en[1:end_idx]
            rest = title_en[end_idx+1:].strip()
            inner = _translate_inner(rest)
            prefix = "【MRV2】" if has_mrv2 else ""
            return f"{prefix}[{tag}] {inner}"

    inner = _translate_inner(title_en)
    prefix = "【MRV2】" if has_mrv2 else ""
    return prefix + inner


def _translate_inner(title_en):
    """Translate the inner part of a title to Chinese."""
    title_lower = title_en.lower()

    if any(w in title_lower for w in ["fix", "bug", "hotfix"]):
        prefix = "修复"
    elif any(w in title_lower for w in ["feat", "add", "support", "implement"]):
        prefix = "新增"
    elif any(w in title_lower for w in ["refactor", "cleanup", "rename", "restruct"]):
        prefix = "重构"
    elif any(w in title_lower for w in ["perf", "optimize", "speed", "throughput"]):
        prefix = "优化"
    elif any(w in title_lower for w in ["test", "ci", "chore", "bump", "upgrade", "workflow"]):
        prefix = "维护"
    elif any(w in title_lower for w in ["doc", "readme"]):
        prefix = "文档"
    else:
        prefix = "更新"

    desc_parts = []
    words = title_en.split()
    for word in words:
        word_clean = word.strip("(),:;.!?[]")
        if not word_clean or word_clean.startswith("#"):
            continue
        word_lower = word_clean.lower()
        if word_lower in ["for", "of", "in", "on", "with", "to", "the", "a", "an", "and", "or"]:
            continue
        zh = _word_to_zh(word_lower)
        if zh:
            desc_parts.append(zh)
        else:
            desc_parts.append(word_clean)

    if desc_parts:
        return f"{prefix}：{' '.join(desc_parts)}"
    return prefix


def _word_to_zh(word_lower):
    """Convert a single word to Chinese if in dictionary."""
    translations = {
        "fix": "修复", "bug": "问题", "add": "添加", "support": "支持",
        "implement": "实现", "feat": "功能", "feature": "功能", "refactor": "重构",
        "optimize": "优化", "improve": "改进", "performance": "性能", "speed": "速度",
        "throughput": "吞吐量", "remove": "移除", "delete": "删除", "update": "更新",
        "upgrade": "升级", "bump": "升级", "clean": "清理", "test": "测试",
        "tests": "测试", "doc": "文档", "docs": "文档", "ci": "CI",
        "chore": "维护", "lower": "降低", "memory": "内存", "required": "所需",
        "capturing": "捕获", "cudagraphs": "CUDA图", "large": "大", "sizes": "尺寸",
        "size": "尺寸", "split": "拆分", "work": "工作", "mypy": "Mypy",
        "license": "许可证", "header": "头", "rust": "Rust", "protobuf": "Protobuf",
        "sources": "源码", "adjust": "调整", "timeout": "超时", "intel": "Intel",
        "gpu": "GPU", "xpu": "XPU", "force": "强制", "channels_last": "channels_last",
        "idefics3": "Idefics3", "multimodal": "多模态", "processor": "处理器",
        "head": "头", "dtype": "数据类型", "kv": "KV", "cache": "缓存",
        "utils": "工具", "attention": "注意力", "backend": "后端", "cpu": "CPU",
        "fusion": "融合", "allreduce": "AllReduce", "rms": "RMS", "flashinfer": "FlashInfer",
        "rocm": "ROCm", "docker": "Docker", "dockerfile": "Dockerfile",
        "qwen": "Qwen", "mtp": "MTP", "minicpm": "MiniCPM", "eagle": "EAGLE",
        "registry": "注册表", "fused": "融合", "moe": "MoE", "configs": "配置",
        "nvidia": "NVIDIA", "rope": "RoPE", "kernel": "内核", "activation": "激活",
        "benchmark": "基准测试", "relu": "ReLU", "squared": "平方",
        "scheduler": "调度器", "offloading": "卸载", "v1": "V1", "worker": "Worker",
        "distributed": "分布式", "communicator": "通信器", "cuda": "CUDA",
        "engine": "引擎", "core": "核心", "transfer": "传输", "params": "参数",
        "tiering": "分层", "region": "区域", "replica": "副本", "aware": "感知",
        "guard": "保护", "mixed": "混合", "quant": "量化", "fusions": "融合",
        "make": "实现", "pin": "固定", "versions": "版本", "tool": "工具",
        "reduce": "减少", "time": "时间", "mypy": "Mypy", "frontend": "前端",
    }
    return translations.get(word_lower)


def generate_titles(message, files):
    """Generate Chinese and English titles from commit message."""
    title_en_raw = message.split("\n")[0].strip()
    pr_num = extract_pr_number(title_en_raw)
    if pr_num:
        title_en = re.sub(r'\s*\(#' + pr_num + r'\)\s*$', '', title_en_raw).strip()
    else:
        title_en = title_en_raw

    title_zh = translate_title_to_chinese(title_en, files)

    return {
        "title_en": title_en,
        "title_zh": title_zh,
        "pr_number": pr_num,
    }


def generate_detailed_comment(commit, tags, titles):
    """Generate detailed Chinese analysis comment for a commit."""
    files = commit.get("files", [])
    stats = commit.get("stats", {})
    title_zh = titles.get("title_zh", "")
    pr_number = titles.get("pr_number")

    parts = []
    parts.append(f"【变更概述】{title_zh}")
    if pr_number:
        parts.append(f"【PR号】#{pr_number}")

    if "bugfix" in tags:
        type_desc = "此提交为问题修复类型"
    elif "feature" in tags:
        type_desc = "此提交为新功能开发类型"
    elif "refactor" in tags:
        type_desc = "此提交为代码重构类型"
    elif "performance" in tags:
        type_desc = "此提交为性能优化类型"
    elif "chore" in tags:
        type_desc = "此提交为日常维护类型"
    elif "docs" in tags:
        type_desc = "此提交为文档更新类型"
    else:
        type_desc = "此提交为常规更新类型"
    parts.append(f"【变更类型】{type_desc}")

    if "mrv2" in tags:
        parts.append("【MRV2关联】此变更涉及 Model Runner V2 核心模块，需重点关注")

    if files:
        file_summary = []
        for f in files[:5]:
            filename = f.get("filename", "")
            status = f.get("status", "")
            additions = f.get("additions", 0)
            deletions = f.get("deletions", 0)
            status_zh = {"added": "新增", "modified": "修改", "removed": "删除", "renamed": "重命名"}.get(status, "变更")
            file_summary.append(f"{status_zh} {filename} (+{additions}/-{deletions})")
        if len(files) > 5:
            file_summary.append(f"... 及其他 {len(files) - 5} 个文件")
        parts.append(f"【变更文件】{'; '.join(file_summary)}")

    if stats:
        additions = stats.get("total_additions", 0)
        deletions = stats.get("total_deletions", 0)
        files_changed = stats.get("files_changed", 0)
        parts.append(f"【统计数据】共修改 {files_changed} 个文件，新增 {additions} 行，删除 {deletions} 行")

    if "high-risk" in tags:
        risk_level = "高风险 - 涉及核心接口或架构变更，可能影响系统稳定性"
    elif "medium-risk" in tags:
        risk_level = "中风险 - 涉及一定范围的功能修改，需要验证"
    else:
        risk_level = "低风险 - 变更范围较小，影响可控"
    parts.append(f"【风险评估】{risk_level}")

    return "\n".join(parts)


def enhance_analysis(analysis, commits_data):
    """为已有分析结果添加新字段。"""
    if not analysis or "commits" not in analysis:
        return analysis

    # 从 commits_data 获取完整文件信息
    commits_map = {}
    for c in commits_data.get("commits", []):
        commits_map[c["sha"]] = c

    enhanced_count = 0
    for ac in analysis["commits"]:
        sha = ac.get("sha")
        if not sha:
            continue

        # 获取完整 commit 数据（包括 files）
        full_commit = commits_map.get(sha, {})

        # 如果分析中没有 files，尝试从 commits_data 获取
        if "files" not in ac or not ac.get("files"):
            ac["files"] = full_commit.get("files", [])

        message = full_commit.get("message", "")
        files = ac.get("files", [])

        # 如果没有 message，尝试从原始 comment 推断
        if not message and "comment" in ac:
            message = ac["comment"]

        # 生成新字段
        if not message:
            # 如果都没有，跳过
            continue

        titles = generate_titles(message, files)

        # 更新 tags（如果不够丰富）
        existing_tags = ac.get("tags", [])
        if not existing_tags or len(existing_tags) < 2:
            title = message.split("\n")[0]
            existing_tags = infer_tags(title, files)
            ac["tags"] = existing_tags

        # 添加新字段
        ac["pr_number"] = titles["pr_number"]
        ac["title_en"] = titles["title_en"]
        ac["title_zh"] = titles["title_zh"]

        # 仅在 comment 不是新格式时重新生成
        old_comment = ac.get("comment", "")
        if not old_comment.startswith("【变更概述】"):
            ac["comment"] = generate_detailed_comment(full_commit, existing_tags, titles)

        enhanced_count += 1

    return analysis, enhanced_count


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    repo = "vllm-project/vllm"
    repo_dir = "data/vllm"

    # 读取所有历史日期
    with open(os.path.join(repo_dir, "dates.json"), "r", encoding="utf-8") as f:
        dates = json.load(f)["dates"]

    # 排除已整改的 2026-07-13
    dates_to_process = [d for d in dates if d != "2026-07-13"]
    print(f"Total dates to enhance: {len(dates_to_process)}")
    print(f"Range: {dates_to_process[0]} ~ {dates_to_process[-1]}")
    print("=" * 60)

    success_count = 0
    failed_dates = []
    total_commits = 0

    for i, date in enumerate(dates_to_process, 1):
        analysis_path = os.path.join(repo_dir, "analysis", f"{date}.json")
        commits_path = os.path.join(repo_dir, "commits", f"{date}.json")

        if not os.path.exists(analysis_path):
            print(f"[{i}/{len(dates_to_process)}] {date}: No analysis file, skipping")
            continue

        if not os.path.exists(commits_path):
            print(f"[{i}/{len(dates_to_process)}] {date}: No commits file, skipping")
            continue

        analysis = load_json(analysis_path)
        commits_data = load_json(commits_path)

        if not analysis or not commits_data:
            print(f"[{i}/{len(dates_to_process)}] {date}: Failed to load data, skipping")
            failed_dates.append(date)
            continue

        result, enhanced_count = enhance_analysis(analysis, commits_data)
        if result is None:
            failed_dates.append(date)
            continue

        # 更新时间戳
        result["generated_at"] = datetime.now(TZ_CN).isoformat()

        # 保存
        save_json_atomic(analysis_path, result)
        total_commits += enhanced_count
        success_count += 1
        print(f"[{i}/{len(dates_to_process)}] {date}: Enhanced {enhanced_count} commits")

    print("=" * 60)
    print(f"Done: {success_count}/{len(dates_to_process)} dates enhanced")
    print(f"Total commits enhanced: {total_commits}")
    if failed_dates:
        print(f"Failed dates: {failed_dates}")

    # 更新索引
    print("\nUpdating analysis index...")
    subprocess.run([sys.executable, "scripts/update_analysis_index.py"])
    print("=" * 60)

    return 0 if not failed_dates else 1


if __name__ == "__main__":
    import subprocess
    sys.exit(main())
