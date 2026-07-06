---
name: small-rna-patent-landscape
description: Build a small-nucleic-acid company patent technology landscape from a patent number list. Use when the user asks to fetch patent originals, analyze ASO/siRNA/mRNA/RNA medicine patent portfolios, create an XLSX patent landscape workbook, classify small RNA technology tags, or generate a multidimensional patent timeline/lane HTML dashboard for one company.
---

# Small RNA Patent Landscape

## Purpose

Use this skill to turn a list of patent publication/application numbers into a company-level patent technology landscape for small nucleic acid therapeutics. The standard output is:

- local patent full-text markdown corpus
- structured XLSX workbook with a strategy-analysis layer
- multidimensional HTML timeline with technology lanes, tag filters, hover cards, distribution summaries, and visible opportunity-gap markers

Prefer Chinese output labels when the final audience is a China-based customer; keep patent claims/abstract source text in the source language unless the user asks for translation.

## Workflow

1. **Normalize patent input**
   - Accept one patent number per line or a pasted list.
   - Preserve the user's order as `输入序号`.
   - If a number has no kind code, try suffixes in this order: original, `A`, `A1`, `A2`, `B`, `B1`, `B2`.
   - Store the successful matched number as `当前匹配公开号`.

2. **Fetch patent originals**
   - Use the available patent MCP/tooling, preferably 智慧芽 MCP, to fetch markdown full text.
   - Save one markdown per successful patent under `patent_markdowns/`.
   - Save `fetch_summary.csv/json` with input number, matched number, status, file path, and fallback attempts.
   - For missing claims, substitute English claims from another family member when available, and mark the substitution.

3. **Build structured patent rows**
   - Extract title, abstract, claims, applicant, publication date, legal status, family numbers, family earliest publication date, family count, and family jurisdictions.
   - Normalize applicants to English names.
   - Use family/legal data from the patent MCP if available. If not available, clearly flag estimated or missing fields.
   - Create one JSON/CSV intermediate file before generating XLSX/HTML.

4. **Classify small RNA technology**
   - Apply the tag taxonomy in `references/tag-taxonomy.md`.
   - Keep both expert tags and customer-readable tags:
     - expert tag example: `SCN1A / Dravet / Nav1.1`
     - customer-readable tag example: `中枢神经遗传病蛋白上调 ASO`
   - Do not use “generation 1/2/3” as the main axis unless the user explicitly asks; modern portfolios are better explained by disease assets, mechanism platforms, chemistry/structure, delivery/tissue, and productization stage.

5. **Generate XLSX**
   - Use the field schema in `references/workbook-schema.md`.
   - Include at minimum a main analysis sheet, tag summary sheet, timeline source sheet, methodology sheet, and the strategy sheets listed in `references/workbook-schema.md`.
   - Add a second-layer strategy analysis:
     -重点专利证据链
     -布局缺口矩阵
     -研发启发卡片
     -龙头布局借鉴
     -策略建议总览
   - Use professional Chinese column names for customer-facing sheets.

6. **Generate HTML timeline**
   - Use the design/output rules in `references/html-dashboard.md`.
   - The page title should be `{Company} 公司多维标签时间轴`.
   - Default view should use customer-readable technology directions, not raw gene names.
   - Provide dimension switches for technology direction, mechanism, RNA modality, chemistry/structure, delivery/tissue, and productization stage.
   - Hover cards should include title, professional subdivision, patent type, mechanism, chemistry, delivery/tissue, family count, entered jurisdictions, importance, evidence chain, borrowable strategy, possible breakthrough, recommended action, and Chinese strategic interpretation.
   - Add strategy cards above the timeline for `查漏补缺`, `研发启发`, and `布局借鉴`.
   - Add visible yellow/dashed `技术缺口` or `机会点` markers on relevant future or next-step timeline cells. These markers should not represent real patents; they represent suggested patent-layout opportunities inferred from the portfolio.
   - For small RNA companies, always consider opportunity markers for delivery/tissue gaps and platform-mechanism migration, especially:
     - CNS/鞘内给药参数补强
     - 眼科/玻璃体腔给药外延
     - 肾脏组织选择性
     - 制剂稳定性与浓度窗口
     - NMD/隐蔽外显子机制迁移
     - 剪接转换适应症拓展
     - 患者筛选/诊断准入壁垒

7. **Validate**
   - Open or render the XLSX enough to confirm sheet names and row counts.
   - Serve and preview the HTML locally when possible; check that the default view and at least one alternate dimension render correctly.
   - Confirm no obvious English-only customer-facing labels remain, except necessary gene/protein/drug abbreviations.

## Output Naming

Use a stable output folder such as `outputs/patent_analysis/`.

Recommended artifacts:

- `{company_slug}_patent_landscape.xlsx`
- `{company_slug}_multidimensional_tag_timeline.html`
- `patent_analysis_rows.json`
- `patent_markdowns/`

## Bundled References

- `references/tag-taxonomy.md`: classification logic and Chinese display names.
- `references/workbook-schema.md`: workbook sheets and required columns.
- `references/html-dashboard.md`: dashboard behavior, hover-card content, and visual conventions.

## Bundled Script

- `scripts/create_landscape_project.py`: creates a reusable project scaffold with `patent_markdowns/`, `outputs/patent_analysis/`, and starter config files.

Use the script as a starting point, then adapt local data-fetching and parsing code to the available MCP/tooling in the active workspace.
