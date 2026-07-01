# Patsnap Data Lens

Wisdom of the skill: Patsnap patent, literature, applicant, and company data must explain why a configuration matters, whether it can be followed, whether there is a patent or supply-chain barrier, and what may happen in the next 1-2 years.

## Core Penetration Chain

Every major recommendation should show this chain in the main report:

`市场配置现象 → 专利/文献趋势 → 关键申请人 → 核心专利 → 技术问题-方案-效果 → 供应链可行性 → 未来 1-2 年判断`

Use this chain to avoid shallow claims such as "a feature is popular" or "patents are rising". The report should explain what the data reveals about design intent, timing, barriers, and sourcing feasibility.

## Lens 0: Patent Dashboard

Goal: avoid raw patent-list output and make patent data readable for product planning.

The main report should show a dashboard by company, product domain, and level-1 technology:

| Dashboard Block | Required Content |
|---|---|
| annual_growth | patent/literature trend by year, growth or inflection |
| company_view | top applicants by OEM/Tier0/Tier1/Tier2 and head-company benchmark relevance |
| domain_view | product domain and level-1 technology distribution |
| applicant_concentration | top applicant share or qualitative concentration level |
| co_applicant_network | joint applicants with publication/family evidence where available |
| inventor_signal | high-frequency inventors, repeated technical direction, or team cluster clues |
| core_patent_highlights | 3-6 cards with technical highlight and planning implication |
| detail_link | Patsnap or source detail URL when available; otherwise mark "详情链接待补" |
| llm_limitation | what the model summary may miss, e.g. claim scope, legal status freshness, translation ambiguity |

Required rule: do not make the core report a raw list of patents. Raw patent lists may appear only in an appendix.

## Lens 1: Patent Moat

Goal: determine whether a configuration has a defensible technical barrier.

Useful tools:

- `patent-search.search_patent_count`
- `patsnap-search.patsnap_search`
- `patsnap-search.patsnap_fetch`
- `patent-briefing.tech_summary`

Evidence to extract:

- patent count by configuration keyword / technical synonym
- granted/effective patent count where available
- top applicants and applicant concentration
- patent families and jurisdiction coverage where available
- core patent title, publication number, filing date, publication date
- legal status and applicant
- claim scope summary
- "problem-solution-effect" summary

Report output:

- moat level: low / medium / high / unknown
- design-around difficulty
- why it matters for product planning
- freshness: Patsnap data cutoff and query window

## Lens 1B: Patent Evidence Chain

Goal: make every core patent claim traceable, verifiable, and useful for product planning.

Each key configuration should include at least one patent evidence chain:

| Field | Meaning |
|---|---|
| configuration | feature or configuration item |
| search_query | retrieval formula, keyword set, or technical synonyms |
| patent_count | total count and time window |
| trend_signal | annual trend or inflection point |
| top_applicants | top applicants and concentration |
| core_patent | publication number, title, applicant, filing date |
| detail_url | Patsnap/source detail page if available; otherwise "详情链接待补" |
| legal_status | granted, pending, expired, invalid, unknown |
| claim_coverage | short summary of covered implementation points |
| problem_solution_effect | technical problem, solution, effect |
| technical_highlight | one-line highlight in product/engineering language |
| limitation_note | model-summary limitation or missing source caveat |
| citation_family_signal | forward citation, family size, jurisdiction coverage |
| product_decision_impact | follow, design-around, bet, watch, avoid |
| cutoff | data cutoff date and tool/source |

Required rule: do not output a strong patent barrier conclusion if publication number, applicant, and date are missing.

## Lens 2: Literature Foresight

Goal: capture earlier research signals than patents, especially for materials, thermal management, batteries, safety, cockpit interaction, and ADAS.

Useful tools:

- `literature-search.search_literature`
- academic web fallback where allowed by the host agent
- `landscape-projects.landscape_job_create`
- `landscape-projects.landscape_job_result`

Evidence to extract:

- paper/literature activity by year
- institutions, companies, and repeated technical themes
- conference/journal topic clusters
- connection to later patent keywords or applicant activity

Report output:

- literature signal: weak / forming / strong / unavailable
- commercialization certainty: low / medium / high
- relationship to patent trend: leading / aligned / lagging / conflicting
- planning implication: pre-research, watch, next-cycle bet, or avoid

## Lens 3: Technology Maturity / S-Curve

Goal: determine the maturity and timing of the technology behind a configuration.

Useful tools:

- `patent-visual.trends`
- `literature-search.search_literature`
- `landscape-projects.landscape_job_create`
- `landscape-projects.landscape_job_result`

Evidence to extract:

- annual patent trend
- growth inflection
- paper/literature activity
- applicant expansion
- technology topic clusters
- grant/legal status mix when available

Report output:

- S-curve stage: emerging / growing / mature / saturated / unknown
- timing implication: now follow / next-cycle bet / watch / too early
- 1-2 year technology state: 已上车 / 量产导入 / 试点验证 / 预研储备 / 观望

## Lens 4: Applicant And Supplier Penetration

Goal: identify who is actually shaping the technology and whether the player mix supports industrialization.

Useful tools:

- `patent-visual.cooperation_applicant_analysis`
- `patent-visual.applicant_technology_analysis`
- `report-gen.company_report_create`
- `patsnap-search.patsnap_fetch`

Evidence to extract:

- OEM/Tier0/Tier1/Tier2 applicant count
- joint applicants and repeated co-applicant patterns
- inventor signal: high-frequency inventors, repeated technical themes, possible team clusters, cross-company repeated names where source-backed
- applicant technology specialization
- geographic/market coverage
- applicant trend by year
- whether Tesla, BYD, Huawei/Harmony Intelligent Mobility, or other leaders appear as applicants, collaborators, or reference benchmarks

Report output:

- supplier base: scarce / forming / diversified / mature / unknown
- industrial feasibility
- likely sourcing constraint
- recommended supplier role: OEM / Tier0 / Tier1 / Tier2
- relationship status: 已验证合作 / 专利联合申请 / 产品/公告线索 / 待验证供应商线索

Inventor-signal limits:

- Inventor data may support technical continuity, repeated R&D direction, and team-cluster clues.
- Inventor data must not be used alone to infer employment relationship, supplier relationship, equity relationship, or confirmed cooperation.
- Joint applicants are stronger than inventor overlap for cooperation inference.

## Lens 5: Key Patent Explanation

Goal: turn patent data from a list into design reasoning.

Useful tools:

- `patent-briefing.tech_summary`
- `patent-briefing.bibliography`
- `patent-briefing.intelligent_image`
- `patent-search.get_patent_forward_citation`
- `patent-search.get_patent_description`

Evidence to extract:

- technical problem
- technical solution
- claimed effect
- forward citation strength
- representative drawings where available
- hidden engineering constraint

Report output:

- design intent
- hidden engineering constraint
- likely next-generation implementation
- product decision impact

## Lens 6: Opportunity Window

Goal: find real opportunities by intersecting market and Patsnap evidence.

Decision rules:

- **Must follow**: high penetration or strong user need, and low/medium patent barrier.
- **Differentiation bet**: low market penetration, rising patent/literature signal, and at least 3 credible supply-chain players or applicants.
- **Watch**: promising signal but insufficient user acceptance, regulatory clarity, or supply-chain depth.
- **Avoid/design-around**: high patent barrier, concentrated applicants, key patents hard to bypass, or negative VOC.

Required report evidence:

- market signal
- user/VOC signal where available
- Patsnap patent signal
- literature foresight signal
- applicant/supply-chain signal
- theory tag
- confidence level

## Lens 7: 1-2 Year Future-State Forecast

Goal: predict the likely state of technologies, OEM/Tier0 activity, and price-band diffusion without changing the skill into a broad strategy report.

Default time window: 1-2 years, aligned with next-generation or mid-cycle model planning.

Forecast dimensions:

| Dimension | States |
|---|---|
| Technology future state | 已上车 / 量产导入 / 试点验证 / 预研储备 / 观望 |
| OEM/Tier0 future state | 领先者 / 跟随者 / 试点者 / 暂未布局 |
| Price-band future state | 高端先行 / 中高端下沉 / 主流普及 / 暂不适合 |

Three-factor basis:

1. market fitment or configuration penetration
2. Patsnap patent/literature trend
3. supplier player count and cooperation network maturity

Every forecast must include:

- forecast state
- top 2 evidence points
- confidence: high / medium / low
- uncertainty: regulation, cost, user acceptance, supplier concentration, or data gap
- cutoff and stale-data impact if any

## Lens 8: Technology Lifecycle Configuration Strategy

Goal: translate S-curve and market evidence into high-end / mid-end / low-end configuration strategy.

Lifecycle stages:

| Stage | Evidence Basis | Product Strategy |
|---|---|---|
| 引领技术 | low-to-medium penetration, strong head-company signal, premium product use, strong patent/literature momentum | high-end benchmark |
| 上升技术 | growing patents/literature, more applicants, early fitment, improving supply base | high/mid-end selling point |
| 成熟技术 | broad fitment, stable suppliers, lower uncertainty | baseline or value-for-money base |
| 接近退出技术 | declining technical signal, lower cost, still usable in constrained products | low-end cost control with UX/brand risk |
| 退出技术 | negative VOC, regulation risk, technical obsolescence, poor brand fit | avoid |

Price-band guidance:

- 高端产品: include leading technology as marker, rising technology as selling point, mature technology as base, exclude exiting technology.
- 中端产品: combine rising and mature technologies for value-for-money competition.
- 低端产品: use mature and near-exit technologies only with explicit risk disclosure.

## Important Limits

- Patent data has publication lag. State the cutoff date.
- Patent count does not equal market adoption.
- Literature signal may be earlier than patent signal but has lower commercialization certainty.
- Supplier names from PR or media must be treated as leads until verified by patents, product pages, filings, or credible OEM cases.
- Future-state forecasts are planning signals, not deterministic predictions.
- If Patsnap data is unavailable, explicitly mark the Patsnap lens as unavailable.
- Patent summaries generated by an LLM are planning aids. State limitations for claim scope, legal status freshness, jurisdiction coverage, and translation ambiguity when relevant.
