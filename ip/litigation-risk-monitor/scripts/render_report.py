"""litigation-risk-monitor HTML 报告渲染（v2 扩展版）。

新增功能（v2）：
  1. 专利卡片含摘要附图（abstract_image_b64 / abstract_image_url）
  2. 专利卡片底部展示 INPADOC 同族专利信息
  3. 风险等级改为浅色背景区分：
       高风险（被诉仍在审）  → 浅红背景  #fff0f0，左边框 #e74c3c
       中等风险（已判决/上诉中）→ 浅橙背景  #fff7ed，左边框 #e67e22
       防御/反诉（中创新航主动持有）→ 浅蓝背景 #f0f6ff，左边框 #3498db
  4. 报告末尾增加涉诉专利汇总列表（含同族公开号/受理局/法律状态/申请日）

用法：
    python render_report.py --data report_data.json --out report.html
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path

try:
    from jinja2 import Template
except Exception:  # pragma: no cover
    Template = None

# ─────────────────────────────────────────────
# CSS + JS 公共样式（内联，离线可用）
# ─────────────────────────────────────────────
_STYLE = """
<style>
*{box-sizing:border-box;}
body{font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;margin:0;padding:24px 32px;color:#222;line-height:1.6;background:#f5f7fa;}
h1{font-size:22px;border-bottom:2px solid #2a6;padding-bottom:8px;margin-bottom:16px;}
h2{font-size:17px;margin-top:32px;border-left:4px solid #2a6;padding-left:10px;color:#1a4a3a;}
h3{font-size:14px;color:#345;margin-top:14px;}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:13px;}
th,td{border:1px solid #ddd;padding:6px 10px;text-align:left;vertical-align:top;}
th{background:#eef2f5;font-weight:600;}
tr:hover td{background:#fafbfc;}
a{color:#1a6ea8;text-decoration:none;}
a:hover{text-decoration:underline;}

/* ── 专利卡片 ── */
.patent-cards{display:flex;flex-wrap:wrap;gap:16px;margin:12px 0;}
.patent-card{
  width:calc(50% - 8px);min-width:320px;
  border-radius:8px;padding:16px;cursor:pointer;
  transition:box-shadow .2s;position:relative;
  border-left:5px solid #ccc;background:#fff;
}
.patent-card:hover{box-shadow:0 4px 18px rgba(0,0,0,.13);}

/* 高风险：被诉仍在审 */
.risk-high{background:#fff0f0;border-left-color:#e74c3c;}
/* 中等风险：已判决/上诉中 */
.risk-medium{background:#fff7ed;border-left-color:#e67e22;}
/* 防御/反诉资产 */
.risk-defense{background:#f0f6ff;border-left-color:#3498db;}

.risk-badge{
  display:inline-block;padding:2px 8px;border-radius:12px;
  font-size:11px;font-weight:700;margin-bottom:8px;
}
.badge-high{background:#fde8e8;color:#c0392b;}
.badge-medium{background:#fef3e2;color:#d35400;}
.badge-defense{background:#ddeeff;color:#1a5fa8;}

.card-pn{font-size:15px;font-weight:700;margin-bottom:4px;}
.card-pn a{color:#1a6ea8;}
.card-meta{font-size:12px;color:#666;margin-bottom:8px;}
.card-title{font-size:13px;font-weight:600;margin-bottom:8px;color:#1a2a3a;}

/* 摘要附图 */
.abstract-img-wrap{
  text-align:center;margin:8px 0;
  background:#f8f9fa;border:1px solid #e0e3e8;border-radius:6px;
  padding:6px;overflow:hidden;
}
.abstract-img-wrap img{
  max-width:100%;max-height:180px;
  object-fit:contain;display:block;margin:0 auto;
}
.no-img{color:#aaa;font-size:12px;padding:16px 0;text-align:center;}

/* 技术三要素 */
.tech-elem{margin:4px 0;font-size:12px;}
.tech-label{display:inline-block;width:60px;color:#666;font-weight:600;}
.tech-val{color:#333;}

/* 同族专利块 */
.family-block{
  margin-top:12px;border-top:1px dashed #ddd;padding-top:10px;
}
.family-block h4{font-size:12px;color:#888;margin:0 0 6px;font-weight:600;letter-spacing:.5px;}
.family-table{width:100%;font-size:11px;margin:0;}
.family-table th{background:#f0f4f8;font-size:11px;padding:4px 6px;}
.family-table td{padding:4px 6px;border-color:#e8edf2;}
.status-active{color:#27ae60;font-weight:600;}
.status-inactive{color:#e74c3c;}
.status-pending{color:#e67e22;}

/* 弹窗 */
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:1000;align-items:center;justify-content:center;}
.modal-overlay.open{display:flex;}
.modal-box{background:#fff;border-radius:10px;padding:24px;max-width:720px;width:90%;max-height:80vh;overflow-y:auto;position:relative;}
.modal-close{position:absolute;top:12px;right:16px;font-size:20px;cursor:pointer;color:#888;background:none;border:none;}
.modal-pn{font-size:16px;font-weight:700;margin-bottom:12px;color:#1a6ea8;}
.claims-text{font-size:13px;white-space:pre-wrap;line-height:1.7;color:#333;}

/* 汇总表 */
.summary-section{margin-top:40px;}
.tag{display:inline-block;padding:1px 6px;border-radius:3px;background:#eef;color:#225;font-size:11px;margin-right:3px;}
.unverified{color:#a33;font-style:italic;}
.footer{margin-top:36px;font-size:12px;color:#888;border-top:1px dashed #ccc;padding-top:10px;}
.case-card{border:1px solid #e0e4ea;border-radius:6px;padding:14px;margin:10px 0;background:#fafbfc;}
.summary-box{background:#f9f9f9;border-left:4px solid #2a6;padding:14px 18px;margin:12px 0;border-radius:0 6px 6px 0;line-height:1.8;}
.chart-container{max-width:720px;margin:16px 0;}
.inventor-section{margin-bottom:20px;border:1px solid #e4e8ee;border-radius:6px;padding:12px;background:#fdfefe;}
.tech-list{margin:4px 0 0 16px;padding:0;list-style:disc;font-size:12px;}
.geo-risk-high{color:#c0392b;font-weight:700;}
.geo-risk-medium{color:#e67e22;font-weight:700;}
.geo-risk-low{color:#27ae60;}

@media(max-width:700px){
  .patent-card{width:100%;}
  body{padding:12px 10px;}
}
</style>
"""

# ─────────────────────────────────────────────
# Jinja2 HTML 骨架模板
# ─────────────────────────────────────────────
HTML_SKELETON = r"""<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>涉诉专利风险监测报告 - {{ generated_at }}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
""" + _STYLE + r"""
</head>
<body>

<h1>⚖️ 涉诉专利风险监测报告</h1>
<p style="color:#555;font-size:13px;">
  生成时间：<b>{{ generated_at }}</b> ｜
  目标申请人：<b>{{ overview.assignee_count }}</b> 家 ｜
  涉诉专利：<b>{{ overview.litigated_count }}</b> 件 ｜
  同族成员：<b>{{ overview.family_count }}</b> 件 ｜
  涉案件数：<b>{{ overview.case_count }}</b> 件
</p>

<!-- 风险图例 -->
<div style="display:flex;gap:12px;flex-wrap:wrap;margin:10px 0 20px;">
  <span style="background:#fff0f0;border-left:4px solid #e74c3c;padding:4px 10px;border-radius:4px;font-size:12px;">🔴 高风险 — 被诉仍在审</span>
  <span style="background:#fff7ed;border-left:4px solid #e67e22;padding:4px 10px;border-radius:4px;font-size:12px;">🟠 中等风险 — 已判决/上诉中</span>
  <span style="background:#f0f6ff;border-left:4px solid #3498db;padding:4px 10px;border-radius:4px;font-size:12px;">🔵 防御/反诉资产 — 主动持有</span>
</div>

<!-- ===== 1. 概览 ===== -->
<h2>1. 概览</h2>
<table>
<tr><th>目标申请人</th><td>{{ overview.assignees | join("、") }}</td></tr>
<tr><th>同族范围</th><td>{{ overview.family_scope }}</td></tr>
<tr><th>发明人回溯</th><td>近 {{ overview.inventor_lookback_years }} 年</td></tr>
</table>

{% if overview.assignee_patent_map %}
<h3>1.1 申请人 → 涉诉专利 → 同族号 映射</h3>
<table>
<tr><th>目标申请人</th><th>涉诉专利号</th><th>专利标题</th><th>INPADOC 同族号</th></tr>
{% for entry in overview.assignee_patent_map %}
  {% for lp in entry.litigated_patents %}
  <tr>
    {% if loop.first %}<td rowspan="{{ entry.litigated_patents | length }}"><b>{{ entry.assignee }}</b></td>{% endif %}
    <td><b>{{ lp.pn }}</b></td>
    <td>{{ lp.title or "—" }}</td>
    <td style="font-size:11px;">{{ lp.family_members | join("<br/>") | safe }}</td>
  </tr>
  {% endfor %}
{% endfor %}
</table>
{% endif %}

<!-- ===== 2. 同族基础分析 ===== -->
<h2>2. 同族基础分析</h2>
<h3>2.1 地域分布</h3>
<table><tr><th>国家/地区</th><th>同族数量</th><th>样本说明</th></tr>
{% for row in family_basic.geo %}<tr><td>{{ row.jurisdiction }}</td><td>{{ row.count }}</td><td>{{ row.scope_note }}</td></tr>{% endfor %}
</table>

<h3>2.2 技术点 (IPC) 分布</h3>
<table><tr><th>IPC</th><th>同族数量</th></tr>
{% for row in family_basic.ipc %}<tr><td>{{ row.code }}</td><td>{{ row.count }}</td></tr>{% endfor %}
</table>

<h3>2.3 法律状态与审查历史</h3>
{% if family_basic.legal_detail %}
<table>
<tr><th>专利号</th><th>标题</th><th>司法管辖</th><th>当前状态</th><th>授权日</th><th>关键历史节点</th><th>审查说明</th></tr>
{% for item in family_basic.legal_detail %}
<tr>
  <td>{{ item.pn }}</td><td>{{ item.title or "—" }}</td>
  <td>{{ item.jurisdiction or "—" }}</td><td>{{ item.current_status or "—" }}</td>
  <td>{{ item.granted_date or "—" }}</td>
  <td>{% if item.key_events %}<ul style="margin:0;padding-left:14px;font-size:11px;">{% for ev in item.key_events %}<li>{{ ev.date }}：{{ ev.event }}</li>{% endfor %}</ul>{% else %}—{% endif %}</td>
  <td>{{ item.prosecution_note or "—" }}</td>
</tr>
{% endfor %}
</table>
{% else %}
<table><tr><th>状态</th><th>数量</th></tr>
{% for row in family_basic.legal %}<tr><td>{{ row.status }}</td><td>{{ row.count }}</td></tr>{% endfor %}
</table>
{% endif %}

{% if family_basic.geo_analysis %}
<h3>2.4 地域布局分析</h3>
<div class="summary-box">{{ family_basic.geo_analysis }}</div>
{% endif %}

{% if family_basic.claim_comparison %}
<h3>2.5 权利要求保护点对比</h3>
<table>
<tr><th>专利号</th><th>司法管辖</th><th>保护范围摘要</th><th>核心保护点</th><th>技术覆盖</th><th>与同族异同</th></tr>
{% for item in family_basic.claim_comparison %}
<tr>
  <td>{{ item.pn }}</td><td>{{ item.jurisdiction }}</td>
  <td>{{ item.protection_scope or "—" }}</td><td>{{ item.key_claims or "—" }}</td>
  <td>{{ item.tech_coverage or "—" }}</td><td>{{ item.diff_note or "—" }}</td>
</tr>
{% endfor %}
</table>
{% endif %}
"""

# 接续 HTML_SKELETON —— 专利卡片部分 + 后续章节
HTML_SKELETON += r"""
<!-- ===== 3. 主要涉诉专利详情（卡片视图）===== -->
<h2>3. 主要涉诉专利详情</h2>
<div class="patent-cards">
{% for p in litigated_patents %}
{# 根据 risk_type 设置卡片样式 #}
{% if p.risk_type == 'high' %}
  {% set card_class = 'patent-card risk-high' %}
  {% set badge_class = 'risk-badge badge-high' %}
  {% set badge_text = '🔴 高风险·被诉仍在审' %}
{% elif p.risk_type == 'medium' %}
  {% set card_class = 'patent-card risk-medium' %}
  {% set badge_class = 'risk-badge badge-medium' %}
  {% set badge_text = '🟠 中等风险·已判决/上诉中' %}
{% else %}
  {% set card_class = 'patent-card risk-defense' %}
  {% set badge_class = 'risk-badge badge-defense' %}
  {% set badge_text = '🔵 防御/反诉资产' %}
{% endif %}

<div class="{{ card_class }}" onclick="openModal('modal-{{ loop.index }}')">
  <span class="{{ badge_class }}">{{ badge_text }}</span>

  <!-- 公开号 + 链接 -->
  <div class="card-pn">
    {% if p.url %}
      <a href="{{ p.url }}" target="_blank" onclick="event.stopPropagation()">{{ p.pn }}</a>
    {% else %}
      {{ p.pn }}
    {% endif %}
  </div>

  <!-- 标题 -->
  <div class="card-title">{{ p.title or "—" }}</div>

  <!-- 基础信息 -->
  <div class="card-meta">
    申请日：{{ p.apply_date or "—" }} ｜
    公开日：{{ p.pub_date or "—" }} ｜
    法律状态：<b>{{ p.legal_status or "—" }}</b>
  </div>

  <!-- 摘要附图 -->
  <div class="abstract-img-wrap">
    {% if p.abstract_image_b64 %}
      <img src="data:image/png;base64,{{ p.abstract_image_b64 }}" alt="摘要附图 {{ p.pn }}" loading="lazy"/>
    {% elif p.abstract_image_url %}
      <img src="{{ p.abstract_image_url }}" alt="摘要附图 {{ p.pn }}" loading="lazy" onerror="this.parentNode.innerHTML='<div class=no-img>📄 附图加载失败（需网络）</div>'"/>
    {% else %}
      <div class="no-img">📄 暂无摘要附图</div>
    {% endif %}
  </div>

  <!-- 技术三要素 -->
  {% if p.tech_problem or p.tech_means or p.tech_effect %}
  <div style="margin:8px 0;">
    {% if p.tech_problem %}<div class="tech-elem"><span class="tech-label">技术问题</span><span class="tech-val">{{ p.tech_problem }}</span></div>{% endif %}
    {% if p.tech_means %}<div class="tech-elem"><span class="tech-label">技术手段</span><span class="tech-val">{{ p.tech_means }}</span></div>{% endif %}
    {% if p.tech_effect %}<div class="tech-elem"><span class="tech-label">技术效果</span><span class="tech-val">{{ p.tech_effect }}</span></div>{% endif %}
  </div>
  {% endif %}

  <!-- 需要确认的点 -->
  {% if p.confirm_points %}
  <div style="margin-top:8px;font-size:12px;">
    <b style="color:#d35400;">⚠ 需确认：</b>{{ p.confirm_points }}
  </div>
  {% endif %}

  <!-- INPADOC 同族专利信息（卡片底部）-->
  {% if p.family_members and p.family_members | length > 0 %}
  <div class="family-block">
    <h4>📋 INPADOC 同族专利（{{ p.family_members | length }} 件）</h4>
    <table class="family-table">
      <tr><th>公开号</th><th>受理局</th><th>法律状态</th><th>申请日</th></tr>
      {% for fm in p.family_members %}
      <tr>
        <td>
          {% if fm.url %}<a href="{{ fm.url }}" target="_blank" onclick="event.stopPropagation()">{{ fm.pn }}</a>
          {% else %}{{ fm.pn }}{% endif %}
        </td>
        <td>{{ fm.jurisdiction or "—" }}</td>
        <td>
          {% if fm.legal_status %}
            {% if 'active' in fm.legal_status.lower() or '有效' in fm.legal_status %}
              <span class="status-active">{{ fm.legal_status }}</span>
            {% elif 'inactive' in fm.legal_status.lower() or '失效' in fm.legal_status or '无效' in fm.legal_status %}
              <span class="status-inactive">{{ fm.legal_status }}</span>
            {% elif 'pending' in fm.legal_status.lower() or '审中' in fm.legal_status or '申请' in fm.legal_status %}
              <span class="status-pending">{{ fm.legal_status }}</span>
            {% else %}{{ fm.legal_status }}{% endif %}
          {% else %}—{% endif %}
        </td>
        <td>{{ fm.apply_date or "—" }}</td>
      </tr>
      {% endfor %}
    </table>
  </div>
  {% endif %}

  <div style="margin-top:10px;font-size:11px;color:#aaa;text-align:right;">点击查看权利要求 →</div>
</div>

<!-- 弹窗 -->
<div class="modal-overlay" id="modal-{{ loop.index }}" onclick="closeModal(this)">
  <div class="modal-box" onclick="event.stopPropagation()">
    <button class="modal-close" onclick="closeModal(document.getElementById('modal-{{ loop.index }}'))">✕</button>
    <div class="modal-pn">
      {% if p.url %}<a href="{{ p.url }}" target="_blank">{{ p.pn }}</a>{% else %}{{ p.pn }}{% endif %}
    </div>
    <p style="font-size:13px;color:#555;margin-bottom:12px;">{{ p.title or "—" }}</p>
    <h4 style="font-size:13px;margin-bottom:8px;color:#345;">权利要求书</h4>
    <div class="claims-text">{{ p.claims or "暂无权利要求数据" }}</div>
  </div>
</div>
{% endfor %}
</div><!-- end .patent-cards -->
"""

# 接续 HTML_SKELETON —— 案件分析、发明人、结论、汇总列表
HTML_SKELETON += r"""
<!-- ===== 4. 涉诉案件深度分析 ===== -->
<h2>4. 涉诉案件深度分析</h2>
{% for c in cases %}
<div class="case-card">
  <h3>案件 {{ loop.index }}：{{ c.title or "未公开标题" }}</h3>
  <p>
    <span class="tag">原告</span>{{ c.plaintiff or '<span class="unverified">Unverified</span>' | safe }}
    <span class="tag">被告</span>{{ c.defendant or '<span class="unverified">Unverified</span>' | safe }}
    <span class="tag">案号/法院</span>{{ c.docket or '<span class="unverified">Unverified</span>' | safe }}
  </p>
  <p><b>涉案专利：</b>{{ c.patents | join("、") }}</p>
  <p><b>争议焦点：</b>{{ c.issue or '<span class="unverified">Unverified</span>' | safe }}</p>
  <p><b>被告答复/抗辩：</b>{{ c.defense or '<span class="unverified">Unverified</span>' | safe }}</p>
  <p><b>审理结果/进程：</b>{{ c.status or '<span class="unverified">Unverified</span>' | safe }}</p>
  <p><b>关键节点：</b>{{ c.timeline or "—" }}</p>
  <p style="font-size:12px;color:#888;"><b>来源：</b>{{ c.sources | join("；") }}</p>
</div>
{% endfor %}

<!-- ===== 5. 核心发明人延伸分析 ===== -->
<h2>5. 核心发明人延伸分析（近 {{ overview.inventor_lookback_years }} 年）</h2>
{% if inventors %}
<h3>5.1 核心发明人近3年专利申请量</h3>
<div class="chart-container">
  <canvas id="inventorChart" height="320"></canvas>
</div>
<script>
(function(){
  var inventors = {{ inventors | tojson }};
  var yearsSet = {};
  inventors.forEach(function(inv){
    var fy = inv.recent_filings_by_year || {};
    Object.keys(fy).forEach(function(y){ yearsSet[y]=1; });
  });
  var years = Object.keys(yearsSet).sort();
  if(!years.length) years = ["近3年"];
  var colors = [
    'rgba(42,102,102,.75)','rgba(231,76,60,.75)','rgba(52,152,219,.75)',
    'rgba(241,196,15,.75)','rgba(155,89,182,.75)','rgba(26,188,156,.75)',
    'rgba(230,126,34,.75)','rgba(149,165,166,.75)'
  ];
  var ctx = document.getElementById('inventorChart');
  if(ctx){
    new Chart(ctx,{
      type:'bar',
      data:{ labels:years, datasets:inventors.map(function(inv,i){
        var fy=inv.recent_filings_by_year||{};
        return{label:inv.name,data:years.map(function(y){return fy[y]||0;}),backgroundColor:colors[i%colors.length]};
      })},
      options:{responsive:true,plugins:{legend:{position:'right'},title:{display:true,text:'核心发明人近3年专利申请量（样本范围：patent.search 结果）'}},scales:{y:{beginAtZero:true,title:{display:true,text:'申请件数'}}}}
    });
  }
})();
</script>

<h3>5.2 发明人详情与技术布局点</h3>
{% for inv in inventors %}
<div class="inventor-section">
  <b>{{ inv.name }}</b>
  {% if inv.assignee_change %}<span class="tag">{{ inv.assignee_change }}</span>{% endif %}
  <table style="margin-top:6px;">
  <tr><th>近N年申请总量</th><td>{{ inv.recent_count }}</td><th>主要IPC</th><td>{{ inv.top_ipc | join("、") }}</td></tr>
  {% if inv.recent_filings_by_year %}
  <tr><th>逐年申请量</th><td colspan="3">{% for yr,cnt in inv.recent_filings_by_year.items() %}{{ yr }}年：{{ cnt }}件；{% endfor %}</td></tr>
  {% endif %}
  <tr><th>趋势备注</th><td colspan="3">{{ inv.note or "—" }}</td></tr>
  </table>
  {% if inv.tech_focus_list %}
  <p style="margin:8px 0 4px;"><b>近3年主要技术布局点：</b></p>
  <ul class="tech-list">{% for tech in inv.tech_focus_list %}<li>{{ tech }}</li>{% endfor %}</ul>
  {% endif %}
</div>
{% endfor %}
{% endif %}

<!-- ===== 6. 三维结论 ===== -->
<h2>6. 三维结论</h2>
<h3>6.1 地域风险</h3>
<p>{{ conclusions.geographic_risk }}</p>
{% if conclusions.geo_litigation_risk %}
<h4 style="font-size:13px;color:#345;margin-top:10px;">潜在涉诉地域分析</h4>
<table>
<tr><th>国家/地区</th><th>风险等级</th><th>风险依据</th></tr>
{% for gr in conclusions.geo_litigation_risk %}
<tr>
  <td>{{ gr.jurisdiction }}</td>
  <td>{% if gr.risk_level=='高' %}<span class="geo-risk-high">高</span>{% elif gr.risk_level=='中' %}<span class="geo-risk-medium">中</span>{% else %}<span class="geo-risk-low">{{ gr.risk_level }}</span>{% endif %}</td>
  <td>{{ gr.reason }}</td>
</tr>
{% endfor %}
</table>
{% endif %}

<h3>6.2 应诉预警</h3>
<p>{{ conclusions.litigation_alert }}</p>
{% if conclusions.litigation_alert_summary %}
<h4 style="font-size:13px;color:#345;margin-top:10px;">综合应诉分析总结</h4>
<div class="summary-box">{{ conclusions.litigation_alert_summary }}</div>
{% endif %}

<h3>6.3 趋势预测</h3>
<p>{{ conclusions.trend_forecast }}</p>

<!-- ===== 7. 涉诉专利汇总列表 ===== -->
<div class="summary-section">
<h2>7. 涉诉专利汇总列表</h2>
<p style="font-size:12px;color:#666;">包含主要涉诉专利及其 INPADOC 同族展开，字段：涉诉专利公开号 / 同族公开号 / 同族受理局 / 简单法律状态 / 申请日。</p>
<table>
<tr>
  <th>涉诉专利公开号</th>
  <th>专利标题</th>
  <th>风险等级</th>
  <th>同族公开号</th>
  <th>同族受理局</th>
  <th>同族法律状态</th>
  <th>同族申请日</th>
</tr>
{% for p in litigated_patents %}
  {% if p.family_members and p.family_members | length > 0 %}
    {% for fm in p.family_members %}
    <tr>
      {% if loop.first %}
      <td rowspan="{{ p.family_members | length }}" style="font-weight:600;">
        {% if p.url %}<a href="{{ p.url }}" target="_blank">{{ p.pn }}</a>{% else %}{{ p.pn }}{% endif %}
      </td>
      <td rowspan="{{ p.family_members | length }}" style="font-size:12px;">{{ p.title or "—" }}</td>
      <td rowspan="{{ p.family_members | length }}">
        {% if p.risk_type=='high' %}<span class="badge-high risk-badge">高风险</span>
        {% elif p.risk_type=='medium' %}<span class="badge-medium risk-badge">中等</span>
        {% else %}<span class="badge-defense risk-badge">防御</span>{% endif %}
      </td>
      {% endif %}
      <td>{% if fm.url %}<a href="{{ fm.url }}" target="_blank">{{ fm.pn }}</a>{% else %}{{ fm.pn }}{% endif %}</td>
      <td>{{ fm.jurisdiction or "—" }}</td>
      <td>
        {% if fm.legal_status %}
          {% if 'active' in fm.legal_status.lower() or '有效' in fm.legal_status %}<span class="status-active">{{ fm.legal_status }}</span>
          {% elif 'inactive' in fm.legal_status.lower() or '失效' in fm.legal_status or '无效' in fm.legal_status %}<span class="status-inactive">{{ fm.legal_status }}</span>
          {% elif 'pending' in fm.legal_status.lower() or '审中' in fm.legal_status %}<span class="status-pending">{{ fm.legal_status }}</span>
          {% else %}{{ fm.legal_status }}{% endif %}
        {% else %}—{% endif %}
      </td>
      <td>{{ fm.apply_date or "—" }}</td>
    </tr>
    {% endfor %}
  {% else %}
  <tr>
    <td style="font-weight:600;">{% if p.url %}<a href="{{ p.url }}" target="_blank">{{ p.pn }}</a>{% else %}{{ p.pn }}{% endif %}</td>
    <td style="font-size:12px;">{{ p.title or "—" }}</td>
    <td>{% if p.risk_type=='high' %}<span class="badge-high risk-badge">高风险</span>{% elif p.risk_type=='medium' %}<span class="badge-medium risk-badge">中等</span>{% else %}<span class="badge-defense risk-badge">防御</span>{% endif %}</td>
    <td colspan="4" style="color:#aaa;font-style:italic;">暂无同族数据</td>
  </tr>
  {% endif %}
{% endfor %}
</table>
</div>

<!-- ===== 8. 附录 ===== -->
<h2>8. 附录：数据来源与字段口径</h2>
<ul>
{% for s in sources %}<li>[{{ s.id }}] {{ s.label }} — {{ s.ref }}</li>{% endfor %}
</ul>
<div class="footer">本报告由 litigation-risk-monitor 技能自动生成，事实依据来自 Patsnap 与公开网络信息，不构成法律意见。</div>

<!-- 弹窗 JS -->
<script>
function openModal(id){ var m=document.getElementById(id); if(m){ m.classList.add('open'); document.body.style.overflow='hidden'; } }
function closeModal(el){ el.classList.remove('open'); document.body.style.overflow=''; }
document.addEventListener('keydown',function(e){ if(e.key==='Escape'){ document.querySelectorAll('.modal-overlay.open').forEach(function(m){ m.classList.remove('open'); }); document.body.style.overflow=''; } });
</script>
</body></html>
"""


# ─────────────────────────────────────────────
# render() 函数 + main() 入口
# ─────────────────────────────────────────────

def render(data: dict, lang: str = "zh") -> str:
    if Template is None:
        raise RuntimeError("jinja2 未安装：请用 runtime.apply_sync 安装后重试")
    tpl = Template(HTML_SKELETON)
    import json as _json
    tpl.globals["tojson"] = lambda v: _json.dumps(v, ensure_ascii=False)
    return tpl.render(
        lang=lang,
        generated_at=data.get("generated_at") or _dt.datetime.utcnow().strftime("%Y-%m-%d %H:%MZ"),
        overview=data.get("overview", {}),
        family_basic=data.get("family_basic", {
            "geo": [], "ipc": [], "legal": [], "legal_detail": [],
            "geo_analysis": "", "claim_comparison": [],
        }),
        # v2 新增：主要涉诉专利列表（含附图 + 同族 + 风险类型）
        litigated_patents=data.get("litigated_patents", []),
        cases=data.get("cases", []),
        inventors=data.get("inventors", []),
        conclusions=data.get("conclusions", {
            "geographic_risk": "",
            "geo_litigation_risk": [],
            "litigation_alert": "",
            "litigation_alert_summary": "",
            "trend_forecast": "",
        }),
        sources=data.get("sources", []),
    )


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True, help="聚合后的报告数据 JSON 路径")
    p.add_argument("--out", required=True, help="输出 HTML 路径")
    p.add_argument("--lang", default="zh")
    a = p.parse_args(argv)

    data = json.loads(Path(a.data).read_text(encoding="utf-8"))
    html = render(data, lang=a.lang)
    out_path = Path(a.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"[render_report] wrote {out_path} ({len(html):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
