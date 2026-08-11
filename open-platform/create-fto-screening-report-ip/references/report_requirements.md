# Generic FTO Screening Report Requirements

## 1. Risk-document structure

The source risk-point document may contain paragraphs, tables, headings, and
embedded figures. Extract all relevant content, not only top-level paragraphs.

Recognize these semantic groups when present:

- project and product/process identity;
- controlled product/process version;
- technical feature groups;
- essential and optional features;
- product evidence references;
- target jurisdictions and relevant commercial acts;
- competitors, assignees, inventors, standards, or classifications;
- search/status cutoffs and decision date;
- known patents, designs, applications, or exclusions;
- confidentiality and distribution constraints.

Do not carry facts from a previous case into a new run. Missing inputs remain
missing and must be shown in the report.

## 2. Recognized input fields

| Field | Required | Meaning |
|---|---|---|
| `project_name` | Yes | Human-readable screening project name |
| `product_name` | Yes | Target product, process, service, or implementation |
| `product_version` | Yes | Controlled design, release, formulation, sequence, or process version |
| `industry` | No | Industry context used only when supported |
| `target_jurisdictions` | Yes | Patent authorities/countries relevant to the commercial acts |
| `relevant_acts` | Yes | Make, use, sell, offer, import, export, supply, or another defined act |
| `technical_features` | Yes | Feature groups and product/process evidence |
| `search_queries` | Yes | User-approved PatSnap expressions and provenance |
| `search_cutoff` | Yes | Publication-search cutoff in ISO 8601 format |
| `status_cutoff` | Yes | Legal-status evidence date in ISO 8601 format |
| `family_counting_convention` | Yes | Publication/application/grant/family unit |
| `target_company` | No | Competitor or rights-holder route where relevant |
| `ipc_filter` / `cpc_filter` | No | Technically justified classification restrictions |
| `decision_context` | Yes | Launch, design freeze, transaction, event, or other decision |

## 3. Search-expression rules

- Preserve every user-provided expression verbatim.
- Record source, reviewer, approval status, fields, filters, and date run.
- Do not silently add a jurisdiction, company, classification, legal-status, or
  date filter.
- Generated expressions must be separately labeled and reviewed before use.
- P070 suggestions are candidate terminology, not validated search scope.
- Retain each patent's matching queries after deduplication.
- Record raw, paginated, retained, duplicate, and family counts.
- A failed or empty query remains visible and is not a no-risk finding.

## 4. Candidate normalization

For each candidate retain, where available:

- PatSnap patent ID;
- publication, application, and grant identifiers;
- authority and kind code;
- title and abstract;
- original/current applicant or assignee;
- priority, filing, publication, and grant dates;
- family key and representative rule;
- legal-status value, source, and date;
- matching query IDs;
- retrieval mode, provider/tool/endpoint, request ID, and retrieval date.

Deduplicate by normalized publication number, PatSnap ID, application number,
or a documented fallback. Never merge records only because their titles match.

## 5. Claim retrieval and selection

- Use P018 `/basic-patent-data/claim-data` in REST mode.
- Identify returned language and whether related-family replacement was used.
- Retain the raw returned claim structure and normalized text.
- Claim 1 is the minimum screening shortcut preserved from the source.
- Review every other independent claim that may materially cover the defined
  product/process or activity before a decision-material conclusion.
- Review dependent claims when they add a potentially mapped limitation.
- Identify claim version, amendment/prosecution state, jurisdictional member,
  translation source, and status date.
- If claims are missing, do not substitute an abstract or description as if it
  were claim text.

## 6. Claim-chart contract

Each comparison must include:

| Field | Requirement |
|---|---|
| Patent and claim | Correct jurisdictional identifier and claim number |
| Claim source | Language, version, endpoint/connector, retrieval date |
| Limitation | One complete limitation or legally meaningful element |
| Product evidence | Versioned fact, drawing, specification, test, or cited source |
| Literal mapping | Mapped / not mapped / uncertain, with explanation |
| Equivalents | Jurisdiction-specific assessment only when appropriate |
| Contrary evidence | Facts or interpretations that weaken the conclusion |
| Confidence | High / moderate / low with basis |
| Missing information | Evidence needed to resolve uncertainty |
| Reviewer | Human/AI role and review status |

Do not derive infringement from semantic similarity, title, abstract,
classification, or an AI score alone.

## 7. AI07 supporting output

If AI07 is used, retain:

- normalized request and model/tool identifier;
- request date and run/task ID;
- patent/claim and product feature input references;
- raw response location;
- parsed feature comparisons;
- conclusion, rationale, confidence, and missing facts;
- conflicts with retrieved claim text or structured human review;
- reviewer disposition.

AI07 output is supporting evidence. It never overrides the primary claim text,
product evidence, official status data, or qualified reviewer judgment.

## 8. Risk labels

Use text labels with written criteria:

- `Higher screening concern` — one or more material claims appear potentially
  mapped and current evidence does not resolve the concern;
- `Moderate screening concern` — mapping or legal/status evidence is uncertain;
- `Lower screening concern` — supported missing limitation, non-target right,
  or other documented reason reduces concern;
- `Pending watchlist` — claims may change and are not currently enforceable;
- `Not assessed` — evidence is insufficient or the step failed.

These are screening labels, not infringement probabilities or legal opinions.

## 9. Required report structure

The HTML and DOCX reports must include:

1. cover and document control;
2. executive screening summary;
3. purpose, target product/process, version, acts, jurisdictions, and decision;
4. scope, assumptions, exclusions, search/status cutoffs, and family convention;
5. technical-feature and product-evidence inventory;
6. data-access mode and complete query/search methodology;
7. candidate and family overview;
8. higher, moderate, lower, pending, and not-assessed lists;
9. claim-limitation comparison for material candidates;
10. status, ownership, family, and claim-version notes;
11. omissions, unresolved evidence, and search limitations;
12. recommendations, owners, timing, and re-review triggers;
13. source/provenance register;
14. screening boundary and legal disclaimer.

## 10. Output files

The runner may generate these run artifacts:

- `queries.json`;
- `patent_list.json`;
- `claim_chart.json`;
- `fto_structured_data.json`;
- an English HTML report;
- an English DOCX report;
- a run manifest or error record when supported by the source script.

Generated artifacts belong in the selected output directory. Do not add them
to the skill package.

## 11. Partial and failure states

The report must show `Partial` or `Not assessed` when:

- the risk document cannot be fully parsed;
- required scope fields are missing;
- no approved search expression exists;
- authentication or entitlement fails;
- a query, page, claim request, or AI step fails;
- status/claim/family evidence is stale or unavailable;
- an output schema cannot be validated.

Preserve successful evidence, list failed steps, and state the effect. Do not
replace missing data with examples, prior-run content, or invented records.

## 12. Legal boundary

The output is an FTO screening based on the defined product/process, version,
activity, jurisdictions, evidence, claims, and dates. It does not guarantee
freedom to operate, establish complete recall, or replace a jurisdiction-
specific opinion from qualified local counsel.
