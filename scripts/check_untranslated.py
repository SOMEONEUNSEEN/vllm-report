import pandas as pd

df = pd.read_excel('vllm_commits_export.xlsx', sheet_name='Commits')
untranslated = df[df['标题（中文）'] == df['标题（英文）']][['标题（中文）', '标题（英文）', 'PR 编号']]
print('未翻译的标题（共', len(untranslated), '条）:')
for _, row in untranslated.iterrows():
    print(f"  #{row['PR 编号']}: {row['标题（中文）']}")
