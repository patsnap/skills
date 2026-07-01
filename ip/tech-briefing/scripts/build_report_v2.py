#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技术简报 V2 HTML 生成器。

依赖同目录下的 v2_css.py 和 v2_data.py。
用法:
    python build_report_v2.py [输出路径]
若未指定输出路径，默认写入 ~/Documents/tech_briefings/tech_briefing_v2_<时间戳>.html
"""
import html
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
# CWD 优先：允许 v2_data.py 放在工作目录 (~/Documents/tech_briefings)，
# 脚本本体放在 Skill 目录中保持不变。
sys.path.insert(0, os.getcwd())
sys.path.insert(0, HERE)

try:
    import v2_css
except ImportError as exc:
    print(f"ImportError: {exc}\n请确认 v2_css.py 与本脚本在同一目录。", file=sys.stderr)
    sys.exit(2)

try:
    import v2_data as D
except ImportError as exc:
    print(
        f"ImportError: {exc}\n请在当前工作目录创建 v2_data.py（可参考 "
        f"{os.path.join(HERE, 'v2_data.sample.py')}）。",
        file=sys.stderr,
    )
    sys.exit(2)


def g(name, default):
    return getattr(D, name, default)


def e(s):
    return html.escape(str(s or ""))


# ---------- 渲染组件 ----------

def render_nav(sub_techs):
    items = [
        '<a href="#overview">技术全景</a>',
        '<a href="#overview-trend" class="sub">└ 技术趋势</a>',
        '<a href="#overview-wordcloud" class="sub">└ 技术主题</a>',
        '<a href="#summary">总结与分析</a>',
        '<a href="#news">技术新闻</a>',
        '<a href="#patents">专利动态</a>',
        '<a href="#literature">学术文献</a>',
        '<a href="#subtechs">关注的子技术</a>',
    ]
    for st in sub_techs:
        name = st.get("name", "")
        n = len(st.get("patents", []))
        items.append(f'<a href="#st-{e(name)}" class="sub">└ {e(name)} ({n})</a>')
    return '<nav class="nav-panel">' + "\n".join(items) + "</nav>"


def render_trend(trend):
    months = trend.get("months", [])
    series = trend.get("series", {})
    if not months or not series:
        return '<p class="empty">暂无趋势数据</p>'
    w, h, pad = 720, 240, 40
    max_v = max((max(v) if v else 0) for v in series.values()) or 1
    step_x = (w - 2 * pad) / max(len(months) - 1, 1)
    colors = ["#1b5cd8", "#ff7d3f", "#2d8b3b", "#c23434", "#8b5cf6", "#0ea5e9"]
    parts = []
    for i, (name, vals) in enumerate(series.items()):
        color = colors[i % len(colors)]
        pts = " ".join(
            f"{pad + j * step_x:.1f},{h - pad - (v / max_v) * (h - 2 * pad):.1f}"
            for j, v in enumerate(vals)
        )
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/>')
        parts.append(
            f'<text x="{w - pad - 80}" y="{pad + 20 + i * 18}" '
            f'fill="{color}" font-size="13">● {e(name)}</text>'
        )
    x_labels = "\n".join(
        f'<text x="{pad + j * step_x:.1f}" y="{h - pad + 18}" '
        f'font-size="11" fill="#666" text-anchor="middle">{e(m)}</text>'
        for j, m in enumerate(months)
    )
    return (
        f'<svg class="trend-svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">'
        f'<line x1="{pad}" y1="{h - pad}" x2="{w - pad}" y2="{h - pad}" stroke="#ddd"/>'
        f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h - pad}" stroke="#ddd"/>'
        f'{" ".join(parts)}{x_labels}</svg>'
    )


def render_bars(totals):
    if not totals:
        return ""
    max_v = max(totals.values()) or 1
    bars = []
    for name, v in totals.items():
        height = int((v / max_v) * 180)
        bars.append(
            f'<div class="bar"><div class="count">{v}</div>'
            f'<div class="fill" style="height:{height}px"></div>'
            f'<div class="label">{e(name)}</div></div>'
        )
    return '<div class="bar-chart">' + "\n".join(bars) + "</div>"


def render_wordcloud(words):
    if not words:
        return '<p class="empty">暂无词云数据</p>'
    spans = []
    for w in words:
        spans.append(
            f'<span style="font-size:{w.get("size", 18)}px;'
            f'color:{w.get("color", "#1b5cd8")}" '
            f'title="专利数量: {w.get("count", 0)}">{e(w.get("word", ""))}</span>'
        )
    return '<div class="word-cloud">' + " ".join(spans) + "</div>"


def _status_class(status):
    s = str(status or "")
    if any(k in s for k in ("授权", "valid", "Granted")):
        return "status-valid"
    if any(k in s for k in ("失效", "expired", "Expired", "Abandoned")):
        return "status-expired"
    return "status-pending"


def render_patent_card(p):
    pid = p.get("pid") or ""
    link = (
        f"https://analytics.zhihuiya.com/patent-view/abst?_type=query"
        f"&source_type=search_result&rows=20&patentId={pid}"
        if pid else "#"
    )
    fields = []
    for key, cls, label in (
        ("problem", "problem", "问题"),
        ("approach", "approach", "手段"),
        ("effect", "effect", "功效"),
    ):
        v = p.get(key)
        if v:
            fields.append(
                f'<div class="tech-field"><span class="tag {cls}">{label}</span>{e(v)}</div>'
            )
    return (
        f'<div class="patent-card">'
        f'<a class="pn" href="{link}" target="_blank">{e(p.get("pn", ""))}</a>'
        f'<span class="tag {_status_class(p.get("status"))}">{e(p.get("status")) or "—"}</span>'
        f'<div class="meta">{e(p.get("title", ""))} · {e(p.get("assignee", ""))} · '
        f'{e(p.get("pbdt", ""))}</div>'
        f'{"".join(fields)}</div>'
    )


def render_patents_section(by_company):
    if not by_company:
        return '<p class="empty">暂无专利数据</p>'
    blocks = []
    for company, patents in by_company.items():
        cards = "\n".join(render_patent_card(p) for p in patents)
        blocks.append(
            f'<div class="accordion-group">'
            f'<div class="accordion-header" onclick="toggleAccordion(this)">'
            f'<span>{e(company)}（{len(patents)}件）</span><span class="caret">▶</span>'
            f'</div><div class="accordion-body">{cards}</div></div>'
        )
    return "\n".join(blocks)


def render_news(items):
    if not items:
        return '<p class="empty">暂未检索到相关行业新闻</p>'
    return "\n".join(
        f'<div class="news-card">'
        f'<a href="{e(n.get("url", "#"))}" target="_blank">{e(n.get("title", ""))}</a>'
        f'<div class="desc">{e(n.get("desc", ""))}</div>'
        f'<div class="source">{e(n.get("source", ""))}</div></div>'
        for n in items
    )


def render_literature(items):
    if not items:
        return '<p class="empty">暂无相关文献</p>'
    parts = []
    for lit in items:
        doi = lit.get("doi", "")
        url = f"https://doi.org/{doi}" if doi else lit.get("url", "")
        title = e(lit.get("title", ""))
        title_html = f'<a href="{e(url)}" target="_blank">{title}</a>' if url else title
        parts.append(
            f'<div class="lit-item">{title_html}'
            f'<div class="meta">{e(lit.get("authors", ""))} · '
            f'{e(lit.get("journal", ""))} · {e(lit.get("year", ""))}</div>'
            f'<div>{e(lit.get("summary", ""))}</div></div>'
        )
    return "\n".join(parts)


def render_subtechs(sub_techs, patent_index):
    if not sub_techs:
        return '<p class="empty">暂无子技术分组</p>'
    blocks = []
    for st in sub_techs:
        name = st.get("name", "")
        pns = st.get("patents", [])
        cards = "\n".join(
            render_patent_card(patent_index[pn]) for pn in pns if pn in patent_index
        )
        blocks.append(
            f'<div class="subtech" id="st-{e(name)}">'
            f'<div class="subtech-header" onclick="toggleSubtech(this)">'
            f'<span>{e(name)}（{len(pns)}组技术）</span><span>▶</span>'
            f'</div><div class="subtech-body">{cards}</div></div>'
        )
    return "\n".join(blocks)


# ---------- 主流程 ----------

def build():
    title = g("TITLE", "技术简报")
    time_range = g("TIME_RANGE", "")
    summary = g("SUMMARY", "暂无分析。")
    patent_totals = g("PATENT_TOTAL_BY_COMPANY", {})
    trend = g("TREND_SERIES", {})
    word_cloud = g("WORD_CLOUD", [])
    sub_techs = g("SUB_TECHS", [])
    patents_by_company = g("PATENTS_BY_COMPANY", {})
    literature = g("LITERATURE", [])
    news = g("NEWS", [])
    patent_index = {p.get("pn"): p for p in g("PATENTS", [])}

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="UTF-8">
<title>{e(title)}</title>
<style>{v2_css.CSS}</style>
</head><body>

<header class="report-header">
  <div class="report-title">{e(title)}</div>
  <div class="report-badge">时间范围：{e(time_range)}</div>
</header>

{render_nav(sub_techs)}

<section id="overview"><h2>技术全景</h2>
  <h3 id="overview-trend">技术趋势</h3>
  {render_trend(trend)}
  {render_bars(patent_totals)}
  <h3 id="overview-wordcloud">技术主题词云</h3>
  {render_wordcloud(word_cloud)}
</section>

<section id="summary"><h2>总结与分析</h2>
  <div>{summary}</div>
</section>

<section id="news"><h2>技术新闻</h2>
  {render_news(news)}
</section>

<section id="patents"><h2>专利动态</h2>
  {render_patents_section(patents_by_company)}
</section>

<section id="literature"><h2>学术文献</h2>
  {render_literature(literature)}
</section>

<section id="subtechs"><h2>关注的子技术</h2>
  {render_subtechs(sub_techs, patent_index)}
</section>

<script>
function toggleAccordion(el) {{
  const body = el.nextElementSibling;
  const open = body.classList.toggle("open");
  el.setAttribute("aria-expanded", open);
}}
function toggleSubtech(el) {{
  el.nextElementSibling.classList.toggle("open");
}}
</script>

</body></html>"""


def main():
    if len(sys.argv) >= 2:
        out = sys.argv[1]
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = os.path.expanduser("~/Documents/tech_briefings")
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, f"tech_briefing_v2_{stamp}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build())
    print(out)


if __name__ == "__main__":
    main()
