# HTML 报告完整模板（v5）

生成报告时，复制以下完整 HTML，将所有 `{{占位符}}` 替换为实际分析内容。

**重要：生成报告时必须严格以本文件为准，SKILL.md 文字描述仅供理解，本模板是最终权威。**

## 占位符说明

| 占位符 | 含义 |
|---|---|
| `{{DOC_TITLE}}` | 文档名称或日期标识 |
| `{{DOC_TYPE}}` | 研发周报 / 会议纪要 / 技术方案 |
| `{{SCAN_DATE}}` | 扫描日期，如 2026-05-26 |
| `{{TOTAL_COUNT}}` | 候选技术点总数 |
| `{{RED_COUNT}}` | 立即行动数量（P1优先级） |
| `{{YELLOW_COUNT}}` | 建议推进数量 |
| `{{PENDING_COUNT}}` | 待确认数量 |
| `{{SEARCHED_COUNT}}` | 已完成MCP检索数量 |
| `{{RECOMMEND_COUNT}}` | 推荐建议数量（通常等于RED_COUNT对应的行动项数） |
| `{{TECH_TITLE}}` | 技术点一句话标题 |
| `{{INNOVATION_TYPE}}` | 新方法/新结构/新参数/新效果/新流程/新材料 |
| `{{PROTECT_PATH}}` | 建议路径：申请专利/商业秘密/暂不保护 |
| `{{PROTECT_SUMMARY}}` | 保护建议简短摘要（1行，显示在卡片标题右侧）|
| `{{NOVELTY_LEVEL}}` | 新颖性潜力：高/中/低 |
| `{{COMPLETENESS_LEVEL}}` | 技术完整度：完整/需补充/碎片 |
| `{{CONFIDENCE}}` | 置信度：高/中/低 |
| `{{TECH_PRESSURE}}` | 相对技术压力：高/中/低 |
| `{{NEXT_STEP}}` | 下一步行动简述 |
| `{{SOURCE_QUOTE}}` | 来源证据：文档原始描述引用 |
| `{{CONCLUSION}}` | 建议结论一句话 |
| `{{PROBLEM}}` | 三要素：技术问题 |
| `{{METHOD}}` | 三要素：技术方案/手段 |
| `{{EFFECT}}` | 三要素：技术效果 |
| `{{KEY_BASIS_N}}` | 关键依据第N条 |
| `{{NOVELTY_BASIS}}` | 新颖性潜力判断依据 |
| `{{COMPLETENESS_BASIS}}` | 技术完整度判断依据 |
| `{{PROTECT_TITLE}}` | 保护建议标题 |
| `{{PROTECT_REASON}}` | 保护建议理由 |
| `{{PATENT_NO}}` | 专利公开号 |
| `{{PATENT_URL}}` | 专利链接 URL |
| `{{PATENT_TITLE}}` | 专利标题 |
| `{{PATENT_RELEVANCE}}` | 相关性等级：高度相关/部分相关/背景参考 |
| `{{PATENT_DIFF}}` | 本质区别 |
| `{{PATENT_IMPACT}}` | 对我方影响：构成障碍/需规避/可参考 |
| `{{DIFF_DESC}}` | 与本方案的区别（卡片内简述） |
| `{{QUESTION_N}}` | 待补充问题第N条 |
| `{{ACTION_DESC}}` | 行动队列任务描述 |
| `{{ACTION_OWNER}}` | 负责人角色 |
| `{{ACTION_DEADLINE}}` | 截止时间建议 |

## 卡片评级类名速查

| 评级 | card 类名 | badge 类名 |
|---|---|---|
| 🔴 立即行动 | `priority-red` | `badge-red` |
| 🟡 建议推进 | `priority-yellow` | `badge-yellow` |
| ⚪ 待确认 | `priority-gray` | `badge-gray` |

## 卡片折叠规则（v5 重要）

- **所有卡片默认展开**：`detail-card` 不加 `collapsed` 类，`card-body-wrap` 的 `style` 设为 `max-height:4000px`
- 用户点击卡片标题后触发 `toggleCard()` 收缩
- 禁止对任何卡片设置 `collapsed` 类或 `max-height:0`

---

## 完整 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>研发创新挖掘雷达 — {{DOC_TITLE}}</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
               "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  background: #f0f4f8; color: #1a2233; min-height: 100vh;
}

/* ── Banner（无logo） ── */
.banner {
  background: linear-gradient(135deg, #0d1f3c 0%, #1a3a6b 60%, #1e4d8c 100%);
  padding: 36px 48px 28px; color: #fff; text-align: center;
}
.banner-title { font-size: 26px; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px; }
.banner-tagline {
  font-size: 13px; line-height: 1.8; opacity: 0.82;
  max-width: 640px; margin: 0 auto 18px;
}
.banner-meta { display: flex; gap: 24px; flex-wrap: wrap; font-size: 13px; opacity: 0.85; justify-content: center; }
.banner-meta span { display: flex; align-items: center; gap: 6px; }

/* ── Stats Bar（吸顶，居中文案）── */
.stats-bar {
  position: sticky; top: 0; z-index: 100;
  background: #fff; border-bottom: 1px solid #e2e8f0;
  padding: 16px 48px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  text-align: center;
}
.stats-summary {
  font-size: 14px; color: #334155; line-height: 1.8;
}
.stats-summary .num-red    { font-weight: 800; color: #dc2626; font-size: 16px; }
.stats-summary .num-blue   { font-weight: 800; color: #1a3a6b; font-size: 16px; }
.stats-summary .num-green  { font-weight: 800; color: #059669; font-size: 16px; }
.stats-summary .num-gray   { font-weight: 800; color: #64748b; font-size: 16px; }

/* ── Layout: sidebar + content ── */
.page-body { display: flex; gap: 0; max-width: 1200px; margin: 0 auto; }

/* Left Nav */
.left-nav {
  width: 200px; flex-shrink: 0;
  position: sticky; top: 73px; align-self: flex-start;
  height: calc(100vh - 73px); overflow-y: auto;
  padding: 24px 0 40px 20px;
}
.left-nav-title { font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; padding-left: 8px; }
.nav-item {
  display: block; padding: 7px 8px 7px 10px; border-radius: 7px;
  font-size: 13px; color: #475569; text-decoration: none; line-height: 1.4;
  margin-bottom: 2px; border-left: 3px solid transparent;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
  cursor: pointer;
}
.nav-item:hover { background: #e8edf5; color: #1e3a6b; }
.nav-item.active { background: #eff6ff; color: #1d4ed8; border-left-color: #3b82f6; font-weight: 600; }
.nav-section-label { font-size: 10px; color: #94a3b8; letter-spacing: 0.5px; padding: 10px 8px 4px; text-transform: uppercase; }

/* Main content */
.main { flex: 1; min-width: 0; padding: 32px 24px 64px; }
.section-header { display: flex; align-items: center; gap: 10px; margin: 36px 0 16px; }
.section-icon { font-size: 20px; }
.section-title-main { font-size: 17px; font-weight: 700; color: #0f172a; }
.section-desc { font-size: 13px; color: #64748b; margin-top: 2px; }

/* ── 板块一：候选列表 ── */
.candidate-table-wrap {
  background: #fff; border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07); overflow-x: auto;
}
.candidate-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.candidate-table thead tr { background: #f8fafc; border-bottom: 2px solid #e2e8f0; }
.candidate-table th {
  padding: 12px 14px; text-align: left;
  font-size: 11px; font-weight: 700; color: #64748b;
  text-transform: uppercase; letter-spacing: 0.6px; white-space: nowrap;
}
.candidate-table td { padding: 14px 14px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
.candidate-table tr:last-child td { border-bottom: none; }
.candidate-table tr:hover td { background: #f8fafc; }
.p-badge {
  display: inline-block; padding: 3px 10px; border-radius: 999px;
  font-size: 11px; font-weight: 700; white-space: nowrap;
}
.p-badge.p1 { background: #fee2e2; color: #b91c1c; }
.p-badge.p2 { background: #fef3c7; color: #92400e; }
.p-badge.p3 { background: #f1f5f9; color: #475569; }
.type-tag {
  display: inline-block; padding: 2px 8px; border-radius: 5px;
  font-size: 11px; font-weight: 600; background: #eff6ff; color: #1d4ed8;
}
.progress-group { display: flex; flex-direction: column; gap: 5px; min-width: 120px; }
.progress-row { display: flex; align-items: center; gap: 6px; }
.progress-label { font-size: 10px; color: #94a3b8; width: 32px; flex-shrink: 0; }
.progress-bar-bg { flex: 1; height: 5px; border-radius: 3px; background: #e2e8f0; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 3px; }
.fill-high    { background: #ef4444; width: 90%; }
.fill-mid     { background: #f59e0b; width: 55%; }
.fill-low     { background: #94a3b8; width: 20%; }
.fill-full    { background: #10b981; width: 100%; }
.fill-partial { background: #f59e0b; width: 60%; }
.fill-frag    { background: #94a3b8; width: 25%; }
.level-pill { display: inline-block; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 600; }
.level-pill.high { background: #fee2e2; color: #b91c1c; }
.level-pill.mid  { background: #fef3c7; color: #92400e; }
.level-pill.low  { background: #f0fdf4; color: #166534; }
.next-step-cell { font-size: 12px; color: #475569; max-width: 160px; line-height: 1.5; }

/* ── 可折叠卡片 ── */
.detail-card {
  background: #fff; border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  margin-bottom: 16px; overflow: hidden; border-left: 5px solid #cbd5e1;
}
.detail-card.priority-red    { border-left-color: #ef4444; }
.detail-card.priority-yellow { border-left-color: #f59e0b; }
.detail-card.priority-gray   { border-left-color: #94a3b8; }
.card-toggle { width: 100%; background: none; border: none; cursor: pointer; text-align: left; padding: 0; }

/* 卡片标题行：左侧标题区 + 右侧保护建议摘要 */
.card-header-row {
  background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%);
  padding: 18px 24px; color: #fff;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 20px;
  align-items: center;
}
.card-header-left { min-width: 0; }
.card-conclusion-index { font-size: 11px; font-weight: 600; letter-spacing: 1px; opacity: 0.7; margin-bottom: 5px; text-transform: uppercase; }
.card-conclusion-title { font-size: 17px; font-weight: 700; line-height: 1.4; margin-bottom: 10px; }
.conclusion-meta { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
.conclusion-tag { padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; background: rgba(255,255,255,0.15); color: #fff; }
.conclusion-tag.conf-high  { background: rgba(16,185,129,0.25); }
.conclusion-tag.conf-mid   { background: rgba(245,158,11,0.25); }
.conclusion-tag.conf-low   { background: rgba(148,163,184,0.25); }
.conclusion-tag.press-high { background: rgba(239,68,68,0.25); }
.conclusion-tag.press-mid  { background: rgba(245,158,11,0.2); }
.conclusion-tag.press-low  { background: rgba(16,185,129,0.2); }
.card-next-step { margin-top: 8px; font-size: 12px; opacity: 0.85; display: flex; align-items: center; gap: 6px; }

/* 右侧保护建议摘要框 */
.card-header-right {
  display: flex; flex-direction: column; align-items: flex-end; gap: 10px;
  min-width: 160px; max-width: 220px;
}
.badge-in-card { padding: 6px 16px; border-radius: 999px; font-size: 12px; font-weight: 700; white-space: nowrap; }
.badge-in-card.badge-red    { background: rgba(239,68,68,0.2); color: #fca5a5; }
.badge-in-card.badge-yellow { background: rgba(245,158,11,0.2); color: #fcd34d; }
.badge-in-card.badge-gray   { background: rgba(148,163,184,0.2); color: #cbd5e1; }
.protect-summary-box {
  background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3);
  border-radius: 8px; padding: 8px 12px; text-align: right;
}
.protect-summary-label { font-size: 10px; color: rgba(255,255,255,0.6); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 3px; }
.protect-summary-text { font-size: 12px; color: #6ee7b7; font-weight: 600; line-height: 1.4; }
.collapse-indicator { font-size: 14px; opacity: 0.7; transition: transform 0.2s; }
.detail-card.collapsed .collapse-indicator { transform: rotate(-90deg); }

.card-body-wrap { overflow: hidden; transition: max-height 0.3s ease; }
.detail-card.collapsed .card-body-wrap { max-height: 0 !important; }
.card-body { padding: 20px 24px; display: flex; flex-direction: column; gap: 18px; }

/* 三要素彩色行 */
.three-elements { border-radius: 10px; overflow: hidden; }
.three-elements-title { font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #94a3b8; text-transform: uppercase; padding: 8px 16px; background: #f8fafc; }
.element-row { display: flex; gap: 0; }
.element-label-cell { font-weight: 700; font-size: 12px; padding: 10px 14px; min-width: 60px; flex-shrink: 0; display: flex; align-items: flex-start; }
.element-value-cell { font-size: 13.5px; padding: 10px 16px 10px 0; color: #1e293b; line-height: 1.6; flex: 1; }
.element-row.problem .element-label-cell { background: #fef9c3; color: #854d0e; }
.element-row.problem  { background: #fefce8; }
.element-row.method  .element-label-cell { background: #dbeafe; color: #1e40af; }
.element-row.method   { background: #eff6ff; }
.element-row.effect  .element-label-cell { background: #dcfce7; color: #166534; }
.element-row.effect   { background: #f0fdf4; }
.element-row.inventor .element-label-cell { background: #f3e8ff; color: #6b21a8; }
.element-row.inventor { background: #faf5ff; }

/* 保护建议（详细版）*/
.protect-box { display: flex; align-items: flex-start; gap: 12px; background: #f0fdf4; border-radius: 10px; padding: 14px 16px; }
.protect-icon { font-size: 20px; flex-shrink: 0; margin-top: 1px; }
.protect-title { font-size: 14px; font-weight: 700; color: #166534; }
.protect-reason { font-size: 13px; color: #15803d; margin-top: 4px; line-height: 1.5; }

/* 待补充问题 */
.questions-box { background: #fffbeb; border-radius: 10px; padding: 14px 18px; border: 1px solid #fde68a; }
.questions-title { font-size: 12px; font-weight: 700; color: #92400e; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px; }
.question-item { display: flex; gap: 10px; font-size: 13.5px; color: #78350f; padding: 5px 0; line-height: 1.6; }
.question-num { font-weight: 700; min-width: 24px; color: #d97706; }

/* 评分双列 */
.score-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.score-box { border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }
.score-box-label { font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.score-value { font-size: 15px; font-weight: 700; }
.score-value.red    { color: #ef4444; }
.score-value.yellow { color: #f59e0b; }
.score-value.gray   { color: #94a3b8; }
.score-value.green  { color: #10b981; }
.score-basis { font-size: 12px; color: #64748b; margin-top: 4px; line-height: 1.5; }

/* 现有技术 */
.section-sub-title { font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px; }
.prior-item {
  display: flex; gap: 10px; align-items: flex-start;
  padding: 10px 14px; border-radius: 8px; background: #f8fafc;
  margin-bottom: 7px; font-size: 13px; transition: box-shadow 0.15s;
}
.prior-item:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.prior-item:last-child { margin-bottom: 0; }
.prior-pn { font-weight: 700; color: #1d4ed8; white-space: nowrap; text-decoration: none; flex-shrink: 0; background: #dbeafe; padding: 2px 8px; border-radius: 5px; font-size: 12px; }
.prior-pn:hover { text-decoration: underline; }
.prior-title { color: #334155; flex: 1; }
.prior-diff { color: #64748b; margin-top: 3px; font-size: 12px; }

/* 来源证据 */
.source-quote {
  background: #f8fafc; border-left: 3px solid #94a3b8;
  border-radius: 0 8px 8px 0; padding: 12px 16px;
  font-size: 13px; color: #475569; line-height: 1.7; font-style: italic;
}
.source-quote-label { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; font-style: normal; }

/* ── 行动队列 ── */
.action-queue { background: #fff; border-radius: 14px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); overflow: hidden; }
.action-item { display: flex; gap: 0; align-items: stretch; border-bottom: 1px solid #f1f5f9; }
.action-item:last-child { border-bottom: none; }
.action-color-bar { width: 5px; flex-shrink: 0; }
.action-color-bar.red    { background: #ef4444; }
.action-color-bar.yellow { background: #f59e0b; }
.action-color-bar.gray   { background: #94a3b8; }
.action-content { padding: 16px 20px; flex: 1; display: flex; gap: 16px; align-items: flex-start; }
.action-num { font-size: 18px; font-weight: 800; color: #e2e8f0; min-width: 28px; flex-shrink: 0; line-height: 1; }
.action-main { flex: 1; }
.action-desc { font-size: 14px; color: #0f172a; font-weight: 600; line-height: 1.5; }
.action-meta { display: flex; gap: 16px; margin-top: 6px; flex-wrap: wrap; }
.action-owner { font-size: 12px; color: #64748b; display: flex; align-items: center; gap: 4px; }
.action-deadline { font-size: 12px; font-weight: 600; }
.action-deadline.urgent  { color: #dc2626; }
.action-deadline.normal  { color: #d97706; }
.action-deadline.relaxed { color: #64748b; }

/* ── 外部证据链 ── */
.evidence-table-wrap { background: #fff; border-radius: 14px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); overflow-x: auto; }
.evidence-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.evidence-table thead tr { background: #f8fafc; border-bottom: 2px solid #e2e8f0; }
.evidence-table th { padding: 12px 14px; text-align: left; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.6px; white-space: nowrap; }
.evidence-table td { padding: 12px 14px; border-bottom: 1px solid #f1f5f9; vertical-align: top; }
.evidence-table tr:last-child td { border-bottom: none; }
.evidence-table tr:hover td { background: #f8fafc; }
.relevance-tag { display: inline-block; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 600; }
.relevance-tag.high { background: #fee2e2; color: #b91c1c; }
.relevance-tag.mid  { background: #fef3c7; color: #92400e; }
.relevance-tag.bg   { background: #f1f5f9; color: #475569; }
.impact-tag { display: inline-block; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 600; }
.impact-tag.block { background: #fee2e2; color: #991b1b; }
.impact-tag.avoid { background: #fef3c7; color: #78350f; }
.impact-tag.ref   { background: #f0fdf4; color: #166534; }

/* 免责 */
.disclaimer { margin-top: 24px; padding: 14px 18px; background: #f1f5f9; border-radius: 10px; font-size: 12px; color: #64748b; line-height: 1.7; }
.disclaimer strong { color: #475569; }

@media (max-width: 860px) {
  .page-body { flex-direction: column; }
  .left-nav { width: 100%; position: static; height: auto; padding: 12px 16px; display: flex; flex-wrap: wrap; gap: 8px; }
  .left-nav-title, .nav-section-label { display: none; }
  .nav-item { padding: 5px 10px; margin-bottom: 0; border-left: none; border-bottom: 2px solid transparent; }
  .nav-item.active { border-bottom-color: #3b82f6; }
}
@media (max-width: 640px) {
  .banner { padding: 28px 20px 24px; }
  .stats-bar { padding: 12px 20px; }
  .main { padding: 20px 12px 48px; }
  .card-header-row { grid-template-columns: 1fr; }
  .card-header-right { align-items: flex-start; max-width: 100%; }
  .score-row { grid-template-columns: 1fr; }
  .banner-meta { gap: 12px; }
}
</style>
</head>
<body>

<!-- ═══ BANNER（居中展示，无logo）═══ -->
<div class="banner">
  <div class="banner-title">研发创新挖掘雷达</div>
  <div class="banner-tagline">
    本次内容融合创新技术三要素建模、TRIZ方法、功能拆解、创新分类、专利/文献外部证据比对、价值判断与创新资产流转等方法论结合生成，为您挖掘值得保护的创新点。
  </div>
  <div class="banner-meta">
    <span>📄 {{DOC_TYPE}}</span>
    <span>🗂 {{DOC_TITLE}}</span>
    <span>📅 {{SCAN_DATE}}</span>
  </div>
</div>

<!-- ═══ STATS BAR（吸顶，居中文案）═══ -->
<div class="stats-bar">
  <div class="stats-summary">
    本次挖掘雷达挖掘出 <span class="num-blue">{{TOTAL_COUNT}}</span> 个候选技术点，经过专家技能思考识别出 <span class="num-red">{{RED_COUNT}}</span> 个立即行动的创新点，因其优先级是 P1，有 <span class="num-red">{{RECOMMEND_COUNT}}</span> 个推荐建议详细看下方报告内容。<span class="num-green">{{SEARCHED_COUNT}}</span> 个创新点均已完成检索。
  </div>
</div>

<!-- ═══ PAGE BODY（左侧导航 + 主内容）═══ -->
<div class="page-body">

<!-- ── 左侧定位导航 ── -->
<nav class="left-nav" id="left-nav">
  <div class="left-nav-title">导航</div>
  <a class="nav-item active" onclick="scrollToSec('sec-candidates')">📋 候选创新点列表</a>
  <a class="nav-item" onclick="scrollToSec('sec-actions')">🚀 行动队列</a>
  <div class="nav-section-label">创新点详情</div>
  <!-- 按实际技术点数量生成，每个技术点一条 nav-item，如：
  <a class="nav-item" onclick="scrollToSec('card-1')">① 技术点标题</a>
  <a class="nav-item" onclick="scrollToSec('card-2')">② 技术点标题</a>
  -->
  <a class="nav-item" onclick="scrollToSec('card-1')">① {{TECH_TITLE_1}}</a>
  <a class="nav-item" onclick="scrollToSec('card-2')">② {{TECH_TITLE_2}}</a>
  <a class="nav-item" onclick="scrollToSec('sec-evidence')">🗂️ 外部证据链</a>
</nav>

<div class="main">

<!-- ═══ 板块一：候选创新点组合列表 ═══ -->
<div class="section-header" id="sec-candidates">
  <span class="section-icon">📋</span>
  <div>
    <div class="section-title-main">候选创新点组合列表</div>
    <div class="section-desc">本次扫描发现 {{TOTAL_COUNT}} 个候选技术点，综合评级一览</div>
  </div>
</div>
<div class="candidate-table-wrap">
  <table class="candidate-table">
    <thead>
      <tr>
        <th>优先级</th><th>创新点</th><th>创新类型</th><th>建议路径</th>
        <th>价值评分</th><th>置信度</th><th>技术压力</th><th>下一步</th>
      </tr>
    </thead>
    <tbody>
      <!-- 复制此行，每个技术点一行 -->
      <tr>
        <td><span class="p-badge p1">🔴 P1</span></td>
        <td><div style="font-weight:600;color:#0f172a;margin-bottom:4px">{{TECH_TITLE}}</div></td>
        <td><span class="type-tag">{{INNOVATION_TYPE}}</span></td>
        <td style="font-size:12px;color:#334155">{{PROTECT_PATH}}</td>
        <td>
          <div class="progress-group">
            <div class="progress-row">
              <span class="progress-label">新颖性</span>
              <div class="progress-bar-bg"><div class="progress-bar-fill fill-high"></div></div>
              <span style="font-size:11px;color:#ef4444;font-weight:600">高</span>
            </div>
            <div class="progress-row">
              <span class="progress-label">完整度</span>
              <div class="progress-bar-bg"><div class="progress-bar-fill fill-full"></div></div>
              <span style="font-size:11px;color:#10b981;font-weight:600">完整</span>
            </div>
          </div>
        </td>
        <td><span class="level-pill high">高</span></td>
        <td><span class="level-pill mid">中</span></td>
        <td class="next-step-cell">{{NEXT_STEP}}</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ═══ 板块二：行动队列 ═══ -->
<div class="section-header" id="sec-actions">
  <span class="section-icon">🚀</span>
  <div>
    <div class="section-title-main">行动队列</div>
    <div class="section-desc">按优先级排列，可直接复制给团队</div>
  </div>
</div>
<div class="action-queue">
  <div class="action-item">
    <div class="action-color-bar red"></div>
    <div class="action-content">
      <div class="action-num">01</div>
      <div class="action-main">
        <div class="action-desc">{{ACTION_DESC}}</div>
        <div class="action-meta">
          <span class="action-owner">👤 {{ACTION_OWNER}}</span>
          <span class="action-deadline urgent">⏰ {{ACTION_DEADLINE}}</span>
        </div>
      </div>
    </div>
  </div>
  <div class="action-item">
    <div class="action-color-bar yellow"></div>
    <div class="action-content">
      <div class="action-num">02</div>
      <div class="action-main">
        <div class="action-desc">{{ACTION_DESC}}</div>
        <div class="action-meta">
          <span class="action-owner">👤 {{ACTION_OWNER}}</span>
          <span class="action-deadline normal">⏰ {{ACTION_DEADLINE}}</span>
        </div>
      </div>
    </div>
  </div>
  <div class="action-item">
    <div class="action-color-bar gray"></div>
    <div class="action-content">
      <div class="action-num">03</div>
      <div class="action-main">
        <div class="action-desc">{{ACTION_DESC}}</div>
        <div class="action-meta">
          <span class="action-owner">👤 {{ACTION_OWNER}}</span>
          <span class="action-deadline relaxed">⏰ {{ACTION_DEADLINE}}</span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══ 板块三：创新点详情（默认全部展开，点击收缩）═══ -->
<div class="section-header" id="sec-details">
  <span class="section-icon">🔬</span>
  <div>
    <div class="section-title-main">创新点详情</div>
    <div class="section-desc">默认全部展开，点击卡片标题可收缩</div>
  </div>
</div>

<!-- ⚠️ 重要：所有卡片均不加 collapsed 类，card-body-wrap 的 style 必须是 max-height:4000px -->
<!-- 🔴 立即行动卡片（默认展开）-->
<div class="detail-card priority-red" id="card-1">
  <button class="card-toggle" onclick="toggleCard('card-1')">
    <div class="card-header-row">
      <div class="card-header-left">
        <div class="card-conclusion-index">技术点 #1 · {{INNOVATION_TYPE}}</div>
        <div class="card-conclusion-title">{{TECH_TITLE}}</div>
        <div class="conclusion-meta">
          <span class="conclusion-tag conf-high">置信度：高</span>
          <span class="conclusion-tag press-mid">技术压力：中</span>
        </div>
        <div class="card-next-step">⚡ 下一步：{{NEXT_STEP}}</div>
      </div>
      <div class="card-header-right">
        <span class="badge-in-card badge-red">🔴 立即行动</span>
        <div class="protect-summary-box">
          <div class="protect-summary-label">保护建议</div>
          <div class="protect-summary-text">{{PROTECT_SUMMARY}}</div>
        </div>
        <span class="collapse-indicator">▼</span>
      </div>
    </div>
  </button>
  <div class="card-body-wrap" style="max-height:4000px">
    <div class="card-body">
      <!-- 1. 技术三要素 -->
      <div class="three-elements">
        <div class="three-elements-title">技术三要素</div>
        <div class="element-row problem">
          <div class="element-label-cell">问题</div>
          <div class="element-value-cell">{{PROBLEM}}</div>
        </div>
        <div class="element-row method">
          <div class="element-label-cell">方案</div>
          <div class="element-value-cell">{{METHOD}}</div>
        </div>
        <div class="element-row effect">
          <div class="element-label-cell">效果</div>
          <div class="element-value-cell">{{EFFECT}}</div>
        </div>
      </div>
      <!-- 2. 保护建议（详细）-->
      <div class="protect-box">
        <div class="protect-icon">🛡️</div>
        <div>
          <div class="protect-title">{{PROTECT_TITLE}}</div>
          <div class="protect-reason">{{PROTECT_REASON}}</div>
        </div>
      </div>
      <!-- 3. 待补充问题 -->
      <div class="questions-box">
        <div class="questions-title">⚠️ 待研发补充的问题 — 可直接转发给发明人</div>
        <div class="question-item"><span class="question-num">Q1</span><span>{{QUESTION_1}}</span></div>
        <div class="question-item"><span class="question-num">Q2</span><span>{{QUESTION_2}}</span></div>
        <div class="question-item"><span class="question-num">Q3</span><span>{{QUESTION_3}}</span></div>
      </div>
      <!-- 4. 评分双列 -->
      <div class="score-row">
        <div class="score-box">
          <div class="score-box-label">新颖性潜力</div>
          <div class="score-value red">🔴 高</div>
          <div class="score-basis">{{NOVELTY_BASIS}}</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">技术完整度</div>
          <div class="score-value green">✅ 完整</div>
          <div class="score-basis">{{COMPLETENESS_BASIS}}</div>
        </div>
      </div>
      <!-- 5. 现有技术 -->
      <div>
        <div class="section-sub-title">参考现有技术</div>
        <div class="prior-item">
          <a class="prior-pn" href="{{PATENT_URL}}" target="_blank">{{PATENT_NO}}</a>
          <div>
            <div class="prior-title">{{PATENT_TITLE}}</div>
            <div class="prior-diff">与本方案区别：{{DIFF_DESC}}</div>
          </div>
        </div>
      </div>
      <!-- 6. 来源证据 -->
      <div class="source-quote">
        <div class="source-quote-label">📎 来源证据</div>
        {{SOURCE_QUOTE}}
      </div>
    </div>
  </div>
</div>

<!-- 🟡 建议推进卡片（默认展开，无 collapsed 类）-->
<div class="detail-card priority-yellow" id="card-2">
  <button class="card-toggle" onclick="toggleCard('card-2')">
    <div class="card-header-row">
      <div class="card-header-left">
        <div class="card-conclusion-index">技术点 #2 · {{INNOVATION_TYPE}}</div>
        <div class="card-conclusion-title">{{TECH_TITLE}}</div>
        <div class="conclusion-meta">
          <span class="conclusion-tag conf-mid">置信度：中</span>
          <span class="conclusion-tag press-high">技术压力：高</span>
        </div>
        <div class="card-next-step">⚡ 下一步：{{NEXT_STEP}}</div>
      </div>
      <div class="card-header-right">
        <span class="badge-in-card badge-yellow">🟡 建议推进</span>
        <div class="protect-summary-box">
          <div class="protect-summary-label">保护建议</div>
          <div class="protect-summary-text">{{PROTECT_SUMMARY}}</div>
        </div>
        <span class="collapse-indicator">▼</span>
      </div>
    </div>
  </button>
  <div class="card-body-wrap" style="max-height:4000px">
    <div class="card-body">
      <!-- 1. 技术三要素 -->
      <div class="three-elements">
        <div class="three-elements-title">技术三要素</div>
        <div class="element-row problem"><div class="element-label-cell">问题</div><div class="element-value-cell">{{PROBLEM}}</div></div>
        <div class="element-row method"><div class="element-label-cell">方案</div><div class="element-value-cell">{{METHOD}}</div></div>
        <div class="element-row effect"><div class="element-label-cell">效果</div><div class="element-value-cell">{{EFFECT}}</div></div>
      </div>
      <!-- 2. 保护建议 -->
      <div class="protect-box">
        <div class="protect-icon">🛡️</div>
        <div>
          <div class="protect-title">{{PROTECT_TITLE}}</div>
          <div class="protect-reason">{{PROTECT_REASON}}</div>
        </div>
      </div>
      <!-- 3. 待补充问题 -->
      <div class="questions-box">
        <div class="questions-title">⚠️ 待研发补充的问题 — 可直接转发给发明人</div>
        <div class="question-item"><span class="question-num">Q1</span><span>{{QUESTION_1}}</span></div>
        <div class="question-item"><span class="question-num">Q2</span><span>{{QUESTION_2}}</span></div>
        <div class="question-item"><span class="question-num">Q3</span><span>{{QUESTION_3}}</span></div>
      </div>
      <!-- 4. 评分双列 -->
      <div class="score-row">
        <div class="score-box">
          <div class="score-box-label">新颖性潜力</div>
          <div class="score-value yellow">🟡 中</div>
          <div class="score-basis">{{NOVELTY_BASIS}}</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">技术完整度</div>
          <div class="score-value yellow">⚠️ 需补充</div>
          <div class="score-basis">{{COMPLETENESS_BASIS}}</div>
        </div>
      </div>
      <!-- 5. 现有技术 -->
      <div>
        <div class="section-sub-title">参考现有技术</div>
        <div class="prior-item">
          <a class="prior-pn" href="{{PATENT_URL}}" target="_blank">{{PATENT_NO}}</a>
          <div>
            <div class="prior-title">{{PATENT_TITLE}}</div>
            <div class="prior-diff">与本方案区别：{{DIFF_DESC}}</div>
          </div>
        </div>
      </div>
      <!-- 6. 来源证据 -->
      <div class="source-quote">
        <div class="source-quote-label">📎 来源证据</div>{{SOURCE_QUOTE}}
      </div>
    </div>
  </div>
</div>

<!-- ═══ 板块四：外部证据链 ═══ -->
<div class="section-header" id="sec-evidence">
  <span class="section-icon">🗂️</span>
  <div>
    <div class="section-title-main">外部证据链</div>
    <div class="section-desc">MCP检索命中的全部核心参考专利汇总</div>
  </div>
</div>
<div class="evidence-table-wrap">
  <table class="evidence-table">
    <thead>
      <tr>
        <th>专利号</th><th>标题</th><th>相关技术点</th>
        <th>相关性</th><th>本质区别</th><th>对我方影响</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a class="prior-pn" href="{{PATENT_URL}}" target="_blank">{{PATENT_NO}}</a></td>
        <td style="max-width:200px;color:#334155">{{PATENT_TITLE}}</td>
        <td style="font-size:12px;color:#64748b">{{PATENT_RELEVANCE_TECH}}</td>
        <td><span class="relevance-tag high">高度相关</span></td>
        <td style="font-size:12px;color:#475569;max-width:180px">{{PATENT_DIFF}}</td>
        <td><span class="impact-tag avoid">需规避</span></td>
      </tr>
      <tr>
        <td><a class="prior-pn" href="{{PATENT_URL}}" target="_blank">{{PATENT_NO}}</a></td>
        <td style="max-width:200px;color:#334155">{{PATENT_TITLE}}</td>
        <td style="font-size:12px;color:#64748b">{{PATENT_RELEVANCE_TECH}}</td>
        <td><span class="relevance-tag mid">部分相关</span></td>
        <td style="font-size:12px;color:#475569;max-width:180px">{{PATENT_DIFF}}</td>
        <td><span class="impact-tag ref">可参考</span></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="disclaimer">
  <strong>免责声明：</strong>本报告由 AI 辅助生成，技术判断仅供参考，不构成法律意见。专利申请前请咨询知识产权专业人士。部分证据来源于公开专利数据库，检索截止日期为报告生成日。
</div>

</div><!-- /main -->
</div><!-- /page-body -->

<script>
function toggleCard(id) {
  const card = document.getElementById(id);
  const wrap = card.querySelector('.card-body-wrap');
  const isCollapsed = card.classList.contains('collapsed');
  if (isCollapsed) {
    card.classList.remove('collapsed');
    wrap.style.maxHeight = '4000px';
  } else {
    card.classList.add('collapsed');
    wrap.style.maxHeight = '0';
  }
}

function scrollToSec(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// 滚动高亮导航
const navItems = document.querySelectorAll('.nav-item');
const sections = ['sec-candidates','sec-actions','sec-details','sec-evidence'];
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(id => {
    const el = document.getElementById(id);
    if (el && el.getBoundingClientRect().top < 120) current = id;
  });
  navItems.forEach(item => {
    item.classList.remove('active');
    const onclick = item.getAttribute('onclick') || '';
    if (onclick.includes(current)) item.classList.add('active');
  });
});
</script>

</body>
</html>
```
