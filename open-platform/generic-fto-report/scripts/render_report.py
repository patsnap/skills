"""
render_report.py
================
将 FTO 分析结果渲染为美观的 HTML 格式报告。

主函数：
    render_html_report(
        fto_result, patent_list, features, queries, title, output_path,
        claim_chart_results=None, candidates=None
    )

Fix #6：全面增加空值保护 _safe_str() / _safe_int()，避免 tech_summary 等字段
        返回奇怪结构时抛出 AttributeError。
Fix #8：新增 Section 6"低风险/已排除专利"汇总表，展示完整 FTO 视角。
"""

import html
import json
from datetime import datetime
from pathlib import Path


# ── 安全转换工具（Fix #6）────────────────────────────────────────────────────

def _safe_str(val, default: str = "") -> str:
    """任意类型安全转字符串，None / dict / list 都不会抛出"""
    if val is None:
        return default
    if isinstance(val, (dict, list)):
        try:
            return json.dumps(val, ensure_ascii=False)
        except Exception:
            return str(val)
    return str(val)


def _safe_int(val, default: int = 0) -> int:
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


# ── 风险等级颜色映射 ──────────────────────────────────────────────────────────
RISK_COLOR = {
    "High":    ("#dc2626", "#fef2f2", "高风险"),
    "Medium":  ("#d97706", "#fffbeb", "中风险"),
    "Low":     ("#16a34a", "#f0fdf4", "低风险"),
    "Unknown": ("#6b7280", "#f9fafb", "未知"),
    "Pending": ("#6b7280", "#f9fafb", "待比对"),
}


def _esc(text) -> str:
    """HTML 转义（Fix #6：先过 _safe_str）"""
    return html.escape(_safe_str(text))


def _risk_badge(risk_level: str) -> str:
    color, bg, label = RISK_COLOR.get(risk_level, ("#6b7280", "#f9fafb", _safe_str(risk_level)))
    return (
        f'<span style="background:{bg};color:{color};border:1px solid {color};'
        f'border-radius:4px;padding:2px 8px;font-size:12px;font-weight:600;">'
        f'{label}</span>'
    )


def _score_bar(score, max_score: int = 100) -> str:
    score = _safe_int(score)
    pct   = min(max(int(score / max_score * 100), 0), 100)
    color = "#dc2626" if pct >= 80 else "#d97706" if pct >= 50 else "#16a34a"
    return (
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<div style="flex:1;background:#e5e7eb;border-radius:4px;height:8px;">'
        f'<div style="width:{pct}%;background:{color};height:8px;border-radius:4px;"></div>'
        f'</div>'
        f'<span style="font-size:12px;color:{color};font-weight:600;">{score}</span>'
        f'</div>'
    )


# ── 主渲染函数 ────────────────────────────────────────────────────────────────

def render_html_report(
    fto_result: dict,
    patent_list: list[dict],
    features: list[dict],
    queries: dict[str, str],
    title: str,
    output_path: str,
    claim_chart_results: list[dict] | None = None,
    candidates: list[dict] | None = None,
) -> None:
    """
    生成完整的 HTML FTO 分析报告并写入文件。
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 优先使用外部传入的 claim_chart_results，否则从 fto_result 取
    if claim_chart_results is not None:
        final_results = claim_chart_results
    else:
        final_results = (
            fto_result.get("_selected_final_res")
            or fto_result.get("analyzed_patents")
            or fto_result.get("final_result", [])
        )
    if not isinstance(final_results, list):
        final_results = []

    report_url = _safe_str(fto_result.get("_report_url", ""))

    # ── 概要统计 ─────────────────────────────────────────────────────────────
    total_patents = len(patent_list)
    high_count    = sum(1 for r in final_results if _safe_str(r.get("risk_level")) == "High")
    medium_count  = sum(1 for r in final_results if _safe_str(r.get("risk_level")) == "Medium")
    low_count     = sum(1 for r in final_results if _safe_str(r.get("risk_level")) == "Low")
    analyzed      = len(final_results)

    sections: list[str] = []

    # ── Section 1：概要 ───────────────────────────────────────────────────────
    sections.append(f"""
    <section class="section">
      <h2 class="section-title">📊 分析概要</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-num">{total_patents}</div>
          <div class="stat-label">检索到专利数</div>
        </div>
        <div class="stat-card">
          <div class="stat-num">{analyzed}</div>
          <div class="stat-label">重点比对专利</div>
        </div>
        <div class="stat-card stat-high">
          <div class="stat-num">{high_count}</div>
          <div class="stat-label">高风险专利</div>
        </div>
        <div class="stat-card stat-medium">
          <div class="stat-num">{medium_count}</div>
          <div class="stat-label">中风险专利</div>
        </div>
        <div class="stat-card stat-low">
          <div class="stat-num">{low_count}</div>
          <div class="stat-label">低风险专利</div>
        </div>
      </div>
      {f'<div class="report-link-box"><a href="{_esc(report_url)}" target="_blank" class="btn-primary">📄 下载完整 FTO 报告（智慧芽原版）</a></div>' if report_url else ''}
    </section>
    """)

    # ── Section 2：技术特征与关键词 ───────────────────────────────────────────
    feat_rows = ""
    for f in features:
        badge = (
            '<span class="badge badge-important">重要</span>'
            if f.get("type") == "important"
            else '<span class="badge badge-normal">普通</span>'
        )
        orig_kws = " / ".join(_esc(k) for k in (f.get("keywords") or []))
        exp_kws  = " / ".join(_esc(k) for k in (f.get("expanded_keywords") or f.get("keywords") or []))
        feat_rows += f"""
        <tr>
          <td>{badge} {_esc(f.get('type_label',''))}</td>
          <td class="desc-cell">{_esc(f.get('description',''))}</td>
          <td class="kw-cell">{orig_kws}</td>
          <td class="kw-cell">{exp_kws}</td>
        </tr>"""

    sections.append(f"""
    <section class="section">
      <h2 class="section-title">🔍 技术特征与扩展关键词</h2>
      <table class="data-table">
        <thead>
          <tr><th>特征类型</th><th>技术特征描述</th><th>原始关键词</th><th>扩展关键词（P070）</th></tr>
        </thead>
        <tbody>{feat_rows}</tbody>
      </table>
    </section>
    """)

    # ── Section 3：检索式 ─────────────────────────────────────────────────────
    query_blocks = ""
    for qname, qtext in queries.items():
        query_blocks += f"""
        <div class="query-block">
          <div class="query-label">{_esc(qname)}</div>
          <pre class="query-text">{_esc(qtext)}</pre>
        </div>"""

    sections.append(f"""
    <section class="section">
      <h2 class="section-title">📋 专利检索式</h2>
      {query_blocks}
    </section>
    """)

    # ── Section 4：专利清单（前 30 条预览）─────────────────────────────────────
    preview_patents = patent_list[:30]
    pat_rows = ""
    for i, p in enumerate(preview_patents, 1):
        pat_rows += f"""
        <tr>
          <td style="text-align:center;">{i}</td>
          <td class="mono">{_esc(p.get('pn', ''))}</td>
          <td>{_esc(p.get('title', '') or p.get('patsnap_title', ''))}</td>
          <td>{_esc(_safe_str(p.get('current_assignee') or p.get('original_assignee', '')))}</td>
          <td>{_esc(_safe_str(p.get('pbdt', '') or p.get('apdt', '')))}</td>
        </tr>"""

    more_hint = (
        f'<p class="hint">仅展示前 30 条，完整清单（{total_patents} 条）见 patent_list.json</p>'
        if total_patents > 30 else ""
    )

    sections.append(f"""
    <section class="section">
      <h2 class="section-title">📑 专利清单（共 {total_patents} 条）</h2>
      {more_hint}
      <table class="data-table">
        <thead>
          <tr><th>#</th><th>公开号</th><th>标题</th><th>申请人</th><th>公开/申请日</th></tr>
        </thead>
        <tbody>{pat_rows}</tbody>
      </table>
    </section>
    """)

    # ── Section 5：FTO 比对结果（高/中风险）────────────────────────────────────
    high_medium = [r for r in final_results if _safe_str(r.get("risk_level")) in ("High", "Medium")]
    result_cards = ""
    for idx, item in enumerate(high_medium, 1):
        risk_level  = _safe_str(item.get("risk_level"), "Low")
        patent_id   = _esc(item.get("patent_id", "") or item.get("pn", ""))
        risk_badge  = _risk_badge(risk_level)
        pub_score   = _safe_int(item.get("public_score", 0))
        match_num   = _safe_int(item.get("feature_match_num", 0))
        doc_summary = _esc(item.get("document") or item.get("risk_summary") or "")

        # 权利要求展示
        claims_html = ""
        # 优先从 features_comparison 取，其次从 claim1 字段取
        claim1_text = _safe_str(item.get("claim1", ""))
        if claim1_text:
            claims_html = f"""
            <div class="claim-item">
              <span class="claim-num">权利要求 1</span>
              <p class="claim-text">{_esc(claim1_text[:800])}</p>
            </div>"""
        for claim in (item.get("claims") or [])[:3]:
            if not isinstance(claim, dict):
                continue
            claims_html += f"""
            <div class="claim-item">
              <span class="claim-num">权利要求 {_esc(claim.get('claim_num', ''))}</span>
              <p class="claim-text">{_esc(claim.get('claim_text', ''))}</p>
            </div>"""

        # 技术特征比对
        feat_compare_rows = ""
        for fc in (item.get("features_comparison") or item.get("features") or [])[:5]:
            if not isinstance(fc, dict):
                continue
            similar_icon  = "✅" if fc.get("similar") or fc.get("match_type") == "identical" else "❌"
            score_html    = _score_bar(fc.get("score", 0))
            claim_feature = _esc(fc.get("claim_feature") or fc.get("tech_feature", ""))
            prod_feature  = _esc(fc.get("product_feature") or fc.get("comparison_feature", ""))
            reasoning     = _esc(fc.get("reasoning", ""))
            feat_compare_rows += f"""
            <tr>
              <td style="text-align:center;">{similar_icon}</td>
              <td class="desc-cell">{claim_feature}</td>
              <td class="desc-cell">{prod_feature}</td>
              <td style="width:120px;">{score_html}</td>
              <td class="desc-cell">{reasoning}</td>
            </tr>"""

        # 比对结论（Fix #6：安全取值）
        conclusion = item.get("conclusion") or {}
        if isinstance(conclusion, dict):
            conclusion_text = _esc(
                conclusion.get("risk_summary") or conclusion.get("zh") or ""
            )
            recommendation  = _esc(conclusion.get("recommendation", ""))
            inf_type        = _esc(conclusion.get("infringement_type", ""))
        else:
            conclusion_text = _esc(_safe_str(conclusion))
            recommendation  = ""
            inf_type        = ""

        bcolor, bbg, _ = RISK_COLOR.get(risk_level, ("#6b7280", "#f9fafb", ""))
        result_cards += f"""
        <div class="result-card" style="border-left:4px solid {bcolor};">
          <div class="result-header">
            <span class="result-num">#{idx}</span>
            <span class="patent-id">{patent_id}</span>
            {risk_badge}
            {'<span class="pub-score">公开度: ' + str(pub_score) + '</span>' if pub_score else ''}
            {'<span class="match-num">匹配特征: ' + str(match_num) + '</span>' if match_num else ''}
            {'<span class="inf-type">侵权类型: ' + inf_type + '</span>' if inf_type else ''}
          </div>
          {'<p class="doc-summary">' + doc_summary + '</p>' if doc_summary else ''}

          {'<div class="subsection"><h4>权利要求摘录</h4>' + claims_html + '</div>' if claims_html else ''}

          {'<div class="subsection"><h4>技术特征比对（前5条）</h4><table class="data-table"><thead><tr><th>匹配</th><th>权利要求特征</th><th>标的产品特征</th><th>相似度</th><th>分析理由</th></tr></thead><tbody>' + feat_compare_rows + '</tbody></table></div>' if feat_compare_rows else ''}

          {'<div class="subsection conclusion-box"><h4>比对结论</h4><p>' + conclusion_text + '</p>' + ('<p class="recommendation">💡 建议：' + recommendation + '</p>' if recommendation else '') + '</div>' if conclusion_text else ''}
        </div>"""

    sections.append(f"""
    <section class="section">
      <h2 class="section-title">⚠️ FTO 比对结果（高风险 / 中风险专利）</h2>
      {result_cards if result_cards else '<p class="hint">暂无高/中风险专利</p>'}
    </section>
    """)

    # ── Section 6：低风险/已排除专利汇总表（Fix #8）────────────────────────────
    low_unknown = [
        r for r in final_results
        if _safe_str(r.get("risk_level")) in ("Low", "Unknown", "Pending")
    ]
    low_rows = ""
    for i, item in enumerate(low_unknown, 1):
        pn    = _esc(item.get("pn", "") or item.get("patent_id", ""))
        title_text = _esc(item.get("title", "") or item.get("patsnap_title", ""))
        rl    = _safe_str(item.get("risk_level", "Low"))
        conclusion = item.get("conclusion") or {}
        reason = ""
        if isinstance(conclusion, dict):
            reason = _esc(conclusion.get("risk_summary") or conclusion.get("recommendation", ""))
        else:
            reason = _esc(_safe_str(conclusion))
        low_rows += f"""
        <tr>
          <td style="text-align:center;">{i}</td>
          <td class="mono">{pn}</td>
          <td>{title_text}</td>
          <td>{_risk_badge(rl)}</td>
          <td class="desc-cell">{reason if reason else '核心技术特征不匹配，可基本排除侵权风险'}</td>
        </tr>"""

    sections.append(f"""
    <section class="section">
      <h2 class="section-title">✅ 低风险 / 已排除专利（{len(low_unknown)} 件）</h2>
      <p class="hint">以下专利已完成侵权比对，核心技术特征差异明显，风险较低，仅作记录留存。</p>
      {'<table class="data-table"><thead><tr><th>#</th><th>公开号</th><th>标题</th><th>风险等级</th><th>排除理由</th></tr></thead><tbody>' + low_rows + '</tbody></table>' if low_rows else '<p class="hint">无低风险专利记录</p>'}
    </section>
    """)

    # ── Section 7：免责声明 ───────────────────────────────────────────────────
    sections.append("""
    <section class="section disclaimer">
      <h2 class="section-title">📌 免责声明</h2>
      <p>本报告由自动化工具辅助生成，仅供参考，不构成法律意见。专利侵权判断应由具备资质的专利律师或专利代理机构出具正式法律意见。请在做出商业决策前咨询专业法律顾问。</p>
      <p style="margin-top:8px;color:#94a3b8;font-size:12px;">数据来源：智慧芽 PatSnap OpenAPI（P070 / P002 / P018 / AI07）| AI07 侵权比对通过 zhihuiya-local MCP ai_chat 接口真实调用</p>
    </section>
    """)

    # ══════════════════════════════════════════════════════════════════════════
    # 完整 HTML 拼装
    # ══════════════════════════════════════════════════════════════════════════

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_esc(title)}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                   "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      font-size: 14px; line-height: 1.6;
      background: #f1f5f9; color: #1e293b;
    }}
    .page-header {{
      background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
      color: #fff; padding: 32px 40px; margin-bottom: 0;
    }}
    .page-header h1 {{ font-size: 24px; font-weight: 700; margin-bottom: 6px; }}
    .page-header .meta {{ font-size: 12px; opacity: .8; }}
    .container {{ max-width: 1280px; margin: 24px auto; padding: 0 24px; }}
    .section {{
      background: #fff; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,.08);
      padding: 24px 28px; margin-bottom: 20px;
    }}
    .section-title {{
      font-size: 16px; font-weight: 700; color: #1e3a5f;
      padding-bottom: 10px; border-bottom: 2px solid #e2e8f0; margin-bottom: 16px;
    }}
    .stats-grid {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; }}
    .stat-card {{
      flex: 1; min-width: 100px; background: #f8fafc;
      border: 1px solid #e2e8f0; border-radius: 8px;
      padding: 16px; text-align: center;
    }}
    .stat-num {{ font-size: 32px; font-weight: 800; color: #1e3a5f; }}
    .stat-label {{ font-size: 12px; color: #64748b; margin-top: 4px; }}
    .stat-high .stat-num {{ color: #dc2626; }}
    .stat-medium .stat-num {{ color: #d97706; }}
    .stat-low .stat-num {{ color: #16a34a; }}
    .data-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .data-table th {{
      background: #f1f5f9; color: #475569; font-weight: 600;
      padding: 10px 12px; border: 1px solid #e2e8f0; text-align: left;
    }}
    .data-table td {{
      padding: 9px 12px; border: 1px solid #e2e8f0; vertical-align: top;
    }}
    .data-table tr:nth-child(even) td {{ background: #f8fafc; }}
    .desc-cell {{ max-width: 280px; }}
    .kw-cell {{ max-width: 200px; word-break: break-all; color: #0369a1; }}
    .mono {{ font-family: monospace; font-size: 12px; }}
    .badge {{ padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
    .badge-important {{ background: #fef2f2; color: #dc2626; border: 1px solid #dc2626; }}
    .badge-normal {{ background: #f0f9ff; color: #0369a1; border: 1px solid #0369a1; }}
    .query-block {{ margin-bottom: 14px; }}
    .query-label {{ font-weight: 600; color: #1e3a5f; margin-bottom: 4px; font-size: 13px; }}
    .query-text {{
      background: #1e293b; color: #e2e8f0;
      padding: 12px 16px; border-radius: 6px;
      font-size: 12px; white-space: pre-wrap; word-break: break-all;
      font-family: "Courier New", monospace; overflow-x: auto;
    }}
    .result-card {{
      border: 1px solid #e2e8f0; border-radius: 8px;
      padding: 20px; margin-bottom: 18px;
    }}
    .result-header {{
      display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
      margin-bottom: 10px;
    }}
    .result-num {{ font-weight: 800; font-size: 18px; color: #1e3a5f; }}
    .patent-id {{ font-family: monospace; font-size: 13px; color: #0369a1; }}
    .pub-score, .match-num, .inf-type {{ font-size: 12px; color: #64748b; }}
    .doc-summary {{ color: #475569; margin-bottom: 12px; font-size: 13px; }}
    .subsection {{ margin-top: 14px; }}
    .subsection h4 {{
      font-size: 13px; font-weight: 600; color: #475569;
      margin-bottom: 8px; padding-bottom: 4px; border-bottom: 1px solid #e2e8f0;
    }}
    .claim-item {{ margin-bottom: 8px; }}
    .claim-num {{
      font-size: 11px; font-weight: 600; background: #dbeafe;
      color: #1d4ed8; padding: 2px 7px; border-radius: 4px;
    }}
    .claim-text {{
      font-size: 12px; color: #374151; margin-top: 4px;
      padding-left: 8px; border-left: 2px solid #bfdbfe;
    }}
    .conclusion-box {{
      background: #f0fdf4; border: 1px solid #bbf7d0;
      border-radius: 6px; padding: 12px 16px;
    }}
    .conclusion-box h4 {{ color: #166534; border-color: #bbf7d0; }}
    .conclusion-box p {{ font-size: 13px; color: #166534; line-height: 1.8; }}
    .recommendation {{ color: #0369a1 !important; margin-top: 6px; }}
    .hint {{ color: #94a3b8; font-size: 12px; margin-bottom: 10px; }}
    .report-link-box {{ margin-top: 14px; }}
    .btn-primary {{
      display: inline-block; background: #2563eb; color: #fff;
      padding: 8px 20px; border-radius: 6px; text-decoration: none;
      font-size: 13px; font-weight: 600;
    }}
    .btn-primary:hover {{ background: #1d4ed8; }}
    .disclaimer p {{ color: #64748b; font-size: 13px; }}
    @media print {{
      body {{ background: #fff; }}
      .query-text {{ color: #000; background: #f3f4f6; }}
    }}
  </style>
</head>
<body>
  <header class="page-header">
    <h1>{_esc(title)}</h1>
    <div class="meta">生成时间：{now} &nbsp;|&nbsp; 数据来源：智慧芽 PatSnap OpenAPI（P070 / P002 / P018 / AI07）</div>
  </header>
  <div class="container">
    {"".join(sections)}
  </div>
</body>
</html>"""

    output_file = Path(output_path)
    output_file.write_text(html_content, encoding="utf-8")
    print(f"[render_report] HTML 报告已写入: {output_file.resolve()}")
