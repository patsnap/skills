# Supply Chain Lens

供应链穿透只服务「下一代车型配置机会判断」，不扩展成泛供应链报告。目标是回答：某个配置如果要上车，背后需要哪些功能模块、关键零部件、核心技术、潜在供应商，以及车企与供应链之间是否存在可验证联系。

## Core Mapping

Every key configuration should be mapped as:

`产品域 → 配置项 → 功能模块 → 关键零部件 → 核心技术 → 供应商类型 → 区域/市场 → 可关注企业 → 车企/供应链关系 → 证据来源`

Example:

| 配置项 | 功能模块 | 关键零部件 | 核心技术 | 供应商类型 |
|---|---|---|---|---|
| 电子外后视镜 | 车身/座舱显示/感知 | 摄像头、显示屏、控制器、除雾/加热结构 | 低延迟显示、HDR 成像、法规适配、冗余安全 | OEM/Tier0 系统集成、Tier1 电子后视镜系统、Tier2 摄像头/显示模组 |
| 二排腿托 | 座椅舒适系统 | 座椅骨架、电机、滑轨、传感器、控制器 | 小空间布置、耐久、电机控制、碰撞安全 | Tier1 座椅系统、Tier2 电机/骨架/滑轨 |
| 地暖 | 热管理/座舱舒适 | 加热膜、线束、温控器、热管理控制 | 低功耗加热、温控安全、材料耐久 | Tier1 热管理/内饰系统、Tier2 加热材料 |
| 座椅抽屉 | 座椅/储物系统 | 抽屉结构、锁止机构、滑轨、碰撞保护 | 结构集成、NVH、碰撞安全、耐久 | Tier1 座椅/内饰系统、Tier2 滑轨/锁止件 |

## Supplier Role Definitions

- **OEM**: 整车品牌或主机厂，负责车型定义和系统集成决策。
- **Tier0**: 生态型系统集成方或深度参与整车/智能化方案定义的平台型合作方。华为系/鸿蒙智行在报告中默认按 Tier0/ecosystem integrator 视角展示，除非客户另有定义。
- **Tier1**: 直接向 OEM 供应系统或总成的企业，如座椅系统、热管理系统、电子后视镜系统供应商。
- **Tier2**: 向 Tier1 提供关键零部件、材料、模组或算法的企业。
- **Patent applicant**: 可能是 OEM、Tier0、Tier1、Tier2、研究机构或个人，需要结合业务证据判断角色。

If the customer uses a different Tier0 definition, follow the customer's definition and state it in the report.

## OEM-Supplier-Patent Relationship Map

The report should include a visible relationship map. Each link must be labeled with one of:

| Relationship Status | Meaning | Minimum Evidence |
|---|---|---|
| 已验证合作 | OEM and supplier relationship is directly supported | official supplier announcement, procurement statement, annual report, teardown database, or credible OEM case |
| 专利联合申请 | two parties appear as joint applicants | Patsnap co-applicant evidence with publication number or family |
| 产品/公告线索 | product page, model launch, regulatory filing, or credible media points to a relationship | official product page, MIIT filing, launch material, supplier page |
| 待验证供应商线索 | only weak signal exists | PR, rumor, recruitment JD, social/media lead; cannot be treated as confirmed |

Do not show a visual link without a status and source. If the evidence is weak, the visual should still display it as "待验证供应商线索" with lower confidence.

## Evidence Sources

### Patsnap / 智慧芽

- joint applicants: identify technical collaboration beyond PR statements.
- applicant technology distribution: determine each supplier's technical focus.
- patent families and legal status: infer international layout and commercialization seriousness.
- key patents and citations: identify lock-point technologies.
- company technology profile where available: summarize technical strengths.

### Overseas Supply-Chain Enrichment

When the product domain is relevant, supplement China-centric analysis with overseas supply-chain signals from Europe, North America, Japan/Korea, and Southeast Asia.

Default overseas benchmark automakers and ecosystems:

- Tesla: global EV platform, electronics, software-defined vehicle, vertical integration signal.
- Volkswagen: global platformization, European supply-chain ecosystem, cost/scale benchmark.
- Toyota: hybrid, reliability, safety, thermal and manufacturing maturity benchmark.
- Hyundai/Kia: E-GMP, global EV commercialization, ADAS/cockpit/chassis supplier linkage.
- Mercedes-Benz: high-end comfort, chassis, safety and cockpit benchmark.

Use named overseas suppliers only when supported by Patsnap company data, patents, official pages, annual reports, credible teardown data, or reliable industry sources. If the evidence is weak, show the company as "待验证海外供应链线索".

Overseas regions:

| Region | Use |
|---|---|
| China | local NEV commercialization, BYD/Huawei ecosystem, China Tier1/Tier2 maturity |
| Europe | premium chassis, cockpit, safety, lighting, thermal, established Tier1 ecosystems |
| North America | Tesla platform/software/electronics benchmark and startup supply-chain signals |
| Japan/Korea | reliability, hybrid/e-drive, ADAS/safety, battery/electronics maturity |
| Southeast Asia | localization, manufacturing transfer, cost-sensitive regional supply-chain clues |

Do not force overseas suppliers into the report if the prompt is purely domestic and no credible evidence is available.

### Non-Patsnap Sources

- supplier official website and product pages
- annual report or prospectus
- OEM supplier announcement or procurement statement
- industry reports such as Zosi, broker reports, S&P Global Mobility
- Tianyancha/Qichacha for equity and investment context
- teardown reports and credible media reviews

Do not treat PR statements alone as proof of technical binding. Use PR as a clue, then verify with patents, joint applications, product pages, filings, or teardown/OEM cases.

## Supplier Technology Card

Each named company should be represented with:

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
| configuration_relevance | related configuration and subsystem |
| core_technology_traits | 2-4 technical traits, source-backed |
| representative_patents | publication numbers or patent families where available |
| cooperation_signal | joint applicant, customer case, announcement, product page, or none |
| maturity | lead_to_verify / scarce / forming / diversified / mature |
| risk | concentration, legal barrier, cost, regulation, capacity, or unknown |
| sources | source name, grade, URL/title, fetch date |

## Supply-Chain Maturity Scoring

Use four levels:

- **scarce**: one or two credible players, limited patent/product evidence.
- **forming**: several applicants or suppliers appear, but customer/OEM validation is limited.
- **diversified**: multiple Tier1/Tier2 players, product pages or OEM cases exist.
- **mature**: broad supplier base, high fitment, patents are no longer the bottleneck.

If evidence is weak, mark as **lead_to_verify** instead of assigning maturity.

## Planning Implications

- **可合作**: supplier maturity is diversified/mature and patent barrier is manageable.
- **需观察**: promising but weak OEM case, regulation, or cost uncertainty.
- **需绕开**: high patent concentration or core claims cover likely implementation.
- **供应风险高**: few suppliers, single-source risk, unclear productization, or capacity concern.

## Quality Rules

- Never name a supplier as "优秀供应商" without evidence.
- For each recommended supplier category, explain why it matters to the configuration decision.
- Supplier insight should not become a standalone company profile; keep it tied to the configuration.
- If supplier data is unavailable, output "供应链数据缺口" and state the impact on confidence.
- Relationship maps must visually distinguish verified links from leads to verify.
- Overseas supplier analysis must include region, market coverage, evidence type, and relevance to the user's product domain.
- PR-only overseas leads must remain "待验证海外供应链线索" and cannot support strong recommendations alone.
