import json

for repo_name, path in [("vllm", "data/vllm/commits/2026-07-19.json"),
                         ("vllm-ascend", "data/vllm-ascend/commits/2026-07-19.json")]:
    print(f"\n{'='*70}\n{repo_name}\n{'='*70}")
    try:
        d = json.load(open(path, "r", encoding="utf-8"))
    except FileNotFoundError:
        print(f"  NOT FOUND: {path}")
        continue
    commits = d.get("commits", [])
    print(f"Total commits: {len(commits)}")
    for i, c in enumerate(commits, 1):
        msg = c.get("message", "").splitlines()[0] if c.get("message") else ""
        print(f"  [{i}] {c['sha'][:8]} - {msg[:120]}")
        for f in c.get("files", [])[:3]:
            print(f"        - {f.get('filename','')} (+{f.get('additions',0)}/-{f.get('deletions',0)})")
        if len(c.get("files", [])) > 3:
            print(f"        ... and {len(c['files']) - 3} more files")
