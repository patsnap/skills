# FTO Report Quality Assessment

> Assessment ID: `{ASSESSMENT_ID}`  
> Version: `{ASSESSMENT_VERSION}`  
> Review date: `{REVIEW_DATE}`  
> Reviewer: `{REVIEWER}`  
> Distribution: `{DISTRIBUTION_CONTROL}`

---

## Fatal-defect notice

**Fatal override:** `{YES_NO}`  
**Quality grade:** `{QUALITY_GRADE}`

> `{FATAL_BANNER_TEXT_OR_NOT_TRIGGERED}`

| Fatal ID | Condition | Evidence | Required cure |
|---|---|---|---|
| `{FTL_ID}` | `{CONDITION}` | `{EVIDENCE}` | `{CURE}` |

If no fatal defect is triggered, state `No fatal defect identified from the
evidence reviewed`. Do not delete the gate.

---

## 1. Report identity and scope

### 1.1 Reviewed report

| Field | Value |
|---|---|
| Report title | `{REPORT_TITLE}` |
| Report author / organization | `{REPORT_AUTHOR}` |
| Report issue date | `{REPORT_DATE}` |
| Report version | `{REPORT_VERSION}` |
| Commissioning party | `{COMMISSIONING_PARTY}` |
| Files and annexes reviewed | `{FILES_REVIEWED}` |
| Intended audience | `{INTENDED_AUDIENCE}` |
| Intended decision | `{INTENDED_DECISION}` |

### 1.2 Subject and commercial activity

| Field | Value |
|---|---|
| Product/process/service | `{TARGET_SUBJECT}` |
| Technical version/configuration | `{TECHNICAL_VERSION}` |
| Essential features | `{ESSENTIAL_FEATURES}` |
| Optional features | `{OPTIONAL_FEATURES}` |
| Commercial act(s) | `{COMMERCIAL_ACTS}` |
| Target market(s)/jurisdiction(s) | `{TARGET_MARKETS}` |
| Decision deadline | `{DECISION_DEADLINE}` |
| Risk tolerance | `{RISK_TOLERANCE}` |

### 1.3 Evidence cutoffs and conventions

| Field | Value |
|---|---|
| Search cutoff | `{SEARCH_CUTOFF}` |
| Legal-status cutoff | `{STATUS_CUTOFF}` |
| Claim version(s) reviewed | `{CLAIM_VERSIONS}` |
| Translation basis | `{TRANSLATION_BASIS}` |
| Family definition | `{FAMILY_DEFINITION}` |
| Counting unit | `{COUNTING_UNIT}` |
| Scenario matrix | `{MARKET_CODE} × {USE_CODE}` |
| Weight adaptation | `{WEIGHT_ADAPTATION_OR_NONE}` |

### 1.4 Scope exclusions and assumptions

- `{EXCLUSION_1}`
- `{EXCLUSION_2}`
- `{ASSUMPTION_1}`
- `{ASSUMPTION_2}`

### 1.5 Missing evidence at intake

| Missing item | Consequence | Evidence request | Owner / due |
|---|---|---|---|
| `{MISSING_ITEM}` | `{CONSEQUENCE}` | `{REQUEST}` | `{OWNER_DUE}` |

---

## 2. Executive summary

### 2.1 Decision-level conclusion

`{EXECUTIVE_CONCLUSION}`

This conclusion is limited to `{TARGET_SUBJECT}`, version
`{TECHNICAL_VERSION}`, the activity `{COMMERCIAL_ACTS}`, jurisdiction(s)
`{TARGET_MARKETS}`, and evidence through `{STATUS_CUTOFF}`.

### 2.2 Overall quality result

| Measure | Result |
|---|---|
| Overall quality score | `{TOTAL_SCORE}` / 100 |
| Quality grade | `{QUALITY_GRADE}` |
| Fatal override | `{FATAL_STATUS}` |
| Suitable for intended decision | `{YES_CONDITIONAL_NO}` |
| Independent verification | `{PERFORMED_PARTIAL_NOT_PERFORMED}` |
| Residual uncertainty | `{RESIDUAL_UNCERTAINTY}` |

### 2.3 Dimension scores

| Dimension | Maximum | Score | Principal finding |
|---|---:|---:|---|
| A. Search-strategy quality | 25 | `{A_SCORE}` | `{A_FINDING}` |
| B. Patent-analysis depth | 30 | `{B_SCORE}` | `{B_FINDING}` |
| C. Legal-opinion quality | 25 | `{C_SCORE}` | `{C_FINDING}` |
| D. Documentation completeness | 20 | `{D_SCORE}` | `{D_FINDING}` |
| **Total** | **100** | **`{TOTAL_SCORE}`** | `{OVERALL_FINDING}` |

### 2.4 Most important findings

1. `{KEY_FINDING_1}`
2. `{KEY_FINDING_2}`
3. `{KEY_FINDING_3}`
4. `{KEY_FINDING_4}`
5. `{KEY_FINDING_5}`

### 2.5 Immediate decision actions

| Priority | Action | Owner | Deadline/trigger | Decision effect |
|---|---|---|---|---|
| Critical | `{ACTION}` | `{OWNER}` | `{TIMING}` | `{EFFECT}` |
| High | `{ACTION}` | `{OWNER}` | `{TIMING}` | `{EFFECT}` |

---

## 3. Three-layer review overview

| Layer | Status | Confidence | Core evidence | Principal gap | Decision effect |
|---|---|---|---|---|---|
| Evidence and reproducibility | `{STATUS}` | `{CONFIDENCE}` | `{EVIDENCE}` | `{GAP}` | `{EFFECT}` |
| Legal reasoning | `{STATUS}` | `{CONFIDENCE}` | `{EVIDENCE}` | `{GAP}` | `{EFFECT}` |
| Decision usefulness | `{STATUS}` | `{CONFIDENCE}` | `{EVIDENCE}` | `{GAP}` | `{EFFECT}` |

### 3.1 Evidence and reproducibility findings

- Strengths: `{LAYER_1_STRENGTHS}`
- Gaps: `{LAYER_1_GAPS}`
- Consequence: `{LAYER_1_CONSEQUENCE}`
- Required evidence: `{LAYER_1_ACTION}`

### 3.2 Legal-reasoning findings

- Strengths: `{LAYER_2_STRENGTHS}`
- Gaps: `{LAYER_2_GAPS}`
- Consequence: `{LAYER_2_CONSEQUENCE}`
- Required review: `{LAYER_2_ACTION}`

### 3.3 Decision-usefulness findings

- Strengths: `{LAYER_3_STRENGTHS}`
- Gaps: `{LAYER_3_GAPS}`
- Consequence: `{LAYER_3_CONSEQUENCE}`
- Required action: `{LAYER_3_ACTION}`

---

## 4. Four-dimension scorecard

### 4.1 Dimension A — Search-strategy quality (`{A_SCORE}` / 25)

| Criterion | Maximum | Score | Evidence | Deduction |
|---|---:|---:|---|---|
| A1. Source and jurisdiction coverage | 8 | `{A1_SCORE}` | `{A1_EVIDENCE}` | `{A1_DEDUCTION}` |
| A2. Query and route design | 6 | `{A2_SCORE}` | `{A2_EVIDENCE}` | `{A2_DEDUCTION}` |
| A3. Time and prosecution coverage | 5 | `{A3_SCORE}` | `{A3_EVIDENCE}` | `{A3_DEDUCTION}` |
| A4. Reproducibility and screening | 6 | `{A4_SCORE}` | `{A4_EVIDENCE}` | `{A4_DEDUCTION}` |

Assessment: `{A_ASSESSMENT}`

### 4.2 Dimension B — Patent-analysis depth (`{B_SCORE}` / 30)

| Criterion | Maximum | Score | Evidence | Deduction |
|---|---:|---:|---|---|
| B1. Claim-comparison rigor | 10 | `{B1_SCORE}` | `{B1_EVIDENCE}` | `{B1_DEDUCTION}` |
| B2. Infringement-risk reasoning | 8 | `{B2_SCORE}` | `{B2_EVIDENCE}` | `{B2_DEDUCTION}` |
| B3. Risk tiering and materiality | 4 | `{B3_SCORE}` | `{B3_EVIDENCE}` | `{B3_DEDUCTION}` |
| B4. Status, ownership, and validity context | 5 | `{B4_SCORE}` | `{B4_EVIDENCE}` | `{B4_DEDUCTION}` |
| B5. Industry-specific coverage | 3 | `{B5_SCORE}` | `{B5_EVIDENCE}` | `{B5_DEDUCTION}` |

Assessment: `{B_ASSESSMENT}`

### 4.3 Dimension C — Legal-opinion quality (`{C_SCORE}` / 25)

| Criterion | Maximum | Score | Evidence | Deduction |
|---|---:|---:|---|---|
| C1. Legal framework and sources | 7 | `{C1_SCORE}` | `{C1_EVIDENCE}` | `{C1_DEDUCTION}` |
| C2. Conclusion reliability | 7 | `{C2_SCORE}` | `{C2_EVIDENCE}` | `{C2_DEDUCTION}` |
| C3. Risk mitigation | 6 | `{C3_SCORE}` | `{C3_EVIDENCE}` | `{C3_DEDUCTION}` |
| C4. Professional communication | 5 | `{C4_SCORE}` | `{C4_EVIDENCE}` | `{C4_DEDUCTION}` |

Assessment: `{C_ASSESSMENT}`

### 4.4 Dimension D — Documentation completeness (`{D_SCORE}` / 20)

| Criterion | Maximum | Score | Evidence | Deduction |
|---|---:|---:|---|---|
| D1. Search record | 6 | `{D1_SCORE}` | `{D1_EVIDENCE}` | `{D1_DEDUCTION}` |
| D2. Analysis traceability | 5 | `{D2_SCORE}` | `{D2_EVIDENCE}` | `{D2_DEDUCTION}` |
| D3. Evidence package | 4 | `{D3_SCORE}` | `{D3_EVIDENCE}` | `{D3_DEDUCTION}` |
| D4. Version and format control | 5 | `{D4_SCORE}` | `{D4_EVIDENCE}` | `{D4_DEDUCTION}` |

Assessment: `{D_ASSESSMENT}`

### 4.5 Score interpretation

The score measures report quality. It is not an infringement probability and
does not guarantee freedom to operate. `{SCORING_QUALIFICATION}`

---

## 5. Independent-search comparison and omissions

### 5.1 Verification status

| Field | Value |
|---|---|
| Status | `{PERFORMED_PARTIAL_NOT_PERFORMED}` |
| Search date(s) | `{INDEPENDENT_SEARCH_DATES}` |
| Providers / connectors | `{PROVIDERS}` |
| Comparison unit | `{COMPARISON_UNIT}` |
| Family rule | `{FAMILY_RULE}` |
| Recall | `{NOT_ESTIMATED_OR_QUALIFIED_HEURISTIC}` |

### 5.2 Route summary

| Route | Query / request | Fields / filters | Raw | Retained | Families | Limitation |
|---|---|---|---:|---:|---:|---|
| Semantic | `{QUERY}` | `{FIELDS_FILTERS}` | `{N}` | `{N}` | `{N}` | `{LIMIT}` |
| Keyword / Boolean | `{QUERY}` | `{FIELDS_FILTERS}` | `{N}` | `{N}` | `{N}` | `{LIMIT}` |
| Classification | `{QUERY}` | `{FIELDS_FILTERS}` | `{N}` | `{N}` | `{N}` | `{LIMIT}` |
| Entity / citation | `{QUERY}` | `{FIELDS_FILTERS}` | `{N}` | `{N}` | `{N}` | `{LIMIT}` |
| Temporal watchlist | `{QUERY}` | `{FIELDS_FILTERS}` | `{N}` | `{N}` | `{N}` | `{LIMIT}` |

### 5.3 Observed set comparison

| Measure | Result |
|---|---:|
| Families in reviewed report (`R`) | `{REPORT_FAMILY_COUNT}` |
| Independent observed union (`U`) | `{UNION_COUNT}` |
| Shared (`R ∩ U`) | `{SHARED_COUNT}` |
| Report-only (`R \ U`) | `{REPORT_ONLY_COUNT}` |
| Independent-only (`U \ R`) | `{INDEPENDENT_ONLY_COUNT}` |

### 5.4 Route overlap

| Route pair | Intersection | Union | Jaccard | Interpretation |
|---|---:|---:|---:|---|
| `{ROUTE_A}` / `{ROUTE_B}` | `{N}` | `{N}` | `{VALUE}` | `{INTERPRETATION}` |

Observed overlap does not establish true recall. `{COVERAGE_LIMITATION}`

### 5.5 Omission review

| Family / patent | Difference category | Status date/source | Claim relevance | Materiality | Required action |
|---|---|---|---|---|---|
| `{IDENTIFIER}` | `{CATEGORY}` | `{STATUS}` | `{CLAIM_REVIEW}` | `{MATERIALITY}` | `{ACTION}` |

### 5.6 Pending-application watchlist

| Application | Jurisdiction | Procedural state/date | Feature/claim to monitor | Trigger | Owner/cadence |
|---|---|---|---|---|---|
| `{APPLICATION}` | `{JURISDICTION}` | `{STATE_DATE}` | `{FEATURE}` | `{TRIGGER}` | `{OWNER_CADENCE}` |

Pending applications are tracked for future claim changes and are not presented
as currently enforceable patent claims.

### 5.7 Verification limitations

- `{VERIFICATION_LIMITATION_1}`
- `{VERIFICATION_LIMITATION_2}`
- `{UNSEARCHED_AREA}`

---

## 6. Search-topic fit

### 6.1 Feature decomposition

| Feature cluster | Essential? | Search concepts | Evidence source | Gap |
|---|---|---|---|---|
| `{FEATURE}` | `{YES_NO}` | `{CONCEPTS}` | `{SOURCE}` | `{GAP}` |

### 6.2 Terminology and classifications

| Type | Terms / codes | Rationale | Limitation |
|---|---|---|---|
| Synonyms and variants | `{TERMS}` | `{RATIONALE}` | `{LIMIT}` |
| Translations / nomenclature | `{TERMS}` | `{RATIONALE}` | `{LIMIT}` |
| IPC/CPC | `{CODES}` | `{RATIONALE}` | `{LIMIT}` |
| Entity / citation seeds | `{SEEDS}` | `{RATIONALE}` | `{LIMIT}` |

### 6.3 Topic-fit conclusion

`{TOPIC_FIT_CONCLUSION}`

---

## 7. Search-scope coverage

### 7.1 Jurisdiction and source matrix

| Jurisdiction | Source(s) | Rights/stages | Coverage | Cutoff | Limitation |
|---|---|---|---|---|---|
| `{JURISDICTION}` | `{SOURCES}` | `{RIGHTS}` | `{COVERAGE}` | `{DATE}` | `{LIMIT}` |

### 7.2 Time-scope rationale

`{TIME_SCOPE_RATIONALE}`

The assessment does not apply a universal database count, 20-year lookback, or
fixed validity period. Fitness is judged against the technology, jurisdiction,
rights, prosecution timing, and decision date.

### 7.3 Reproducibility

| Control | Status | Evidence | Gap / action |
|---|---|---|---|
| Exact queries retained | `{STATUS}` | `{EVIDENCE}` | `{ACTION}` |
| Fields and filters retained | `{STATUS}` | `{EVIDENCE}` | `{ACTION}` |
| Result counts reconcile | `{STATUS}` | `{EVIDENCE}` | `{ACTION}` |
| Screening criteria retained | `{STATUS}` | `{EVIDENCE}` | `{ACTION}` |
| Family/deduplication rule retained | `{STATUS}` | `{EVIDENCE}` | `{ACTION}` |

### 7.4 Scope conclusion

`{SCOPE_CONCLUSION}`

---

## 8. Claim-comparison rigor

### 8.1 Method review

| Control | Status | Evidence | Consequence |
|---|---|---|---|
| Correct jurisdictional member | `{STATUS}` | `{EVIDENCE}` | `{CONSEQUENCE}` |
| Current claim version | `{STATUS}` | `{EVIDENCE}` | `{CONSEQUENCE}` |
| Claim source / translation | `{STATUS}` | `{EVIDENCE}` | `{CONSEQUENCE}` |
| Limitation-by-limitation mapping | `{STATUS}` | `{EVIDENCE}` | `{CONSEQUENCE}` |
| Product/process evidence | `{STATUS}` | `{EVIDENCE}` | `{CONSEQUENCE}` |
| Construction/equivalents qualification | `{STATUS}` | `{EVIDENCE}` | `{CONSEQUENCE}` |

### 8.2 Representative claim-quality review

| Patent / claim | Limitation | Product evidence | Report conclusion | QA finding | Confidence |
|---|---|---|---|---|---|
| `{PATENT_CLAIM}` | `{LIMITATION}` | `{PRODUCT_EVIDENCE}` | `{REPORT_POSITION}` | `{QA_FINDING}` | `{CONFIDENCE}` |

### 8.3 Claim-analysis conclusion

`{CLAIM_ANALYSIS_CONCLUSION}`

---

## 9. Higher-risk patent list

**Higher-risk patents:** `{HIGHER_RISK_COUNT}`

| Patent / family | Jurisdiction | Claim/status date | Product mapping | Report position | QA finding | Linked action |
|---|---|---|---|---|---|---|
| `{IDENTIFIER}` | `{JURISDICTION}` | `{CLAIM_STATUS}` | `{MAPPING}` | `{POSITION}` | `{FINDING}` | `{ACTION_ID}` |

If none are identified, state the searched scope and why the result does not
constitute a guarantee of no risk.

---

## 10. Moderate-risk patent list

| Patent / family | Jurisdiction | Claim/status date | Product mapping | Uncertainty | Next step |
|---|---|---|---|---|---|
| `{IDENTIFIER}` | `{JURISDICTION}` | `{CLAIM_STATUS}` | `{MAPPING}` | `{UNCERTAINTY}` | `{NEXT_STEP}` |

---

## 11. Lower-risk patent list

| Patent / family | Jurisdiction | Basis for lower risk | Residual uncertainty | Monitoring need |
|---|---|---|---|---|
| `{IDENTIFIER}` | `{JURISDICTION}` | `{BASIS}` | `{UNCERTAINTY}` | `{MONITORING}` |

Lower risk does not mean no risk. State whether the basis is a missing
limitation, non-target jurisdiction, non-enforceable status, different activity,
or another supported reason.

---

## 12. Response-measure quality

| Finding | Existing report response | Specific? | Feasible? | Owner/timing? | Residual-risk treatment | QA result |
|---|---|---|---|---|---|---|
| `{FINDING}` | `{RESPONSE}` | `{YES_NO}` | `{YES_NO}` | `{OWNER_TIMING}` | `{RESIDUAL}` | `{RESULT}` |

### 12.1 Gaps in existing responses

- `{RESPONSE_GAP_1}`
- `{RESPONSE_GAP_2}`

### 12.2 Response-quality conclusion

`{RESPONSE_QUALITY_CONCLUSION}`

---

## 13. Risk-mitigation recommendations

**Recommended actions:** `{RECOMMENDED_ACTION_COUNT}`

| ID | Priority | Finding addressed | Action | Owner | Timing/trigger | Dependency | Decision | Residual risk |
|---|---|---|---|---|---|---|---|---|
| `{ACTION_ID}` | `{PRIORITY}` | `{FINDING}` | `{ACTION}` | `{OWNER}` | `{TIMING}` | `{DEPENDENCY}` | `{DECISION}` | `{RESIDUAL}` |

Potential action types include claim-specific design-around, further product
fact collection, official status/file-history review, targeted prior-art work,
counsel opinion, licence/acquisition analysis, supplier/indemnity review,
monitoring, launch hold, or documented risk acceptance.

---

## 14. Consolidated issue register

| Issue ID | Layer | Dimension | Severity | Finding | Evidence | Score effect | Owner | Status |
|---|---|---|---|---|---|---:|---|---|
| `{ISSUE_ID}` | `{LAYER}` | `{DIMENSION}` | `{SEVERITY}` | `{FINDING}` | `{EVIDENCE}` | `{DEDUCTION}` | `{OWNER}` | `{STATUS}` |

### 14.1 Critical issues

`{CRITICAL_ISSUES_OR_NONE}`

### 14.2 Material issues

`{MATERIAL_ISSUES_OR_NONE}`

### 14.3 Improvement opportunities

`{IMPROVEMENT_ITEMS_OR_NONE}`

---

## 15. Conclusion and remediation plan

### 15.1 Final assessment

`{FINAL_ASSESSMENT}`

### 15.2 Reliance decision

- Suitable for intended decision: `{YES_CONDITIONAL_NO}`
- Conditions before reliance: `{CONDITIONS}`
- Decision-maker: `{DECISION_MAKER}`
- Required counsel review: `{COUNSEL_REVIEW}`

### 15.3 Remediation sequence

| Sequence | Action | Acceptance criterion | Owner | Due/trigger | Status |
|---:|---|---|---|---|---|
| 1 | `{ACTION}` | `{ACCEPTANCE_CRITERION}` | `{OWNER}` | `{TIMING}` | `{STATUS}` |
| 2 | `{ACTION}` | `{ACCEPTANCE_CRITERION}` | `{OWNER}` | `{TIMING}` | `{STATUS}` |
| 3 | `{ACTION}` | `{ACCEPTANCE_CRITERION}` | `{OWNER}` | `{TIMING}` | `{STATUS}` |

### 15.4 Re-review triggers

- product/process/design change: `{TRIGGER}`;
- new jurisdiction or commercial activity: `{TRIGGER}`;
- claim grant/amendment/opposition/reexamination/litigation: `{TRIGGER}`;
- ownership/licence change: `{TRIGGER}`;
- newly published relevant family: `{TRIGGER}`;
- launch, transaction, event, or governance gate: `{TRIGGER}`.

### 15.5 Sign-off

| Role | Name | Decision / comment | Date |
|---|---|---|---|
| Reviewer | `{NAME}` | `{COMMENT}` | `{DATE}` |
| Technical owner | `{NAME}` | `{COMMENT}` | `{DATE}` |
| Legal / IP reviewer | `{NAME}` | `{COMMENT}` | `{DATE}` |
| Decision owner | `{NAME}` | `{COMMENT}` | `{DATE}` |

---

## 16. Review boundary and disclaimer

This assessment evaluates the quality of the identified FTO or patent-risk
report and, where stated, compares its search set with separately obtained
patent data. It is limited to the defined product or process, configuration,
commercial activity, jurisdiction, claim version, source coverage, and review
date.

Patent applications may remain unpublished; pending claims may change; granted
claims, legal status, ownership, product facts, and law may change. Database
coverage, indexing, machine translation, family grouping, and status
normalization have limitations. Observed search overlap is not proof of true
recall, and a zero-result search is not proof of no patent risk.

This document is a report-quality assessment and decision-support work product.
It is not legal advice, does not itself provide a legal opinion, and does not
guarantee freedom to operate. Qualified counsel should review material legal or
commercial decisions for the applicable jurisdiction.

---

## Appendix A — Evidence-source register

| Source ID | Proposition supported | Source/provider | Record/tool/query | Date accessed | Jurisdiction | URL/reference | Limitation |
|---|---|---|---|---|---|---|---|
| `{SOURCE_ID}` | `{PROPOSITION}` | `{SOURCE}` | `{RECORD}` | `{DATE}` | `{JURISDICTION}` | `{REFERENCE}` | `{LIMITATION}` |

## Appendix B — Search-log register

| Search ID | Route | Provider/database | Query/request | Fields/filters | Run date | Raw | Retained | Reviewer |
|---|---|---|---|---|---|---:|---:|---|
| `{SEARCH_ID}` | `{ROUTE}` | `{PROVIDER}` | `{QUERY}` | `{FIELDS_FILTERS}` | `{DATE}` | `{N}` | `{N}` | `{REVIEWER}` |

## Appendix C — Family and identifier register

| Family key | Representative | Jurisdictional member | Publication | Application | Grant | Priority | Status/date | Route(s) |
|---|---|---|---|---|---|---|---|---|
| `{FAMILY_KEY}` | `{REPRESENTATIVE}` | `{MEMBER}` | `{PUBLICATION}` | `{APPLICATION}` | `{GRANT}` | `{PRIORITY}` | `{STATUS}` | `{ROUTES}` |

## Appendix D — Claim and product-evidence register

| Patent/claim | Claim source/version | Limitation | Product/process evidence | Evidence version/date | Mapping | Reviewer note |
|---|---|---|---|---|---|---|
| `{PATENT_CLAIM}` | `{CLAIM_SOURCE}` | `{LIMITATION}` | `{PRODUCT_EVIDENCE}` | `{VERSION_DATE}` | `{MAPPING}` | `{NOTE}` |

## Appendix E — Change history

| Assessment version | Date | Author | Change | Evidence/conclusion affected | Approval |
|---|---|---|---|---|---|
| `{VERSION}` | `{DATE}` | `{AUTHOR}` | `{CHANGE}` | `{EFFECT}` | `{APPROVAL}` |
