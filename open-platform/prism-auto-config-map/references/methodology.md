# Methodology: QFD / House of Quality + Matrix Analysis

棱镜车智仍保留原有 5 Lens，但展示和推理主轴收束为两层：第一层用 QFD / House of Quality 把用户痛点翻译为工程和配置语言；第二层用 Matrix Analysis 把市场、专利、供应链、生命周期和竞品标尺合成配置动作。

## 1. Primary Lens: QFD / House of Quality

Purpose: translate graded customer pain points into configuration items, engineering characteristics, target values, and planning actions.

QFD must be shown as the main methodology card. Use it to connect:

- pain point level: P0 critical / P1 high / P2 medium / P3 low
- user need or job-to-be-done
- customer importance weight: 1-5
- visible configuration
- engineering characteristic
- competitor satisfaction or fitment status
- Patsnap evidence strength
- target value or next-generation requirement
- planning action

Recommended fields:

| Field | Meaning |
|---|---|
| pain_level | P0/P1/P2/P3 based on severity, frequency, and impact on purchase/experience |
| user_need | user language, scenario, or pain point |
| importance_weight | 1-5, explain why if >=4 |
| configuration | feature or package |
| engineering_characteristic | measurable engineering enabler or subsystem |
| competitor_satisfaction | high / medium / low / missing |
| patsnap_strength | strong / forming / weak / unavailable |
| target_value | next-generation target, not necessarily numeric |
| planning_action | must_follow / differentiation_bet / watch / avoid_or_design_around |

Report tag: `[QFD / House of Quality]`

## 2. Primary Lens: Matrix Analysis

Purpose: combine multiple decision factors into a readable opportunity matrix.

Matrix Analysis should absorb the supporting methods instead of introducing more disconnected cards. It should score each configuration across:

- market penetration
- QFD importance
- competitor gap
- technology lifecycle stage
- patent barrier
- supply-chain maturity
- head-company benchmark signal
- user/VOC risk

Decision mapping:

| Matrix Result | Meaning | Minimum Basis |
|---|---|---|
| must_follow | next-generation baseline | high QFD importance + high penetration or clear head-company benchmark + manageable barrier |
| differentiation_bet | distinctive next-cycle feature | medium/high QFD importance + rising lifecycle + Patsnap/supply-chain signal + low current penetration |
| watch | promising but not ready | one or more missing signals: user acceptance, regulation, cost, supply, or patent clarity |
| avoid_or_design_around | avoid direct copy or redesign | high patent barrier, negative VOC, exiting lifecycle, or weak fit with target persona |

Report tag: `[Matrix Analysis]`

## 3. Supporting Tags

The following methods remain active but should be summarized as supporting logic, not displayed as equal-weight methodology cards unless the report has room.

### Benchmarking / 竞品对标

Defines competitor pool, target position, comparison dimensions, head-company benchmarks, and performance gaps.

Report tag: `[Benchmarking]`

### Kano Model

Classifies configurations as must-have, one-dimensional, attractive, reverse, or unknown. Kano labels should support QFD and Matrix decisions.

Report tag: `[Kano]`

### Technology S-Curve

Uses patent and literature signals to judge whether the technology is emerging, growing, mature, saturated, or unknown.

Report tag: `[S-Curve]`

### Patent Barrier Matrix

Uses patent density, legal status, applicant concentration, key claims, design-around space, and supplier diversity to identify barriers.

Report tag: `[Patent Barrier]`

### Patsnap Penetration

Explains the decision through the chain:

`市场配置现象 → 专利/文献趋势 → 关键申请人 → 核心专利 → 技术问题-方案-效果 → 供应链可行性 → 未来 1-2 年判断`

Report tag: `[Patsnap Penetration]`

### Supply Linkage

Shows industrialization feasibility and OEM/Tier0/Tier1/Tier2 relationship confidence.

Report tag: `[Supply Linkage]`

## 4. Technology Lifecycle Strategy

Classify technologies into five planning states:

| Stage | Meaning | Planning Use |
|---|---|---|
| 引领技术 | benchmark-setting, low-to-medium penetration, strong brand/technology signal | high-end flagship marker |
| 上升技术 | adoption rising, user value becoming visible | selling point for high/mid-end products |
| 成熟技术 | stable supply, broad fitment, low uncertainty | baseline or value-for-money base |
| 接近退出技术 | cost-effective but experience/brand risk emerging | low-end cost-control option only |
| 退出技术 | declining, negative UX/regulatory/brand risk | avoid in next-generation recommendations |

Price-band rule:

- 高端: 引领技术 + 上升技术 + 成熟技术; no 退出技术.
- 中端: 上升技术 + 成熟技术 to build value-for-money competitiveness.
- 低端: 成熟技术 + 接近退出技术 for cost control, with explicit risk disclosure.

## 5. Recommended Theory Display

The HTML report should show:

- two large cards: QFD / House of Quality and Matrix Analysis
- one compact strip of supporting tags: Benchmarking, Kano, S-Curve, Patent Barrier, Patsnap Penetration, Supply Linkage
- visible pain-point levels in the QFD section
- a configuration opportunity matrix that directly produces planning actions
