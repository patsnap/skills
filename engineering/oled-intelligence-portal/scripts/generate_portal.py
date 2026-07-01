#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用技术领域情报门户生成器
支持任意技术领域关键词，动态生成多页 HTML 情报门户
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# ─── 输入数据从环境变量或 stdin 读取 ───────────────────────────────────────────
def load_portal_data():
    """从 EUREKA_PORTAL_DATA_JSON 环境变量或 stdin 读取 portal_data"""
    data_json = os.environ.get("EUREKA_PORTAL_DATA_JSON")
    if data_json:
        return json.loads(data_json)
    # fallback: read from first argument file
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            return json.load(f)
    raise ValueError("No portal data provided. Set EUREKA_PORTAL_DATA_JSON or pass data file as argument.")

# ─── 颜色主题（按领域关键词自动映射）────────────────────────────────────────────
THEME_MAP = {
    "default":   {"primary": "#1e3a8a", "mid": "#3b82f6", "accent": "#06b6d4", "name": "blue"},
    "电池":      {"primary": "#064e3b", "mid": "#10b981", "accent": "#34d399", "name": "green"},
    "battery":   {"primary": "#064e3b", "mid": "#10b981", "accent": "#34d399", "name": "green"},
    "医药":      {"primary": "#4c1d95", "mid": "#7c3aed", "accent": "#a78bfa", "name": "purple"},
    "药":        {"primary": "#4c1d95", "mid": "#7c3aed", "accent": "#a78bfa", "name": "purple"},
    "glp":       {"primary": "#4c1d95", "mid": "#7c3aed", "accent": "#a78bfa", "name": "purple"},
    "能源":      {"primary": "#78350f", "mid": "#f59e0b", "accent": "#fbbf24", "name": "amber"},
    "solar":     {"primary": "#78350f", "mid": "#f59e0b", "accent": "#fbbf24", "name": "amber"},
    "太阳能":    {"primary": "#78350f", "mid": "#f59e0b", "accent": "#fbbf24", "name": "amber"},
    "半导体":    {"primary": "#1e1b4b", "mid": "#6366f1", "accent": "#818cf8", "name": "indigo"},
    "芯片":      {"primary": "#1e1b4b", "mid": "#6366f1", "accent": "#818cf8", "name": "indigo"},
    "ai":        {"primary": "#0f172a", "mid": "#334155", "accent": "#38bdf8", "name": "slate"},
    "人工智能":  {"primary": "#0f172a", "mid": "#334155", "accent": "#38bdf8", "name": "slate"},
}

def get_theme(keyword: str) -> dict:
    kw_lower = keyword.lower()
    for key, theme in THEME_MAP.items():
        if key in kw_lower:
            return theme
    return THEME_MAP["default"]


# ─── HTML 片段生成函数 ────────────────────────────────────────────────────────

def make_news_cards_html(news_list: list) -> str:
    if not news_list:
        return '<p class="text-gray-400 text-sm">暂无相关新闻</p>'
    cards = []
    for n in news_list[:8]:
        url = n.get("url") or "#"
        title = n.get("title", "（无标题）")
        date = n.get("date", "")
        source = n.get("source", "")
        summary = n.get("summary", n.get("content", ""))[:200]
        cards.append(f"""
        <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all mb-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs text-gray-400">{date}</span>
            <span class="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full">{source}</span>
          </div>
          <a href="{url}" target="_blank" class="text-base font-semibold text-gray-800 hover:text-blue-600 leading-snug block mb-2">{title}</a>
          <p class="text-sm text-gray-500 leading-relaxed">{summary}</p>
        </div>""")
    return "\n".join(cards)


def make_patent_rows_html(patents: list) -> str:
    if not patents:
        return '<tr><td colspan="4" class="text-center text-gray-400 py-4">暂无专利数据</td></tr>'
    rows = []
    for p in patents[:30]:
        title = p.get("title", "")
        applicant = p.get("applicant", "")
        pub_no = p.get("pub_no", "")
        pub_date = p.get("pub_date", "")
        abstract = p.get("abstract", "")[:100]
        url = p.get("url", "#")
        rows.append(f"""
        <tr class="border-b border-gray-100 hover:bg-blue-50 transition-colors">
          <td class="py-3 px-4"><a href="{url}" target="_blank" class="text-blue-700 hover:underline font-medium text-sm">{pub_no}</a></td>
          <td class="py-3 px-4 text-sm text-gray-800">{title}</td>
          <td class="py-3 px-4 text-sm text-gray-600">{applicant}</td>
          <td class="py-3 px-4 text-xs text-gray-400">{pub_date}</td>
        </tr>""")
    return "\n".join(rows)


def make_company_cards_html(companies: list, keyword: str, theme: dict) -> str:
    cards = []
    for c in companies:
        slug = c.get("slug", "")
        name_cn = c.get("name_cn", "")
        name_en = c.get("name_en", "")
        news_count = len(c.get("news", []))
        news_preview = c.get("news", [{}])[0].get("title", "暂无动态") if c.get("news") else "暂无动态"
        cards.append(f"""
        <div onclick="window.location='{slug}.html'"
             class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 cursor-pointer
                    hover:shadow-xl hover:-translate-y-2 transition-all duration-300
                    border-l-4" style="border-left-color:{theme['mid']}">
          <div class="flex items-start justify-between mb-3">
            <div>
              <h3 class="text-lg font-bold text-gray-800">{name_cn}</h3>
              <p class="text-xs text-gray-400">{name_en}</p>
            </div>
            <span class="text-xs font-medium px-2 py-1 rounded-full text-white"
                  style="background:{theme['mid']}">{news_count} 条动态</span>
          </div>
          <p class="text-sm text-gray-500 leading-relaxed line-clamp-2">{news_preview}</p>
        </div>""")
    return "\n".join(cards)


def make_tech_tag_cards_html(tech_tags: list, theme: dict) -> str:
    cards = []
    for t in tech_tags:
        slug = t.get("slug", "")
        name_cn = t.get("name_cn", "")
        name_en = t.get("name_en", "")
        desc = t.get("description", "")
        news_count = len(t.get("news", []))
        cards.append(f"""
        <div onclick="window.location='tech-{slug}.html'"
             class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 cursor-pointer
                    hover:shadow-xl hover:-translate-y-2 transition-all duration-300">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-bold text-gray-800">{name_cn}</span>
            <span class="text-xs px-2 py-0.5 rounded-full font-medium"
                  style="background:{theme['accent']}22;color:{theme['mid']}">{name_en}</span>
          </div>
          <p class="text-xs text-gray-500 mb-3 leading-relaxed">{desc}</p>
          <div class="text-xs text-gray-400">{news_count} 条相关新闻</div>
        </div>""")
    return "\n".join(cards)


def make_events_html(events: list) -> str:
    if not events:
        return '<p class="text-gray-400 text-sm">暂无重大事件</p>'
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
    items = []
    for i, e in enumerate(events[:10]):
        color = colors[i % len(colors)]
        title = e.get("title", "")
        date = e.get("date", "")
        summary = e.get("summary", "")[:200]
        url = e.get("url") or "#"
        items.append(f"""
        <div class="flex gap-4 mb-6">
          <div class="flex-shrink-0 w-1 rounded-full" style="background:{color}"></div>
          <div class="flex-1">
            <div class="text-xs text-gray-400 mb-1">{date}</div>
            <a href="{url}" target="_blank"
               class="text-base font-semibold text-gray-800 hover:text-blue-600 block mb-1">{title}</a>
            <p class="text-sm text-gray-500 leading-relaxed">{summary}</p>
          </div>
        </div>""")
    return "\n".join(items)


# ─── 页面生成 ─────────────────────────────────────────────────────────────────

def generate_index(data: dict, theme: dict, out_dir: Path):
    keyword = data["keyword"]
    date_range = data.get("date_range", "")
    stats = data.get("stats", {})
    companies = data.get("companies", [])
    tech_tags = data.get("tech_tags", [])
    events = data.get("major_events", [])
    patents = data.get("patents", [])

    company_cards = make_company_cards_html(companies, keyword, theme)
    tech_cards = make_tech_tag_cards_html(tech_tags, theme)
    events_html = make_events_html(events)
    patent_rows = make_patent_rows_html(patents[:5])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{keyword} 技术情报门户</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  body {{ font-family: 'Inter', 'Microsoft YaHei Light', sans-serif; }}
  .gradient-hero {{ background: linear-gradient(135deg, {theme['primary']}, {theme['mid']}, {theme['accent']}); }}
  .stat-card {{ backdrop-filter: blur(10px); background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.2); }}
</style>
</head>
<body class="bg-gray-50">

<!-- Hero -->
<section class="gradient-hero text-white py-20 px-8">
  <div class="max-w-6xl mx-auto">
    <div class="mb-2 text-sm opacity-70">📡 技术情报简报门户</div>
    <h1 class="text-5xl font-bold mb-3">{keyword} 技术情报</h1>
    <p class="text-lg opacity-80 mb-8">覆盖周期：{date_range} &nbsp;|&nbsp; 由 Eureka × 智慧芽 自动生成</p>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="stat-card rounded-2xl p-5 text-center">
        <div class="text-3xl font-bold">{stats.get('total_news', 0)}</div>
        <div class="text-sm opacity-80 mt-1">条新闻动态</div>
      </div>
      <div class="stat-card rounded-2xl p-5 text-center">
        <div class="text-3xl font-bold">{stats.get('total_patents', 0)}</div>
        <div class="text-sm opacity-80 mt-1">件相关专利</div>
      </div>
      <div class="stat-card rounded-2xl p-5 text-center">
        <div class="text-3xl font-bold">{stats.get('total_companies', 0)}</div>
        <div class="text-sm opacity-80 mt-1">家监控企业</div>
      </div>
      <div class="stat-card rounded-2xl p-5 text-center">
        <div class="text-3xl font-bold">{stats.get('total_tech_tags', 0)}</div>
        <div class="text-sm opacity-80 mt-1">个技术分支</div>
      </div>
    </div>
  </div>
</section>

<!-- Navigation -->
<nav class="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-100">
  <div class="max-w-6xl mx-auto px-8 py-3 flex gap-6 text-sm font-medium text-gray-600">
    <a href="#companies" class="hover:text-blue-600">🏢 企业动态</a>
    <a href="#tech" class="hover:text-blue-600">🔬 技术分支</a>
    <a href="#events" class="hover:text-blue-600">📰 重大事件</a>
    <a href="#patents" class="hover:text-blue-600">📋 专利速览</a>
  </div>
</nav>

<!-- Companies -->
<section id="companies" class="max-w-6xl mx-auto px-8 py-14">
  <div class="flex items-center justify-between mb-8">
    <div>
      <h2 class="text-2xl font-bold text-gray-800">🏢 企业动态监控</h2>
      <p class="text-gray-400 text-sm mt-1">点击企业卡片查看详细新闻</p>
    </div>
    <span class="text-xs text-gray-400 bg-gray-100 px-3 py-1 rounded-full">{stats.get('total_companies', 0)} 家企业</span>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
    {company_cards}
  </div>
</section>

<!-- Tech Tags -->
<section id="tech" class="bg-gray-100 py-14">
  <div class="max-w-6xl mx-auto px-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">🔬 技术分支追踪</h2>
        <p class="text-gray-400 text-sm mt-1">点击技术标签查看相关动态</p>
      </div>
      <span class="text-xs text-gray-400 bg-white px-3 py-1 rounded-full">{stats.get('total_tech_tags', 0)} 个分支</span>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {tech_cards}
    </div>
  </div>
</section>

<!-- Events -->
<section id="events" class="max-w-6xl mx-auto px-8 py-14">
  <h2 class="text-2xl font-bold text-gray-800 mb-8">📰 重大事件时间轴</h2>
  <div class="max-w-3xl">
    {events_html}
  </div>
</section>

<!-- Patents -->
<section id="patents" class="bg-gray-100 py-14">
  <div class="max-w-6xl mx-auto px-8">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-800">📋 专利速览</h2>
      <a href="patents.html" class="text-sm text-blue-600 hover:underline font-medium">查看全部 {stats.get('total_patents', 0)} 件专利 →</a>
    </div>
    <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="py-3 px-4 text-left">公开号</th>
            <th class="py-3 px-4 text-left">标题</th>
            <th class="py-3 px-4 text-left">申请人</th>
            <th class="py-3 px-4 text-left">公开日</th>
          </tr>
        </thead>
        <tbody>
          {patent_rows}
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- Footer -->
<footer class="text-center py-8 text-xs text-gray-400 border-t border-gray-100 mt-8">
  <p>本门户由 <strong>Eureka × 智慧芽</strong> 自动生成 &nbsp;|&nbsp; 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
  <p class="mt-1">新闻数据来源：智慧芽新闻检索 &nbsp;|&nbsp; 专利数据来源：智慧芽专利数据库</p>
</footer>

</body>
</html>"""

    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"✅ index.html generated")


def generate_company_page(company: dict, keyword: str, theme: dict, out_dir: Path):
    slug = company.get("slug", "")
    name_cn = company.get("name_cn", "")
    name_en = company.get("name_en", "")
    news_html = make_news_cards_html(company.get("news", []))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name_cn} — {keyword} 情报</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>body {{ font-family: 'Inter','Microsoft YaHei Light',sans-serif; }}</style>
</head>
<body class="bg-gray-50">
<div class="min-h-screen" style="background:linear-gradient(135deg,{theme['primary']},{theme['mid']},30%,{theme['accent']})">
  <div class="px-8 py-6">
    <a href="index.html" class="text-white/70 hover:text-white text-sm">← 返回门户首页</a>
  </div>
  <div class="px-8 pb-12">
    <h1 class="text-4xl font-bold text-white mb-1">{name_cn}</h1>
    <p class="text-white/60 text-lg">{name_en} · {keyword} 领域动态</p>
  </div>
</div>
<div class="max-w-4xl mx-auto px-8 -mt-6 pb-16">
  <div class="bg-gray-50 rounded-3xl p-8">
    <h2 class="text-lg font-semibold text-gray-700 mb-6">最新动态 ({len(company.get('news', []))} 条)</h2>
    {news_html}
  </div>
</div>
</body>
</html>"""

    (out_dir / f"{slug}.html").write_text(html, encoding="utf-8")
    print(f"✅ {slug}.html generated")


def generate_tech_page(tag: dict, keyword: str, theme: dict, out_dir: Path):
    slug = tag.get("slug", "")
    name_cn = tag.get("name_cn", "")
    name_en = tag.get("name_en", "")
    desc = tag.get("description", "")
    news_html = make_news_cards_html(tag.get("news", []))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name_cn} — {keyword} 技术情报</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>body {{ font-family: 'Inter','Microsoft YaHei Light',sans-serif; }}</style>
</head>
<body class="bg-gray-50">
<div style="background:linear-gradient(135deg,{theme['accent']},{theme['mid']})">
  <div class="px-8 py-6">
    <a href="index.html" class="text-white/70 hover:text-white text-sm">← 返回门户首页</a>
  </div>
  <div class="px-8 pb-12">
    <h1 class="text-4xl font-bold text-white mb-1">{name_cn}</h1>
    <p class="text-white/70 text-lg">{name_en}</p>
    <p class="text-white/60 text-sm mt-3 max-w-2xl">{desc}</p>
  </div>
</div>
<div class="max-w-4xl mx-auto px-8 -mt-6 pb-16">
  <div class="bg-gray-50 rounded-3xl p-8">
    <h2 class="text-lg font-semibold text-gray-700 mb-6">技术动态 ({len(tag.get('news', []))} 条)</h2>
    {news_html}
  </div>
</div>
</body>
</html>"""

    (out_dir / f"tech-{slug}.html").write_text(html, encoding="utf-8")
    print(f"✅ tech-{slug}.html generated")


def generate_patents_page(data: dict, theme: dict, out_dir: Path):
    keyword = data["keyword"]
    patents = data.get("patents", [])
    patent_rows = make_patent_rows_html(patents)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>专利汇总 — {keyword} 情报门户</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>body {{ font-family: 'Inter','Microsoft YaHei Light',sans-serif; }}</style>
</head>
<body class="bg-gray-50">
<div style="background:linear-gradient(135deg,#4c1d95,#7c3aed,#a78bfa)" class="px-8 py-12">
  <a href="index.html" class="text-white/70 hover:text-white text-sm block mb-6">← 返回门户首页</a>
  <h1 class="text-4xl font-bold text-white mb-2">📋 专利汇总</h1>
  <p class="text-white/70">{keyword} 领域 · 共 {len(patents)} 件专利</p>
</div>
<div class="max-w-6xl mx-auto px-8 py-10">
  <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
    <table class="w-full">
      <thead class="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-100">
        <tr>
          <th class="py-3 px-4 text-left">公开号</th>
          <th class="py-3 px-4 text-left">标题</th>
          <th class="py-3 px-4 text-left">申请人</th>
          <th class="py-3 px-4 text-left">公开日</th>
        </tr>
      </thead>
      <tbody>
        {patent_rows}
      </tbody>
    </table>
  </div>
</div>
</body>
</html>"""

    (out_dir / "patents.html").write_text(html, encoding="utf-8")
    print(f"✅ patents.html generated")


# ─── 主函数 ───────────────────────────────────────────────────────────────────

def main():
    data = load_portal_data()
    keyword = data.get("keyword", "未知领域")
    theme = get_theme(keyword)

    # 输出目录
    output_dir = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", f"{keyword}-portal")
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 开始生成 [{keyword}] 情报门户 → {out_dir}")
    print(f"🎨 主题色：{theme['name']}")

    # 生成各页面
    generate_index(data, theme, out_dir)

    for company in data.get("companies", []):
        generate_company_page(company, keyword, theme, out_dir)

    for tag in data.get("tech_tags", []):
        generate_tech_page(tag, keyword, theme, out_dir)

    generate_patents_page(data, theme, out_dir)

    # 输出摘要
    total_files = 2 + len(data.get("companies", [])) + len(data.get("tech_tags", []))
    print(f"\n🎉 生成完成！共 {total_files} 个 HTML 文件")
    print(f"📂 输出目录：{out_dir.resolve()}")
    print(f"🌐 请在浏览器中打开：{out_dir.resolve() / 'index.html'}")

    # 机器可读摘要（供 Eureka 解析）
    summary = {
        "success": True,
        "output_dir": str(out_dir.resolve()),
        "index_html": str((out_dir / "index.html").resolve()),
        "total_files": total_files,
        "keyword": keyword,
        "stats": data.get("stats", {})
    }
    print("\n__EUREKA_SUMMARY__")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
