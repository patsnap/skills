"""litigation-risk-monitor 默认参数与字段口径。"""
from __future__ import annotations

# 默认输入
DEFAULT_INVENTOR_LOOKBACK_YEARS = 3
DEFAULT_FAMILY_SCOPE = "inpadoc"  # original | inpadoc | extended
DEFAULT_REPORT_LANG = "zh"
DEFAULT_MAX_LITIGATED_PER_ASSIGNEE = 30
DEFAULT_TOP_INVENTORS = 10

# 诉讼信号关键词（Patsnap legal events / 公网双语）
LITIGATION_KEYWORDS = [
    "litigation", "lawsuit", "infringement", "complaint",
    "injunction", "itc", "patent suit",
    "诉讼", "侵权", "起诉", "专利诉讼", "侵害专利权",
    "FRAND", "SEP", "licensing dispute",
]

# 报告骨架顺序（固定）
REPORT_SECTIONS = [
    "overview",
    "family_basic",
    "case_deep_dive",
    "inventor_trend",
    "three_dim_conclusion",
    "appendix_sources",
]

# 三维结论键
CONCLUSION_DIMENSIONS = [
    "geographic_risk",
    "litigation_alert",
    "trend_forecast",
]

# 字段口径说明（出现在报告附录）
FIELD_NOTES = {
    "matched_total": "查询范围内的命中总数（Patsnap）",
    "returned_count": "当前样本/分页返回数",
    "family_scope": "INPADOC 同族（默认）",
    "litigation_signal": "Patsnap legal 模块 + web.search 双向交叉",
}
