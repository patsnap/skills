# Topic Limitation Workflow

Use this reference to add a Patsnap/Zhihuiya technology-topic limitation to applicant-first retrieval. The logic mirrors `patsnap-topic-search-strategy`, but the final formulas must remain applicant-constrained.

## 1. Clarify Topic Scope

Clarify only missing parameters that materially affect retrieval:

| Parameter | Notes |
|---|---|
| Original user topic | Preserve verbatim. |
| Technical boundary | What is included and excluded. |
| Database scope | Country/region, patent type, legal status, time window, language. |
| Retrieval purpose | Applicant portfolio review, competitor comparison, monitoring, FTO pre-search, report input, or downstream screening. |
| Seeds | Known patents, papers, products, standards, applicants, keywords, IPC/CPC codes. |
| Deliverable | Choose `formula_only_mode` for executable formula/methodology only, or `retrieval_dataset_mode` for executed retrieval, datasets, deduplication, and downstream inputs. |

Before drafting formulas, write a concise definition of the technology topic so the user can confirm the core concept.

If the user asks for a full draft before confirmation, mark every boundary item as `待用户确认`.

Do not run topic presearch, count prediction, or applicant-topic combined retrieval before the topic definition, boundary table, decomposition table, and first-pass search-element matrix are written.

## Mandatory Topic Preflight Package

Before any section named `检索策略`, `Search Strategy`, `技术主题关键词`, `申请人表达式`, or any formula block, output this package. Keep the headings and tables visible in the report. Do not compress them into prose.

Formula firewall:

- Do not output `ANCS`, `TA_ALL`, `APPLICANT_TOPIC_FINAL`, or any combined query before Step 0-7 of the pre-retrieval package exists.
- `Step 3` must be topic boundary confirmation. Never use `Step 3` for formal search strategy.
- `Step 2` must be technology topic definition. Never use `Step 2` for keyword matrix.
- Search element or keyword matrices belong only to `Step 5`.
- Search strategy can only start at Step 8 or later.

Chinese fixed step order:

```text
Step 0：原始需求与执行模式
Step 1：申请人实体扩展表
Step 2：技术主题定义
Step 3：技术边界确认表
Step 4：技术主题分解表
Step 5：检索元素矩阵
Step 6：噪声与排除边界表
Step 7：检索前门禁状态
Step 8：检索策略与公式
```

Invalid shortcut:

```text
Step 2：固态电池技术主题关键词矩阵
TA_ALL=(...)
Step 3：组合检索式
```

This is invalid. First output Step 2 technology definition, Step 3 boundary table, Step 4 decomposition table, Step 5 search element matrix, Step 6 noise table, and Step 7 gate status.

### 1. Technology Topic Definition

Write 3-5 sentences:

- What the topic means technically.
- What the topic is not.
- Why the topic matters for patent retrieval.
- Which terms are broad, ambiguous, or likely noisy.
- Confirmation status: `confirmed`, `待用户确认`, or `agent-inferred`.

### 2. Topic Boundary Confirmation Table

| Boundary item | Include / Exclude / Pending | Rationale | Retrieval impact | Confirmation status |
|---|---|---|---|---|
| Core technical object |  |  |  |  |
| Must-have technical feature |  |  |  |  |
| Optional/adjacent technology |  |  |  |  |
| Explicit exclusion |  |  |  |  |
| Ambiguous term |  |  |  |  |

### 3. Topic Decomposition Table

| Facet | Branch | What belongs here | What is excluded | Retrieval role | Confirmation status |
|---|---|---|---|---|---|
| Object/material/component |  |  |  | Core / Recall / Precision / Noise |  |
| Function/effect/problem |  |  |  | Core / Recall / Precision / Noise |  |
| Mechanism/process/method |  |  |  | Core / Recall / Precision / Noise |  |
| Application/end product |  |  |  | Core / Recall / Precision / Noise |  |
| Classification anchors |  |  |  | Core / Recall / Precision / Noise |  |
| Exclusion/noise |  |  |  | Noise |  |

### 4. Search Element Matrix

| Element id | Facet | CN terms | EN terms | Lower concepts / variants | Field scope | Proximity rule | Formula role | Confirmation status |
|---|---|---|---|---|---|---|---|---|
| E1 |  |  |  |  | title/abstract/claims/classification | AND / OR / $Wn / $PREn / $SEN / $PARA | Core / Recall / Precision / Noise |  |

### 5. Noise and Exclusion Boundary Table

| Noise id | Noise source | Why it is noise | Exclusion terms/classes | Risk of over-exclusion | Confirmation status |
|---|---|---|---|---|---|
| N1 |  |  |  |  |  |

### 6. Gate Status Before Search

| Gate | Required evidence | Status | Next action |
|---|---|---|---|
| Topic definition | 3-5 sentence definition exists | Pass / Fail |  |
| Boundary confirmation | Boundary table exists | Pass / Fail |  |
| Decomposition | Decomposition table exists | Pass / Fail |  |
| Search element matrix | Matrix exists with CN/EN terms, fields, proximity, formula role | Pass / Fail |  |
| Noise boundary | Noise table exists or explicit no-noise rationale exists | Pass / Fail |  |

If any status is `Fail`, stop. Do not write search strategy, applicant-topic formula, scale prediction, or retrieval results.

For broad battery topics such as 固态电池, explicitly separate at least:

- all-solid-state battery vs semi-solid/gel/quasi-solid battery;
- solid electrolyte material system, such as sulfide, oxide, polymer, halide, composite electrolyte;
- electrode-electrolyte interface and interfacial modification;
- cell structure, stack/lamination, pressure, packaging, and manufacturing process;
- application scope such as power battery, energy storage, consumer electronics;
- noise boundary for conventional liquid lithium-ion battery, generic separator/electrolyte additive, and unrelated solid-state electronics.

## 2. Decompose the Topic

Build a decomposition table before writing the final formula.

| Facet | What to capture | Example prompts |
|---|---|---|
| Object/material/component | The thing being improved, processed, measured, prepared, or used. | material, device, molecule, system, module, ingredient |
| Function/effect/problem | The performance goal or problem solved. | safety, stability, conductivity, retention, yield, sensitivity |
| Mechanism/process/method | How the technology works. | coating, separation, fermentation, extraction, catalytic route |
| Application/end product | Where the technology is used. | battery, food, sensor, packaging, drug, manufacturing line |
| Exclusion/noise | Stable false-positive domains. | unrelated industry, generic process terms, broad materials |
| Classification anchors | IPC/CPC or domain taxonomies. | use parent `_LOW` fields when lower-subgroup recall is intended |

Do not treat the applicant name as a topic facet. Applicant expressions are handled separately.

The decomposition table is mandatory. A statement such as "固态电池技术主题预检" is not enough to satisfy this gate.

A table titled only `技术主题关键词` is not enough. It must be transformed into the mandatory package above before formulas are produced.

## 3. Build the Term Matrix

Include:

- Chinese terms.
- English terms.
- Abbreviations and spelling variants.
- Lower concepts and representative members.
- Trade names, common product names, and chemical names when relevant.
- Process-state terms and equipment/feedstock/reaction terms when relevant.
- Upper concepts only when strongly constrained by other facets.
- Adjacent terms and translation variants when missed samples justify them.
- IPC/CPC anchors, using `IPC_LOW`/`CPC_LOW` for parent-group recall.

Term matrix:

| Element id | Facet | CN terms | EN terms | Lower concepts / variants | Field scope | Proximity rule | Confirmation status | Notes |
|---|---|---|---|---|---|---|---|---|

For compound concepts, model whether terms must appear near each other, in order, in the same sentence, or in the same paragraph. Use `$Wn`, `$PREn`, `$SEN`, or `$PARA` when it improves precision without losing known relevant records.

Do not execute `S0_TOPIC_SEED` or any topic-count query until this matrix exists.

## 4. Construct Layered Topic Formulas

Build topic formulas separately from applicant formulas.

| Layer | Purpose | Typical content |
|---|---|---|
| `S0_TOPIC_SEED` | Collect seed records and validate terminology. | Narrow title/abstract/claims terms, known codes, known seed concepts. |
| `S1_TOPIC_CORE` | Main concept retrieval. | Core object + core mechanism/function/application. |
| `S2_TOPIC_RECALL` | Recall expansion. | Synonyms, lower concepts, variants, classification anchors, seed-derived terms. |
| `S3_TOPIC_PRECISION` | Precision constraints. | Required function/application/method constraints, proximity, field weighting. |
| `S4_TOPIC_FINAL_BALANCED` | Balanced topic formula. | Combination of core and recall branches with precision constraints. |
| `N_*` | Noise exclusions. | Stable false-positive domains confirmed by review or highly predictable from topic wording. |

Do not provide only shorthand formulas. Both execution modes must include expanded formulas:

```text
TOPIC_FINAL_BALANCED_EXPANDED = (<fully expanded S4 formula>)
NOISE_TOTAL_EXPANDED = (<fully expanded N1 OR N2 ...>)  # only when noise exists
```

## 5. Combine with Applicant Formulas

Use applicant formulas from `applicant-retrieval-workflow.md`.

Required combined formulas:

```text
APPLICANT_TOPIC_FINAL =
(APPLICANT_TOTAL) AND (TOPIC_FINAL_BALANCED)
```

Expanded executable form:

```text
APPLICANT_TOPIC_FINAL_EXPANDED =
(<fully expanded applicant expressions>) AND (<fully expanded topic formula>)
```

If noise exclusions are used:

```text
APPLICANT_TOPIC_PRECISION_EXPANDED =
(<fully expanded applicant expressions>) AND (<fully expanded topic formula>) NOT (<fully expanded noise formula>)
```

Rules:

- Do not hide applicant filters inside topic branches.
- Do not rely on applicant names to remove technical noise.
- Keep applicant counts, topic-only test counts, applicant-topic counts, and precision/noise-filtered counts separate.
- If the topic formula is broad because it will be applicant-constrained, say so explicitly and identify the precision risk.

## 6. Execute or Simulate Retrieval

In `formula_only_mode`, do not execute retrieval unless the user explicitly asks. Provide expanded formulas, assumptions, pending confirmations, and a PatSnap Expert Search execution checklist.

In `retrieval_dataset_mode`, when a Patsnap/Open Platform connector is available, execute or validate count checkpoints in this order:

1. Confirm pre-retrieval artifacts exist: applicant expansion table, topic definition/boundary table, decomposition table, search-element matrix.
2. Applicant formula count.
3. Topic seed/core count.
4. Applicant-topic combined count.
5. Precision/noise-filtered count.
6. Sample review if records are available.

If retrieval cannot be executed, downgrade to `formula_only_mode` and provide an execution checklist for PatSnap Expert Search.

Retrieval checkpoint table:

| Checkpoint | Formula version | Count | What the count means | Action |
|---|---|---:|---|---|

## 7. Validate Recall and Precision

Do not claim final recall or precision unless the user provides executed result sets, sampled labels, and independent recall samples.

Provide validation guidance:

- Known seed patents: check whether they are recovered by `APPLICANT_TOPIC_FINAL_EXPANDED`.
- Independent recall samples: compare missed relevant records and classify the miss reason.
- Precision sample: label a random or stratified sample from the executed result set.
- Noise review: identify stable noise by domain, classification, term pattern, or applicant artifact.

When the user provides missed relevant records or noise hits, classify each issue as:

- Boundary disagreement.
- Missing object/material term.
- Missing function/effect term.
- Missing process/method term.
- Missing application/end-product term.
- Field-scope issue.
- Translation/language gap.
- Classification gap.
- Stable noise cluster.
- Bracket/operator error.

Then update the decomposition table, term matrix, noise table, strategy table, and expanded formulas consistently.

## 8. Quality Gates

Before finalizing, check:

- The technical topic is defined in plain language.
- User-confirmed scope and agent-inferred scope are separated.
- The topic definition, boundary table, decomposition table, and first-pass search-element matrix were produced before any topic count/presearch.
- The topic is expanded across multiple dimensions, not only literal synonyms.
- Compound relationships use proximity operators when useful.
- Parent classification recall uses `_LOW` fields when appropriate.
- Noise exclusions are based on stable domains or reviewed samples, not only applicant names.
- Expanded formulas contain no unresolved placeholders such as `S1`, `S2`, `N1`, or `APPLICANT_TOTAL`.
- The final formula can be explained by applicant side, topic side, and noise side.
- The report provides validation guidance without overstating unverified recall/precision.
- In `formula_only_mode`, completion does not require counts or datasets, but must explicitly state `dataset_status: not_executed`.
- In `retrieval_dataset_mode`, completion requires retrieval provenance, deduplication, and representative dataset handoff fields.
