#!/usr/bin/env python3
"""
Export all commits and analysis data from vllm-report to an Excel file.
"""
import json
import os
import re
from pathlib import Path
from urllib.parse import quote

import pandas as pd

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_FILE = PROJECT_DIR / "vllm_commits_export.xlsx"

REPO_URLS = {
    "vllm-project/vllm": "https://github.com/vllm-project/vllm",
    "vllm-project/vllm-ascend": "https://github.com/vllm-project/vllm-ascend",
}


def parse_commit_message(message: str) -> dict:
    """Parse commit message into title and body."""
    lines = message.split("\n")
    title = lines[0] if lines else ""
    # Find the separator line "---" and extract the diff stat before it
    body_lines = []
    diff_stat = ""
    in_diff = False
    for line in lines[1:]:
        if line.strip() == "---":
            in_diff = True
            continue
        if in_diff:
            diff_stat += line + "\n"
        else:
            body_lines.append(line)
    body = "\n".join(body_lines).strip()
    diff_stat = diff_stat.strip()
    return {"title": title, "body": body, "diff_stat": diff_stat}


def extract_pr_number(message: str) -> str:
    """Extract PR number from commit message title or analysis data."""
    match = re.search(r"\(#(\d+)\)", message)
    if match:
        return match.group(1)
    return ""


def get_github_commit_url(repo: str, sha: str) -> str:
    """Generate GitHub commit URL."""
    base = REPO_URLS.get(repo, f"https://github.com/{repo}")
    return f"{base}/commit/{sha}"


def get_github_pr_url(repo: str, pr_number: str) -> str:
    """Generate GitHub PR URL."""
    if not pr_number:
        return ""
    base = REPO_URLS.get(repo, f"https://github.com/{repo}")
    return f"{base}/pull/{pr_number}"


def load_json_safe(path: Path) -> dict | None:
    """Load JSON file safely."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, Exception):
        return None


def collect_all_commits() -> list[dict]:
    """Collect commits that have impact on Ascend."""
    rows = []

    # Discover all commit files
    for repo_dir in ["vllm", "vllm-ascend"]:
        commits_dir = DATA_DIR / repo_dir / "commits"
        analysis_dir = DATA_DIR / repo_dir / "analysis"

        if not commits_dir.exists():
            continue

        for commit_file in sorted(commits_dir.glob("*.json")):
            date_str = commit_file.stem
            commits_data = load_json_safe(commit_file)
            if not commits_data:
                continue

            analysis_file = analysis_dir / f"{date_str}.json"
            analysis_data = load_json_safe(analysis_file)

            analysis_map = {}
            if analysis_data and "commits" in analysis_data:
                for ac in analysis_data["commits"]:
                    analysis_map[ac.get("sha", "")] = ac

            repo = commits_data.get("repo", f"vllm-project/{repo_dir}")

            for commit in commits_data.get("commits", []):
                sha = commit.get("sha", "")
                message = commit.get("message", "")
                parsed = parse_commit_message(message)
                pr_from_msg = extract_pr_number(parsed["title"])

                ac = analysis_map.get(sha, {})

                pr_number = ac.get("pr_number", "") or pr_from_msg

                tags = ac.get("tags", [])
                risk_level = ""
                if "high-risk" in tags:
                    risk_level = "high"
                elif "medium-risk" in tags:
                    risk_level = "medium"
                elif "low-risk" in tags:
                    risk_level = "low"

                files = commit.get("files", [])
                file_list = [f.get("filename", "") for f in files]
                file_list_str = "\n".join(file_list)

                stats = commit.get("stats", {})
                additions = stats.get("total_additions", 0)
                deletions = stats.get("total_deletions", 0)
                files_changed = stats.get("files_changed", len(files))

                ascend_impact = ac.get("ascend_impact", {})
                ascend_affected = ascend_impact.get("ascend_affected", False)
                ascend_functionality = ascend_impact.get("functionality", "")
                ascend_testing = ascend_impact.get("testing", "")
                needs_test_update = ascend_impact.get("needs_test_update", False)

                test_impact = ac.get("test_impact", {})
                needs_new_test = test_impact.get("needs_new_test", False)
                test_reason = test_impact.get("reason", "")
                suggested_tests = test_impact.get("suggested_test_areas", [])
                suggested_tests_str = "\n".join(suggested_tests)

                # Filter: only MRV2 related commits
                # Check both tags and file paths
                is_mrv2 = "mrv2" in tags
                if not is_mrv2:
                    files = commit.get("files", [])
                    mrv2_paths = ["vllm/v1/worker/gpu/", "spec_decode/"]
                    for f in files:
                        if isinstance(f, dict):
                            filepath = f.get("filename", "")
                        else:
                            filepath = str(f)
                        if any(p in filepath for p in mrv2_paths):
                            is_mrv2 = True
                            break
                if not is_mrv2:
                    continue

                # Filter: only vllm repo, not vllm-ascend
                if "vllm-ascend" in repo:
                    continue

                title_zh = ac.get("title_zh", "")
                title_en = ac.get("title_en", parsed["title"])
                if not title_zh:
                    title_zh = title_en

                # Format commit date to YYYY-MM-DD HH:MM:SS
                commit_date_raw = commit.get("date", "")
                commit_date = ""
                commit_date_sort = ""
                if commit_date_raw:
                    try:
                        dt = pd.to_datetime(commit_date_raw, utc=True)
                        commit_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                        commit_date_sort = dt.isoformat()
                    except Exception:
                        commit_date = commit_date_raw
                        commit_date_sort = commit_date_raw

                row = {
                    "PR 编号": pr_number,
                    "PR 链接": get_github_pr_url(repo, pr_number),
                    "标题（中文）": title_zh,
                    "标题（英文）": title_en,
                    "Commit 合入时间": commit_date,
                    "_sort_time": commit_date_sort,
                    "Ascend 影响": "是" if ascend_affected else "否",
                    "Ascend 功能影响": ascend_functionality,
                    "Ascend 测试建议": ascend_testing,
                    "需要新增测试": "是" if needs_new_test else "否",
                    "需要更新测试": "是" if needs_test_update else "否",
                    "建议测试区域": suggested_tests_str,
                    "风险等级": risk_level,
                    "变更类型": ", ".join(tags),
                    "日期": date_str,
                    "仓库": repo,
                    "Commit SHA": sha,
                    "Commit 链接": get_github_commit_url(repo, sha),
                    "作者": commit.get("author", {}).get("name", ""),
                    "新增行数": additions,
                    "删除行数": deletions,
                    "变更文件数": files_changed,
                    "变更文件列表": file_list_str,
                    "详细描述/评论": ac.get("comment", ""),
                }
                rows.append(row)

    return rows


def export_to_excel(rows: list[dict], output_path: Path):
    """Export rows to an Excel file with formatting."""
    if not rows:
        print("No data to export.")
        return

    df = pd.DataFrame(rows)

    # Sort by commit date descending (newest first)
    if "_sort_time" in df.columns:
        df["_sort_time_dt"] = pd.to_datetime(df["_sort_time"], errors="coerce", utc=True)
        df = df.sort_values("_sort_time_dt", ascending=False)
        df = df.drop(columns=["_sort_time", "_sort_time_dt"])

    # Column order: Impact info first, then PR info, then title, then details
    column_order = [
        "PR 编号",
        "PR 链接",
        "标题（中文）",
        "标题（英文）",
        "Commit 合入时间",
        "Ascend 影响",
        "Ascend 功能影响",
        "Ascend 测试建议",
        "需要新增测试",
        "需要更新测试",
        "建议测试区域",
        "风险等级",
        "变更类型",
        "日期",
        "仓库",
        "Commit SHA",
        "Commit 链接",
        "作者",
        "新增行数",
        "删除行数",
        "变更文件数",
        "变更文件列表",
        "详细描述/评论",
    ]

    final_columns = [c for c in column_order if c in df.columns]
    df = df[final_columns]

    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.hyperlink import Hyperlink

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Commits")

        worksheet = writer.sheets["Commits"]

        # Header style
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Impact highlight style
        impact_font = Font(bold=True, color="C00000")
        impact_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

        # Hyperlink style
        hyperlink_font = Font(color="0563C1", underline="single")

        # Apply header style
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment

        # Convert PR 链接 column (column B) to hyperlinks showing PR number
        pr_link_col = 2  # Column B
        pr_number_col = 1  # Column A
        for row_idx in range(2, worksheet.max_row + 1):
            pr_link_cell = worksheet.cell(row=row_idx, column=pr_link_col)
            pr_number_cell = worksheet.cell(row=row_idx, column=pr_number_col)
            
            url = pr_link_cell.value
            pr_number = pr_number_cell.value
            if url and str(url).startswith("http") and pr_number:
                pr_link_cell.value = f"#{pr_number}"
                pr_link_cell.hyperlink = url
                pr_link_cell.font = hyperlink_font
                pr_link_cell.alignment = Alignment(horizontal="center")

        # Auto-adjust column widths and apply impact highlighting
        for col_idx, column in enumerate(worksheet.columns, 1):
            max_length = 0
            column_letter = get_column_letter(col_idx)
            for row_idx, cell in enumerate(column, 1):
                if cell.value:
                    str_value = str(cell.value)
                    max_length = max(max_length, len(str_value))
                # Highlight impact columns (columns 6-11: Ascend 影响, Ascend 功能影响, etc.)
                if row_idx > 1 and col_idx >= 6 and col_idx <= 11:
                    cell.fill = impact_fill
            adjusted_width = min(max_length + 2, 80)
            worksheet.column_dimensions[column_letter].width = adjusted_width

        # Create a new sheet for high-risk Ascend impacts
        high_risk_df = df[
            (df["Ascend 影响"].astype(str).str.contains("是|true|True")) & 
            (df["风险等级"].str.lower() == "high")
        ].copy()
        
        if not high_risk_df.empty:
            high_risk_df.to_excel(writer, index=False, sheet_name="High Risk")
            
            high_risk_ws = writer.sheets["High Risk"]
            
            # Apply header style
            for cell in high_risk_ws[1]:
                cell.font = header_font
                cell.fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
                cell.alignment = header_alignment
            
            # Convert PR links to hyperlinks
            for row_idx in range(2, high_risk_ws.max_row + 1):
                pr_link_cell = high_risk_ws.cell(row=row_idx, column=2)
                pr_number_cell = high_risk_ws.cell(row=row_idx, column=1)
                
                url = pr_link_cell.value
                pr_number = pr_number_cell.value
                if url and str(url).startswith("http") and pr_number:
                    pr_link_cell.value = f"#{pr_number}"
                    pr_link_cell.hyperlink = url
                    pr_link_cell.font = hyperlink_font
                    pr_link_cell.alignment = Alignment(horizontal="center")
            
            # Apply impact highlighting
            for col_idx, column in enumerate(high_risk_ws.columns, 1):
                max_length = 0
                column_letter = get_column_letter(col_idx)
                for row_idx, cell in enumerate(column, 1):
                    if cell.value:
                        str_value = str(cell.value)
                        max_length = max(max_length, len(str_value))
                    if row_idx > 1 and col_idx >= 6 and col_idx <= 11:
                        cell.fill = impact_fill
                adjusted_width = min(max_length + 2, 80)
                high_risk_ws.column_dimensions[column_letter].width = adjusted_width
            
            print(f"  - {len(high_risk_df)} high-risk commits saved to 'High Risk' sheet")

    print(f"Exported {len(rows)} commits to {output_path}")


def main():
    print("Collecting commits data...")
    rows = collect_all_commits()
    print(f"Collected {len(rows)} commits total.")
    export_to_excel(rows, OUTPUT_FILE)
    print("Done.")


if __name__ == "__main__":
    main()
