"""
fto-review output generator  —  v8.1

Changes:
  - CSS 固定存放在 assets/fto_report.css，生成时原样内嵌到 HTML
  - 删除内联样式属性，防止每次生成 HTML 样式漂移
  - 动态视觉状态仅通过固定 class 切换：grade-* / recall-* / risk-* / pct-*
  - 仅生成正式 HTML；harness 作为独立后置检查，不在报告生成时自动执行
"""

from __future__ import annotations

import datetime as _dt
import html
import json
import sys
from pathlib import Path
from typing import Any

# CSS 文件相对于本脚本的路径
_SCRIPT_DIR = Path(__file__).parent
_CSS_SRC = _SCRIPT_DIR.parent / "assets" / "fto_report.css"

MANDATORY_MODULES = [
    "执行摘要（含独立验证摘要 + 工具可用性说明）",
    "三层审核总览（事实层/法律判断层/决策可用层）",
    "① 检索主题符合性评价",
    "② 检索范围全面性评价",
    "独立检索验证结果（漏检核查或验证缺口）",
    "③ 技术比对分析严谨性评价",
    "④ 高风险专利数量及清单",
    "⑤ 中风险专利数量及清单",
    "⑥ 低风险专利数量及清单",
    "⑦ 应对措施是否明确具体可靠",
    "⑧ 风险规避建议清单",
    "四维度详细评估得分 + 综合问题清单",
    "审核结论与改进建议",
]

METHODOLOGY_LAYERS = ["事实层", "法律判断层", "决策可用层"]


# ── 固定 class 辅助（不输出内联样式） ───────────────────────────────────────
def grade_class(grade: str) -> str:
    return {
        "优秀": "grade-excellent",
        "良好": "grade-good",
        "合格": "grade-pass",
        "需改进": "grade-warning",
        "不合格": "grade-fail",
        "未评分": "grade-none",
    }.get(grade, "grade-none")


def recall_class(rating: str) -> str:
    if "充分" in rating:
        return "recall-ok"
    if "偏低" in rating:
        return "recall-low"
    if "严重" in rating:
        return "recall-bad"
    return "recall-none"


def pct_class(value: int) -> str:
    bucket = int(round(max(0, min(100, value)) / 10) * 10)
    return f"pct-{bucket}"


# ── 数据加载 ────────────────────────────────────────────────────────────────
def empty_data() -> dict[str, Any]:
    today = _dt.date.today().isoformat()
    return {
        "report_title": "FTO报告质量评估报告",
        "subject_report": "未填写",
        "submitter": "未填写",
        "product_description": "未填写",
        "target_market": "未填写",
        "scenario": "未识别",
        "exhibition_applicable": False,
        "industry_profile": "未识别",
        "maturity": "未判断",
        "audit_date": today,
        "auditor": "fto-review v8.1",
        "confidentiality": "内部使用",
        "total_score": None,
        "grade": "未评分",
        "conclusion": "未形成结论",
        "methodology_layers": {
            "事实层": {"status": "待评估", "confidence": "未评估", "findings": "待填写"},
            "法律判断层": {"status": "待评估", "confidence": "未评估", "findings": "待填写"},
            "决策可用层": {"status": "待评估", "confidence": "未评估", "findings": "待填写"},
        },
        "verification": {
            "status": "未完成独立检索验证",
            "tool_status": "未提供",
            "original_pool_count": None,
            "independent_pool_count": None,
            "overlap_count": None,
            "estimated_total": None,
            "recall_rate": None,
            "recall_rating": "未验证",
            "top_ipcs": [],
            "top_assignees": [],
            "omissions": [],
            "validity_checks": [],
            "independent_pool_sample": [],
            "note": "未获得真实独立专利池，不计算召回率。",
        },
        "dimensions": [
            {"name": "搜索策略质量", "score": None, "max": 25, "comment": "待评估"},
            {"name": "专利分析深度", "score": None, "max": 30, "comment": "待评估"},
            {"name": "法律意见专业性", "score": None, "max": 25, "comment": "待评估"},
            {"name": "文档记录完整性", "score": None, "max": 20, "comment": "待评估"},
        ],
        "modules": {name: "待填写" for name in MANDATORY_MODULES},
        "risk_lists": {"high": [], "medium": [], "low": []},
        "countermeasures": [],
        "issues": {"critical": [], "important": [], "suggestions": []},
        "mandatory_actions": [],
    }


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def load_data(json_path: str | None) -> dict[str, Any]:
    data = empty_data()
    if not json_path:
        print("[INFO] 未传入 JSON 数据文件，生成空白审核骨架。")
        return data
    with open(json_path, "r", encoding="utf-8") as f:
        return deep_merge(data, json.load(f))


# ── 文本辅助 ────────────────────────────────────────────────────────────────
def score_text(value: Any, max_score: Any = None) -> str:
    if value is None or value == "":
        return "未评分"
    return f"{value}/{max_score}" if max_score else str(value)


def pct(score: Any, max_score: Any) -> int:
    try:
        return max(0, min(100, round(float(score) / float(max_score) * 100)))
    except Exception:
        return 0


def recall_pct(rate_str: str | None) -> int:
    if not rate_str:
        return 0
    try:
        return max(0, min(100, round(float(str(rate_str).replace("%", "")))))
    except Exception:
        return 0


def e(value: Any) -> str:
    return html.escape("" if value is None else str(value))


# ── 行生成辅助 ──────────────────────────────────────────────────────────────
def issue_rows(items: list[dict[str, Any]], empty: str) -> str:
    if not items:
        return f"<tr><td colspan='3'>{e(empty)}</td></tr>"
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{e(item.get('id', '-'))}</td>"
            f"<td>{e(item.get('desc', item.get('description', '')))}</td>"
            f"<td>{e(item.get('impact', item.get('suggestion', '-')))}</td>"
            "</tr>"
        )
    return "".join(rows)


def patent_rows(items: list[dict[str, Any]], empty: str) -> str:
    if not items:
        return f"<tr><td colspan='5'>{e(empty)}</td></tr>"
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{e(item.get('patent_no', item.get('no', '-')))}</td>"
            f"<td>{e(item.get('title', '-'))}</td>"
            f"<td>{e(item.get('assignee', '-'))}</td>"
            f"<td>{e(item.get('status', '-'))}</td>"
            f"<td>{e(item.get('basis', item.get('risk_basis', '-')))}</td>"
            "</tr>"
        )
    return "".join(rows)


def omission_rows(items: list[dict[str, Any]]) -> str:
    """遗漏专利行，高/中风险通过固定 class 高亮。"""
    if not items:
        return "<tr><td colspan='5'>未发现遗漏专利</td></tr>"
    rows = []
    for item in items:
        risk = str(item.get("risk_level", "")).lower()
        if "high" in risk or "高" in risk:
            row_class = "risk-high"
        elif "medium" in risk or "中" in risk:
            row_class = "risk-medium"
        else:
            row_class = "risk-normal"
        pno = item.get("patent_no", "-")
        url = item.get("url", "")
        pno_cell = f'<a href="{e(url)}" target="_blank">{e(pno)}</a>' if url else e(pno)
        rows.append(
            f"<tr class='{row_class}'>"
            f"<td>{pno_cell}</td>"
            f"<td>{e(item.get('title', '-'))}</td>"
            f"<td>{e(item.get('assignee', '-'))}</td>"
            f"<td>{e(item.get('status', '-'))}</td>"
            f"<td>{e(item.get('source', '独立检索'))}</td>"
            "</tr>"
        )
    return "".join(rows)


def recall_gauge(rate_str: str | None, rating: str) -> str:
    """召回率仪表盘，宽度和颜色均通过固定 class 控制。"""
    pct_val = recall_pct(rate_str)
    r_class = recall_class(rating)
    return (
        f"<div class='gauge-wrap {r_class}'>"
        "<div class='gauge-label'>原报告召回率估算</div>"
        f"<div class='gauge-bar'><div class='gauge-fill {pct_class(pct_val)}'></div></div>"
        f"<div class='gauge-value'>{e(rate_str or '未验证')} &nbsp; {e(rating)}</div>"
        "</div>"
    )


# ── CSS 注入：从固定 CSS 文件原样内嵌到 HTML ───────────────────────────────
def _load_fixed_css() -> str:
    """读取唯一固定样式源。CSS 缺失时直接失败，避免产出无样式报告。"""
    if not _CSS_SRC.exists():
        raise FileNotFoundError(f"固定CSS源文件未找到：{_CSS_SRC}")
    return _CSS_SRC.read_text(encoding="utf-8")


# ── HTML 生成 ───────────────────────────────────────────────────────────────
def generate_html(data: dict[str, Any], out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fixed_css = _load_fixed_css()

    grade = str(data.get("grade", "未评分"))
    g_class = grade_class(grade)

    dims = []
    for dim in data["dimensions"]:
        width = pct(dim.get("score"), dim.get("max"))
        dims.append(
            f"<div class='dim'><span>{e(dim.get('name'))}</span>"
            f"<div class='bar'><i class='bar-fill {g_class} {pct_class(width)}'></i></div>"
            f"<b>{e(score_text(dim.get('score'), dim.get('max')))}</b>"
            f"<small>{e(dim.get('comment', ''))}</small></div>"
        )

    def module_text(name: str) -> str:
        return e(data["modules"].get(name, "原报告未提供，待审核补充。"))

    layer_rows = []
    for layer in METHODOLOGY_LAYERS:
        info = data.get("methodology_layers", {}).get(layer, {})
        layer_rows.append(
            "<tr>"
            f"<td>{e(layer)}</td>"
            f"<td>{e(info.get('status', '待评估'))}</td>"
            f"<td>{e(info.get('confidence', '未评估'))}</td>"
            f"<td>{e(info.get('findings', '待填写'))}</td>"
            "</tr>"
        )

    v = data["verification"]
    actions = data.get("mandatory_actions") or ["待填写整改行动"]
    action_items = "".join(f"<li>{e(action)}</li>" for action in actions)

    gauge_html = recall_gauge(v.get("recall_rate"), v.get("recall_rating", "未验证"))
    omission_html = omission_rows(v.get("omissions", []))

    top_ipcs = v.get("top_ipcs") or []
    top_assignees = v.get("top_assignees") or []
    assignee_str = "、".join(top_assignees) if top_assignees else "未提取"

    html_text = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(data['report_title'])}</title>
<style id="fto-fixed-css" data-version="v7.1-fixed">
{fixed_css}
</style>
</head>
<body>
<header class="hero">
  <h1>{e(data['report_title'])}</h1>
  <p class="subtitle">FTO report quality assessment · fto-review v7.1-fixed</p>
  <div class="meta">
    <div><span>被审核报告</span>{e(data['subject_report'])}</div>
    <div><span>目标市场</span>{e(data['target_market'])}</div>
    <div><span>审核场景</span>{e(data['scenario'])}</div>
    <div><span>审核日期</span>{e(data['audit_date'])}</div>
  </div>
</header>
<main class="wrap">
  <section class="card">
    <h2><span class="chapter-no">1.</span>报告头部与基本信息</h2>
    <table>
      <tr><th>项目</th><th>内容</th></tr>
      <tr><td>被审核报告</td><td>{e(data['subject_report'])}</td></tr>
      <tr><td>提交方</td><td>{e(data['submitter'])}</td></tr>
      <tr><td>产品/技术描述</td><td>{e(data['product_description'])}</td></tr>
      <tr><td>目标市场</td><td>{e(data['target_market'])}</td></tr>
      <tr><td>审核场景</td><td>{e(data['scenario'])}</td></tr>
      <tr><td>展会专项</td><td>{'适用' if data.get('exhibition_applicable') else 'N/A'}</td></tr>
      <tr><td>行业领域</td><td>{e(data['industry_profile'])}</td></tr>
      <tr><td>保密等级</td><td>{e(data['confidentiality'])}</td></tr>
      <tr><td>审核引擎</td><td>{e(data.get('auditor', 'fto-review v7.1'))}</td></tr>
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">2.</span>执行摘要</h2>
    <div class="score {g_class}">{e(score_text(data.get('total_score'), 100))}</div>
    <p class="grade-label">质量等级：{e(grade)}</p>
    <p><b>审核结论：</b>{e(data.get('conclusion'))}</p>
    <p><b>报告成熟度：</b>{e(data.get('maturity'))}</p>
  </section>

  <section class="card">
    <h2><span class="chapter-no">3.</span>三层审核总览</h2>
    <table>
      <tr><th>层级</th><th>状态</th><th>置信度</th><th>核心发现</th></tr>
      {''.join(layer_rows)}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">4.</span>四维度评分</h2>
    {''.join(dims)}
  </section>

  <section class="card verify">
    <h2><span class="chapter-no">5.</span>独立检索验证与漏检核查</h2>
    {gauge_html}
    <table>
      <tr><th>指标</th><th>结果</th></tr>
      <tr><td>验证状态</td><td>{e(v.get('status'))}</td></tr>
      <tr><td>检索轨道明细</td><td>{e(v.get('tool_status'))}</td></tr>
      <tr><td>原报告专利池</td><td>{e(score_text(v.get('original_pool_count')))}</td></tr>
      <tr><td>独立检索专利池</td><td>{e(score_text(v.get('independent_pool_count')))}</td></tr>
      <tr><td>重叠数量（n_C）</td><td>{e(score_text(v.get('overlap_count')))}</td></tr>
      <tr><td>Chapman估算总量（N̂）</td><td>{e(score_text(v.get('estimated_total')))}</td></tr>
      <tr><td>原报告召回率</td><td><b>{e(v.get('recall_rate', '未验证'))}</b></td></tr>
      <tr><td>召回率评级</td><td><b>{e(v.get('recall_rating'))}</b></td></tr>
      <tr><td>独立发现 TOP IPC</td><td>{''.join(f'<span class="ipc-tag">{e(c)}</span>' for c in top_ipcs) or '未提取'}</td></tr>
      <tr><td>主要申请人（独立检索）</td><td>{e(assignee_str)}</td></tr>
      <tr><td>估算说明</td><td>{e(v.get('note'))}</td></tr>
    </table>
    <h3>遗漏专利清单 <span class="tag-new">{len(v.get('omissions', []))} 件</span></h3>
    <table>
      <tr><th>专利号</th><th>名称</th><th>申请人</th><th>法律状态</th><th>检索来源</th></tr>
      {omission_html}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">6.</span>检索主题符合性评价</h2>
    <p>{module_text('① 检索主题符合性评价')}</p>
  </section>

  <section class="card">
    <h2><span class="chapter-no">7.</span>检索范围全面性评价</h2>
    <p>{module_text('② 检索范围全面性评价')}</p>
  </section>

  <section class="card">
    <h2><span class="chapter-no">8.</span>技术比对分析严谨性评价</h2>
    <p>{module_text('③ 技术比对分析严谨性评价')}</p>
  </section>

  <section class="card">
    <h2><span class="chapter-no">9.</span>高风险专利数量及清单</h2>
    <p>{module_text('④ 高风险专利数量及清单')}</p>
    <table><tr><th>专利号</th><th>名称</th><th>权利人</th><th>状态</th><th>依据</th></tr>
    {patent_rows(data['risk_lists'].get('high', []), '未识别高风险专利')}</table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">10.</span>中风险专利数量及清单</h2>
    <p>{module_text('⑤ 中风险专利数量及清单')}</p>
    <table><tr><th>专利号</th><th>名称</th><th>权利人</th><th>状态</th><th>依据</th></tr>
    {patent_rows(data['risk_lists'].get('medium', []), '未识别中风险专利')}</table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">11.</span>低风险专利数量及清单</h2>
    <p>{module_text('⑥ 低风险专利数量及清单')}</p>
    <table><tr><th>专利号</th><th>名称</th><th>权利人</th><th>状态</th><th>依据</th></tr>
    {patent_rows(data['risk_lists'].get('low', []), '未识别低风险专利')}</table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">12.</span>应对措施明确具体可靠性评价</h2>
    <p>{module_text('⑦ 应对措施是否明确具体可靠')}</p>
  </section>

  <section class="card mitigation">
    <h2><span class="chapter-no">13.</span>风险规避建议清单</h2>
    <p>{module_text('⑧ 风险规避建议清单')}</p>
  </section>

  <section class="card">
    <h2><span class="chapter-no">14.</span>综合问题清单</h2>
    <h3>严重问题</h3>
    <table><tr><th>编号</th><th>问题</th><th>影响/建议</th></tr>
    {issue_rows(data['issues'].get('critical', []), '未填写严重问题')}</table>
    <h3>重要问题</h3>
    <table><tr><th>编号</th><th>问题</th><th>影响/建议</th></tr>
    {issue_rows(data['issues'].get('important', []), '未填写重要问题')}</table>
    <h3>建议优化</h3>
    <table><tr><th>编号</th><th>建议</th><th>说明</th></tr>
    {issue_rows(data['issues'].get('suggestions', []), '未填写建议优化项')}</table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">15.</span>审核结论与整改行动</h2>
    <p><b>审核结论：</b>{e(data.get('conclusion'))}</p>
    <ol>{action_items}</ol>
  </section>

  <section class="card">
    <h2><span class="chapter-no">16.</span>审核边界与免责声明</h2>
    <p>本报告为FTO质量审核辅助产物，不构成正式法律意见。FTO审核主要覆盖专利自由实施风险；不应推定已覆盖商标、版权、商业秘密、监管合规、产品安全、合同限制等非专利风险。独立检索验证基于智慧芽PatSnap数据库，受限于数据库覆盖范围和检索截止日期。</p>
  </section>
</main>
</body>
</html>"""
    out_path.write_text(html_text, encoding="utf-8")
    print(f"[OK] HTML 报告已生成：{out_path}")
    return out_path


def main() -> None:
    json_path = sys.argv[1] if len(sys.argv) >= 2 else None
    data = load_data(json_path)
    base_dir = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path(__file__).parent.parent / "output"
    base_dir.mkdir(parents=True, exist_ok=True)
    safe_date = str(data.get("audit_date") or _dt.date.today().isoformat()).replace("-", "")
    html_path = base_dir / f"fto_review_report_{safe_date}.html"
    generate_html(data, html_path)
    print("\n输出产物：")
    print(f"   HTML : {html_path}")


if __name__ == "__main__":
    main()
