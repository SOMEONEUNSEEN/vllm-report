#!/usr/bin/env python3
"""
每日刷新 Excel 表格 - 整合脚本
流程：
1. 调用 export_commits_to_excel.py 导出 Excel（基于现有数据）
2. 调用 translate_titles.py 翻译未翻译的标题
"""
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta

TZ_CN = timezone(timedelta(hours=8))


def run_step(step_num: int, total: int, description: str, cmd: list[str]) -> bool:
    """运行一个步骤"""
    print(f"\n[{step_num}/{total}] {description}")
    print("-" * 60)
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"  [警告] {description} 失败 (退出码: {result.returncode})")
        return False
    print(f"  [完成] {description}")
    return True


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    now = datetime.now(TZ_CN)

    print("=" * 60)
    print("  每日 Excel 表格刷新")
    print(f"  执行时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    py = sys.executable
    total_steps = 2
    success = True

    # Step 1: 导出 Excel（基于现有数据）
    success &= run_step(1, total_steps, "导出 Excel 表格（MRV2 相关 commits + 高风险 sheet）",
                        [py, "scripts/export_commits_to_excel.py"])

    # Step 2: 翻译未翻译的标题
    success &= run_step(2, total_steps, "翻译未翻译的标题",
                        [py, "scripts/translate_titles.py"])

    print("\n" + "=" * 60)
    if success:
        print("  [成功] 所有步骤已完成")
    else:
        print("  [部分成功] 部分步骤失败，请检查日志")
    print(f"  完成时间: {datetime.now(TZ_CN).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  输出文件: {os.path.join(project_dir, 'vllm_commits_export.xlsx')}")
    print("=" * 60)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
