# -*- coding: utf-8 -*-
"""Run the full high-value patent screening pipeline end to end.

Prerequisites:
  pip install requests python-docx
  export ZHIHUIYA_API_KEY="<your key>"   (or put it in api_key.txt)
  export HVP_QUERY="<your PatSnap query>" (or put it in query.txt)

Run from a working directory where intermediate JSON and the final
reports should be written:
  python run_all.py            # HTML report only (default)
  python run_all.py --word     # also generate the optional Word report

python-docx is only needed when --word is used.
"""
import runpy
import sys

# HTML is the required deliverable; Word is optional and only run with --word.
STAGES = [
    ('hv_1_fetch', '检索候选 (P002)'),
    ('hv_2_numeric', '数值富集 P014/P015'),
    ('hv_3_legal', '法律事件 P034/P027/P028/P029'),
    ('hv_4_score', '打分与选取 30/30/20/20'),
    ('hv_5_display', '展示字段 P021/P025/P041'),
    ('hv_6_assemble', '组装记录 + 追溯 JSON'),
    ('hv_7_html_a', '生成 HTML 报告（公开公告号含跳转链接）'),
]
WORD_STAGE = ('hv_8_word', '生成可选 Word 报告')

if __name__ == '__main__':
    want_word = '--word' in sys.argv
    stages = STAGES + ([WORD_STAGE] if want_word else [])
    for mod, desc in stages:
        print(f'\n===== {mod}  {desc} =====')
        runpy.run_module(mod, run_name='__main__')
    arts = '高价值专利包筛选报告.html / 高价值专利包筛选数据.json'
    if want_word:
        arts += ' / 高价值专利包筛选报告.docx'
    print('\nDONE. Artifacts:', arts)
    if not want_word:
        print('（如需 Word 报告，重新运行并加 --word，或单独执行 python hv_8_word.py）')
