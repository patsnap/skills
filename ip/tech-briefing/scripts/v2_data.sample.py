# -*- coding: utf-8 -*-
"""v2_data.py 数据结构示例。

每次生成报告时，由 Claude 根据实际检索结果重新创建此文件到
~/Documents/tech_briefings/v2_data.py（不是本目录），然后运行
build_report_v2.py 生成 HTML。

所有数字必须来自实际检索结果，不得手写或估算。
"""

# 报告标题
TITLE = "华为 & 小米 5G 技术简报"

# 时间范围（展示用字符串）
TIME_RANGE = "2025-11 ~ 2026-05"

# 总结分析（支持 HTML；用 <p>、<ul> 组织）
SUMMARY = """
<p>基于 xxx 件专利的分析，华为在 xxx 方向持续加码，小米聚焦 xxx 场景...</p>
<ul>
  <li><strong>技术趋势：</strong>xxx</li>
  <li><strong>竞争格局：</strong>xxx</li>
  <li><strong>热点技术：</strong>xxx</li>
  <li><strong>建议关注：</strong>xxx</li>
</ul>
"""

# 各公司专利总量（count_patent 实际返回值）
PATENT_TOTAL_BY_COMPANY = {
    "华为": 0,
    "小米": 0,
}

# 趋势数据（月度公开量）
TREND_SERIES = {
    "months": ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"],
    "series": {
        "华为": [0, 0, 0, 0, 0, 0],
        "小米": [0, 0, 0, 0, 0, 0],
    },
}

# 词云数据（count 必须是实际包含该词的专利数）
WORD_CLOUD = [
    # {"word": "毫米波", "size": 28, "color": "#1b5cd8", "count": 12},
]

# 所有纳入报告的专利扁平列表（子技术通过 pn 引用）
PATENTS = [
    # {
    #   "pn": "CN12345678A", "pid": "xxx-patsnap-id",
    #   "title": "...", "assignee": "华为技术有限公司",
    #   "apdt": "2025-10-12", "pbdt": "2026-03-15",
    #   "status": "审中",
    #   "problem": "...", "approach": "...", "effect": "...",
    #   "company": "华为", "branch": "控制与算法",
    # },
]

# 按公司分组（每条引用 PATENTS 中的对象，便于 UI 展开）
PATENTS_BY_COMPANY = {
    # "华为": [<patent_dict>, ...],
    # "小米": [...],
}

# 学术文献
LITERATURE = [
    # {
    #   "title": "...", "authors": "Zhang et al.",
    #   "journal": "IEEE Trans.", "year": "2026",
    #   "doi": "10.xxxx/xxx", "url": "",
    #   "summary": "该论文提出了...，实验表明...",
    # },
]

# 行业新闻
NEWS = [
    # {"title": "...", "url": "...", "desc": "...", "source": "sogou/XX网"},
]

# 子技术分组（patents 为 pn 列表，必须存在于 PATENTS 中）
SUB_TECHS = [
    # {"name": "毫米波天线", "patents": ["CN12345678A", "CN87654321A"]},
]
