"""
match_scorer.py — 供需匹配评分引擎 v2.0
权重模型：专利 40% + 公开新闻 30% + 招投标 30%
每个维度二层细分，满分 100 分
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import math


# ─────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────

@dataclass
class PatentScores:
    """专利信息匹配得分（满分 40 分，输入均为 0~1 归一化值）"""
    # 一层：技术重叠度（18分）
    ipc_overlap: float = 0.0          # IPC/CPC 分类重合数 (8分)  ≥3个同类IPC→1.0
    keyword_similarity: float = 0.0   # 权利要求关键词命中率 (10分) NLP语义相似度≥0.75→1.0

    # 一层：研发活跃度（12分）
    recent_filing_trend: float = 0.0  # 近3年新申请数量趋势 (7分)  年均增长≥20%→1.0
    citation_impact: float = 0.0      # 被引用次数影响力 (5分)     被引≥50次→1.0

    # 一层：专利布局意图（10分）
    family_coverage: float = 0.0      # 同族专利覆盖国家数 (5分)   覆盖≥5国→1.0
    cross_citation: float = 0.0       # 与目标技术交叉引用关系 (5分) 有直接引用→1.0


@dataclass
class NewsScores:
    """公开新闻信息得分（满分 30 分，输入均为 0~1 归一化值）"""
    # 一层：技术需求信号（14分）
    collab_intent_news: float = 0.0   # 技术合作/引进意向报道 (8分)  明确寻求合作→1.0
    expansion_news: float = 0.0       # 产线扩产/新建项目新闻 (6分)  有扩产公告→1.0

    # 一层：研发投入信号（10分）
    rd_center_news: float = 0.0       # 研发中心/实验室建设报道 (5分) 有新研发设施→1.0
    gov_collab_news: float = 0.0      # 政府/高校联合研发项目 (5分)   有产学研合作→1.0

    # 一层：行业曝光度（6分）
    expo_presence: float = 0.0        # 展会/论坛技术展示 (3分)      近1年有展会→1.0
    industry_cert: float = 0.0        # 行业奖项/认证获取 (3分)      获同领域认证→1.0


@dataclass
class BidScores:
    """招投标信息匹配得分（满分 30 分，输入均为 0~1 归一化值）"""
    # 一层：采购意图强度（14分）
    keyword_hit: float = 0.0          # 招标公告技术关键词命中 (8分)  ≥3个关键词→1.0
    budget_scale: float = 0.0         # 预算金额规模 (6分)            预算≥500万→1.0

    # 一层：采购历史深度（10分）
    winning_history: float = 0.0      # 近2年同类技术中标记录 (6分)   ≥2次同类中标→1.0
    collab_history: float = 0.0       # 与技术提供方历史合作 (4分)    有直接合作记录→1.0

    # 一层：采购紧迫度（6分）
    recency_90d: float = 0.0          # 招标时间窗口近90天 (4分)      近30天发布→1.0
    repeat_purchase: float = 0.0      # 重复招标/补充采购标志 (2分)   有续采行为→1.0


@dataclass
class MatchResult:
    """单个接受方的完整匹配结果"""
    company_name: str
    patent_score: float       # 满分 40
    news_score: float         # 满分 30
    bid_score: float          # 满分 30
    total_score: float        # 满分 100
    grade: str                # ⭐ ~ ⭐⭐⭐⭐⭐
    grade_label: str          # 文字等级
    action: str               # 建议动作
    evidence: list[str] = field(default_factory=list)  # 支撑证据列表


# ─────────────────────────────────────────────
# 评分权重常量
# ─────────────────────────────────────────────

PATENT_WEIGHTS = {
    "ipc_overlap":         8,
    "keyword_similarity":  10,
    "recent_filing_trend": 7,
    "citation_impact":     5,
    "family_coverage":     5,
    "cross_citation":      5,
}  # 合计 40

NEWS_WEIGHTS = {
    "collab_intent_news":  8,
    "expansion_news":      6,
    "rd_center_news":      5,
    "gov_collab_news":     5,
    "expo_presence":       3,
    "industry_cert":       3,
}  # 合计 30

BID_WEIGHTS = {
    "keyword_hit":         8,
    "budget_scale":        6,
    "winning_history":     6,
    "collab_history":      4,
    "recency_90d":         4,
    "repeat_purchase":     2,
}  # 合计 30


# ─────────────────────────────────────────────
# 评分逻辑
# ─────────────────────────────────────────────

def _clamp(v: float) -> float:
    """将值限制在 0~1"""
    return max(0.0, min(1.0, v))


def calc_patent_score(s: PatentScores) -> float:
    return round(sum(
        _clamp(getattr(s, k)) * w
        for k, w in PATENT_WEIGHTS.items()
    ), 2)


def calc_news_score(s: NewsScores) -> float:
    return round(sum(
        _clamp(getattr(s, k)) * w
        for k, w in NEWS_WEIGHTS.items()
    ), 2)


def calc_bid_score(s: BidScores) -> float:
    return round(sum(
        _clamp(getattr(s, k)) * w
        for k, w in BID_WEIGHTS.items()
    ), 2)


def calc_match_score(
    patent: PatentScores,
    news: NewsScores,
    bid: BidScores,
) -> tuple[float, float, float, float]:
    """
    返回 (patent_score, news_score, bid_score, total_score)
    总分满分 100
    """
    ps = calc_patent_score(patent)
    ns = calc_news_score(news)
    bs = calc_bid_score(bid)
    total = round(ps + ns + bs, 2)
    return ps, ns, bs, total


# ─────────────────────────────────────────────
# 等级评定
# ─────────────────────────────────────────────

_GRADE_TABLE = [
    (85, "⭐⭐⭐⭐⭐", "强烈推荐", "立即跟进，优先级最高"),
    (70, "⭐⭐⭐⭐",   "高度匹配", "重点跟进，准备方案"),
    (55, "⭐⭐⭐",    "中度匹配", "常规跟进，持续观察"),
    (40, "⭐⭐",     "低度匹配", "列入观察名单"),
    ( 0, "⭐",      "弱匹配",   "暂不优先"),
]


def get_grade(total: float) -> tuple[str, str, str]:
    """返回 (grade_stars, grade_label, action)"""
    for threshold, stars, label, action in _GRADE_TABLE:
        if total >= threshold:
            return stars, label, action
    return "⭐", "弱匹配", "暂不优先"


# ─────────────────────────────────────────────
# 主入口：对单个企业进行综合评分
# ─────────────────────────────────────────────

def score_company(
    company_name: str,
    patent: PatentScores,
    news: NewsScores,
    bid: BidScores,
    evidence: Optional[list[str]] = None,
) -> MatchResult:
    """
    对单个潜在接受方企业进行完整评分，返回 MatchResult。
    """
    ps, ns, bs, total = calc_match_score(patent, news, bid)
    grade, label, action = get_grade(total)
    return MatchResult(
        company_name=company_name,
        patent_score=ps,
        news_score=ns,
        bid_score=bs,
        total_score=total,
        grade=grade,
        grade_label=label,
        action=action,
        evidence=evidence or [],
    )


# ─────────────────────────────────────────────
# 批量排序：Top-N 潜在接受方
# ─────────────────────────────────────────────

def rank_companies(results: list[MatchResult], top_n: int = 10) -> list[MatchResult]:
    """按总分降序排列，返回 Top-N"""
    return sorted(results, key=lambda r: r.total_score, reverse=True)[:top_n]


# ─────────────────────────────────────────────
# 输出格式化
# ─────────────────────────────────────────────

def format_result_markdown(r: MatchResult, rank: int) -> str:
    evidence_str = "\n  - ".join(r.evidence) if r.evidence else "（暂无具体证据）"
    return f"""### {rank}. {r.company_name}

| 维度 | 得分 | 满分 |
|------|------|------|
| 专利信息匹配 | {r.patent_score} | 40 |
| 公开新闻信息 | {r.news_score} | 30 |
| 招投标信息 | {r.bid_score} | 30 |
| **综合匹配度** | **{r.total_score}** | **100** |

**等级**：{r.grade} {r.grade_label}  
**建议动作**：{r.action}  
**核心匹配证据**：
  - {evidence_str}
"""


def format_top10_markdown(ranked: list[MatchResult]) -> str:
    lines = ["## 🏆 Top 潜在接受方匹配结果\n"]
    for i, r in enumerate(ranked, 1):
        lines.append(format_result_markdown(r, i))
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 快捷辅助：从原始数值构建归一化得分
# ─────────────────────────────────────────────

def normalize_ipc_overlap(matched_ipc_count: int, threshold: int = 3) -> float:
    """IPC 重合数 → 0~1"""
    return min(matched_ipc_count / threshold, 1.0)

def normalize_citation(citation_count: int, threshold: int = 50) -> float:
    """被引次数 → 0~1（对数压缩）"""
    if citation_count <= 0:
        return 0.0
    return min(math.log1p(citation_count) / math.log1p(threshold), 1.0)

def normalize_budget(budget_wan: float, threshold: float = 500.0) -> float:
    """预算（万元）→ 0~1"""
    return min(budget_wan / threshold, 1.0)

def normalize_filing_trend(yoy_growth_pct: float, threshold: float = 20.0) -> float:
    """年均申请增长率（%）→ 0~1"""
    return min(max(yoy_growth_pct, 0.0) / threshold, 1.0)

def normalize_family_coverage(country_count: int, threshold: int = 5) -> float:
    """同族覆盖国家数 → 0~1"""
    return min(country_count / threshold, 1.0)

def normalize_recency(days_since_publish: int) -> float:
    """距发布天数 → 0~1（越近越高）"""
    if days_since_publish <= 30:
        return 1.0
    elif days_since_publish <= 90:
        return 0.5
    else:
        return 0.0


# ─────────────────────────────────────────────
# Demo / 单元测试
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # 示例：某企业的评分
    patent = PatentScores(
        ipc_overlap=normalize_ipc_overlap(4),
        keyword_similarity=0.82,
        recent_filing_trend=normalize_filing_trend(25),
        citation_impact=normalize_citation(60),
        family_coverage=normalize_family_coverage(6),
        cross_citation=1.0,
    )
    news = NewsScores(
        collab_intent_news=0.9,
        expansion_news=0.7,
        rd_center_news=0.5,
        gov_collab_news=0.6,
        expo_presence=1.0,
        industry_cert=0.8,
    )
    bid = BidScores(
        keyword_hit=1.0,
        budget_scale=normalize_budget(800),
        winning_history=1.0,
        collab_history=0.5,
        recency_90d=normalize_recency(20),
        repeat_purchase=1.0,
    )

    result = score_company(
        company_name="示例科技有限公司",
        patent=patent,
        news=news,
        bid=bid,
        evidence=[
            "专利CN202310XXXXX.X，IPC: H01M10/0525，被引62次",
            "2024年3月发布招标公告《固态电池生产线技术改造项目》，预算800万元",
            "2024年11月参加上海储能展，展示固态电池样品",
        ],
    )

    print(format_result_markdown(result, 1))
    print(f"总分验证：{result.total_score}/100")
