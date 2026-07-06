# High-Value Patent Screening Standard

## Scoring Model

Score every returned candidate patent on a 100-point scale:

| Indicator | Weight | Data source |
| --- | ---: | --- |
| 简单同族被引专利数量多 | 30 | `[P015].patent_cited.cited_by_simple_family` |
| 简单同族专利数量多 | 30 | `len([P014].patent_family.simple_family)` |
| 属于核心发明人专利 | 20 | Top five inventors by patent count in `[P002]` returned candidates |
| 出现过专利法律事件 | 20 | `[P034]` litigation, `[P027]` reexamination/invalidation, `[P028]` license, or `[P029]` transfer |

## Numeric Indicator Normalization

Use percentile scoring when there are at least 10 candidates:

- `简单同族被引专利数量得分 = percentile_rank(cited_by_simple_family) * 30`
- `简单同族专利数量得分 = percentile_rank(simple_family_count) * 30`

Use deterministic fallback scoring when percentile scoring is not practical:

- If all simple-family cited-by counts are zero or missing, assign 0 for that indicator.
- If all non-zero simple-family cited-by counts are equal, assign 15 for that indicator.
- If all simple family counts are zero or missing, assign 0 for that indicator.
- If all non-zero simple family counts are equal, assign 15 for that indicator.
- Missing values are `未获取` and receive 0 for the missing indicator unless the user supplies another rule.

## Binary Indicator Scoring

Core inventor:

- Score 20 if any inventor of the patent is one of the top five inventors in the returned candidate set.
- Score 0 otherwise.

Legal event:

- Score 20 if any of these arrays is non-empty:
  - `[P034].patent_litigation_data`
  - `[P027].patent_reexam_invalid_data`
  - `[P028].patent_license_data`
  - `[P029].patent_transfer_data`
- Score 0 otherwise.

## Core Inventor Rule

Define core inventors from the returned candidate universe:

1. Split inventor strings on the inventor delimiters `|`, `;`, `；`, and line breaks only. Do NOT split on `,` / `，`: PatSnap/Zhihuiya formats the inventor field as `LASTNAME, FIRSTNAME|LASTNAME, FIRSTNAME`, so the comma separates surname from given name *within* one inventor and `|` separates inventors. Splitting on the comma fragments names (e.g. `TANNER, CHRISTOPHER RICHARD` would wrongly become `TANNER` and `CHRISTOPHER RICHARD`).
2. Trim whitespace and remove empty names.
3. Count each inventor once per patent.
4. Rank inventors by candidate-set patent count descending.
5. Break ties by total high-value score of the inventor's patents, then by name ascending.
6. Treat the top five inventors as core inventors.

Cross-language note: the same inventor may appear as a Western name on one family member and a transliterated name (e.g. Chinese) on another. Do not merge across languages; count names exactly as returned in the candidate set, and state this in the report.

If the user supplies a separate core inventor list, use the user-supplied list and state that override in the report.

## Legal-Event Categories

Qualifying legal events:

- `诉讼`: `[P034]`, non-empty `patent_litigation_data`.
- `无效/复审`: `[P027]`, non-empty `patent_reexam_invalid_data`.
- `许可`: `[P028]`, non-empty `patent_license_data`.
- `权利转移`: `[P029]`, non-empty `patent_transfer_data`.

Normalize the report event summary to these four Chinese categories, while preserving original event labels, dates, case numbers, parties, and countries in the trace.

## Selection Ratio

The selected high-value patents must be 10%-15% of the patents returned by the search query.

Default:

```text
selected_count = ceil(candidate_count * 0.10)
```

Constraints:

- If `candidate_count > 0`, select at least 1 patent.
- Do not exceed `ceil(candidate_count * 0.15)` unless the user explicitly asks for a broader list.
- If score ties at the cutoff would force the list above 15%, use tie-break rules instead of including all tied records.

## Tie-Break Rules

When scores are tied, rank by:

1. Higher simple-family cited-by patent count.
2. Higher simple family patent count.
3. Legal-event hit.
4. Core inventor hit.
5. More legal-event categories.
6. Earlier application date.
7. Publication number ascending.

## Report Table Schema

Use these columns in the high-value patent list:

| Column | Notes |
| --- | --- |
| 排名 | Rank after scoring and tie-breaks |
| 高价值评分 | 0-100 score |
| 被选定为高价值的原因 | Evidence-based rationale |
| 专利公开公告号 | Publication number / `pn`, rendered as a clickable hyperlink to the Zhihuiya/PatSnap patent page: `https://analytics.zhihuiya.com/patent-view/abst?patentId=<patent_id>&q=<pn>` (minimal non-expiring form; reader must be logged in) |
| 标题 | Original title from P002 |
| 摘要附图 | P021 drawing URL/path or `无可用摘要附图` |
| [标]当前申请(专利权)人 | Current applicant/patentee from P002 |
| 简单法律状态 | P041 simple legal status |
| Patsnap专利标题 | P025 `patsnap_title` |
| AI技术三要素-技术问题 | P025 technical problem |
| AI技术三要素-技术手段 | P025 technical approach |
| AI技术三要素-技术功效 | P025 benefit/effect |
| 简单同族被引专利数量 | P015 `cited_by_simple_family` |
| 简单同族专利数量 | P014 `len(simple_family)` |
| 是否核心发明人专利 | Yes/No plus matched inventor names |
| 法律事件 | `诉讼` / `无效/复审` / `许可` / `权利转移` categories and key dates |
| 数据缺口 | Missing or failed enrichment fields |

## Rationale Wording

Keep the selection reason compact and evidence-based:

```text
简单同族被引专利数量位于候选集P92；简单同族专利数量18件；命中核心发明人：张三；存在许可、权利转移事件。
```

When evidence is incomplete:

```text
简单同族被引专利数量未获取；简单同族专利数量位于候选集P85；未命中核心发明人；法律事件接口未返回数据。
```
