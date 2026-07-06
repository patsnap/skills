# Model Rules

## Source Labels

- `客户指南依据`: Directly from the customer-provided management specification.
- `客户样例/确认`: From the sample report or confirmed by the user during design.
- `模型建议`: Added to make the model operational across industries.
- `外部惯例补充`: Added from GHG Protocol, IFRS S2, PCAF, or carbon data verification practices.

## Main Formula

```text
综合评分 = 企业基本信用评价得分 × α
        + 碳账户综合评价得分 × β
        + 绿色低碳转型评价得分 × γ
```

`α + β + γ = 100%`.

## Industry α/β/γ Defaults

| Industry class | α | β | γ | Source |
|---|---:|---:|---:|---|
| 高碳排放强度、高转型压力 | 35% | 40% | 25% | 客户指南依据 |
| 中碳排放强度、中等转型压力 | 45% | 35% | 20% | 客户指南依据 |
| 污水处理行业特例 | 20% | 45% | 35% | 客户样例/确认 |
| 低碳排放强度、低转型压力 | 55% | 25% | 20% | 客户指南依据 |
| 资源依赖型、生态敏感行业 | 40% | 35% | 25% | 客户指南依据 |
| 创新驱动型、绿色技术行业 | 40% | 30% | 30% | 客户指南依据 |

When the enterprise is a wastewater company, use `污水处理行业特例` by default.

## Enterprise Basic Credit Evaluation

Main dimensions:

| Dimension | Weight | Source |
|---|---:|---|
| 信用合规 | 30% | 客户指南依据 |
| 财务能力 | 25% | 客户指南依据 |
| 生产与合规管理 | 20% | 客户指南依据 |
| 创新与品牌建设 | 25% | 客户指南依据 |

If detailed sub-scores are unavailable but a customer report already provides a dimension or module score, use the provided score and record the source.

## Customer-Confirmed Score Reuse

When a customer sample report, customer-confirmed result, or prior评级报告 already provides module scores, dimension rows, SWV component scores, or veto-check outcomes:

- Treat those values as confirmed inputs after showing them in the confirmation gate.
- Preserve the customer-confirmed score source in `source_payload`, `dimension_rows`, or missing-data disclosure.
- Do not recalculate the supplied score from incomplete raw data unless the user asks to override it.
- Do not impute missing raw fields with `0`, industry average, baseline score, or ad hoc default.
- Missing raw fields behind a confirmed score should be disclosed as `未采集数据` or `待补充/待核验`; they should not force `不评级` unless the score itself cannot be substantiated and the user accepts `保持缺失`.

## Carbon Account SWV Evaluation

```text
碳账户综合评价得分 = S映射分 × Ws + W映射分 × Ww + V映射分 × Wv
```

### SWV Industry Defaults

| Industry class | Ws S资产 | Ww W强度 | Wv V行为 | Source |
|---|---:|---:|---:|---|
| 高碳排放强度、高转型压力 | 25% | 50% | 25% | 模型建议 |
| 中碳排放强度、中等转型压力 | 30% | 40% | 30% | 模型建议 |
| 污水处理行业特例 | 20% | 45% | 35% | 客户样例/确认 |
| 低碳排放强度、低转型压力 | 25% | 35% | 40% | 模型建议 |
| 资源依赖型、生态敏感行业 | 40% | 30% | 30% | 模型建议 |
| 创新驱动型、绿色技术行业 | 35% | 35% | 30% | 模型建议 |

### S Calculation

```text
企业碳账户价值 =
碳配额量 × 碳交易价格
+ CCER数量 × CCER交易价格
+ 经核证碳汇量 × 碳汇交易价格
+ 绿电/绿证持有量 × 电力排放因子 × 碳交易价格
- 经核查碳排放量 × 碳交易价格

x1 = 企业碳账户价值 / 企业产量值或产值
x2 = 行业碳账户价值 / 行业产量值或产值
S = x1 / x2
```

Map S to scores:

| Range | Grade | Score |
|---|---|---:|
| S > 2.00 | Aaa | 90 |
| 1.50 < S <= 2.00 | Aa | 80 |
| 1.00 < S <= 1.50 | A | 70 |
| 0.80 < S <= 1.00 | Bbb | 60 |
| 0.60 < S <= 0.80 | Bb | 50 |
| 0.40 < S <= 0.60 | B | 40 |
| 0.20 < S <= 0.40 | Ccc | 30 |
| 0.10 < S <= 0.20 | Cc | 20 |
| 0.00 < S <= 0.10 | C | 10 |

Model suggestion: S > 3.00 still caps at Aaa/90.

### W Calculation

```text
W = 企业碳排放强度 / 企业所在行业碳排放强度基准值
```

Map W to scores:

| Range | Grade | Score |
|---|---|---:|
| 0.01 < W <= 0.90 | Aaa | 90 |
| 0.90 < W <= 0.95 | Aa | 80 |
| 0.95 < W <= 1.00 | A | 70 |
| 1.00 < W <= 1.02 | Bbb | 60 |
| 1.02 < W <= 1.04 | Bb | 50 |
| 1.04 < W <= 1.06 | B | 40 |
| 1.06 < W <= 1.08 | Ccc | 30 |
| 1.08 < W <= 1.10 | Cc | 20 |
| W > 1.10 | C | 10 |

Do not automatically award the best score for W = 0; treat as suspicious unless the source explains it.

### V Calculation

```text
V = (核查数据有误次数 + 购买数据虚报次数 + 绿证交易未及时履约次数 + 碳交易未及时履约次数) / 碳行为总次数
```

Map V to scores:

| Range | Grade | Score |
|---|---|---:|
| V = 0 | Aaa | 90 |
| 0.00 < V <= 0.01 | Aa | 80 |
| 0.01 < V <= 0.05 | A | 70 |
| 0.05 < V <= 0.06 | Bbb | 60 |
| 0.06 < V <= 0.08 | Bb | 50 |
| 0.08 < V <= 0.10 | B | 40 |
| 0.10 < V <= 0.12 | Ccc | 30 |
| 0.12 < V <= 0.15 | Cc | 20 |
| V > 0.15 | C | 10 |

If `碳行为总次数` is missing or zero without explanation, confirm with the user before scoring.

If a customer-confirmed `碳账户综合评价得分` or S/W/V component score table is supplied, use the confirmed score and disclose any unavailable raw S/W/V calculation fields. Do not use missing S/W/V raw fields to replace the confirmed score with model defaults.

## Green Low-Carbon Transition Evaluation

Main dimensions:

| Dimension | Weight | Source |
|---|---:|---|
| 自愿减排项目投资与绩效 | 40% | 客户指南依据 |
| 绿色转型实施绩效 | 30% | 客户指南依据 |
| 技改降碳实施成效 | 30% | 客户指南依据 |

Model suggestion: cap each dimension at its maximum when bonus points apply.

## Final Grade Mapping

| Comprehensive score | Grade |
|---|---|
| >= 90 | AAA |
| 85 <= score < 90 | AA |
| 80 <= score < 85 | A |
| 75 <= score < 80 | BBB |
| 70 <= score < 75 | BB |
| 65 <= score < 70 | B |
| 60 <= score < 65 | CCC |
| 50 <= score < 60 | CC |
| score < 50 | C |

Confirmed rule: comprehensive score < 40 still outputs C, unless a no-rating trigger applies.

## No-Rating And Adjustment Rules

No-rating triggers:

- 严重失信主体名单 = yes
- 数据造假 = yes
- 重大环境处罚 = yes
- 重大银行不良记录 = yes
- impossible-to-score key required fields remain missing after user confirmation

Required veto checks should be read from either flat fields or `veto_check`: `serious_dishonesty_flag`, `carbon_data_fraud`, `major_environment_penalty`, and `major_bank_bad_record`.

Adjustment triggers:

- General environment penalty: lower carbon account grade one level per occurrence.
- General bank bad record: lower carbon account grade one level per occurrence.
- Carbon trading, green certificate, or CCER serious fulfillment delay: lower one level per occurrence.

No-rating triggers take precedence over score calculation.
