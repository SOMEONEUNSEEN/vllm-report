#!/usr/bin/env python3
"""
批量重新分析所有历史数据，使其包含新的字段：
- pr_number: PR号
- title_en: 英文标题
- title_zh: 中文标题
- comment: 详细中文分析
"""
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta

TZ_CN = timezone(timedelta(hours=8))


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    with open('data/vllm/dates.json', 'r', encoding='utf-8') as f:
        dates = json.load(f)['dates']

    # 排除已整改的 2026-07-13
    dates_to_process = [d for d in dates if d != '2026-07-13']
    print(f"Total dates to re-analyze: {len(dates_to_process)}")
    print(f"Range: {dates_to_process[0]} ~ {dates_to_process[-1]}")
    print("=" * 60)

    success_count = 0
    failed_dates = []

    for i, date in enumerate(dates_to_process, 1):
        print(f"\n[{i}/{len(dates_to_process)}] Re-analyzing {date}...")
        cmd = [
            sys.executable, "scripts/analyze_commits.py",
            "--repo", "vllm-project/vllm",
            "--date", date,
            "--force",
            "--local-repo", ".tmp_vllm",
        ]
        result = subprocess.run(cmd, capture_output=False)
        if result.returncode == 0:
            success_count += 1
        else:
            failed_dates.append(date)
            print(f"  Failed: {date}")
        print()

    print("=" * 60)
    print(f"Done: {success_count}/{len(dates_to_process)} dates re-analyzed")
    if failed_dates:
        print(f"Failed dates: {failed_dates}")

    # 更新索引
    print("\nUpdating analysis index...")
    subprocess.run([sys.executable, "scripts/update_analysis_index.py"])
    print("=" * 60)

    return 0 if not failed_dates else 1


if __name__ == "__main__":
    import json
    sys.exit(main())
