# Query & Taxonomy Construction Methodology

Abstracted from a real expert-grade manual patent landscape engagement (humanoid / embodied-AI domain).
This document encodes **how a professional analyst constructs search queries and a technology breakdown table** — the reusable decision logic, not the domain-specific strings. Use it as a reference for the built-in search planning step and `pps-tag` taxonomy proposal.

The worked examples below are anonymized fragments. Do not reuse client-specific keyword strings verbatim; reuse the **structure and decision rules**.

---

## Part A — Search Query Construction Methodology

The single biggest gap between a naive keyword query and an expert query is **field-scoped operators + a constant topic anchor**. Expert queries are not flat keyword bags; they are layered logical structures.

### A1. Field-scoped operators are the primary precision lever

PatSnap query syntax exposes field operators that scope a term to a part of the document. Choosing the right field per clause is the #1 driver of precision/recall.

| Operator | Scope | When to use |
|---|---|---|
| `TTL` / `TTL_ALL` | Title (all languages) | Highest precision. Use for the **defining term** of a narrow concept, or for **NOT** rules where a title mention is decisive. |
| `TA` / `TA_ALL` | Title + Abstract | Default for a **core concept** — broad enough to recall, tight enough to stay on-topic. |
| `TAC` / `TAC_ALL` | Title + Abstract + Claims | Use when the concept lives in claims (control methods, algorithms). Wider recall. |
| `TACD` / `TACD_ALL` | Title + Abstract + Claims + Description | **Widest text recall.** Use for the **topic anchor** (see A2) so the anchor catches patents that only mention the domain in the body. |
| `DESC_F` / `DESC_B` / `DESC_S` | Description first part / background / specific-embodiment | Surgical. Use `DESC_S` in **NOT** rules to exclude patents whose *embodiment* is off-topic (e.g. industrial-arm embodiment) even if the abstract looks relevant. |
| `IPC` / `CPC` / `MIPC` / `MCPC` | Classification (M = main classification only) | Recall booster and noise filter. See A4. |
| `all_an` / `AUTHORITY` / `E_PRIORITY_DATE` | Assignee / jurisdiction / earliest priority date | Scope and targeted exclusions. |

**Rule of thumb:**
- Anchor the **topic** with the widest field (`TACD_ALL`).
- Define the **sub-concept** with a medium field (`TA_ALL` / `TAC_ALL`).
- Cut **noise** with the narrowest decisive field (`TTL_ALL`, `DESC_S`, `all_an`).

### A2. The constant topic anchor

Every branch query in an expert set AND-joins a **constant topic-anchor clause** — a stable disjunction of the domain's defining terms in both languages, scoped to `TACD_ALL`.

```
... AND TACD_ALL:(<domain term 1> OR <domain term 2> OR "<EN term 1>" OR "<EN term 2>" OR <synonyms…>)
```

Why this beats NOT-only filtering:
- A NOT list is open-ended — you can never enumerate all off-topic patterns.
- A positive anchor is closed — it guarantees every hit is *about the domain*, then each branch clause narrows *which sub-topic*.

**Process:** build the anchor disjunction once (all domain names, abbreviations, EN+CN, common misspellings), then reuse it verbatim across every branch query. When a branch is itself the anchor (e.g. the whole-domain count), relax the per-branch clause.

### A3. Proximity operators for relation control

| Operator | Meaning | Use |
|---|---|---|
| `$W5` / `$Wn` | within n words, ordered or near | Tie two terms that must co-occur closely (`"end effector" $W5 robot`). Cuts false hits where both words appear but unrelated. |
| `$SEN` / `$sen` | within the same sentence | Looser than `$Wn`, tighter than AND. Good for "concept + action" pairs (`(visual OR vision) $sen (capture OR process)`). |
| plain `AND` | anywhere in field | Use only when co-occurrence anywhere is acceptable. |

Escalation ladder when a branch is too noisy: `AND` → `$SEN` → `$Wn` → move the weaker term to `TTL`.

### A4. IPC/CPC as a recall by-pass, not just a filter

Naive use: IPC only as include/exclude in a confirmation table.
Expert use: IPC/CPC is a **parallel recall path** OR-joined with weak keywords.

```
( <strong keyword clause> )
OR ( <weak/ambiguous keyword clause> AND IPC:(<anchor class>) )
OR IPC:(<highly specific class that is self-sufficient>)
```

Logic:
- A strong keyword stands alone.
- A weak keyword (too generic) is **rescued** only when co-occurring with an anchoring IPC class.
- A highly specific IPC class (e.g. a class that *only* covers the target mechanism) can stand alone as its own recall path.
- `MIPC` / `MCPC` (main classification only) in a NOT rule excludes patents whose *primary* subject is off-topic, while tolerating it as a secondary mention.

### A5. Tiered NOT rules — by field, assignee, and classification

Expert NOT rules are not a flat keyword blacklist. They are tiered by decisiveness:

| NOT tier | Example pattern | Why |
|---|---|---|
| NOT whole IPC class | `NOT IPC:A61` | Entire off-topic domain (medical) |
| NOT main classification | `NOT MIPC:G06V` | Patent is *primarily* about the off-topic class |
| NOT title term | `NOT TTL_ALL:(压力 OR 触觉)` | Title mention is decisive evidence of wrong sub-topic |
| NOT embodiment | `NOT DESC_S:(工业机器人 OR SCARA OR 六轴机器人 ...)` | The *specific embodiment* is off-topic even if abstract looks right |
| NOT specific assignee | `NOT all_an:<known-off-scope entity>` | A specific company keeps polluting results in this branch |

Record the **reason** for every NOT rule. A NOT rule without a recorded reason is a future false-negative waiting to happen.

### A6. The canonical branch-query skeleton

Every expert branch query reduces to this shape:

```
(
   <strong keyword clause, field-scoped>
   OR ( <weak keyword clause> AND <IPC/CPC anchor> )
   OR <self-sufficient IPC clause>
)
AND <CONSTANT TOPIC ANCHOR (TACD_ALL)>
NOT ( <tiered NOT rules with recorded reasons> )
```

When you generate a branch query in M2.5, fill this skeleton. When you present it in the Step 1-E confirmation table, show it decomposed into these four parts so the user can audit each lever.

### A7. Scope envelope clauses (apply to the whole set)

Held constant across all queries, set once in Step 0/1:
- Jurisdiction: `AUTHORITY:(CN OR US OR EP)`
- Time basis: earliest priority date is common for tech-trend work — `E_PRIORITY_DATE:[20230101 TO *]` (vs. publication date `pbdt` for market/legal views; state which and why).
- Family counting: simple family for tech stats; publication text level for market/legal.

---

## Part B — Technology Breakdown Table Methodology

The deliverable that drives Layer 2 taxonomy recommendation is a **technology breakdown table**: a strict 4-column hierarchy.

### B1. The 4-column structure

| Column | Content | Rule |
|---|---|---|
| Level-1 branch | Top technical domain | 4–6 branches typical. Maps to system architecture (e.g. hardware / software-control / platform). |
| Level-2 branch | Sub-system or capability | 3–8 per level-1. |
| Level-3 branch | Concrete technique | The atomic taggable unit. **Total level-3 count ≤ ~40** across the whole table (a hard practical ceiling for human tagging). |
| Technical description | 1–2 sentences | States *what the technique does and why it matters* — written so a tagger can decide membership. This is the membership rubric, not marketing copy. |

This is exactly the `B1 → B1.1 / B1.2 / B1.3` structure: level-1 = B1, level-2/3 = the sub-techniques. **Layer 2's job is to PROPOSE this table, not to tag each patent** — tagging happens in the client's SaaS tool against this table.

### B2. How to decompose — top-down by architecture, bottom-up by evidence

Expert decomposition is **two-pass**:

1. **Top-down (architecture-first):** Start from how the system is physically/logically built. For a device: hardware structure → control software → platform/tooling. This gives stable level-1/level-2 skeleton independent of what patents happen to exist.
2. **Bottom-up (evidence-driven):** Run seed searches and abstract sampling; let the actual patent clusters confirm, split, or merge level-3 nodes. A level-3 node that returns ~0 patents is merged up; a level-3 node that returns thousands is split.

The final table is the reconciliation: architecture defines the shape, evidence sets the granularity.

### B3. Granularity control rules

- **Level-3 is the tagging atom.** It must be (a) searchable as a distinct query, (b) describable in one sentence, (c) non-overlapping with siblings.
- **≤40 level-3 nodes total.** If you exceed this, merge the smallest or least-distinct nodes. Human tagging beyond ~40 categories loses consistency.
- **Each level-3 maps to one branch query** (Part A skeleton). If you cannot write a clean query for a node, the node is too vague — redefine it.
- **Mutually exclusive at each level** for single-value tagging. If a patent plausibly fits two siblings, the table boundary is wrong — sharpen the descriptions, or note the overlap as a known cross-cutting theme.

### B4. From breakdown table to "key technical questions"

Beyond the static taxonomy, expert engagements extract **key technical questions** (关键技术问题) per branch — the open problems the field is trying to solve (e.g. "high-DOF compact dexterous-hand actuation", "full-scene high-precision perception of reflective/transparent objects"). These are:
- The seeds for **technology-evolution storylines** (each question → one evolution path → ≥3 representative families).
- Typically **≥10 questions**, split roughly evenly across major level-1 branches.

Capture these in the taxonomy proposal as a parallel list — they drive Layer 3's evolution analysis, not the tagging table.

### B5. Recommended-patent-package linkage

Each level-3 branch (细分领域) that is a delivery priority becomes a **recommended patent package**: ≥3 families per package, ≥10 packages total. Each patent in a package carries a **recommendation reason** drawn from a fixed rubric:

```
disruptive_technology | novel_application_scenario | pulls_latent_user_demand |
major_performance_gain | novel_function | novel_interaction_mode
```

This rubric is what fills `recommendation_reason` in `patent_index.core` and the package deliverable.

---

## Part C — How the skill should apply this

| Skill step | Apply |
|---|---|
| Search planning Step 1-A/B/D | Use Part A2 anchor, A4 IPC by-pass, A5 tiered NOT. Use the `/33072f` query-planning / keyword-extension tools (`suggest_keywords`, `query_classification_helper`) to draft, then audit against this methodology. |
| Search planning Step 1-E | Present each branch query decomposed into the A6 four-part skeleton so the user audits each lever. |
| Search planning M2.5 | Generate one A6-skeleton query per confirmed branch. |
| `pps-tag` taxonomy proposal | Produce the Part B 4-column table (≤40 level-3), plus the B4 key-question list. Tagging itself is done in the client SaaS tool. |
| `pps-tag` / search planning M4 | Use the B5 recommendation-reason rubric for `recommendation_reason`. |

## Part D — Precision validation (addresses "how accurate is the retrieval?")

A confirmation table shows *what* the query is; it does not show *how accurate* it is. Add a sampling-based precision check before committing a query set:

1. After a branch query returns hits, **random-sample N (≈20–30) hits**.
2. For each, read title+abstract and judge relevant / not-relevant against the level-3 description (B1).
3. Report **precision = relevant / N** per branch.
4. For recall sanity: sample from the **just-outside boundary** (hits removed by a NOT rule, or near-miss seed hits) and check how many were wrongly excluded.
5. Surface per-branch precision in the Step 1-E confirmation table. A branch below a precision threshold (e.g. <80%) gets its query tightened (escalate proximity, narrow field, add NOT) before proceeding.

This converts "trust me, the query is good" into an auditable number the user confirms.
