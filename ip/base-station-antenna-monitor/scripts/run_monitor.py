#!/usr/bin/env python3
"""
基站天线专利监控脚本 v2
面向普罗斯通信技术，监控17家核心企业近一个月基站天线专利动态

变更说明 v2:
1. 分页检索：offset 步进，直到取完全部或达到 retrieval_cap（默认1000）
2. 统计数据基于实际取回的全量去重专利，不使用样本估算
3. 分类时只读取标题、摘要、权要和AI技术三要素，不读取全文
4. 核心技术摘要直接使用专利标题
"""

import json
import sys
import os
import argparse
import time
from datetime import datetime, timedelta
from collections import defaultdict

# ─────────────────────────────────────────────
# 目标企业配置
# ─────────────────────────────────────────────
TARGET_COMPANIES = [
    {"cn": "华为",       "en": "Huawei"},
    {"cn": "康普",       "en": "CommScope"},
    {"cn": "京信",       "en": "Jingxin"},
    {"cn": "爱立信",     "en": "Ericsson"},
    {"cn": "凯瑟琳",     "en": "Kathrein"},
    {"cn": "通宇",       "en": "Tongyu"},
    {"cn": "摩比",       "en": "Mobi"},
    {"cn": "虹信",       "en": "Hengxin"},
    {"cn": "ACE",        "en": "ACE"},
    {"cn": "亨鑫",       "en": "Hengxin Technology"},
    {"cn": "安弗施",     "en": "Amphenol"},
    {"cn": "安费诺",     "en": "Amphenol"},
    {"cn": "恩电开",     "en": "RFS"},
    {"cn": "立讯",       "en": "Luxshare"},
    {"cn": "KMW",        "en": "KMW"},
    {"cn": "Galtronics", "en": "Galtronics"},
    {"cn": "中兴",       "en": "ZTE"},
]

# 所有企业名称列表（用于 assignees 过滤）
ALL_ASSIGNEES = [c["cn"] for c in TARGET_COMPANIES] + [c["en"] for c in TARGET_COMPANIES]

# ─────────────────────────────────────────────
# 技术分支关键词映射（只匹配标题+摘要+权要+AI三要素）
# ─────────────────────────────────────────────
BRANCH_KEYWORDS = {
    "振子": [
        "振子", "辐射单元", "偶极子", "辐射体", "辐射片", "辐射臂",
        "radiating element", "dipole", "radiation unit", "radiator",
    ],
    "天线罩": [
        "天线罩", "radome", "防护罩", "外罩", "保护罩",
        "protective cover", "housing cover",
    ],
    "反射板": [
        "反射板", "反射器", "底板", "地板", "接地板",
        "reflector", "ground plane", "back plate", "backplane", "groundplane",
    ],
}

# 基站天线核心关键词（用于检索查询）
BASE_STATION_KEYWORDS = [
    "基站天线", "阵列天线", "双极化天线", "MIMO天线",
    "base station antenna", "array antenna", "panel antenna",
]

# 高频技术术语（用于关键词统计）
TECH_TERMS = [
    "振子", "天线罩", "反射板", "波束", "馈电", "相位", "阵列",
    "MIMO", "5G", "NR", "辐射", "极化", "增益", "带宽",
    "多频", "宽频", "双极化", "隔离度", "校准", "移相", "波控",
    "巴伦", "寄生层", "无电缆", "通感一体化", "TDD",
]

# ─────────────────────────────────────────────
# 检索配置
# ─────────────────────────────────────────────
PAGE_SIZE = 100          # 每页最多取100条（工具上限）
RETRIEVAL_CAP = 1000     # 默认检索上限，超过则停止并提示
SEARCH_DELAY = 0.3       # 翻页间隔（秒），避免过快请求


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def get_date_range(days: int):
    """返回 (date_from_int, date_to_int) 格式如 20250101"""
    today = datetime.now()
    start = today - timedelta(days=days)
    return int(start.strftime("%Y%m%d")), int(today.strftime("%Y%m%d"))


def classify_branch(title: str, abstract: str, claims: str = "", ai_elements: str = "") -> str:
    """
    根据标题、摘要、权要、AI技术三要素判断技术分支。
    注意：不读取全文（description）。
    """
    text = " ".join([
        title or "",
        abstract or "",
        claims or "",
        ai_elements or "",
    ]).lower()
    matched = []
    for branch, keywords in BRANCH_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                matched.append(branch)
                break
    return "、".join(matched) if matched else "其他"


def deduplicate(patents: list) -> list:
    """按专利号去重，保留首次出现"""
    seen = set()
    result = []
    for p in patents:
        pid = p.get("publication_number") or p.get("patent_id") or p.get("title", "")
        if pid and pid not in seen:
            seen.add(pid)
            result.append(p)
    return result


def extract_keywords_from_patents(patents: list) -> list:
    """从专利标题+摘要统计高频技术关键词"""
    from collections import Counter
    freq = Counter()
    for p in patents:
        # 只用标题和摘要，不用全文
        text = (p.get("title") or "") + " " + (p.get("abstract") or "")
        for term in TECH_TERMS:
            if term in text:
                freq[term] += 1
    return [kw for kw, cnt in freq.most_common(20) if cnt >= 2]


def safe_str(val) -> str:
    if val is None:
        return ""
    if isinstance(val, list):
        return "、".join(str(v) for v in val)
    return str(val)


def normalize_patent(raw: dict) -> dict:
    """
    统一字段名。
    技术概要（summary）直接使用专利标题，不截取摘要。
    分类时使用标题+摘要+权要+AI三要素，不使用全文。
    """
    p = {}
    p["patent_id"]          = raw.get("patent_id") or raw.get("id") or raw.get("pn") or ""
    p["publication_number"] = raw.get("publication_number") or raw.get("pub_num") or p["patent_id"]
    p["title"]              = raw.get("title") or raw.get("name") or ""
    p["assignee"]           = raw.get("assignee") or raw.get("applicant") or raw.get("assignees") or ""
    p["publication_date"]   = raw.get("publication_date") or raw.get("pub_date") or raw.get("published_date") or ""
    p["legal_status"]       = raw.get("legal_status") or raw.get("status") or ""
    p["abstract"]           = raw.get("abstract") or raw.get("summary") or ""

    # 权要和AI技术三要素（如有）
    p["claims"]             = raw.get("claims") or ""
    p["ai_elements"]        = raw.get("ai_elements") or raw.get("tech_elements") or ""

    # 核心技术摘要 = 直接使用专利标题（不截取摘要）
    p["summary"] = p["title"]

    # 技术分支分类（只用标题+摘要+权要+AI三要素，不用全文）
    p["branch"] = classify_branch(
        p["title"], p["abstract"], p["claims"], p["ai_elements"]
    )

    # PatSnap 链接（如有）
    p["url"] = raw.get("url") or raw.get("patent_url") or ""

    return p


# ─────────────────────────────────────────────
# 分页检索逻辑
# ─────────────────────────────────────────────

class PaginatedSearcher:
    """
    封装分页检索逻辑。
    - 每次查询 PAGE_SIZE=100 条
    - 自动翻页直到：offset >= matched_total 或 返回空 或 达到 retrieval_cap
    - 超过 retrieval_cap 时停止并设置 truncated=True
    """

    def __init__(self, search_fn, retrieval_cap: int = RETRIEVAL_CAP):
        self.search_fn = search_fn      # callable: (offset, limit) -> (results, matched_total)
        self.retrieval_cap = retrieval_cap
        self.truncated = False          # 是否因 cap 而截断
        self.matched_total = 0          # 数据库实际命中数
        self.retrieved_count = 0        # 本次实际取回数

    def fetch_all(self) -> list:
        """执行分页检索，返回合并后的全量结果列表"""
        all_results = []
        offset = 0

        while True:
            # 已达 retrieval_cap，停止
            if offset >= self.retrieval_cap:
                self.truncated = True
                print(f"[WARN] 已达 retrieval_cap={self.retrieval_cap}，停止检索。"
                      f"数据库总命中={self.matched_total}，实际取回={len(all_results)}")
                break

            limit = min(PAGE_SIZE, self.retrieval_cap - offset)
            results, matched_total = self.search_fn(offset, limit)
            self.matched_total = matched_total  # 每次更新（以最后一次为准）

            if not results:
                # 返回空，检索完毕
                print(f"[INFO] 第 {offset//PAGE_SIZE + 1} 页返回空，检索完毕。")
                break

            all_results.extend(results)
            print(f"[INFO] 已取回 offset={offset}，本页 {len(results)} 条，"
                  f"累计 {len(all_results)} / {matched_total} 条")

            offset += len(results)

            # 已取完全部
            if matched_total > 0 and offset >= matched_total:
                print(f"[INFO] 全部 {matched_total} 条已取完（检索完整）。")
                break

            # 安全限制：如果本页返回数少于预期，也视为结束
            if len(results) < limit:
                print(f"[INFO] 本页返回数({len(results)}) < limit({limit})，视为最后一页。")
                break

            time.sleep(SEARCH_DELAY)

        self.retrieved_count = len(all_results)
        return all_results


def build_search_fn(mcp_search_tool, keywords, assignees, date_from, date_to, strategy="keyword"):
    """
    构建一个 (offset, limit) -> (results, matched_total) 的检索函数。
    实际调用 MCP patsnap 搜索工具。
    注意：本脚本在 Eureka skill 运行时，搜索通过 Eureka 内部工具调用，
    此处为接口约定，运行时由 Eureka 注入。
    """
    def search_fn(offset: int, limit: int):
        # 实际检索由 Eureka 调用 mcp_patent-search__patsnap_search
        # 参数规范：keywords, filters.assignees, filters.date_from, filters.date_to
        # 注意：topk 对应 limit，offset 需要工具支持
        result = mcp_search_tool(
            search_strategy=strategy,
            keywords=keywords,
            sources=["patent"],
            topk=limit,
            offset=offset,
            filters={
                "assignees": assignees,
                "date_from": date_from,
                "date_to": date_to,
                "date_type": "publication",
            }
        )
        results = result.get("results", [])
        matched_total = result.get("matched_total", 0)
        return results, matched_total

    return search_fn


# ─────────────────────────────────────────────
# HTML 生成
# ─────────────────────────────────────────────

def generate_html(
    patents: list,
    keywords: list,
    date_from: int,
    date_to: int,
    retrieval_stats: dict,
) -> str:
    total = len(patents)
    branch_count = defaultdict(int)
    for p in patents:
        for b in p.get("branch", "其他").split("、"):
            branch_count[b.strip()] += 1

    # 企业统计（真实数据）
    company_count = defaultdict(int)
    for p in patents:
        company_count[safe_str(p.get("assignee"))] += 1

    # 检索完整性提示
    is_truncated = retrieval_stats.get("truncated", False)
    matched_total = retrieval_stats.get("matched_total", total)
    retrieval_cap = retrieval_stats.get("retrieval_cap", RETRIEVAL_CAP)
    coverage_note = ""
    if is_truncated:
        coverage_note = (
            f'<div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;'
            f'padding:12px 18px;margin-bottom:20px;color:#856404;">'
            f'⚠️ <strong>检索未完整</strong>：数据库总命中 <strong>{matched_total}</strong> 件，'
            f'已达检索上限 retrieval_cap={retrieval_cap}，实际取回 <strong>{total}</strong> 件。'
            f'建议缩小时间范围或企业范围，或联系管理员提升检索上限。</div>'
        )
    else:
        coverage_note = (
            f'<div style="background:#d1fae5;border:1px solid #34d399;border-radius:8px;'
            f'padding:12px 18px;margin-bottom:20px;color:#065f46;">'
            f'✅ <strong>检索完整</strong>：数据库总命中 <strong>{matched_total}</strong> 件，'
            f'已全部取回（去重后 <strong>{total}</strong> 件）。</div>'
        )

    # 生成专利行（技术概要直接用标题）
    rows_html = ""
    for i, p in enumerate(patents, 1):
        pub_date = safe_str(p.get("publication_date", ""))
        status = safe_str(p.get("legal_status", ""))
        status_class = (
            "status-active"   if "有效" in status or "active" in status.lower() else
            "status-pending"  if "审" in status or "pending" in status.lower() else
            "status-inactive"
        )
        branch = safe_str(p.get("branch", "其他"))
        branch_tag = ""
        for b in branch.split("、"):
            b = b.strip()
            cls = (
                "tag-vibrator"  if b == "振子"   else
                "tag-radome"    if b == "天线罩" else
                "tag-reflector" if b == "反射板" else
                "tag-other"
            )
            if b:
                branch_tag += f'<span class="branch-tag {cls}">{b}</span>'

        pub_num = safe_str(p.get("publication_number") or p.get("patent_id", ""))
        title   = safe_str(p.get("title", ""))
        assignee = safe_str(p.get("assignee", ""))
        # 核心技术摘要 = 专利标题（直接调用）
        summary = title

        # 专利号链接（如有 url）
        url = safe_str(p.get("url", ""))
        if url:
            pub_num_cell = f'<a href="{url}" target="_blank" style="color:#1a56a0;text-decoration:none;">{pub_num}</a>'
        else:
            pub_num_cell = pub_num

        rows_html += f"""
        <tr>
            <td class="center">{i}</td>
            <td class="mono">{pub_num_cell}</td>
            <td>{title}</td>
            <td class="center">{assignee}</td>
            <td class="center">{pub_date}</td>
            <td class="center"><span class="status-badge {status_class}">{status or '—'}</span></td>
            <td class="summary-cell">{summary}</td>
            <td class="center">{branch_tag}</td>
        </tr>"""

    # 关键词标签
    kw_html = "".join(f'<span class="kw-chip">{kw}</span>' for kw in keywords[:20])

    # 企业分布条形图（真实数据）
    max_cnt = max(company_count.values()) if company_count else 1
    company_bars = ""
    for company, cnt in sorted(company_count.items(), key=lambda x: -x[1])[:17]:
        if not company:
            continue
        pct = int(cnt / max_cnt * 100)
        company_bars += f"""
        <div class="bar-row">
            <div class="bar-label">{company}</div>
            <div class="bar-wrap">
                <div class="bar-fill" style="width:{pct}%"></div>
                <span class="bar-num">{cnt}</span>
            </div>
        </div>"""

    report_date   = datetime.now().strftime("%Y年%m月%d日")
    date_from_str = f"{str(date_from)[:4]}年{str(date_from)[4:6]}月{str(date_from)[6:]}日"
    date_to_str   = f"{str(date_to)[:4]}年{str(date_to)[4:6]}月{str(date_to)[6:]}日"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>基站天线技术专利监控报告</title>
<style>
  :root {{
    --primary: #1a56a0;
    --primary-light: #e8f0fb;
    --accent: #f0932b;
    --green: #27ae60;
    --gray: #6b7280;
    --border: #e5e7eb;
    --bg: #f8fafc;
    --white: #ffffff;
    --text: #1f2937;
    --text-light: #6b7280;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    font-size: 14px;
    line-height: 1.6;
  }}
  .page-wrap {{ max-width: 1400px; margin: 0 auto; padding: 24px 20px 60px; }}

  /* ── 顶部标题区 ── */
  .report-header {{
    background: linear-gradient(135deg, #1a56a0 0%, #0d3d7c 100%);
    color: white;
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
  }}
  .report-header::before {{
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
  }}
  .header-tag {{
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 12px;
    margin-bottom: 12px;
    letter-spacing: 1px;
  }}
  .report-header h1 {{
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: 1px;
  }}
  .header-meta {{
    font-size: 13px;
    opacity: 0.75;
    margin-top: 10px;
  }}
  .header-meta span {{ margin-right: 20px; }}

  /* ── 统计卡片 ── */
  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
  }}
  .stat-card {{
    background: var(--white);
    border-radius: 12px;
    padding: 20px 24px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }}
  .stat-card .label {{
    font-size: 12px;
    color: var(--text-light);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .stat-card .value {{
    font-size: 32px;
    font-weight: 700;
    color: var(--primary);
    line-height: 1;
  }}
  .stat-card .sub {{
    font-size: 12px;
    color: var(--text-light);
    margin-top: 4px;
  }}

  /* ── 区块卡片 ── */
  .section {{
    background: var(--white);
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 24px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }}
  .section-title {{
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--primary-light);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .section-title::before {{
    content: '';
    display: inline-block;
    width: 4px; height: 18px;
    background: var(--primary);
    border-radius: 2px;
  }}

  /* ── 关键词 ── */
  .kw-chip {{
    display: inline-block;
    background: var(--primary-light);
    color: var(--primary);
    border: 1px solid #c3d8f5;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    margin: 4px;
    font-weight: 500;
  }}

  /* ── 企业分布图 ── */
  .bar-row {{
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    gap: 10px;
  }}
  .bar-label {{
    width: 100px;
    text-align: right;
    font-size: 13px;
    color: var(--text-light);
    flex-shrink: 0;
  }}
  .bar-wrap {{
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--bg);
    border-radius: 4px;
    overflow: hidden;
  }}
  .bar-fill {{
    height: 22px;
    background: linear-gradient(90deg, var(--primary) 0%, #4a8fd4 100%);
    border-radius: 0 4px 4px 0;
    min-width: 4px;
  }}
  .bar-num {{
    font-size: 12px;
    color: var(--text-light);
    font-weight: 600;
    white-space: nowrap;
  }}

  /* ── 两列布局 ── */
  .two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 24px;
  }}

  /* ── 专利表格 ── */
  .table-wrap {{ overflow-x: auto; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  thead tr {{
    background: linear-gradient(135deg, #1a56a0, #2563c4);
    color: white;
  }}
  thead th {{
    padding: 12px 12px;
    text-align: left;
    font-weight: 600;
    white-space: nowrap;
  }}
  thead th.center {{ text-align: center; }}
  tbody tr:nth-child(even) {{ background: #fafbfe; }}
  tbody tr:hover {{ background: var(--primary-light); }}
  tbody td {{
    padding: 11px 12px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }}
  td.center {{ text-align: center; }}
  td.mono {{
    font-family: 'SFMono-Regular', Consolas, monospace;
    font-size: 12px;
    color: var(--primary);
  }}
  td.summary-cell {{ font-size: 12px; color: #4b5563; max-width: 280px; }}

  /* ── 状态徽章 ── */
  .status-badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    white-space: nowrap;
  }}
  .status-active   {{ background: #d1fae5; color: #065f46; }}
  .status-pending  {{ background: #fef3c7; color: #92400e; }}
  .status-inactive {{ background: #f3f4f6; color: #6b7280; }}

  /* ── 技术分支标签 ── */
  .branch-tag {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
    margin: 1px;
    white-space: nowrap;
  }}
  .tag-vibrator  {{ background: #ede9fe; color: #5b21b6; }}
  .tag-radome    {{ background: #d1fae5; color: #065f46; }}
  .tag-reflector {{ background: #fed7aa; color: #9a3412; }}
  .tag-other     {{ background: #f3f4f6; color: #6b7280; }}

  /* ── 分支统计 ── */
  .branch-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 6px;
  }}
  .branch-card {{
    border-radius: 10px;
    padding: 16px;
    text-align: center;
  }}
  .bc-vibrator  {{ background: #ede9fe; }}
  .bc-radome    {{ background: #d1fae5; }}
  .bc-reflector {{ background: #fed7aa; }}
  .bc-other     {{ background: #f3f4f6; }}
  .branch-card .bc-num   {{ font-size: 28px; font-weight: 700; }}
  .branch-card .bc-label {{ font-size: 12px; margin-top: 4px; color: var(--text-light); }}
  .bv {{ color: #5b21b6; }}
  .bd {{ color: #065f46; }}
  .br {{ color: #9a3412; }}
  .bo {{ color: #6b7280; }}

  /* ── 页脚 ── */
  .report-footer {{
    text-align: center;
    color: var(--text-light);
    font-size: 12px;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
  }}

  @media (max-width: 900px) {{
    .stat-grid   {{ grid-template-columns: repeat(2,1fr); }}
    .two-col     {{ grid-template-columns: 1fr; }}
    .branch-grid {{ grid-template-columns: repeat(2,1fr); }}
  }}
</style>
</head>
<body>
<div class="page-wrap">

  <!-- 报告标题 -->
  <div class="report-header">
    <div class="header-tag">普罗斯通信技术 · 专利竞争情报</div>
    <h1>📡 基站天线技术专利监控报告</h1>
    <p style="opacity:0.85;margin-top:6px;">监控17家核心竞争对手在基站天线领域的最新专利动态</p>
    <div class="header-meta">
      <span>📅 监控周期：{date_from_str} — {date_to_str}</span>
      <span>🏭 监控企业：17家</span>
      <span>🕐 生成时间：{report_date}</span>
    </div>
  </div>

  <!-- 检索完整性提示 -->
  {coverage_note}

  <!-- 统计卡片（全量真实数据） -->
  <div class="stat-grid">
    <div class="stat-card">
      <div class="label">公开专利总数</div>
      <div class="value">{total}</div>
      <div class="sub">去重后全量</div>
    </div>
    <div class="stat-card">
      <div class="label">涉及企业数</div>
      <div class="value">{len([c for c in company_count if c])}</div>
      <div class="sub">共监控 17 家</div>
    </div>
    <div class="stat-card">
      <div class="label">技术分支覆盖</div>
      <div class="value">{len([b for b in branch_count if b and b != "其他"])}</div>
      <div class="sub">振子 / 天线罩 / 反射板</div>
    </div>
    <div class="stat-card">
      <div class="label">核心技术关键词</div>
      <div class="value">{len(keywords)}</div>
      <div class="sub">高频词汇</div>
    </div>
  </div>

  <!-- 核心技术关键词 + 企业分布 -->
  <div class="two-col">
    <div class="section" style="margin-bottom:0">
      <div class="section-title">核心技术关键词</div>
      <div>{kw_html if kw_html else '<span style="color:#999">暂无高频关键词</span>'}</div>
    </div>
    <div class="section" style="margin-bottom:0">
      <div class="section-title">企业专利分布（真实数据）</div>
      {company_bars if company_bars else '<span style="color:#999">暂无数据</span>'}
    </div>
  </div>
  <div style="margin-bottom:24px"></div>

  <!-- 技术分支统计 -->
  <div class="section">
    <div class="section-title">技术分支分布</div>
    <div class="branch-grid">
      <div class="branch-card bc-vibrator">
        <div class="bc-num bv">{branch_count.get("振子", 0)}</div>
        <div class="bc-label">⚡ 振子</div>
      </div>
      <div class="branch-card bc-radome">
        <div class="bc-num bd">{branch_count.get("天线罩", 0)}</div>
        <div class="bc-label">🔵 天线罩</div>
      </div>
      <div class="branch-card bc-reflector">
        <div class="bc-num br">{branch_count.get("反射板", 0)}</div>
        <div class="bc-label">🟠 反射板</div>
      </div>
      <div class="branch-card bc-other">
        <div class="bc-num bo">{branch_count.get("其他", 0)}</div>
        <div class="bc-label">⚪ 其他</div>
      </div>
    </div>
  </div>

  <!-- 专利清单 -->
  <div class="section">
    <div class="section-title">专利清单（共 {total} 件）</div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th class="center" style="width:44px">#</th>
            <th style="width:140px">专利号</th>
            <th>专利标题</th>
            <th class="center" style="width:90px">申请人</th>
            <th class="center" style="width:100px">公开/公告日</th>
            <th class="center" style="width:80px">法律状态</th>
            <th style="min-width:220px">核心技术摘要</th>
            <th class="center" style="width:100px">技术分支</th>
          </tr>
        </thead>
        <tbody>
          {rows_html if rows_html else '<tr><td colspan="8" style="text-align:center;padding:40px;color:#999">暂无专利数据</td></tr>'}
        </tbody>
      </table>
    </div>
  </div>

  <div class="report-footer">
    <p>本报告由 Eureka 专利监控系统自动生成 · 数据来源：智慧芽 PatSnap · 仅供普罗斯通信技术内部参考</p>
    <p style="margin-top:4px">生成时间：{report_date}</p>
  </div>
</div>
</body>
</html>"""
    return html


# ─────────────────────────────────────────────
# 主逻辑（从 JSON 文件读取已检索数据，或接收注入数据）
# ─────────────────────────────────────────────

def load_patents_from_json(json_path: str) -> tuple:
    """
    从 JSON 文件加载已检索的专利数据。
    支持格式：
      - list of patents
      - {"results": [...], "matched_total": N, "truncated": bool}
    返回 (patents_list, retrieval_stats)
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data, {"matched_total": len(data), "truncated": False, "retrieval_cap": RETRIEVAL_CAP}
    patents = data.get("results", data.get("patents", data.get("data", [])))
    stats = {
        "matched_total": data.get("matched_total", len(patents)),
        "truncated":     data.get("truncated", False),
        "retrieval_cap": data.get("retrieval_cap", RETRIEVAL_CAP),
    }
    return patents, stats


def main():
    parser = argparse.ArgumentParser(description="基站天线专利监控报告生成器 v2")
    parser.add_argument("--days",          type=int,   default=30,            help="往前追溯天数，默认30")
    parser.add_argument("--input",         type=str,   default="",            help="已检索专利JSON文件路径（可选）")
    parser.add_argument("--output",        type=str,   default="report.html", help="输出HTML文件路径")
    parser.add_argument("--retrieval-cap", type=int,   default=RETRIEVAL_CAP, help=f"检索上限，默认{RETRIEVAL_CAP}")
    args = parser.parse_args()

    date_from, date_to = get_date_range(args.days)
    print(f"[INFO] 监控周期: {date_from} → {date_to}")
    print(f"[INFO] 目标企业: {len(TARGET_COMPANIES)} 家")
    print(f"[INFO] retrieval_cap: {args.retrieval_cap}")

    # ── 加载专利数据 ──
    raw_patents = []
    retrieval_stats = {
        "matched_total": 0,
        "truncated": False,
        "retrieval_cap": args.retrieval_cap,
    }

    if args.input and os.path.exists(args.input):
        print(f"[INFO] 从文件加载专利数据: {args.input}")
        raw_patents, retrieval_stats = load_patents_from_json(args.input)
    else:
        # 从环境变量读取（Eureka skill 运行时注入）
        env_data = os.environ.get("PATENT_DATA_JSON", "")
        if env_data:
            try:
                data = json.loads(env_data)
                if isinstance(data, list):
                    raw_patents = data
                    retrieval_stats["matched_total"] = len(data)
                elif isinstance(data, dict):
                    raw_patents = data.get("results", data.get("patents", []))
                    retrieval_stats["matched_total"] = data.get("matched_total", len(raw_patents))
                    retrieval_stats["truncated"]     = data.get("truncated", False)
                print(f"[INFO] 从环境变量加载: {len(raw_patents)} 条，"
                      f"matched_total={retrieval_stats['matched_total']}，"
                      f"truncated={retrieval_stats['truncated']}")
            except Exception as e:
                print(f"[WARN] 解析环境变量数据失败: {e}")

    if not raw_patents:
        print("[WARN] 未找到专利数据，将生成空报告模板")
        retrieval_stats["matched_total"] = 0

    # ── 标准化 + 去重 ──
    patents = [normalize_patent(p) for p in raw_patents]
    before_dedup = len(patents)
    patents = deduplicate(patents)
    print(f"[INFO] 标准化后: {before_dedup} 条，去重后: {len(patents)} 条")

    # 如果 retrieval_stats 中 matched_total 未设置，用去重后数量
    if retrieval_stats["matched_total"] == 0:
        retrieval_stats["matched_total"] = len(patents)

    # ── 提取关键词（基于真实全量数据）──
    keywords = extract_keywords_from_patents(patents)
    print(f"[INFO] 高频关键词({len(keywords)}): {', '.join(keywords[:10])}")

    # ── 生成 HTML ──
    html = generate_html(patents, keywords, date_from, date_to, retrieval_stats)

    output_path = args.output
    out_dir = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", "")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, os.path.basename(args.output))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] HTML报告已生成: {output_path}")

    # 输出统计摘要（全量真实数据）
    branch_count = defaultdict(int)
    for p in patents:
        for b in p.get("branch", "其他").split("、"):
            branch_count[b.strip()] += 1

    print(f"\n{'='*50}")
    print(f"[SUMMARY] 检索状态: {'⚠️ 未完整（已达retrieval_cap）' if retrieval_stats['truncated'] else '✅ 完整'}")
    print(f"[SUMMARY] 数据库总命中: {retrieval_stats['matched_total']} 件")
    print(f"[SUMMARY] 实际取回去重: {len(patents)} 件")
    print(f"[SUMMARY] 技术分支: {dict(branch_count)}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
