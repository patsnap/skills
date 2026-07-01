---
name: patent-pre-evaluation-report
description: |
  Create and iteratively improve Chinese patent pre-application evaluation reports from a technical proposal, disclosure draft, invention idea, or prior report. Use when the user asks for 专利申请前预评估, 专利预评估报告, 查新点提炼, 可专利性分析, 非正常申请风险排查, 申请策略建议, or report updates driven by PatSnap/智慧芽 search evidence.
---

# Patent Pre-Application Evaluation Report

## Overview

Use this skill to turn a technical proposal into a structured Chinese patent pre-application evaluation report, output as a complete **HTML file** whose CSS and layout exactly match the `CUMT-IP-PRE-2026-0001.html` reference template (deep-blue/gold color scheme, A4 portrait cover page, section-number circles, progress bars, conclusion quick-view page).

Treat the report as an iterative artifact: draft from the proposal, run real PatSnap/智慧芽 searches via the installed MCP tools, incorporate evidence, reassess risks, and update the conclusion.

Load `references/report-workflow.md` when drafting or revising a report.

## Core Workflow

### Step 1 — Clarify Input
- If the user provides only a technology idea, extract: invention title, field, problem, solution, technical effects, application scenario, and likely inventors/applicant.
- If the user provides a disclosure or prior report, preserve existing facts; mark uncertain or missing content as `待补充`.
- If the user asks to iterate, identify the specific sections affected by new evidence.

### Step 2 — Extract Technical Structure (MCP)
Call the following MCP tools from `hub-mcp-gateway-novelty-search` in order:
1. `novelty_summary` — extract tech problem / solution / efficacy (three elements)
2. `novelty_feature_extract` — classify technical features and build the feature table
3. Convert strongest feature combinations into numbered 查新点 (3–6 points). Keep each 查新点 concrete: component, data, rule, parameter, workflow, model, or interaction logic — not broad effects.

### Step 3 — Build Search Strategy (MCP)
Call in order:
1. `novelty_keywords_extract` — generate Chinese/English keyword groups + IPC classification
2. `novelty_keywords_extend` — expand synonyms, hypernyms, hyponyms for each keyword
3. `novelty_query_planner` — plan multi-round Boolean retrieval queries

Output of this step populates the **检索范围与策略** chapter (databases, languages, date range, keyword table, IPC table, Boolean query strings).

### Step 4 — Execute Real Search (MCP)
For each 查新点, call:
1. `novelty_search_agent` (preferred, full-pipeline AI search entry point) — OR split into:
   - `novelty_semantic_search` (semantic similarity search)
   - `novelty_patent_search` (keyword Boolean search)
   - `novelty_paper_search` (academic paper search)
2. `novelty_fetch_patent_data` — fetch title, abstract, assignee, publication date, abstract figure for top hits
3. `novelty_abstract_figure_similarity` — evaluate abstract figure similarity against the input solution (optional, when figures are available)

Record for every search: database, query string, date range, total hits, screened count, and selected references. Cite these in the report. Do not invent publication numbers, dates, applicants, or similarity scores.

### Step 5 — Feature Comparison (MCP)
1. `novelty_feature_comparison` (or `novelty_feature_comparison_async` + `novelty_cc_result` for large sets) — compare each close reference feature-by-feature against 查新点
2. `novelty_rl_predict` — predict novelty / inventiveness score for top references
3. `novelty_report_generate` — generate the comparison narrative paragraph

Classify each feature as: `相同` / `相近` / `部分公开` / `未见` / `待复核`.
Do not claim novelty from absence of evidence alone; phrase as "在当前检索样本中未见相同公开".

### Step 6 — Evaluate & Iterate
- Map each search result to one or more 查新点.
- Classify relevance: `密切相关` / `相关` / `一般相关`.
- When evidence weakens a 查新点, suggest narrowing, recombination, dependent-claim placement, or additional experimental support.
- When evidence supports a strong conclusion, explain which distinguishing features carry novelty/inventiveness.
- For market/industry context (转化价值评估 chapter), optionally call `novelty_website_search`.

### Step 7 — Generate HTML Report
After all MCP results are collected, generate a **single self-contained HTML file** with the following requirements:

**Style requirements (must match reference template exactly):**
- CSS variables: `--primary: #1a3a6b`, `--primary-light: #2a5298`, `--accent: #c8a94b`, `--accent-light: #f5e6b8`, `--danger: #c0392b`, `--warning: #e67e22`, `--success: #27ae60`, `--info: #2980b9`, `--gray: #f4f6f9`, `--border: #d0d7e3`
- Cover page: A4 portrait (`width: 210mm; max-width: 210mm; min-height: 297mm; margin: 0 auto`), `linear-gradient(145deg, #0d1f4a, #1a3a6b, #2a5298)` deep-blue gradient background; see Cover Page Layout below
- Main content area: `width: 210mm; max-width: 210mm; margin: 0 auto; padding: 24px 0 60px` (no left/right padding so content width equals cover width)
- Section number circles: `#1a3a6b` background, white text
- Section titles: `border-bottom: 2px solid #c8a94b` gold underline
- Left-border highlights: `border-left: 4px solid #c8a94b`
- Table headers: `#1a3a6b` background, white text
- Similarity progress bars: red (≥70%) / orange (40–69%) / green (<40%)
- Conclusion quick-view page: deep-blue gradient background + gold-border cards
- Fixed print button: bottom-right corner
- Footer: `#1a3a6b` background

**Cover Page Layout (竖版A4封面，从上到下):**
1. Top deep-blue bar (`height: 14mm`, `linear-gradient(90deg, #0d1f4a, #1a3a6b, #2a5298)`)
2. Gold decorative line (`height: 4px`, gradient gold)
3. Institution header: left = "中国矿业大学" (17pt, bold, letter-spacing 3px) + English full name; right = circular gold-border "矿" badge
4. Divider line (blue-gold gradient)
5. Confidentiality badge (gold-border ellipse label: "内部保密 · 申请前预评估 · PatSnap 智慧芽支持")
6. Chinese main title (21pt, deep-blue bold, centered, two lines)
7. English subtitle (gray uppercase)
8. Report type box (deep-blue gradient background + gold text "专利 申 请 前 评 估 报 告")
9. Basic info table (2-col 8-row: report number, date, unit, field, inventors, IPC, confidentiality level, recommendation)
10. Red risk alert bar (red background, key risk conclusion + recommendation)
11. Confidentiality notice (light-gray dashed border, small text, usage restrictions)
12. Bottom deep-blue bar: left = institution name, right = report number + date (gold text)

**Appendix card style (附件区块样式):**
- Section title uses same gold-underline style as other chapters
- Each appendix item rendered as a rounded card: `border: 1px solid #d0d7e3`, `border-radius: 8px`, `background: #fff`, `padding: 20px`, `margin-bottom: 12px`
- Left gold circle badge: `background: #c8a94b`, `color: #fff`, `font-weight: bold`, `border-radius: 50%`, `width: 32px`, `height: 32px`, display inline-flex, align-center
- Appendix title: `color: #1a3a6b`, `font-weight: bold`, `font-size: 1.05em`
- Description text: `color: #666`, `font-size: 0.9em`, `margin-top: 6px`

**Report chapters (in order):**
1. 封面 & 基本信息（竖版A4，见 Cover Page Layout）
2. 数据安全与保密声明（固定模板，见下方说明，放在政策背景之前）
3. 政策背景（固定模板文字，含职称改革政策，见下方说明）
4. 技术方案要点（来自 Step 2 MCP 结果）
5. 查新点与查新要求（来自 Step 2 MCP 结果）
6. 检索范围与策略（来自 Step 3 MCP 结果）
7. 检索结果与相关文献（来自 Step 4 MCP 真实检索结果）
8. 逐项技术特征比对（来自 Step 5 MCP 比对结果）
9. 可专利性风险判断（来自 Step 5 RL评分 + AI分析）
10. 非正常申请风险排查（AI生成）
11. 申请文件质量评估（AI生成）
12. 转化价值评估（AI生成，可选调用 novelty_website_search）
13. 申请策略建议（AI综合生成）
14. 综合结论快览页（AI综合，含评分卡片）

**数据安全与保密声明（固定内容，每份报告必须包含）：**
- 章节编号圆圈内仅显示 🔒 emoji，不含文字（避免溢出圆圈）
- 章节标题：数据安全与保密声明
- 使用与正文其他章节完全一致的 `section` / `section-header` / `section-num` / `section-title` CSS class，不加内联样式覆盖
- 4条声明内容（以表格/卡片形式展示）：
  1. **内部使用与权限控制**：本报告仅供中国矿业大学科研院知识产权管理办公室、项目发明人及经授权代理机构使用，未经授权不得外传。
  2. **脱敏检索与最小披露**：外部检索仅使用关键词、IPC分类号和抽象技术特征，不上传技术交底书原文、核心参数完整表或未公开实验数据。
  3. **平台安全说明**：智慧芽（PatSnap）安全与合规能力可参见官方网站：https://www.zhihuiya.com/security-center。
  4. **留痕与复核**：提交、检索、修改、导出、盖章等环节应在知产办流程中留痕；AI辅助结论须经知识产权管理人员复核后使用。

**政策背景（固定内容，每份报告必须包含，共5条政策）：**
1. 教育部、科技部《关于规范高等学校SCI论文相关指标使用 树立正确评价导向的若干意见》（教科技〔2020〕2号）
2. 教育部《关于加强高校有组织科研 推动高水平自立自强的若干意见》（教科技〔2022〕1号）
3. 国务院办公厅《专利转化运用专项行动方案（2023—2025年）》
4. **人力资源和社会保障部、教育部《关于深化高等学校教师职称制度改革的指导意见》（人社部发〔2020〕100号）**：明确将专利成果转化情况纳入职称评审，鼓励以专利转化实绩替代论文数量要求，推动"以用促创"。
5. **教育部《破除"唯论文"不良导向若干措施》及配套政策**：支持将发明专利授权数量、许可转让收益、产学研合作纳入职称评定，以专利转化金额及经济效益作为职称晋升依据。

**附件章节（必须生成，紧接第14章之后，缺失任何一个视为报告不完整）：**

附件1：检索式完整记录
- 内容：各查新点在智慧芽全球专利数据库中使用的完整检索式，含布尔逻辑运算符、字段限定和IPC分类号限定；以及CNKI/万方补充检索式（如未执行则标注"待填"）
- 数据来源：Step 3 `novelty_query_planner` 输出 + Step 4 实际执行的检索式

附件2：密切相关专利文献题录及摘要
- 内容：D1—DN所有密切相关专利的完整题录（申请号、公开号、申请人、发明人、IPC分类、公开日、摘要全文）
- 数据来源：Step 4 `novelty_fetch_patent_data` 返回结果；期刊/学位论文未经CNKI/万方检索则标注"待补充"

附件3：相似专利清单（含智慧芽相似度）
- 内容：P1—PN所有相似专利列表，含公开号、申请人类型、IPC分类、智慧芽相似度得分、关联查新点编号
- 数据来源：Step 4 `novelty_search_agent` / `novelty_semantic_search` 返回的相似度评分；不得手动填写评分

附件4：技术特征比对明细
- 内容：各查新点所有技术子特征（F1-1、F1-2…FN-M）与最接近对比文献的逐项对照，含相同点、差异点说明及比对结论
- 数据来源：Step 5 `novelty_feature_comparison` 输出；与正文第八章保持一致

附件5：委托人提供资料清单
- 内容：发明人提交的技术交底书、实验数据、图纸、论文草稿等材料目录（用户未提供则标注"待补充"）
- 数据来源：Step 1 用户输入整理

附件6：政策文件参考目录
- 内容：报告引用的政策文件列表，包括但不限于：教科技〔2020〕1号、国务院办公厅《专利转化运用专项行动方案（2023—2025年）》、国家知识产权局令第77号、人社部发〔2020〕100号、教育部破除唯论文配套政策、江苏省专利申请预审规范及教师职称评价相关文件
- 数据来源：固定政策模板 + 正文第三章政策背景引用

**Output path:** `@session/reports/[报告编号].html`
Use `files.begin_write` → repeated `files.append` → `files.finish_write` for large HTML files (never write the entire file in one payload).

### Step 8 — Final Decision
Give one of: `建议申请` / `修改后申请` / `暂缓申请` / `不建议申请`.
Include: application type, independent-claim focus, dependent-claim candidates, evidence gaps, and next actions.
Add review caveat: AI辅助结论及PatSnap检索结果，正式申请前须经知识产权专员或专利代理人复核。

## Output Rules

- Write primarily in Chinese unless the user asks otherwise.
- Professional report tone, not marketing copy.
- Use tables for: search strategy, close references, feature comparison, patentability risk, abnormal application risk.
- Preserve provenance: cite search date, database, query, result count, screened count, and evidence source for every search conclusion.
- Mark uncertain bibliographic data as `待复核`; never invent publication numbers, applicants, dates, or similarity scores.
- Keep confidentiality language visible when the report is based on unpublished technology.
- **Final output must always be a complete HTML file saved to `@session/reports/`**, not a Markdown block in chat.
- **附件1—附件6必须全部生成**，每个附件用独立卡片渲染，缺失任何一个附件视为报告不完整。
- **数据安全与保密声明必须生成**，位于政策背景章节之前。
- **section-num 圆圈内仅放数字或单个emoji**，不放文字，避免溢出。

## References

- `references/report-workflow.md`: report section skeleton, MCP tool call sequence, PatSnap evidence schema, risk scoring guidance, HTML style guide, and iteration checklist.

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
