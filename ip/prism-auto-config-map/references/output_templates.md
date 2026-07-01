# Output Templates

Use these structures for markdown drafts and HTML data preparation.

## Hero Decision Summary

| Field | Meaning |
|---|---|
| headline_conclusion | one sentence that states the future opportunity, risk, or action |
| market_scope | segment, price band, powertrain, model list |
| data_cutoff | market/configuration statistics cutoff |
| patsnap_cutoff | Patsnap patent/literature/company data cutoff |
| web_fetch_date | external web fetch date |
| forward_looking_caveat | stale data impact or publication-lag note |
| visual_asset | local photoreal asset path from `assets/vehicle_visuals/metadata.json`, with SVG fallback if needed |

`headline_conclusion` should be prominent and concise. It should not read like a generic summary.

## Evidence Row

| Field | Meaning |
|---|---|
| conclusion_id | stable id, e.g. C01 |
| theory_tag | QFD / House of Quality / Matrix Analysis / Benchmarking / Kano / S-Curve / Patent Barrier / Patsnap Penetration / Supply Linkage |
| claim | concise conclusion |
| market_evidence | configuration, parameter, official, or review signal |
| user_evidence | VOC, complaint, owner review, social weak signal |
| patsnap_evidence | patent, literature, applicant, citation, or supply-chain evidence |
| supplier_evidence | supplier role, source-backed company, relationship status, or lead_to_verify |
| future_state | 1-2 year state for technology/OEM-price band |
| confidence | high / medium / low |
| data_gap | missing data and impact |

## Product-Domain Technology Map

| Field | Meaning |
|---|---|
| product_domain | smart cockpit, intelligent chassis, thermal management, battery/e-drive, ADAS/safety, seat comfort, exterior body electronics |
| level_1_technology | primary technology branch under the domain |
| level_2_configuration_or_component | concrete configuration, subsystem, or component |
| supplier_type | OEM / Tier0 / Tier1 / Tier2 / research institution / unknown |
| analysis_object | what the report will compare or investigate |
| why_in_scope | why this branch matters to the user prompt |

## QFD / House Of Quality Row

| Field | Meaning |
|---|---|
| pain_level | P0 critical / P1 high / P2 medium / P3 low |
| user_need | target persona pain point or use scenario |
| importance_weight | 1-5 |
| configuration | visible configuration or package |
| engineering_characteristic | measurable engineering enabler or subsystem |
| competitor_satisfaction | high / medium / low / missing |
| patsnap_strength | strong / forming / weak / unavailable |
| target_value | next-generation planning target |
| planning_action | must_follow / differentiation_bet / watch / avoid_or_design_around |

## Matrix Analysis Row

| Field | Meaning |
|---|---|
| configuration | feature or package |
| market_penetration | high / medium / low / unknown |
| qfd_importance | 1-5 |
| lifecycle_stage | 引领技术 / 上升技术 / 成熟技术 / 接近退出技术 / 退出技术 / unknown |
| patent_barrier | low / medium / high / unknown |
| supply_maturity | scarce / forming / diversified / mature / lead_to_verify / unknown |
| head_company_signal | Tesla / BYD / Huawei / overseas leader / none / not_applicable |
| matrix_decision | must_follow / differentiation_bet / watch / avoid_or_design_around |
| rationale | short decision explanation |

## Patsnap Penetration Chain

| Step | Required Content |
|---|---|
| 市场配置现象 | penetration, fitment, VOC, head-company benchmark |
| 专利/文献趋势 | patent trend, literature foresight, inflection |
| 关键申请人 | OEM / Tier0 / Tier1 / Tier2 / institution |
| 核心专利 | publication number, applicant, date, legal status |
| 问题-方案-效果 | technical problem, solution, claimed effect |
| 供应链可行性 | supplier count, cooperation signal, maturity |
| 未来 1-2 年判断 | technology state, OEM/Tier0 state, price-band state |

## Technology Patent-Literature Pool

Create one pool for every level-1 technology in the product-domain map. The main report shows a summary card; the full data goes to `patent_pools/{technology_slug}.html` or a same-page `#pool-{technology_slug}` anchor when multi-page output is unavailable.

| Field | Meaning |
|---|---|
| technology_slug | stable URL-safe slug, e.g. `seat-actuator`, `thermal-comfort-control` |
| product_domain | product domain from the technology map |
| level_1_technology | primary technology branch; every analyzed level-1 technology must be represented |
| level_2_configurations | linked configurations/components under this technology |
| search_query | patent retrieval formula, keywords, synonyms, and exclusions |
| search_window | filing/publication/literature time window |
| patent_pool_count | full count of relevant patents in this technology pool |
| literature_pool_count | full count of relevant papers/literature records; may be 0 |
| literature_signal | strong / forming / weak / unavailable; if 0 show "论文信号暂无，以专利为主" |
| trend_signal | annual patent/literature trend or inflection summary |
| layout_clusters | distribution of layout points, e.g. structure, control, material/process, system integration, UX, safety/regulation |
| applicant_role_split | OEM / Tier0 / Tier1 / Tier2 / institution / unknown distribution |
| representative_patents | 3-6 core patents selected for the main report |
| full_patent_list | complete patent pool for the detail page; do not truncate due to template limits |
| full_literature_list | complete literature/paper pool when available |
| future_state | 1-2 year technology/OEM-price-band forecast |
| confidence | high / medium / low |
| data_gap | missing data and planning impact |
| pool_detail_path | `patent_pools/{technology_slug}.html` or `#pool-{technology_slug}` |

## Representative Patent PSE Card

Use 3-5 cards per level-1 technology in the main report. Keep the full patent fields in the detail page.

| Field | Meaning |
|---|---|
| publication_number | patent publication number |
| title | patent title or readable short title |
| applicant | applicant(s), with OEM/Tier0/Tier1/Tier2/institution role when known |
| filing_or_publication_date | filing/publication date and cutoff note |
| legal_status | granted / pending / expired / invalid / unknown |
| technical_problem | product or engineering problem addressed |
| solution | claimed or summarized technical solution |
| expected_effect | expected technical/user/business effect |
| product_planning_implication | how the patent affects next-vehicle configuration planning |
| risk_or_design_around | patent, regulation, UX, cost, supplier, or implementation risk and suggested workaround |
| detail_url | Patsnap/source detail URL or "详情链接待补" |
| limitation_note | LLM summary limitation, missing claim/legal review, stale data, or translation caveat |

## Patent Pool Detail Page

Use this structure for every level-1 technology detail page. Do not create one page per individual patent; individual patents should link to Patsnap/source detail URLs where available.

| Section | Required Content |
|---|---|
| Header | technology name, product domain, pool count, literature count, cutoff, confidence |
| Technology summary | linked configurations/components, user need, engineering role, planning implication |
| Retrieval scope | search query, synonyms, exclusions, source/tool, search window |
| Layout clusters | distribution by layout point with counts and short interpretation |
| Trend view | static SVG/CSS sparkline or table for annual patent and literature signals |
| Representative patents | publication number, title, applicant, date, legal status, problem-solution-effect, planning implication, detail URL |
| Full patent list | complete table grouped by layout point, applicant, year, or legal status when data is rich |
| Full literature list | complete paper/literature table; if unavailable, show the no-literature fallback |
| Applicant/supplier view | OEM/Tier0/Tier1/Tier2/institution split, cooperation signal, maturity |
| Data gap notes | unavailable fields, stale data, LLM limitation, and confidence impact |

Detail-link rules:

- Patent rows should include a Patsnap/source detail link when available.
- Paper/literature rows should include a URL when available.
- If no URL is available, show "详情链接待补"; do not omit the detail-link column.
- Detail page visuals must use `../assets/vehicle_visuals/...` for both `src` and `data-fallback`.

## AI Forward Innovation Discovery

Add this module after the patent-paper penetration wall in delivery-grade HTML reports.

| Field | Meaning |
|---|---|
| innovation_name | concise new configuration or feature concept |
| related_technology_domain | linked product domain and level-1 technology |
| discovery_basis | patent pool signal, literature signal, configuration gap, VOC, or supply-chain clue |
| vehicle_fit_concept | how the idea could be packaged or mounted on the next vehicle |
| one_to_two_year_feasibility | high / medium / low with short reason |
| supply_chain_maturity | scarce / forming / diversified / mature / lead_to_verify |
| risk | regulation / UX / cost / patent barrier / thermal safety / supplier concentration / data gap |
| recommended_action | prototype / supplier scan / design-around / watch / reject for now |
| confidence | high / medium / low |

## Configuration Opportunity Quadrant

| Quadrant | Decision Meaning | Minimum Evidence |
|---|---|---|
| must_follow | next vehicle should include it as baseline | high penetration or strong user need |
| differentiation_bet | use as next-cycle distinctive feature | low penetration + Patsnap patent/literature/supply-chain strong signal |
| watch | promising but not ready | one strong signal missing |
| avoid_or_design_around | avoid direct copy or redesign | high patent barrier or negative VOC |

## Patent Evidence Chain

| Field | Meaning |
|---|---|
| configuration | feature or configuration item |
| search_query | retrieval formula, keyword set, or technical synonyms |
| patent_count | count and time window |
| trend_signal | annual trend, inflection, or no clear signal |
| top_applicants | applicants and concentration |
| core_patent | publication number, title, applicant, filing date |
| detail_url | Patsnap/source detail URL or "详情链接待补" |
| legal_status | granted / pending / expired / invalid / unknown |
| claim_coverage | covered implementation point |
| problem_solution_effect | technical problem, solution, effect |
| technical_highlight | reader-friendly product/engineering highlight |
| limitation_note | LLM summary limitation, missing legal status, stale data, or translation caveat |
| citation_family_signal | citation/family/jurisdiction signal |
| product_decision_impact | follow / design-around / bet / watch / avoid |
| cutoff | data cutoff and tool/source |

## Patent-Paper Dashboard Card

| Field | Meaning |
|---|---|
| product_domain | domain being analyzed |
| level_1_technology | technology branch |
| technology_slug | stable id used for detail-page path or same-page anchor |
| pool_detail_path | link to the full patent/literature pool |
| patent_pool_count | full pool count, not just displayed representative patents |
| literature_pool_count | literature/paper count; 0 is allowed with fallback note |
| literature_signal | strong / forming / weak / unavailable |
| layout_clusters | concise distribution of technical layout points |
| company_or_applicant | OEM/Tier0/Tier1/Tier2/institution |
| annual_growth_signal | rising / flat / declining / inflection / unavailable |
| applicant_concentration | low / medium / high / unknown |
| co_applicant_signal | joint applicants and publication evidence |
| inventor_signal | high-frequency inventor or team-cluster clue with limitation |
| core_patent_highlight | publication number + one-line highlight |
| detail_url | source detail URL or "详情链接待补" |
| planning_implication | follow / bet / watch / design-around / avoid |

## Supplier Technology Card

| Field | Meaning |
|---|---|
| company_name | supplier or OEM/Tier0/Tier1/Tier2 name |
| role | OEM / Tier0 / Tier1 / Tier2 / patent_applicant / unknown |
| region | China / Europe / North America / Japan-Korea / Southeast Asia / Global / unknown |
| market_coverage | China / overseas / global / regional |
| overseas_relevance | benchmark / sourcing_candidate / technology_reference / localization_lead / not_applicable |
| linked_oem | connected automaker or ecosystem, if any |
| relationship_status | 已验证合作 / 专利联合申请 / 产品/公告线索 / 待验证供应商线索 |
| evidence_type | Patsnap company / joint patent / official source / annual report / teardown / web lead / unavailable |
| related_configuration | configuration and subsystem |
| core_technology_traits | source-backed technical traits |
| representative_patents | publication numbers or patent families |
| cooperation_signal | joint applicant, customer case, filing, announcement, product page, or PR lead |
| maturity | lead_to_verify / scarce / forming / diversified / mature |
| planning_implication | cooperate / watch / design-around / high supply risk |
| sources | source name, grade, date, URL/title |

## OEM-Supplier-Patent Relationship Row

| Field | Meaning |
|---|---|
| oem | automaker or brand ecosystem |
| tier0_or_integrator | Tier0/ecosystem player if relevant |
| supplier | Tier1/Tier2 or patent applicant |
| configuration | linked configuration or subsystem |
| relationship_status | 已验证合作 / 专利联合申请 / 产品/公告线索 / 待验证供应商线索 |
| evidence | source title, patent publication number, announcement, filing, or data gap |
| confidence | high / medium / low |

## 1-2 Year Future-State Matrix

| Field | Meaning |
|---|---|
| configuration | feature or configuration item |
| technology_state | 已上车 / 量产导入 / 试点验证 / 预研储备 / 观望 |
| oem_tier0_state | 领先者 / 跟随者 / 试点者 / 暂未布局 |
| price_band_state | 高端先行 / 中高端下沉 / 主流普及 / 暂不适合 |
| factor_market | fitment or penetration evidence |
| factor_patsnap | patent/literature evidence |
| factor_supply_chain | supplier maturity evidence |
| confidence | high / medium / low |
| uncertainty | regulation / cost / user acceptance / supplier concentration / data gap |

## Technology Lifecycle x Price-Band Strategy Matrix

| Field | Meaning |
|---|---|
| configuration | feature or technology |
| lifecycle_stage | 引领技术 / 上升技术 / 成熟技术 / 接近退出技术 / 退出技术 |
| high_end_strategy | benchmark / selling_point / baseline / exclude |
| mid_end_strategy | selling_point / baseline / cost_watch / exclude |
| low_end_strategy | baseline / cost_control / risk_disclose / exclude |
| evidence_basis | market + Patsnap + supply-chain basis |
| risk_note | UX, regulation, cost, brand, patent, or data-gap risk |

## Recommendation Card

```markdown
### [Kano][Patent Barrier][Supply Linkage] Configuration Name

- Decision: must_follow / differentiation_bet / watch / avoid_or_design_around
- Target user need:
- Configuration logic:
- Market evidence:
- User evidence:
- Patsnap penetration chain:
- Supplier linkage:
- Future state:
- Risk / design-around:
- Confidence:
```

## HTML Rendering Notes

Use `assets/report_template.html` as the visual skeleton. Replace placeholder text and tables directly or via the host agent's renderer.

The final HTML must:

- work offline
- include no external scripts
- show `headline_conclusion` in the hero area
- show data cutoff dates and forward-looking limitation
- include "数据聚焦与服务对象"
- include product-domain technology map when a domain is specified
- emphasize QFD / House of Quality and Matrix Analysis as the main methodology
- show graded pain points in QFD
- emphasize Patsnap patent-paper dashboard and technology penetration wall visually
- render one technology patent/literature pool summary card for every level-1 technology in the product-domain map
- link each technology pool summary to `patent_pools/{technology_slug}.html`; if multi-page output is unavailable, link to same-page anchors instead
- keep main-report charts compact and move long patent/literature tables to detail pages or same-page appendices
- preserve full data in `full_patent_list` and `full_literature_list`; do not silently crop rich datasets to fit a fixed visual template
- show "论文信号暂无，以专利为主" when literature/paper retrieval returns no usable records
- include OEM-supplier-patent relationship map
- include overseas supply-chain fields when evidence supports them
- include technology lifecycle x price-band strategy
- include source grades and acquisition paths
- include theory tags in the text
- use a balanced hero visual panel plus selective small chapter images for reading rhythm; use local photoreal visual assets first, degrade to SVG fallback, then CSS/chart placeholders when no image exists
- use responsive card grids, scrollable tables, wrapped long text, and high-contrast chart labels so desktop and mobile layouts remain readable
- use `assets/vehicle_visuals/...` image paths in `index.html`
- use `../assets/vehicle_visuals/...` image paths in `patent_pools/*.html`
- never use `/Users/...`, `/tmp/...`, `../prism_auto_config_map/...`, remote image URLs, or remote image fallbacks as final report image paths
- include the report-local `assets/vehicle_visuals/` directory in the delivered folder and zip
