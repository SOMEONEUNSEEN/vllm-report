"""Extract commit details for manual AI analysis."""
import json
import os

OUTPUT_DIR = ".tmp_commits_analysis"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for repo_name, path in [("vllm", "data/vllm/commits/2026-07-19.json"),
                         ("vllm-ascend", "data/vllm-ascend/commits/2026-07-19.json")]:
    d = json.load(open(path, "r", encoding="utf-8"))
    commits = d.get("commits", [])
    repo_dir = os.path.join(OUTPUT_DIR, repo_name)
    os.makedirs(repo_dir, exist_ok=True)

    for i, c in enumerate(commits, 1):
        sha_short = c["sha"][:8]
        out_path = os.path.join(repo_dir, f"{i:02d}_{sha_short}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"=== Commit {i}/{len(commits)} ===\n")
            f.write(f"Repo: {repo_name}\n")
            f.write(f"SHA: {c['sha']}\n")
            f.write(f"Author: {c.get('author', {}).get('name', '')}\n")
            f.write(f"Date: {c.get('date', '')}\n")
            f.write(f"\n--- Message ---\n{c.get('message', '')}\n")
            stats = c.get("stats", {})
            f.write(f"\n--- Stats ---\n")
            f.write(f"Files changed: {stats.get('files_changed', 0)}\n")
            f.write(f"Additions: {stats.get('total_additions', 0)}\n")
            f.write(f"Deletions: {stats.get('total_deletions', 0)}\n")
            f.write(f"\n--- Files ---\n")
            for fi, file in enumerate(c.get("files", []), 1):
                f.write(f"\n[File {fi}] {file.get('filename', '')}\n")
                f.write(f"  status: {file.get('status', '')}\n")
                f.write(f"  additions: {file.get('additions', 0)}, deletions: {file.get('deletions', 0)}\n")
                patch = file.get("patch", "")
                if patch:
                    f.write(f"  patch:\n{patch}\n")
                else:
                    f.write(f"  patch: (empty)\n")
        print(f"Wrote {out_path}")

print("\nDone. Files in .tmp_commits_analysis/")
