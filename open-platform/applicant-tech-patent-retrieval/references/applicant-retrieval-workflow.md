# Applicant-Topic Patent Retrieval Workflow

Use this reference to retrieve patents for one or more target applicants within a confirmed technology topic. This workflow is applicant-first: the applicant universe is defined and audited before topic-limited retrieval is executed.

## 1. Preflight

Before any retrieval work, confirm:

| Item | Rule |
|---|---|
| Original request | Preserve verbatim before interpretation. |
| Applicant field | Required before retrieval/count validation/final applicant formula. User must choose `ALL_AN`, `AN`, `ANC`, `ANS`, `ANS_EXACT`, `ANCS`, or `ANCS_EXACT`. |
| Target applicant(s) | Required. If only a brand or group name is provided, treat it as the starting point for evidence-based entity expansion and disambiguation. |
| Technology topic | Required. If vague, define the likely boundary and ask for confirmation. |
| Scope | Ask only if material: exact legal entity only, group-level, subsidiaries, acquired entities, jurisdiction, time range, patent type, legal status. |
| Execution mode | `formula_only_mode` for strategy/formula-only work; `retrieval_dataset_mode` for executed retrieval, datasets, deduplication, and downstream inputs. |
| Retrieval mode | Must be `applicant_topic_limited_retrieval`. |
| Topic limitation | Must be explicit and traceable to the topic workflow. |

Do not execute retrieval, count validation, final applicant formula construction, merge, deduplication, or report completion if the applicant field is unconfirmed. `ANCS` is recommended but must be explicitly selected.

Allowed before applicant-field confirmation:

- Preserve the user's original request.
- Disambiguate applicant identity.
- Clarify exact legal-entity/group scope.
- Draft the topic definition and boundary for confirmation.
- Decide whether the user needs `formula_only_mode` or `retrieval_dataset_mode`.
- Draft a pending applicant entity expansion table when the applicant is a known group/company and public/user-provided evidence is enough to list candidate entities. Mark unverified entities as `Pending`.

Pre-retrieval hard stop:

- Do not execute applicant count, applicant-wide scale prediction, topic presearch, or applicant-topic combined search until both artifacts exist:
  - applicant entity expansion table;
  - topic definition/boundary/decomposition/search-element matrix.
- Do not write the report's `检索策略` or formula section until the topic workflow's Mandatory Topic Preflight Package is present and all gates are `Pass` or explicitly marked `待用户确认` in full-draft mode.
- Do not output `ANCS`, `TA_ALL`, or any combined query before the visible Step 0-7 pre-retrieval package exists.
- `Step 3` is reserved for topic boundary confirmation. Never use `Step 3` for formal search strategy.
- `Step 2` is reserved for technology topic definition. Never use `Step 2` for keyword matrix.
- Keyword matrix or search element matrix belongs only to `Step 5`.

### 1A. Applicant Alias Disambiguation

Trigger this step when the user input is a brand name, abbreviation, group name, historical group name, or a name that can point to multiple legal entities.

Execution rules:

- Do not infer one legal entity silently.
- List candidate entities with industry/domain, current/historical relationship, and likely retrieval path.
- For historical merger/rename groups, list both historical and current entities and explain the time relationship.
- Ask the user to confirm which entities or group route should be included before applicant-field confirmation and retrieval.

Cross-industry template:

```text
您输入的“[简称]”可能对应以下多个申请主体，请确认本次检索范围：
1. [完整法律主体A]（[行业/领域]）
2. [完整法律主体B]（[行业/领域]）
3. [完整法律主体C]（[行业/领域]）
4. 其他（请告知完整名称）
```

Historical group template:

```text
您输入的“[简称]”涉及集团历史沿革，可能对应以下多个主体，请确认本次检索范围：
1. [现用上市/核心主体]（当前主体，常用检索口径）
2. [集团母公司]（[合并年份]后新集团）
3. [历史主体]（[合并年份]前独立法人，部分专利仍可能以此名义存档）
4. [研究院/子公司]（可能单独申请专利）
5. 其他（请告知）
```

## 2. Applicant Entity Expansion

For each applicant group, collect:

- Canonical legal name.
- Chinese name.
- English name.
- Historical names.
- Abbreviations and applicant aliases.
- Subsidiaries and controlled legal entities.
- R&D centers, manufacturing entities, and branches.
- Acquired entities when in scope.
- Joint ventures only when the user wants broad ecosystem coverage or evidence supports inclusion.

Large applicant rule:

- Do not treat a large company, brand, listed company group, or common abbreviation as a single applicant expression.
- For companies such as 宁德时代/CATL, first produce an expansion table covering the core/listed entity, group or parent entities when relevant, major R&D entities, manufacturing subsidiaries, historical names, English names, and user-provided entities.
- If the entity relationship is plausible but not verified, include it as `Pending` instead of omitting it.
- Do not run `ANCS:("<brand or short name>")` as the only applicant-side strategy unless the user explicitly confirms a single-entity shortcut.

Classify every candidate:

| Include status | Meaning |
|---|---|
| `Yes` | Evidence supports inclusion in the applicant-side search. |
| `No` | Out of scope or unrelated. |
| `Pending` | Relationship is plausible but not proven; keep out of the main formula until approved. |

Required evidence fields:

| Field | Purpose |
|---|---|
| `relationship_basis` | Subsidiary, historical name, acquisition, R&D center, manufacturing entity, branch, applicant alias, or user-provided entity. |
| `evidence_source` | Business registry, official website, annual report, Patsnap applicant profile, patent applicant co-occurrence, or user-provided evidence. |
| `evidence_excerpt` | Short evidence note. |
| `confidence` | High / Medium / Low. |
| `include_in_search` | Yes / No / Pending. |

Consistency rule:

- Every entity with `include_in_search = Yes` must appear in `APPLICANT_TOTAL_EXPANDED`.
- Every entity in `APPLICANT_TOTAL_EXPANDED` must have a corresponding row with `include_in_search = Yes`.
- Entities marked `No` or `Pending` must not appear in the final applicant formula.
- The expansion table must be produced before any scale/count/presearch tool call. Count results may refine the table later, but cannot replace it.

## 3. Applicant Search Expressions

Build expressions with the confirmed applicant field:

```text
{applicant_field}:("applicant value")
```

Rules:

- Use the same applicant field throughout the run unless the report explicitly documents a separate validation experiment.
- Use `:` between field and value. Never use `=`.
- Do not use `ANSC`; it is a typo for `ANCS`.
- Test exact legal names and known applicant variants before broad consolidated expressions.
- For Chinese applicant values, use straight double quotes when required by query syntax.
- For English multi-word values, test quoted phrase form first.
- If a shortened platform-standard expression improves recall, use it only after count validation and applicant aggregation confirm it is not noisy.
- Preserve counts against the exact expression that produced them.

Applicant search expression audit table:

| Applicant group | Included applicant entity | Applicant expression used | Expression type | Verification evidence | Count validation | Confidence | Included in final query |
|---|---|---|---|---|---|---|---|

Add a note:

```text
Applicant field confirmed by user: <field>
Confirmation evidence: <user message or selection>
```

## 4. Applicant-Topic Formula and Retrieval

Read `topic-limitation-workflow.md` before writing topic formulas. Build the applicant and topic formulas separately before combining them.

In `formula_only_mode`, stop after producing expanded formulas, assumptions, and a PatSnap execution checklist. Do not require counts, datasets, deduplication, or Word report unless the user asks for them.

In `retrieval_dataset_mode`, retrieve each included applicant expression or applicant batch combined with the topic formula.

Before either mode can produce final formulas or execute retrieval, verify:

| Pre-retrieval artifact | Required status |
|---|---|
| Applicant entity expansion table | Present, with `Yes`/`No`/`Pending` and evidence/assumption notes. |
| Topic definition and boundary table | Present, confirmed or marked `待用户确认`. |
| Topic decomposition table | Present, covering object/material, function/effect, mechanism/process, application, exclusions/noise, and classification anchors when relevant. |
| Search-element matrix | Present, with CN/EN terms, field scope, proximity rule, and confirmation status. |
| Scale/count tool calls | Not allowed before the above artifacts exist. |

Keep the retrieval reproducible:

| Field | Requirement |
|---|---|
| `applicant_group` | Normalized group name. |
| `matched_applicant_entity` | Entity or expression that matched. |
| `applicant_expression_used` | Exact applicant expression or applicant total formula. |
| `topic_formula_version` | `S0`, `S1`, `S2`, `S3`, `S4`, `APPLICANT_TOPIC_FINAL`, or precision variant. |
| `retrieval_batch_id` | Unique batch identifier. |
| `source_database` | Patsnap/Zhihuiya or other source. |
| `retrieval_date` | Date of retrieval. |
| `filters` | Jurisdiction/date/legal/status filters if any. |
| `topic_limitation_flag` | Confirmed topic name or `pending-confirmation draft`. |

Retrieval batch log:

| Batch id | Applicant group | Applicant expression | Topic formula version | Filters | Retrieved count | Included count | Notes |
|---|---|---|---|---|---:|---:|---|

Use batch labels that distinguish the applicant and topic layers without conflicting with the report Step 0-7 gates, for example:

- `BATCH_APPLICANT_COUNT`
- `BATCH_TOPIC_LIMITED`
- `BATCH_PRECISION_NOISE_FILTERED`

## 5. Merge Rules

Merge all included applicant-topic results under normalized `applicant_group` and `topic_formula_version`.

Preserve:

- Original publication/application numbers.
- Normalized publication/application numbers.
- Applicant expression provenance.
- Matched applicant names.
- Topic formula version.
- Retrieval batch id.
- Family ids when available.
- Legal status and patent type when available.

Keep ambiguous or excluded entities in a separate table:

| Candidate entity | Possible relationship | Evidence | Risk of false inclusion | Recommendation |
|---|---|---|---|---|

## 6. Deduplication

Report all available views:

| Deduplication level | Primary key | Use |
|---|---|---|
| Source/publication-level | Publication number + kind code | Audit and source reproducibility. |
| Application-level | Application number or normalized application id | Applicant-topic filing count and statistics. |
| Simple-family-level | Simple family id or priority-based family key | Preferred downstream representative dataset. |

Deduplication summary:

| Applicant group | Topic formula version | Raw/source records | Application-level unique records | Simple-family-level unique records | Deduplication keys used | Notes |
|---|---|---:|---:|---:|---|---|

If simple-family fields are unavailable:

```text
simple_family_status: unavailable
downstream_dataset_type: application_level_representative_fallback
```

## 7. Representative Selection

When multiple records collapse into one representative, choose:

1. `CN` when a usable CN family member exists.
2. `WO`, `US`, or `EP` when no usable CN member exists.
3. Other jurisdictions only when no usable CN/WO/US/EP member exists or when they are the only text-complete records.

Within the selected tier, prefer:

- Rich title, abstract, and claims.
- Better publication stage/legal certainty when text quality is comparable.
- Current legal status.
- Earliest application or priority date for invention identity.
- Target-market relevance if the user specified a market.

Preserve:

- `merged_publication_numbers`
- `merged_application_numbers`
- `merged_family_members`
- `merged_applicant_expressions`
- `topic_formula_version`
- `representative_selection_reason`
- `representative_jurisdiction_priority`
- `simple_family_representative_flag`

## 8. Report and Artifacts

Required artifacts:

| Artifact | Required | Purpose |
|---|---|---|
| `<applicant>_<topic>_patent_search_strategy.md` | Yes in `formula_only_mode` | Editable formula/methodology report. |
| `<applicant>_<topic>_patent_retrieval_report.md` | Yes in `retrieval_dataset_mode` | Editable traceable report. |
| `<applicant>_<topic>_patent_retrieval_report.docx` | Yes in `retrieval_dataset_mode` unless opted out | Formal report. |
| Full hit/source dataset | Yes in `retrieval_dataset_mode` | Audit and reproducibility. |
| Application-level dataset | Yes in `retrieval_dataset_mode` when fields support it | Filing-level statistics and fallback. |
| Simple-family representative dataset | Yes in `retrieval_dataset_mode` when family fields support it | Preferred downstream dataset. |
| Query/audit appendix | Yes | Applicant expressions, topic formulas, count validation when available, and excluded entities/noise. |

Report sections:

0. Step 0：原始需求与执行模式.
1. Step 1：申请人实体扩展表.
2. Step 2：技术主题定义.
3. Step 3：技术边界确认表.
4. Step 4：技术主题分解表.
5. Step 5：检索元素矩阵.
6. Step 6：噪声与排除边界表.
7. Step 7：检索前门禁状态.
8. Step 8：检索策略与公式, only after all Step 0-7 gates are `Pass` or `Pending`.
9. Applicant search expression audit table.
10. Expanded final formulas.
11. Retrieval batch log, only in `retrieval_dataset_mode`.
12. Merge and deduplication summary, only in `retrieval_dataset_mode`.
13. Downstream dataset selection, only in `retrieval_dataset_mode`.
14. Validation guidance and limitations.
15. Handoff gate.
16. Manual review and data gaps.

Invalid report order:

```text
Step 2：固态电池技术主题关键词矩阵
TA_ALL=(...)
Step 3: 正式检索策略
Applicant expression: ANCS=(...)
Topic expression: TA_ALL=(...)
```

This order is invalid because Step 3 must be topic boundary confirmation and formulas may not appear before Step 8.

## 9. Handoff Gate

Use this table before declaring the result ready:

| Check | Required state | Actual state | Pass / fail | Action |
|---|---|---|---|---|
| Execution mode | `formula_only_mode` or `retrieval_dataset_mode` |  |  |  |
| Retrieval mode | `applicant_topic_limited_formula` or `applicant_topic_limited_retrieval` |  |  |  |
| Applicant field | Explicitly confirmed by user |  |  |  |
| Applicant disambiguation | Completed when needed |  |  |  |
| Applicant entity expansion table | Present before any count/presearch/retrieval |  |  |  |
| Topic boundary | Confirmed, or marked `待用户确认` in full-draft mode |  |  |  |
| Topic decomposition and search-element matrix | Present before any topic presearch or combined retrieval |  |  |  |
| Applicant formula consistency | Entity table and `APPLICANT_TOTAL_EXPANDED` match bidirectionally |  |  |  |
| Topic formula completeness | Expanded final formula contains no unresolved `S1/S2/N1` placeholders |  |  |  |
| Noise formula completeness | `NOISE_TOTAL_EXPANDED` provided when exclusions are used |  |  |  |
| Execution checklist | Required in `formula_only_mode` |  |  |  |
| Source hit count separated from downstream count | Required in `retrieval_dataset_mode`: `source_hit_count_usage: audit_only` |  |  |  |
| Representative dataset generated | Required in `retrieval_dataset_mode`: file exists and is named |  |  |  |
| Downstream dataset type | Required in `retrieval_dataset_mode`: `simple_family_representative` or explicit application-level fallback |  |  |  |
| Downstream count | Required in `retrieval_dataset_mode`: actual representative record count |  |  |  |
| Full hit list excluded from downstream representative input | Required in `retrieval_dataset_mode`: full hits used only as source/audit artifact |  |  |  |

Valid handoff block:

```text
execution_mode: retrieval_dataset_mode
target_applicant: <applicant group>
applicant_field: <confirmed field>
technology_topic: <confirmed topic>
retrieval_mode: applicant_topic_limited_retrieval
topic_limitation: <topic formula version>
source_hit_count: <raw/source count> (audit/source only)
source_hit_count_usage: audit_only
downstream_dataset_type: simple_family_representative
downstream_dataset_file: <applicant>_<topic>_simple_family_representative.csv
downstream_dataset_count: <actual representative count>
ready_for: downstream_review_or_analysis
```

Valid formula-only handoff:

```text
execution_mode: formula_only_mode
target_applicant: <applicant group>
applicant_field: <confirmed field>
technology_topic: <confirmed topic or pending-confirmation draft>
retrieval_mode: applicant_topic_limited_formula
expanded_formula_status: complete
dataset_status: not_executed
ready_for: patsnap_execution
```

Invalid handoff:

```text
source_hit_count: 12000
ready_for: downstream_review_or_analysis
```

This is invalid because it does not identify the representative dataset, topic scope, or the difference between raw/source hits and downstream count.
