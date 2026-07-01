"""
report_generator.py — 科技成果转移转化供需匹配报告生成器 v3.0
生成自包含 HTML 报告，内嵌 ECharts 可视化
"""

from __future__ import annotations
import json
from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────
# HTML 报告生成主函数
# ─────────────────────────────────────────────

def generate_html_report(
    tech_info: dict,
    advancement_scores: dict,
    patent_value: dict,
    top_companies: list[dict],
    report_date: Optional[str] = None,
) -> str:
    """
    生成完整的科技成果供需匹配 HTML 报告

    参数:
    - tech_info: 技术内容分析结果
        {source, topic, summary, advantages, ip_status, scenarios, trl, trl_level}
    - advancement_scores: 先进性评估结果
        {scores: {factor: {score, weight, comment}}, total, grade, grade_label}
    - patent_value: 专利价值评估结果
        {tech_value, market_value, legal_value, strategic_value, estimated_value_range}
    - top_companies: Top-10 潜在接受方列表
        [{company_name, total_score, patent_score, news_score, bid_score,
          grade, grade_label, action, evidence: []}]
    - report_date: 报告日期，默认今天

    返回: 完整 HTML 字符串
    """
    if report_date is None:
        report_date = datetime.now().strftime("%Y年%m月%d日")

    topic = tech_info.get("topic", "未命名技术")
    source = tech_info.get("source", "—")
    trl = tech_info.get("trl", "—")
    trl_level = tech_info.get("trl_level", "—")

    # ── 雷达图数据 ──
    adv_scores = advancement_scores.get("scores", {})
    radar_data = _build_radar_data(adv_scores)
    adv_total = advancement_scores.get("total", 0)
    adv_grade = advancement_scores.get("grade_label", "—")

    # ── 接受方柱状图数据 ──
    companies_chart = _build_companies_chart(top_companies)

    # ── 三维度堆叠图数据 ──
    stacked_chart = _build_stacked_chart(top_companies)

    # ── 专利价值数据 ──
    value_range = patent_value.get("estimated_value_range", "—")
    pv_tech = patent_value.get("tech_value", {})
    pv_market = patent_value.get("market_value", {})
    pv_legal = patent_value.get("legal_value", {})
    pv_strat = patent_value.get("strategic_value", {})

    # ── 公司卡片 HTML ──
    company_cards_html = _build_company_cards(top_companies)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>科技成果供需匹配报告 — {topic}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
  :root {{
    --primary: #1a56db;
    --primary-light: #e8f0fe;
    --accent: #0ea5e9;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --purple: #8b5cf6;
    --bg: #f0f4f8;
    --card: #ffffff;
    --text: #1e293b;
    --text-sub: #64748b;
    --border: #e2e8f0;
    --shadow: 0 4px 24px rgba(0,0,0,0.08);
    --radius: 16px;
    --radius-sm: 10px;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
  }}

  /* ── 顶部封面 ── */
  .cover {{
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #1a56db 100%);
    color: white;
    padding: 56px 48px 48px;
    position: relative;
    overflow: hidden;
  }}
  .cover::before {{
    content: "";
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
  }}
  .cover::after {{
    content: "";
    position: absolute;
    bottom: -40px; left: 40%;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(14,165,233,0.12);
  }}
  .cover-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 12px;
    letter-spacing: 1px;
    margin-bottom: 20px;
  }}
  .cover h1 {{
    font-size: 32px;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
  }}
  .cover-sub {{
    font-size: 15px;
    opacity: 0.75;
    margin-bottom: 32px;
  }}
  .cover-meta {{
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
  }}
  .cover-meta-item {{
    display: flex;
    flex-direction: column;
  }}
  .cover-meta-item .label {{ font-size: 11px; opacity: 0.6; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }}
  .cover-meta-item .value {{ font-size: 16px; font-weight: 600; }}

  /* ── 主内容布局 ── */
  .main {{ max-width: 1200px; margin: 0 auto; padding: 32px 24px 64px; }}

  /* ── 章节标题 ── */
  .section-title {{
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    margin: 40px 0 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .section-title::before {{
    content: "";
    display: block;
    width: 4px; height: 20px;
    background: var(--primary);
    border-radius: 2px;
  }}

  /* ── 卡片 ── */
  .card {{
    background: var(--card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 24px;
    margin-bottom: 20px;
  }}

  /* ── 技术摘要卡片 ── */
  .tech-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 20px;
  }}
  .tech-item {{ padding: 16px; background: var(--primary-light); border-radius: var(--radius-sm); }}
  .tech-item .k {{ font-size: 11px; color: var(--primary); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }}
  .tech-item .v {{ font-size: 14px; color: var(--text); font-weight: 500; line-height: 1.5; }}

  .trl-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
  }}

  /* ── 先进性雷达 ── */
  .chart-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
  }}
  @media (max-width: 768px) {{ .chart-row {{ grid-template-columns: 1fr; }} }}
  .chart-container {{ height: 340px; }}

  /* ── 先进性得分表 ── */
  .score-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  .score-table th {{ background: var(--primary); color: white; padding: 10px 14px; text-align: left; font-weight: 600; }}
  .score-table th:first-child {{ border-radius: 8px 0 0 0; }}
  .score-table th:last-child {{ border-radius: 0 8px 0 0; }}
  .score-table td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); }}
  .score-table tr:last-child td {{ border-bottom: none; }}
  .score-table tr:hover td {{ background: var(--primary-light); }}
  .progress-bar {{
    height: 6px; background: var(--border); border-radius: 3px; overflow: hidden;
    width: 120px; display: inline-block; vertical-align: middle; margin-right: 8px;
  }}
  .progress-fill {{ height: 100%; border-radius: 3px; background: linear-gradient(90deg, var(--primary), var(--accent)); }}

  /* ── 专利价值四象限 ── */
  .quadrant-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}
  .quadrant-card {{
    border-radius: var(--radius-sm);
    padding: 20px;
    border: 1px solid var(--border);
  }}
  .q-tech {{ border-top: 3px solid var(--primary); }}
  .q-market {{ border-top: 3px solid var(--accent); }}
  .q-legal {{ border-top: 3px solid var(--success); }}
  .q-strat {{ border-top: 3px solid var(--purple); }}
  .quadrant-card .q-title {{ font-weight: 700; margin-bottom: 8px; font-size: 14px; }}
  .quadrant-card ul {{ padding-left: 16px; font-size: 13px; color: var(--text-sub); line-height: 2; }}
  .value-highlight {{
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #f0f4ff, #e8f0fe);
    border-radius: var(--radius-sm);
    margin-top: 16px;
  }}
  .value-highlight .val {{ font-size: 28px; font-weight: 800; color: var(--primary); }}
  .value-highlight .sub {{ font-size: 12px; color: var(--text-sub); margin-top: 4px; }}

  /* ── 接受方图表 ── */
  .companies-chart {{ height: 360px; }}
  .stacked-chart {{ height: 360px; }}

  /* ── 接受方卡片列表 ── */
  .company-list {{ display: flex; flex-direction: column; gap: 16px; }}
  .company-card {{
    background: var(--card);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    padding: 20px;
    display: grid;
    grid-template-columns: 48px 1fr auto;
    gap: 16px;
    align-items: start;
    transition: box-shadow 0.2s;
  }}
  .company-card:hover {{ box-shadow: 0 8px 32px rgba(26,86,219,0.12); border-color: var(--primary); }}
  .rank-badge {{
    width: 48px; height: 48px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 800;
    color: white;
    flex-shrink: 0;
  }}
  .rank-1 {{ background: linear-gradient(135deg, #f59e0b, #d97706); }}
  .rank-2 {{ background: linear-gradient(135deg, #94a3b8, #64748b); }}
  .rank-3 {{ background: linear-gradient(135deg, #cd7c3e, #a05c28); }}
  .rank-other {{ background: linear-gradient(135deg, var(--primary), var(--accent)); }}
  .company-name {{ font-size: 16px; font-weight: 700; margin-bottom: 8px; }}
  .company-tags {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }}
  .tag {{
    padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 500;
  }}
  .tag-patent {{ background: #ede9fe; color: #7c3aed; }}
  .tag-news {{ background: #fef3c7; color: #b45309; }}
  .tag-bid {{ background: #d1fae5; color: #065f46; }}
  .evidence-list {{ font-size: 12px; color: var(--text-sub); line-height: 1.8; }}
  .evidence-list li {{ list-style: none; padding-left: 14px; position: relative; }}
  .evidence-list li::before {{ content: "›"; position: absolute; left: 0; color: var(--primary); font-weight: 700; }}
  .score-pill {{
    background: var(--primary);
    color: white;
    padding: 8px 16px;
    border-radius: 24px;
    text-align: center;
    min-width: 80px;
    flex-shrink: 0;
  }}
  .score-pill .num {{ font-size: 24px; font-weight: 800; display: block; }}
  .score-pill .sub {{ font-size: 10px; opacity: 0.8; }}

  .grade-stars {{ font-size: 13px; margin-bottom: 4px; }}
  .action-tag {{
    display: inline-block;
    background: var(--success);
    color: white;
    padding: 3px 10px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 600;
    margin-top: 4px;
  }}

  /* ── 页脚 ── */
  .footer {{
    text-align: center;
    padding: 32px;
    color: var(--text-sub);
    font-size: 12px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
  }}
  .footer strong {{ color: var(--primary); }}
</style>
</head>
<body>

<!-- ══ 封面 ══ -->
<div class="cover">
  <div class="cover-badge">🔬 科技成果转移转化 · 供需匹配分析报告</div>
  <h1>{topic}</h1>
  <p class="cover-sub">基于专利信息 · 公开新闻 · 招投标数据的三维度智能匹配</p>
  <div class="cover-meta">
    <div class="cover-meta-item">
      <span class="label">技术来源</span>
      <span class="value">{source}</span>
    </div>
    <div class="cover-meta-item">
      <span class="label">成熟度等级</span>
      <span class="value">TRL {trl} · {trl_level}</span>
    </div>
    <div class="cover-meta-item">
      <span class="label">先进性评分</span>
      <span class="value">{adv_total} 分 · {adv_grade}</span>
    </div>
    <div class="cover-meta-item">
      <span class="label">报告日期</span>
      <span class="value">{report_date}</span>
    </div>
    <div class="cover-meta-item">
      <span class="label">潜在接受方</span>
      <span class="value">Top {len(top_companies)} 家企业</span>
    </div>
  </div>
</div>

<!-- ══ 主内容 ══ -->
<div class="main">

  <!-- § 1 技术内容摘要 -->
  <div class="section-title">01 · 技术内容分析</div>
  <div class="card">
    <div class="tech-grid">
      <div class="tech-item">
        <div class="k">技术主题</div>
        <div class="v">{tech_info.get('topic','—')}</div>
      </div>
      <div class="tech-item">
        <div class="k">技术来源</div>
        <div class="v">{tech_info.get('source','—')}</div>
      </div>
      <div class="tech-item">
        <div class="k">知识产权状态</div>
        <div class="v">{tech_info.get('ip_status','—')}</div>
      </div>
      <div class="tech-item">
        <div class="k">成熟度等级</div>
        <div class="v"><span class="trl-badge">TRL {trl} · {trl_level}</span></div>
      </div>
    </div>
    <div style="margin-bottom:16px">
      <div style="font-size:13px;font-weight:600;color:var(--text-sub);margin-bottom:8px">技术简介</div>
      <div style="font-size:14px;line-height:1.8;color:var(--text)">{tech_info.get('summary','—')}</div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div>
        <div style="font-size:13px;font-weight:600;color:var(--text-sub);margin-bottom:8px">核心优势</div>
        <ul style="padding-left:18px;font-size:13px;line-height:2.2;color:var(--text)">
          {''.join(f'<li>{a}</li>' for a in tech_info.get('advantages', ['—']))}
        </ul>
      </div>
      <div>
        <div style="font-size:13px;font-weight:600;color:var(--text-sub);margin-bottom:8px">应用场景</div>
        <ul style="padding-left:18px;font-size:13px;line-height:2.2;color:var(--text)">
          {''.join(f'<li>{s}</li>' for s in tech_info.get('scenarios', ['—']))}
        </ul>
      </div>
    </div>
  </div>

  <!-- § 2 先进性评估 -->
  <div class="section-title">02 · 技术先进性评估</div>
  <div class="chart-row">
    <div class="card">
      <div style="font-weight:600;margin-bottom:12px;color:var(--text-sub);font-size:13px">八维雷达评分图</div>
      <div id="radarChart" class="chart-container"></div>
    </div>
    <div class="card" style="display:flex;flex-direction:column;justify-content:space-between">
      <div>
        <div style="font-weight:600;margin-bottom:16px;color:var(--text-sub);font-size:13px">分项得分明细</div>
        <table class="score-table">
          <thead><tr><th>评估因子</th><th>权重</th><th>得分</th><th>进度</th></tr></thead>
          <tbody>
            {_build_score_table_rows(adv_scores)}
          </tbody>
        </table>
      </div>
      <div style="margin-top:16px;padding:16px;background:linear-gradient(135deg,#f0f4ff,#e8f0fe);border-radius:12px;text-align:center">
        <div style="font-size:36px;font-weight:800;color:var(--primary)">{adv_total}<span style="font-size:16px;font-weight:400;opacity:0.6">/100</span></div>
        <div style="font-size:14px;font-weight:600;color:var(--text);margin-top:4px">{adv_grade}</div>
      </div>
    </div>
  </div>

  <!-- § 3 专利价值评估 -->
  <div class="section-title">03 · 专利价值评估</div>
  <div class="card">
    <div class="quadrant-grid">
      <div class="quadrant-card q-tech">
        <div class="q-title" style="color:var(--primary)">🔬 技术价值</div>
        <ul>{''.join(f'<li>{i}</li>' for i in pv_tech.get('items', ['—']))}</ul>
      </div>
      <div class="quadrant-card q-market">
        <div class="q-title" style="color:var(--accent)">📈 市场价值</div>
        <ul>{''.join(f'<li>{i}</li>' for i in pv_market.get('items', ['—']))}</ul>
      </div>
      <div class="quadrant-card q-legal">
        <div class="q-title" style="color:var(--success)">⚖️ 法律价值</div>
        <ul>{''.join(f'<li>{i}</li>' for i in pv_legal.get('items', ['—']))}</ul>
      </div>
      <div class="quadrant-card q-strat">
        <div class="q-title" style="color:var(--purple)">🎯 战略价值</div>
        <ul>{''.join(f'<li>{i}</li>' for i in pv_strat.get('items', ['—']))}</ul>
      </div>
    </div>
    <div class="value-highlight">
      <div class="val">{value_range}</div>
      <div class="sub">综合估值区间（人民币）</div>
    </div>
  </div>

  <!-- § 4 供需匹配 — 图表 -->
  <div class="section-title">04 · 潜在接受方供需匹配</div>
  <div class="chart-row">
    <div class="card">
      <div style="font-weight:600;margin-bottom:12px;color:var(--text-sub);font-size:13px">综合匹配度 Top 排名</div>
      <div id="companiesChart" class="companies-chart"></div>
    </div>
    <div class="card">
      <div style="font-weight:600;margin-bottom:12px;color:var(--text-sub);font-size:13px">三维度得分结构</div>
      <div id="stackedChart" class="stacked-chart"></div>
    </div>
  </div>

  <!-- § 4 供需匹配 — 企业卡片 -->
  <div class="card">
    <div style="font-weight:600;margin-bottom:16px;font-size:15px">Top {len(top_companies)} 潜在接受方详情</div>
    <div class="company-list">
      {company_cards_html}
    </div>
  </div>

  <!-- § 5 模型说明 -->
  <div class="section-title">05 · 评分模型说明</div>
  <div class="card">
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:16px">
      <div style="text-align:center;padding:20px;background:#ede9fe;border-radius:12px">
        <div style="font-size:28px;font-weight:800;color:#7c3aed">40%</div>
        <div style="font-size:13px;font-weight:600;margin-top:6px;color:#4c1d95">专利信息匹配</div>
        <div style="font-size:11px;color:#7c3aed;margin-top:4px">技术重叠 · 研发活跃 · 布局意图</div>
      </div>
      <div style="text-align:center;padding:20px;background:#fef3c7;border-radius:12px">
        <div style="font-size:28px;font-weight:800;color:#b45309">30%</div>
        <div style="font-size:13px;font-weight:600;margin-top:6px;color:#78350f">公开新闻信息</div>
        <div style="font-size:11px;color:#b45309;margin-top:4px">需求信号 · 研发投入 · 行业曝光</div>
      </div>
      <div style="text-align:center;padding:20px;background:#d1fae5;border-radius:12px">
        <div style="font-size:28px;font-weight:800;color:#065f46">30%</div>
        <div style="font-size:13px;font-weight:600;margin-top:6px;color:#064e3b">招投标信息</div>
        <div style="font-size:11px;color:#065f46;margin-top:4px">采购意图 · 历史深度 · 采购紧迫度</div>
      </div>
    </div>
    <div style="font-size:12px;color:var(--text-sub);line-height:1.8;padding:12px;background:var(--bg);border-radius:8px">
      <strong>数据来源：</strong>智慧芽专利数据库（PatSnap）· gov-bid.com 政府招标信息平台 · 公开互联网新闻检索<br>
      <strong>评分说明：</strong>每项指标归一化至 0~1 区间，加权求和，满分 100 分。数据受限维度在报告中已标注"数据受限"。<br>
      <strong>免责声明：</strong>本报告仅供科技成果转移转化参考，不构成投资或商业建议。
    </div>
  </div>

</div><!-- /main -->

<div class="footer">
  由 <strong>Eureka · PatSnap 智慧芽</strong> 驱动 · 科技成果供需匹配分析报告 · {report_date}
</div>

<script>
// ── ECharts 雷达图 ──
(function() {{
  var chart = echarts.init(document.getElementById('radarChart'));
  var option = {{
    tooltip: {{ trigger: 'item' }},
    radar: {{
      indicator: {json.dumps(radar_data['indicator'], ensure_ascii=False)},
      center: ['50%', '52%'],
      radius: '68%',
      axisName: {{ color: '#64748b', fontSize: 12 }},
      splitLine: {{ lineStyle: {{ color: '#e2e8f0' }} }},
      splitArea: {{ areaStyle: {{ color: ['#f8fafc', '#f1f5f9'] }} }},
      axisLine: {{ lineStyle: {{ color: '#cbd5e1' }} }}
    }},
    series: [{{
      type: 'radar',
      data: [{{
        value: {json.dumps(radar_data['values'])},
        name: '先进性评分',
        areaStyle: {{ color: 'rgba(26,86,219,0.15)' }},
        lineStyle: {{ color: '#1a56db', width: 2 }},
        itemStyle: {{ color: '#1a56db' }}
      }}],
      symbol: 'circle',
      symbolSize: 6
    }}]
  }};
  chart.setOption(option);
  window.addEventListener('resize', function() {{ chart.resize(); }});
}})();

// ── 综合匹配度横向柱状图 ──
(function() {{
  var chart = echarts.init(document.getElementById('companiesChart'));
  var data = {json.dumps(companies_chart, ensure_ascii=False)};
  var option = {{
    tooltip: {{
      trigger: 'axis',
      axisPointer: {{ type: 'shadow' }},
      formatter: function(params) {{
        return params[0].name + '<br/>综合匹配度：<b>' + params[0].value + '</b> 分';
      }}
    }},
    grid: {{ left: '3%', right: '8%', bottom: '3%', containLabel: true }},
    xAxis: {{
      type: 'value', max: 100,
      axisLabel: {{ formatter: '{{value}}分', fontSize: 11 }},
      splitLine: {{ lineStyle: {{ color: '#f1f5f9' }} }}
    }},
    yAxis: {{
      type: 'category',
      data: data.names,
      axisLabel: {{ fontSize: 12, color: '#1e293b' }},
      inverse: true
    }},
    series: [{{
      type: 'bar',
      data: data.scores,
      barMaxWidth: 28,
      itemStyle: {{
        borderRadius: [0, 6, 6, 0],
        color: function(params) {{
          var colors = [
            new echarts.graphic.LinearGradient(0,0,1,0,[
              {{offset:0, color:'#f59e0b'}}, {{offset:1, color:'#fbbf24'}}
            ]),
            new echarts.graphic.LinearGradient(0,0,1,0,[
              {{offset:0, color:'#94a3b8'}}, {{offset:1, color:'#cbd5e1'}}
            ]),
            new echarts.graphic.LinearGradient(0,0,1,0,[
              {{offset:0, color:'#cd7c3e'}}, {{offset:1, color:'#f5a970'}}
            ])
          ];
          if (params.dataIndex < 3) return colors[params.dataIndex];
          return new echarts.graphic.LinearGradient(0,0,1,0,[
            {{offset:0, color:'#1a56db'}}, {{offset:1, color:'#0ea5e9'}}
          ]);
        }}
      }},
      label: {{ show: true, position: 'right', formatter: '{{c}}分', fontSize: 12, color: '#64748b' }}
    }}]
  }};
  chart.setOption(option);
  window.addEventListener('resize', function() {{ chart.resize(); }});
}})();

// ── 三维度堆叠柱状图 ──
(function() {{
  var chart = echarts.init(document.getElementById('stackedChart'));
  var data = {json.dumps(stacked_chart, ensure_ascii=False)};
  var option = {{
    tooltip: {{
      trigger: 'axis',
      axisPointer: {{ type: 'shadow' }},
    }},
    legend: {{
      data: ['专利(40)', '新闻(30)', '招投标(30)'],
      bottom: 0, itemWidth: 12, itemHeight: 12, fontSize: 11
    }},
    grid: {{ left: '3%', right: '4%', bottom: '40px', top: '10px', containLabel: true }},
    xAxis: {{
      type: 'category',
      data: data.names,
      axisLabel: {{ rotate: 30, fontSize: 11, color: '#1e293b', interval: 0 }}
    }},
    yAxis: {{
      type: 'value', max: 100,
      splitLine: {{ lineStyle: {{ color: '#f1f5f9' }} }}
    }},
    series: [
      {{
        name: '专利(40)', type: 'bar', stack: 'total', barMaxWidth: 32,
        data: data.patent,
        itemStyle: {{ color: '#7c3aed', borderRadius: [0,0,0,0] }}
      }},
      {{
        name: '新闻(30)', type: 'bar', stack: 'total',
        data: data.news,
        itemStyle: {{ color: '#f59e0b' }}
      }},
      {{
        name: '招投标(30)', type: 'bar', stack: 'total',
        data: data.bid,
        itemStyle: {{ color: '#10b981', borderRadius: [4,4,0,0] }}
      }}
    ]
  }};
  chart.setOption(option);
  window.addEventListener('resize', function() {{ chart.resize(); }});
}})();
</script>
</body>
</html>"""
    return html


# ─────────────────────────────────────────────
# 辅助构建函数
# ─────────────────────────────────────────────

ADVANCEMENT_FACTORS = [
    ("技术原理突破性", 15),
    ("核心方法新颖性", 10),
    ("技术可替代性",   10),
    ("技术壁垒高度",   10),
    ("工艺兼容性",     15),
    ("产业化成熟度",   15),
    ("技术稳定性",     10),
    ("规模化潜力",     15),
]


def _build_radar_data(adv_scores: dict) -> dict:
    indicator = []
    values = []
    for factor, weight in ADVANCEMENT_FACTORS:
        info = adv_scores.get(factor, {})
        raw_score = info.get("score", 0)  # 0~10 原始分
        weighted = raw_score * weight / 10
        indicator.append({"name": factor, "max": weight})
        values.append(round(weighted, 1))
    return {"indicator": indicator, "values": values}


def _build_score_table_rows(adv_scores: dict) -> str:
    rows = []
    for factor, weight in ADVANCEMENT_FACTORS:
        info = adv_scores.get(factor, {})
        raw_score = info.get("score", 0)
        weighted = round(raw_score * weight / 10, 1)
        pct = int(raw_score * 10)
        rows.append(
            f'<tr>'
            f'<td>{factor}</td>'
            f'<td style="color:var(--text-sub)">{weight}%</td>'
            f'<td style="font-weight:600;color:var(--primary)">{weighted}</td>'
            f'<td><span class="progress-bar"><span class="progress-fill" style="width:{pct}%"></span></span>{raw_score}/10</td>'
            f'</tr>'
        )
    return "\n".join(rows)


def _build_companies_chart(companies: list[dict]) -> dict:
    names = [c.get("company_name", "—")[:8] for c in companies]
    scores = [c.get("total_score", 0) for c in companies]
    return {"names": names, "scores": scores}


def _build_stacked_chart(companies: list[dict]) -> dict:
    names = [c.get("company_name", "—")[:6] for c in companies]
    patent = [c.get("patent_score", 0) for c in companies]
    news = [c.get("news_score", 0) for c in companies]
    bid = [c.get("bid_score", 0) for c in companies]
    return {"names": names, "patent": patent, "news": news, "bid": bid}


def _build_company_cards(companies: list[dict]) -> str:
    cards = []
    for i, c in enumerate(companies, 1):
        rank_class = {1: "rank-1", 2: "rank-2", 3: "rank-3"}.get(i, "rank-other")
        evidence_items = "".join(
            f'<li>{e}</li>' for e in c.get("evidence", ["暂无具体证据"])
        )
        ps = c.get("patent_score", 0)
        ns = c.get("news_score", 0)
        bs = c.get("bid_score", 0)
        ts = c.get("total_score", 0)
        action_color = {
            "强烈推荐": "var(--danger)",
            "高度匹配": "var(--primary)",
            "中度匹配": "var(--warning)",
        }.get(c.get("grade_label", ""), "var(--success)")

        cards.append(f"""
<div class="company-card">
  <div class="rank-badge {rank_class}">{i}</div>
  <div>
    <div class="company-name">{c.get('company_name','—')}</div>
    <div class="company-tags">
      <span class="tag tag-patent">专利 {ps}分</span>
      <span class="tag tag-news">新闻 {ns}分</span>
      <span class="tag tag-bid">招投标 {bs}分</span>
    </div>
    <div class="grade-stars">{c.get('grade','⭐')} {c.get('grade_label','—')}</div>
    <ul class="evidence-list">{evidence_items}</ul>
    <span class="action-tag" style="background:{action_color}">{c.get('action','—')}</span>
  </div>
  <div class="score-pill">
    <span class="num">{ts}</span>
    <span class="sub">满分100</span>
  </div>
</div>""")
    return "\n".join(cards)


# ─────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────
if __name__ == "__main__":
    tech_info = {
        "source": "某高校材料研究院",
        "topic": "无重稀土高性能永磁材料制备技术",
        "summary": "本技术采用纳米晶界调控方法，在不引入重稀土元素的前提下，实现磁能积≥55 MGOe，矫顽力≥25 kOe，可替代传统含重稀土永磁体用于高端电机与风电发电机场景。",
        "advantages": ["无重稀土，成本降低约35%", "磁性能达国际领先水平", "工艺与现有烧结线兼容", "已完成中试，TRL 7级"],
        "scenarios": ["新能源汽车驱动电机", "风力发电机", "工业伺服电机", "消费电子微型电机"],
        "ip_status": "已授权发明专利3件（CN202310XXXXX.X）",
        "trl": 7,
        "trl_level": "系统原型验证",
    }
    advancement_scores = {
        "scores": {
            "技术原理突破性": {"score": 9, "weight": 15, "comment": "纳米晶界调控为行业领先方案"},
            "核心方法新颖性": {"score": 8, "weight": 10, "comment": "无重稀土路线独特"},
            "技术可替代性":   {"score": 8, "weight": 10, "comment": "可替代性低"},
            "技术壁垒高度":   {"score": 8, "weight": 10, "comment": "工艺壁垒高"},
            "工艺兼容性":     {"score": 9, "weight": 15, "comment": "与现有烧结线高度兼容"},
            "产业化成熟度":   {"score": 8, "weight": 15, "comment": "中试完成，TRL 7"},
            "技术稳定性":     {"score": 8, "weight": 10, "comment": "批次一致性良好"},
            "规模化潜力":     {"score": 9, "weight": 15, "comment": "量产路径清晰"},
        },
        "total": 85.5,
        "grade": "L4",
        "grade_label": "高价值技术",
    }
    patent_value = {
        "tech_value": {"items": ["权利要求涵盖核心制备工艺", "被引用42次", "IPC分类 H01F1/057"]},
        "market_value": {"items": ["目标市场 TAM 约800亿元", "同族专利覆盖中美日德", "商业化进展：中试完成"]},
        "legal_value": {"items": ["已授权，有效期至2043年", "权利要求稳定，未经无效挑战", "PQI 78/100"]},
        "strategic_value": {"items": ["构建无重稀土技术壁垒", "SEP候选可能性低但战略价值高", "可许可/转让/入股三种方式"]},
        "estimated_value_range": "360万 ~ 900万元",
    }
    top_companies = [
        {"company_name": "宁德时代新能源科技", "total_score": 87.5, "patent_score": 37.2, "news_score": 26.8, "bid_score": 23.5, "grade": "⭐⭐⭐⭐⭐", "grade_label": "强烈推荐", "action": "立即跟进", "evidence": ["专利CN202210XXXXX，IPC H01F1/057，被引68次", "2024年Q3扩产公告：动力电机生产线投资50亿元", "招标：电机驱动系统技术改造，预算1200万元"]},
        {"company_name": "比亚迪股份有限公司", "total_score": 82.3, "patent_score": 34.1, "news_score": 24.5, "bid_score": 23.7, "grade": "⭐⭐⭐⭐", "grade_label": "高度匹配", "action": "重点跟进", "evidence": ["近3年永磁电机专利申请增长28%", "2024年参加上海电机展，展示新型永磁电机", "中标：新能源汽车核心零部件采购，含永磁材料"]},
        {"company_name": "金风科技股份", "total_score": 76.8, "patent_score": 31.5, "news_score": 22.3, "bid_score": 23.0, "grade": "⭐⭐⭐⭐", "grade_label": "高度匹配", "action": "重点跟进", "evidence": ["风电发电机专利布局覆盖6国", "新闻：与中科院合作研发新一代永磁直驱风机", "招标：风电磁性材料采购框架协议，预算2000万元"]},
        {"company_name": "华友钴业股份", "total_score": 68.2, "patent_score": 27.8, "news_score": 18.5, "bid_score": 21.9, "grade": "⭐⭐⭐", "grade_label": "中度匹配", "action": "常规跟进", "evidence": ["磁性功能材料专利布局活跃", "产学研：与浙大联合研发高性能磁材"]},
        {"company_name": "正海磁材股份有限公司", "total_score": 65.4, "patent_score": 26.2, "news_score": 17.8, "bid_score": 21.4, "grade": "⭐⭐⭐", "grade_label": "中度匹配", "action": "常规跟进", "evidence": ["稀土永磁材料专业制造商", "近2年新申请专利12件，聚焦高矫顽力方向"]},
    ]
    html = generate_html_report(tech_info, advancement_scores, patent_value, top_companies)
    with open("/tmp/demo_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Demo 报告已生成：/tmp/demo_report.html")
