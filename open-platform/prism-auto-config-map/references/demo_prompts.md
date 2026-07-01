# Demo Prompts

Use these for stable sales demos and QA.

## Demo 1: Segment Opportunity

Prompt:

> 近一年上市的 20-30 万 B 级 EREV SUV,哪些配置已经成为必备,哪些还有差异化机会? 请输出棱镜车智-专利文献数据穿透报告。

Expected highlights:

- `headline_conclusion` appears in the hero area
- competitor pool is explicitly scoped
- Tesla, BYD, and Huawei/Harmony Intelligent Mobility appear as head-company benchmarks when relevant
- methodology display focuses on QFD / House of Quality and Matrix Analysis, not a flat list of many methods
- QFD shows graded pain points and engineering characteristics
- heatmap shows penetration
- Patsnap evidence wall appears as dashboard/cards, not a raw patent list
- data cutoff dates are visible

## Demo 2: Named Model Comparison

Prompt:

> 对比理想 L6/L7、问界 M7/M8、零跑 C16、阿维塔 07、智界 R7,输出下一代 B-SUV 专利文献数据穿透报告。

Expected highlights:

- model list preserved
- head-company benchmark appears without replacing the user's model pool
- Tesla, BYD, and Huawei/Harmony Intelligent Mobility appear or exclusion reasons are stated
- configuration gaps are mapped into quadrants
- no broad company strategy expansion
- local photoreal visual asset is used or gracefully replaced by SVG/CSS/chart placeholder

## Demo 3: Target Persona Recommendation

Prompt:

> 年轻家庭 25 万级 B-SUV,哪些配置该跟进,哪些适合作为专利壁垒型差异化?

Expected highlights:

- QFD / House of Quality maps young-family pain points to features and engineering characteristics
- pain points are graded P0/P1/P2/P3 and carry 1-5 importance weight
- Kano classification drives recommendation
- every differentiation bet has Patsnap patent/literature/supply-chain evidence
- report states which departments/roles the report serves

## Demo 4: Specific Feature Timing

Prompt:

> 电子外后视镜、地暖、二排腿托、座椅抽屉,哪些未来 6-18 个月值得布局?

Expected highlights:

- S-curve timing judgment
- patent barrier matrix
- technology lifecycle stage: 引领技术 / 上升技术 / 成熟技术 / 接近退出技术 / 退出技术
- literature foresight included when available
- watch/avoid cards for weak or risky features
- stale data impact is disclosed when applicable

## Demo 5: Supply-Chain Penetration

Prompt:

> 电子外后视镜、地暖、二排腿托、座椅抽屉分别涉及哪些功能模块、关键零部件和潜在 Tier0/Tier1/Tier2 供应商? 请只服务下一代 B-SUV 配置机会判断,不要扩展成泛供应链报告。

Expected highlights:

- configuration to module/component/technology/supplier mapping
- overseas supplier leads are included when supported by Patsnap or credible web evidence, especially Europe, North America, Japan/Korea, and Southeast Asia
- named companies are source-backed or marked as leads to verify
- OEM-supplier-patent relationship map distinguishes 已验证合作 / 专利联合申请 / 产品公告线索 / 待验证供应商线索
- supplier technology cards include role, linked OEM, relationship status, representative patents, cooperation signal, maturity, and planning implication
- supply-chain maturity feeds the opportunity quadrant

## Demo 6: 1-2 Year Future-State Forecast

Prompt:

> 基于 20-30 万 B 级 EREV SUV,预测未来 1-2 年电子外后视镜、地暖、二排腿托、座椅抽屉在技术、OEM/Tier0、价格段三个维度的状态。

Expected highlights:

- technology state: 已上车 / 量产导入 / 试点验证 / 预研储备 / 观望
- OEM/Tier0 state: 领先者 / 跟随者 / 试点者 / 暂未布局
- price-band state: 高端先行 / 中高端下沉 / 主流普及 / 暂不适合
- every forecast has three-factor basis and uncertainty
- Patsnap data cutoff and publication lag are visible

## Demo 8: Product Domain First

Prompt:

> 聚焦智能底盘,对比 25-35 万新能源 SUV 的空气悬架、CDC、后轮转向、线控制动和主动防倾杆,哪些适合下一代车型?

Expected highlights:

- report first shows product-domain technology map: intelligent chassis → level-1 technologies → level-2 configurations/components
- QFD / House of Quality links driving comfort, safety, handling, cost, and brand perception to engineering characteristics
- Matrix Analysis combines penetration, lifecycle, patent barrier, and supply maturity
- high-end / mid-end / low-end technology lifecycle strategy is visible

## Demo 9: Patent Dashboard

Prompt:

> 围绕智能座舱的 HUD、AI 助手、多屏联动和后排控制,请不要罗列专利,用专利看板说明哪些方向增长快、谁在布局、核心亮点是什么。

Expected highlights:

- patent output is dashboard/card based
- annual growth, applicant concentration, co-applicant network, inventor signal, and core patent highlights are visible
- core patent cards include detail URL or "详情链接待补"
- model-generated patent summary limitations are shown

## Demo 10: Delivery-Grade Full Flow Test

Prompt:

> 对比理想 L6/L7、问界 M7/M8、零跑 C16、阿维塔 07、智界 R7，面向 20-30 万级年轻家庭 B-SUV / EREV SUV 下一代车型规划，重点分析电子外后视镜、地暖/热舒适、二排腿托、座椅抽屉、智能座舱显示交互等配置，判断哪些已经成为必备配置，哪些适合作为未来 6-18 个月的差异化押注。请完整输出棱镜车智-专利论文数据穿透 HTML 报告，并为每个产品域一级技术生成专利/论文池详情页。

Expected highlights:

- output uses a fresh directory and does not overwrite prior test reports
- `index.html`, `patent_pools/*.html`, and `assets/vehicle_visuals/` are delivered together
- hero right side contains a main visual, caption/status tags, four methodology cards, and at least three summary metrics
- every core section contains a visual expression: local image, static chart, relationship card, heatmap, evidence card, or compact dashboard
- product-domain technology map is a table with product domain, level-1 technology, level-2 configuration/component, related model/benchmark, patent/literature pool, supplier role, and planning action
- heatmap includes a data-gap column
- each level-1 technology has a summary card, 3-5 representative patent PSE cards, and a detail page
- detail pages include patent detail links, paper/literature links or "详情链接待补", local visual block, full patent/literature tables, and data gap notes
- AI 前瞻创新发现 module recommends 3-5 new configuration ideas with basis, vehicle-fit concept, feasibility, supply maturity, risk, and action
- final zip contains no `__MACOSX` or `.DS_Store`

## Demo 7: Head-Company Benchmark

Prompt:

> 以特斯拉、比亚迪、华为系作为头部参照,判断 25 万级 B-SUV 下一代智能座舱和舒适配置应该怎么选。

Expected highlights:

- Tesla, BYD, and Huawei/Harmony Intelligent Mobility are separated by benchmark role
- report avoids claiming unsupported direct supplier relationships
- smart cockpit or China NEV local photoreal visual asset is selected from `assets/vehicle_visuals/photo_real`

## QA Checklist

- Contains `headline_conclusion`.
- Contains data cutoff dates and forward-looking caveat.
- Contains "数据聚焦与服务对象".
- Contains "理论依据 / Methodology".
- Methodology section highlights QFD / House of Quality and Matrix Analysis.
- Product-domain prompts include product-domain technology map before detailed analysis.
- QFD includes pain level and importance weight.
- Key conclusions have theory tags.
- Data source reliability grades are visible.
- Patsnap evidence is not hidden in appendix and is not a raw patent list.
- Patent evidence chain includes publication number, applicant, date, legal status where available, claim coverage, and decision impact.
- Patent dashboard includes annual growth, applicant concentration, co-applicant signal, inventor signal, detail URL field, and limitation note.
- Supplier findings include role, linked OEM, relationship status, evidence source, maturity, and planning implication.
- Overseas supplier findings include region, market coverage, evidence type, and confidence.
- Relationship map distinguishes verified links from leads to verify.
- Future-state forecasts cover technology, OEM/Tier0, and price-band states.
- Technology lifecycle x price-band strategy matrix is present for configuration recommendations.
- HTML works offline and does not require image generation or external scripts after assets are packaged.
- Main report images use `assets/vehicle_visuals/...`; detail page images use `../assets/vehicle_visuals/...`.
- No final image path uses `/Users/...`, `/tmp/...`, `../prism_auto_config_map/...`, or remote image URLs.
- HTML files parse with `python3 -m html.parser`.
- Main report links to every patent pool detail page, and each detail page links back to the main report.
- Delivery zips contain HTML, `patent_pools/`, and `assets/`, and remain usable after unzip into a temporary directory.
- Out-of-scope content is not expanded.
