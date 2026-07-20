#!/usr/bin/env python3
"""
每日刷新看板数据 - 刷新前一天的提交数据和分析结果
"""
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta

TZ_CN = timezone(timedelta(hours=8))

def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    
    yesterday = (datetime.now(TZ_CN) - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now(TZ_CN).strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 60)
    print("  vLLM Daily Dashboard Refresh")
    print(f"  刷新日期: {yesterday}")
    print(f"  执行时间: {today}")
    print("=" * 60)
    print()
    
    repos = [
        ("vllm-project/vllm", ".tmp_vllm"),
        ("vllm-project/vllm-ascend", None),
    ]
    
    success = True
    
    for i, (repo, local_repo) in enumerate(repos, 1):
        print(f"[{i}/4] Fetching {repo} commits for {yesterday}...")
        cmd = [
            sys.executable, "scripts/fetch_commits.py",
            "--repo", repo,
            "--branch", "main",
            "--refresh-date", yesterday,
        ]
        if local_repo:
            cmd.extend(["--local-repo", local_repo])
        else:
            cmd.append("--api-only")
        
        result = subprocess.run(cmd, capture_output=False)
        if result.returncode != 0:
            print(f"  Warning: Failed to fetch {repo} commits")
            success = False
        print()
    
    print("[3/4] Analyzing commits...")
    for repo, local_repo in repos:
        print(f"  Analyzing {repo}...")
        cmd = [
            sys.executable, "scripts/analyze_commits.py",
            "--repo", repo,
            "--date", yesterday,
            "--force",
        ]
        if local_repo:
            cmd.extend(["--local-repo", local_repo])
        result = subprocess.run(cmd, capture_output=False)
        if result.returncode != 0:
            print(f"  Warning: Failed to analyze {repo}")
            success = False
        print()
    
    print("[4/4] Updating analysis index...")
    cmd = [sys.executable, "scripts/update_analysis_index.py"]
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print("  Warning: Failed to update analysis index")
        success = False
    print()
    
    print("=" * 60)
    print("  Dashboard refresh completed!")
    print(f"  Date: {yesterday}")
    print(f"  Time: {datetime.now(TZ_CN).strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
