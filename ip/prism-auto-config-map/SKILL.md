---
name: prism-auto-config-map
description: |
  棱镜车智-专利论文数据穿透 Skill。用于车企下一代车型规划、竞品配置对标、
  技术趋势预测、供应链机会识别和售前 Demo。围绕特定细分市场、车型清单或
  关键配置，基于 QFD/质量屋 + Matrix Analysis 为主轴，辅以 Benchmarking、
  Kano、技术 S 曲线、专利壁垒矩阵，融合官方参数、配置库、VOC 与智慧芽专利/论文/文献/企业产业链数据，
  输出强视觉 HTML 前瞻决策报告。核心价值是把市场配置现象穿透到专利、
  论文/文献、关键申请人、供应链合作关系和未来 1-2 年量产机会。
  不适用于 FTO 法律意见、精确 BOM 成本测算、泛财报融资分析或脱离车型
  配置决策的公司战略画像。
---

# 棱镜车智-专利论文数据穿透

## Use When

Use this skill when the user asks for automotive competitor configuration analysis, future vehicle planning, or feature timing decisions where Patsnap patent/literature/supply-chain evidence should explain the "why now" behind the recommendation.

Typical requests:

- "20-30 万 B 级 EREV SUV 哪些配置已经成为必备,哪些还有差异化机会"
- "对比理想 L6/L7、问界 M7/M8、零跑 C16、阿维塔 07、智界 R7,输出下一代 B-SUV 配置机会地图"
- "年轻家庭 25 万级 B-SUV,哪些配置该跟进,哪些适合作为专利壁垒型差异化"
- "电子外后视镜、地暖、二排腿托、座椅抽屉,哪些未来 6-18 个月值得布局"
- "把特斯拉、比亚迪、华为系作为头部标尺,看下一代智能座舱/舒适配置机会"

Do not expand into broad intelligence work. If the user asks for company strategy, financing, organization, FTO, or precise BOM/TCO, narrow the task back to patent/literature/supply-chain evidence for next-generation vehicle configuration decisions.

## Core Audience

The report must include a visible "数据聚焦与服务对象" section. State that the analysis is designed for:

- 产品规划: define next-generation feature packages and trim logic.
- 战略/竞品情报: compare market leaders and detect timing windows.
- 研发预研: identify technical routes, patents, literature signals, and design constraints.
- 采购/供应链: find OEM/Tier0/Tier1/Tier2 linkage clues and sourcing risk.
- 售前/管理层 Demo: communicate the decision headline and evidence chain quickly.

## Freshness And Forecast Rules

This skill is forward-looking. Always use the latest data available in the execution environment.

- Show `数据统计截止日期`, `Patsnap 数据截止日期`, and `外部网页获取日期` in the hero area.
- Prefer data collected or refreshed as close as possible to the report date.
- If a source is stale, show a "前瞻性影响说明" card and lower confidence.
- Patent publication lag must be disclosed. Do not treat recent absence of patents as absence of activity.
- For 1-2 year forecasts, combine market fitment, Patsnap patent/literature trend, and supply-chain maturity.

## Core Workflow

1. **Define the competitor pool**: price band, segment, powertrain, launch window, target persona, model list, and head-company benchmark.
2. **Add head-company references**: include or explicitly discuss Tesla, BYD, Huawei/Harmony Intelligent Mobility, and relevant China NEV or overseas leaders when the segment allows it. If one is excluded, state why.
3. **Resolve product-domain hierarchy**: if the prompt locks a domain such as intelligent chassis, smart cockpit, thermal management, battery/e-drive, seat comfort, or ADAS, first map product domain → level-1 technologies → level-2 configurations/components → analysis objects.
4. **Run configuration benchmarking**: compare seat, interior, exterior, cabin, ADAS/comfort, thermal, battery, and safety-related configurations. Keep the user's model pool; use head companies only as benchmarks.
5. **Build QFD / House of Quality**: translate graded pain points into customer needs, engineering characteristics, competitor satisfaction, Patsnap evidence strength, target values, and planning actions.
6. **Run Matrix Analysis**: combine penetration, QFD weight, lifecycle stage, patent barrier, supply-chain maturity, and head-company benchmark into must_follow / differentiation_bet / watch / avoid_or_design_around.
7. **Apply Patsnap patent-paper dashboard + technology penetration wall**: for every level-1 technology in the product-domain map, build a patent/literature pool, then show market phenomenon → annual patent/literature trend → key applicants → co-applicants/inventor signals → core patent highlights → problem-solution-effect → supply-chain feasibility → 1-2 year forecast.
8. **Apply supply-chain linkage lens**: map configuration → function module → key components → core technology → OEM/Tier0/Tier1/Tier2 → China/overseas region → cooperation signal → evidence source.
9. **Build the one-line decision**: create `headline_conclusion`, one concise sentence explaining the future opportunity, risk, or action.
10. **Render HTML**: use `assets/report_template.html` and local assets under `assets/vehicle_visuals/`. Image generation or web image fetching is optional enhancement, never a hard dependency.

## Required Theory Tags

Every major conclusion must carry at least one theory tag. The final methodology display should focus on QFD / House of Quality and Matrix Analysis; other methods are supporting tags.

- `[QFD / House of Quality]`
- `[Matrix Analysis]`
- `[Benchmarking]`
- `[Kano]`
- `[S-Curve]`
- `[Patent Barrier]`
- `[Patsnap Penetration]`
- `[Supply Linkage]`

The final report must include a visible "理论依据 / Methodology" section so non-specialists can see why the analysis is grounded.

## Evidence Rules

- For market facts, prefer official or high-credibility sources. Read `references/data_sources.md` before making source claims.
- For Patsnap-driven claims, read `references/patsnap_data_lens.md` and show the full penetration chain in the main report, not only in the appendix.
- For supplier or supply-chain claims, read `references/supply_chain_lens.md`; supplier findings must be source-backed or explicitly marked as "待验证供应商线索".
- Do not use patent volume as a proxy for sales, user demand, or actual take rate.
- A "differentiation bet" requires at least one Patsnap strong signal: patent trend, literature foresight, Tier1/Tier2 supply-chain evidence, or a key patent with clear design intent.
- A "must follow" requires market or user evidence: high penetration, official fitment, clear VOC demand, or safety/regulatory basis.
- A "design-around/avoid" must state whether the reason is patent barrier, user rejection, regulatory uncertainty, cost, or implementation risk.
- Patent evidence for key configurations must be traceable to publication number, applicant, filing/publication date, legal status where available, tool/source, and data cutoff.
- OEM-supplier links must be labeled as one of: 已验证合作, 专利联合申请, 产品/公告线索, 待验证供应商线索.
- If a data source is unavailable, output a data gap card and lower confidence. Never invent source-backed numbers.

## Head-Company Benchmark Rule

For vehicle benchmarking, do not miss domestic and overseas leaders:

- Default head-company benchmarks: Tesla, BYD, Huawei/Harmony Intelligent Mobility.
- Add Volkswagen, Toyota, Hyundai, Mercedes-Benz, or other overseas leaders when the product domain or market scope makes them relevant.
- Head companies are benchmarks, not replacements for the user's specified competitor pool.
- If Tesla, BYD, or Huawei/Harmony Intelligent Mobility is not applicable, explicitly state the exclusion reason in the report.

## Product-Domain First Rule

When the user names or implies a product domain, the report must first show the domain map before judging configurations:

`产品域 → 一级技术 → 二级配置/零部件 → 竞品配置 → 专利/文献/供应链证据 → 规划动作`

Typical domains: smart cockpit, intelligent chassis, ADAS/safety, thermal management, battery/e-drive, seat and comfort, exterior and body electronics.

## Patent-Paper Dashboard And Patent Pool Rules

- Do not output a raw patent list as the main analysis.
- Use a patent-paper dashboard by company, product domain, and level-1 technology: annual patent growth, literature/paper signal, applicant concentration, co-applicant network, inventor signal, core patent highlights, patent pool scale, and planning implications.
- Every level-1 technology identified in the product-domain map must have a corresponding technology penetration card. If the report analyzes six level-1 technologies, render six cards; do not show only selected examples.
- Each technology card must include product domain, level-1 technology, linked level-2 configurations/components, patent pool count, search window, query terms/synonyms, literature/paper count and signal, layout cluster distribution, representative patents, applicant/supplier role split, 1-2 year forecast, confidence, and data gaps.
- If literature/paper retrieval has no results, explicitly show "论文信号暂无，以专利为主" and continue. Do not fail report generation because literature data is unavailable.
- Treat the patent pool as the complete retrieved set for that level-1 technology. The main report should show summary metrics and 3-6 representative patents; the full patent and literature lists should live in a detail page or same-page appendix.
- Preferred static output structure: `index.html` for the main report and `patent_pools/{technology_slug}.html` for one detail page per level-1 technology. If the host agent can only produce one HTML file, degrade to same-page anchors such as `#pool-{technology_slug}` while preserving the same content structure.
- Patent pool detail pages must show the full patent pool, full literature/paper pool when available, layout clusters, representative patent explanations, source notes, data gaps, and links to Patsnap/source detail pages where available.
- Do not generate one HTML page per individual patent; that is too slow and unnecessary. Individual patents should link to Patsnap/source detail URLs.
- Core patent cards must include publication number, applicant, filing/publication date, legal status when available, technical highlight, product planning implication, detail URL when available, and LLM limitation note.
- Inventor signals may indicate technical continuity, team clustering, or repeated research direction, but must not be used alone to infer employment, commercial cooperation, or supplier relationship.

## HTML Generation And Portability Rules

- Generated reports must be static HTML that can open offline and use relative paths for packaged assets.
- Do not depend on external scripts, CDN chart libraries, or remote images.
- Use `assets/report_template.html` as the main visual skeleton. Reuse its CSS for both `index.html` and patent pool detail pages.
- Use summary charts in the main report: sparklines, layout cluster bars, applicant role cards, and heatmaps. Put long tables and full pools into detail pages or same-page appendices.
- The template must stretch with data volume: rich datasets should not be truncated; sparse datasets should still render with data gap cards and confidence reduction.
- Ensure responsive behavior: desktop can use two-column or card-grid layouts; mobile should fall back to single column with horizontally scrollable tables and wrapped long text.

## Delivery-Grade Report Rules

When HTML output is requested, generate a delivery-grade multi-page report by default, not a bare workflow validation page.

- Hero right side must contain: main visual, caption/status tags, four methodology cards (QFD, Matrix, Patent, Lifecycle), and three or more test/report summary metrics.
- Every core section must include at least one visual expression: local image, static CSS/SVG chart, relationship card, heatmap, evidence card, or compact dashboard. Do not leave long sections as plain prose only.
- Product-domain technology map must be rendered as a table with: product domain, level-1 technology, level-2 configurations/components, related models/benchmarks, patent/literature pool, supplier role, and planning action.
- Configuration penetration heatmap must include a data-gap column distinguishing official confirmation, public-page confirmation, unverified, and authorization-required configuration-library confirmation.
- Main Patsnap section must include 3-5 representative patent PSE cards per level-1 technology. PSE means technical problem, solution, expected effect, product planning implication, and risk/design-around advice.
- Add an "AI 前瞻创新发现" module after the patent-paper penetration wall. Recommend 3-5 forward-looking configuration ideas based on patent pools, literature signals, and target scenarios. Each idea must state related technology domain, discovery basis, vehicle-fit concept, 1-2 year feasibility, supply-chain maturity, risk, and recommended action.
- Patent pool detail pages must include a local visual block, retrieval scope, layout clusters, representative patents with detail URLs, full patent list, full literature list, applicant/supplier view, and data gap notes.
- Each patent row should link to Patsnap/source details when available. Each paper/literature row should link to a source URL when available; otherwise show "详情链接待补".

## Image Stability And Packaging Rules

Final report images must remain visible after the report is moved or zipped.

- Copy `assets/vehicle_visuals/` into the report output directory before final delivery.
- Main report image paths must use `assets/vehicle_visuals/...`.
- Patent pool detail page image paths must use `../assets/vehicle_visuals/...`.
- `data-fallback` paths must follow the same relative-path rule as `src`.
- Do not use `/Users/...`, `/tmp/...`, `../prism_auto_config_map/...`, or remote image URLs as final image paths.
- Photoreal assets and SVG fallback assets are packaged visuals only; they are not evidence and must not be described as official OEM images.

## Real Test Output Rules

For real skill tests and demo reruns:

- Create a new output directory for each test run. Do not overwrite previous reports unless the user explicitly asks.
- Prefer `index.html` plus `patent_pools/*.html` plus `assets/` plus a zip package.
- Name delivery test packages clearly, for example `prism_auto_config_map_0529_delivery_upgraded.zip` for a skill package or `{scenario}_report.zip` for a generated report.
- Before delivery, validate HTML parsing, local multi-page links, image path existence, zip contents, and offline portability after unzip.

## Technology Lifecycle Strategy

Classify each key configuration or technology as:

- 引领技术: benchmark-setting, high-end signal, usually lower penetration but strong strategic value.
- 上升技术: rising adoption, meaningful user value, suitable as selling point.
- 成熟技术: stable supply and broad fitment, suitable as baseline.
- 接近退出技术: useful for cost control but with experience or brand risk.
- 退出技术: should not appear in high-end or next-generation flagship recommendations.

Pricing guidance:

- 高端产品: must include leading technology as benchmark, rising technology as selling point, mature technology as base, and no exiting technology.
- 中端产品: use rising + mature technologies to build value-for-money competitiveness.
- 低端产品: use mature + near-exit technologies for cost control, with explicit experience and brand-risk disclosure.

## Output Structure

Default output is a local HTML report using `assets/report_template.html`. The report must contain these sections:

1. Hero decision summary with `headline_conclusion`
2. Data freshness and forward-looking caveat
3. 数据聚焦与服务对象
4. Methodology focus: QFD / House of Quality + Matrix Analysis, with supporting tags summarized
5. 产品域技术地图
6. Competitor pool and head-company benchmark
7. Configuration penetration heatmap
8. QFD / House of Quality with pain-point levels
9. Matrix Analysis opportunity board
10. Patsnap patent-paper dashboard + technology penetration wall, including patent pools for every level-1 technology
11. OEM-supplier-patent relationship map, including overseas supply-chain leads where evidence supports them
12. Technology lifecycle x price-band strategy matrix
13. Next-generation configuration recommendation + evidence appendix

When responding in chat, provide a concise summary and the generated HTML path. If HTML generation is not requested or impossible, still structure the markdown in the same order.

If multi-page HTML generation is supported, produce:

- `index.html`: main decision report with summary cards for every level-1 technology.
- `patent_pools/{technology_slug}.html`: one patent/literature pool detail page per level-1 technology.

If multi-page generation is not supported, keep a single `index.html` and render the same detail content under same-page anchors.

## Visual Asset Rules

- Prefer local photoreal assets from `assets/vehicle_visuals/photo_real/`.
- Use local SVG assets under `assets/vehicle_visuals/` as low-fidelity fallback only.
- Read `assets/vehicle_visuals/metadata.json` before selecting a visual.
- Match by brand, market, powertrain, or scene. If no exact match exists, use the closest generic scene.
- If no image asset is available, render CSS/chart placeholders and continue.
- If image generation or web image fetching is available, it may be used as an enhancement only. Record source type and usage notes; never fail the skill because image generation is unavailable.
- Do not claim local AI-generated photoreal or SVG visuals are official OEM images.
- Photoreal assets are visual enhancement only; never use them as analytical evidence.

## Reference Loading

- Read `references/methodology.md` when defining the analysis lens or explaining theory basis.
- Read `references/data_sources.md` before collecting or ranking non-Patsnap evidence.
- Read `references/patsnap_data_lens.md` before making patent, literature, S-curve, or applicant claims.
- Read `references/supply_chain_lens.md` before naming suppliers, Tier0/Tier1/Tier2 roles, or OEM-supplier relationships.
- Read `references/output_templates.md` before drafting the final report.
- Read `references/config_taxonomy.md` when normalizing configuration names.
- Read `references/demo_prompts.md` for stable demo scenarios and acceptance checks.

## Quality Gate

Before final delivery, verify:

- The report contains `headline_conclusion` in a prominent hero position.
- The report shows data cutoff dates and any forward-looking limitation.
- The report contains "数据聚焦与服务对象" and "理论依据 / Methodology".
- Key conclusions include theory tags.
- Methodology display focuses on QFD / House of Quality and Matrix Analysis; other methods are summarized as supporting tags.
- If a product domain is named, the report contains product-domain technology mapping before detailed configuration analysis.
- Each differentiation bet has a Patsnap evidence row.
- Each named supplier or supplier category has evidence, maturity, role labels, and relationship status; otherwise it is marked as a lead to verify.
- Head-company benchmark includes Tesla, BYD, Huawei/Harmony Intelligent Mobility, or a stated reason for exclusion; overseas leaders are added when relevant.
- Patent and literature/paper evidence is displayed as dashboard/cards and technology-level patent pools, not as an unstructured raw list in the main report.
- Every level-1 technology in the product-domain map has a patent/literature pool summary card and a detail page or same-page anchor.
- Literature/paper absence is explicitly marked as "论文信号暂无，以专利为主" and does not block report generation.
- QFD pain points are graded by severity/importance and linked to engineering characteristics.
- Inventor signals are used only as technical continuity clues with limitations.
- Key configurations include 1-2 year future-state labels for technology, OEM/Tier0, and price band.
- Technology lifecycle strategy is visible for high-end / mid-end / low-end product positioning.
- Non-Patsnap data sources have reliability grade and acquisition path.
- The HTML can open offline and does not depend on external scripts.
- Missing image generation or web access does not block report generation.

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
