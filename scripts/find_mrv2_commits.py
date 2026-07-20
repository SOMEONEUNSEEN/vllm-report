#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime

DATA_DIR = "data"
REPOS = ["vllm", "vllm-ascend"]

MRV2_PATTERNS = [
    re.compile(r"model.*runner.*v2", re.IGNORECASE),
    re.compile(r"MRV2", re.IGNORECASE),
    re.compile(r"model_runner_v2", re.IGNORECASE),
    re.compile(r"ModelRunnerV2", re.IGNORECASE),
    re.compile(r"use_v2_model_runner", re.IGNORECASE),
    re.compile(r"V2ModelRunner", re.IGNORECASE),
    re.compile(r"v2.*model.*runner", re.IGNORECASE),
]


def matches_mrv2(text):
    if not text:
        return False
    for pattern in MRV2_PATTERNS:
        if pattern.search(text):
            return True
    return False


def find_mrv2_commits():
    results = []
    for repo in REPOS:
        commits_dir = os.path.join(DATA_DIR, repo, "commits")
        if not os.path.isdir(commits_dir):
            continue
        
        for filename in sorted(os.listdir(commits_dir), reverse=True):
            if not filename.endswith(".json") or filename == ".gitkeep":
                continue
            
            date = filename.replace(".json", "")
            filepath = os.path.join(commits_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                continue
            
            for commit in data.get("commits", []):
                sha = commit.get("sha", "")[:8]
                message = commit.get("message", "")
                author = commit.get("author", {}).get("name", "")
                commit_date = commit.get("date", "")
                
                matched = False
                matched_reasons = []
                
                if matches_mrv2(message):
                    matched = True
                    matched_reasons.append("commit message")
                
                for f in commit.get("files", []):
                    filename = f.get("filename", "")
                    patch = f.get("patch", "")
                    if matches_mrv2(filename):
                        matched = True
                        matched_reasons.append(f"file: {filename}")
                    if matches_mrv2(patch):
                        matched = True
                        matched_reasons.append(f"patch: {filename}")
                
                if matched:
                    results.append({
                        "date": date,
                        "repo": repo,
                        "sha": sha,
                        "author": author,
                        "commit_date": commit_date,
                        "message": message.split("\n")[0],
                        "reasons": matched_reasons,
                    })
    
    return sorted(results, key=lambda x: (x["date"], x["commit_date"]), reverse=True)


def print_results(results):
    print(f"Found {len(results)} MRV2-related commits:\n")
    
    current_date = None
    for r in results:
        if r["date"] != current_date:
            current_date = r["date"]
            print(f"\n{'='*60}")
            print(f"📅 {current_date}")
            print(f"{'='*60}")
        
        repo_icon = "🔵" if r["repo"] == "vllm" else "🟢"
        reasons_str = " | ".join(r["reasons"])
        print(f"\n{repo_icon} [{r['sha']}] {r['message']}")
        print(f"   Author: {r['author']}")
        print(f"   Matched: {reasons_str}")


if __name__ == "__main__":
    results = find_mrv2_commits()
    print_results(results)
