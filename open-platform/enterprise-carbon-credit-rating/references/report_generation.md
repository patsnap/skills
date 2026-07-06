# Report Generation

## Required Output

Generate a formal `.docx` enterprise carbon credit rating report. Do not generate a Web system.

Use `assets/企业碳资信评级报告模板_v0.1.docx` as the default layout reference. The report should include:

1. Cover
2. Table of contents or rating summary
3. Report statement
4. Enterprise basic information
5. Model method and weights
6. Basic credit evaluation
7. Carbon account SWV evaluation
8. Green low-carbon transition evaluation
9. Adjustment items and no-rating judgment
10. Missing data list
11. Risk prompts
12. Comprehensive score and rating
13. Improvement recommendations
14. Appendices, including data sources, parameters, institution info, and model version

When a customer sample report is provided, use it as a content coverage reference: the generated report should retain the customer report's rating conclusion, report number/date, enterprise identity fields, α/β/γ, S/W/V conclusions, dimension scores, recommendations, and institution information where visible or confirmed. Improvements should be additive: better structure, source labels, missing-data disclosure, and formal report styling.

## Required Disclosures

Always disclose:

- model version
- parameter version or parameter source
- α/β/γ weights and industry class
- SWV weights
- missing fields marked `未采集数据`
- no-rating triggers
- adjustment items and downgrade reason
- source type labels for guide-based, sample-confirmed, model-suggested, and external-practice items

If customer-confirmed scores are reused, disclose that they come from `客户样例/确认` and do not present them as newly calculated from unavailable raw fields.

## No-Rating Wording

Use precise wording:

```text
因[触发原因]，本期不出具企业碳资信等级。
```

Examples:

- `因企业被纳入严重失信主体名单，本期不出具企业碳资信等级。`
- `因关键必要指标未采集且用户确认保持缺失，本期不出具企业碳资信等级。`
- `因发现碳数据造假，本期不出具企业碳资信等级。`

## Missing Data Wording

For noncritical missing fields:

```text
该指标未采集数据，不参与本项评价计算，并在风险提示中披露。
```

Do not impute missing data with zero, industry average, or ad hoc estimates.

If a raw field is unavailable but the customer has supplied the corresponding confirmed score or dimension row, keep the score and disclose the raw field gap as `待补充/待核验`. This is different from a raw-field scoring path, where missing key fields can lead to `不评级`.

## User Confirmation Wording

Before scoring, present:

```text
我已从资料中识别到以下企业信息和行业参数，请确认：
企业名称：[...]
统一社会信用代码：[...]
所属行业：[...]
行业分类：[...]
评价周期：[...]
α/β/γ：[...]
SWV：[...]
默认参数：[...]
客户报告/客户确认分项分数：[...]
缺失关键字段：[...]
非关键未采集字段：[...]
```

Then ask the user to confirm or modify the values.

## Validation

Before final delivery:

- Open or parse the generated DOCX to confirm paragraphs and tables exist.
- If LibreOffice/`soffice` is available, render the DOCX to page images and inspect them.
- If rendering is unavailable, state that visual QA could not be completed and report structural validation instead.
