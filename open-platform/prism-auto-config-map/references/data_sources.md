# Data Sources And Reliability

This file defines non-Patsnap data sources, acquisition paths, reliability grades, freshness rules, and fallback behavior.

## Freshness Principle

棱镜车智-专利文献数据穿透服务未来预测,所有检索都应使用当前执行环境可获得的最新数据。

- The report must display `数据统计截止日期`, `Patsnap 数据截止日期`, and `外部网页获取日期`.
- Use the newest available official pages, configuration libraries, patent/literature snapshots, and supplier pages.
- If a source is older than the analysis need, add a "前瞻性影响说明" and lower confidence.
- For time-series charts, show the actual coverage window, not only the report date.
- Do not use stale snapshots to make strong 6-18 month timing recommendations.

## A Grade: Official Or Quasi-Official

Use first for objective parameters, safety, regulatory facts, and launch timing.

| Source | Data | Acquisition | Reliability | Freshness Rule | Fallback |
|---|---|---|---|---|---|
| MIIT vehicle announcement | model filing, dimensions, curb weight, battery, energy consumption | official query system / official pages / PDF parsing | A | use latest announcement batch available | use OEM official page and mark regulatory data missing |
| OEM official website | price, trim, official configuration, launch info | page scrape or manual URL | A | fetch latest model/trim page | use Autohome/Dongchedi and mark "not OEM confirmed" |
| C-NCAP | crash/safety assessment | official result pages | A | latest published result | mark safety rating unavailable |
| C-IASI | safety, repairability, occupant protection | official result pages/PDF | A | latest published result | mark insurance safety index unavailable |
| Government/regulatory policy | regulation, access rule, safety requirement | official site/PDF | A | latest effective or draft date | mark regulatory uncertainty |

## B Grade: Commercial Or Industry Data

Use for configuration penetration, volume, market calibration, and supplier/product evidence. Formal production should use licensed API or authorized data export where possible.

| Source | Data | Acquisition | Reliability | Freshness Rule | Fallback |
|---|---|---|---|---|---|
| Autohome configuration library | configuration matrix, parameters | licensed API preferred; crawler only for demo/back-up | B | refresh close to report date | Dongchedi + OEM pages |
| Dongchedi configuration library | configuration and tested data | licensed API preferred; crawler back-up | B | refresh close to report date | Autohome + media review |
| Insurance/compulsory insurance volume | real registrations, channel pressure | commercial purchase | B | latest month/quarter | public sales as weak proxy, mark volume gap |
| S&P Global Mobility / similar | market forecast, strategy context | subscription | B | latest forecast release | public excerpts only, lower confidence |
| Zosi / broker reports | system-level trends, technology context | subscription or public abstracts | B | latest report date | media review and Patsnap trend only |
| Tianyancha / Qichacha | company, equity, investment | commercial API | B | latest registry snapshot | company official and news, lower confidence |
| Supplier official website / annual report | product lines, customers, technical capabilities | official page, annual report, prospectus | B | latest page/report | mark supplier role as lead_to_verify if not cross-validated |
| Teardown / supply-chain database | component supplier evidence | subscription or credible teardown report | B | latest teardown/model year | use patent/applicant evidence as support |

## C Grade: Public Web

Use as support. Do not let C-grade sources alone drive high-confidence conclusions.

| Source | Data | Acquisition | Reliability | Freshness Rule | Fallback |
|---|---|---|---|---|---|
| 12365Auto / 车质网 | complaints, quality feedback | scrape/search | C | latest complaint window | owner reviews and media comments |
| Media reviews | test drive, configuration photos, comparison | search/scrape/RSS | C | latest review for target model year | OEM official images and specs |
| Owner reviews | satisfaction, real use scenes | scrape/search | C | latest sample window | mark VOC insufficient |
| Xiaohongshu/Douyin/Bilibili | scenario, attention, sentiment | search/scrape where allowed | C-weak | latest visible posts, sample disclosed | do not use as deciding evidence |

## D Grade: Weak Signals

Use only as auxiliary evidence.

- recruitment JD
- supplier PR statements
- dealer quotes
- forum discussions
- second-hand residual value
- unverified social posts

## Head-Company Benchmark Requirement

When analyzing whole-vehicle enterprise comparison or segment opportunity, include top-company references when relevant:

- Tesla: overseas benchmark for EV architecture, software-defined vehicle, cost-down, and charging ecosystem.
- BYD: China NEV benchmark for vertical integration, battery/electric drive, high-volume platformization.
- Huawei/Harmony Intelligent Mobility: China Tier0/ecosystem benchmark for intelligent cockpit, ADAS, channel, and cross-OEM collaboration.
- Other China NEV leaders or overseas leaders should be added when they directly shape the segment.

If the user provides a strict model list, preserve it, then add a small "头部标尺" comparison rather than changing the user's pool.

## Source Citation Requirements

Each evidence row should include:

- source name
- grade
- acquisition mode
- fetch date or data cutoff
- exact URL or document title when available
- confidence impact
- forward-looking limitation if the source is stale

## Degradation Rules

- If no B-grade configuration database is available, use OEM configuration pages plus media reviews as small-sample analysis and show a sample limitation card.
- If no VOC is available, do not make strong reverse-Kano claims.
- If no Patsnap data is available, do not output strong patent barrier or S-curve maturity claims.
- If supplier evidence is based only on PR or media, mark it as "待验证供应商线索" and do not call it a confirmed supplier.
- If official and commercial sources conflict, show both and recommend the official source for objective parameters.
- If data freshness is insufficient, show the limitation in the hero freshness strip and reduce confidence.
