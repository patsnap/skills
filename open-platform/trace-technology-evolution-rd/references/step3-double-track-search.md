# Stage 3: Four-Track Patent and Literature Research

## Position in the workflow

- Input: reviewed component and critical-unit SVOP anchor packets.
- Output: accepted/rejected evidence registers and reproducible search logs.
- Downstream: Stage 4 evidence screening and assessment.
- The source called this a double-track search, then expanded it to four tracks. The localized method consistently uses four conceptual tracks.

## Research question

For each functional unit, determine:

1. which technical approaches are documented in the target domain;
2. which approaches are documented in other domains under comparable mechanisms and conditions;
3. what scientific or technical results support or contradict those approaches;
4. which standards, engineering cases, product events, funding events, regulatory changes, or new entrants alter interpretation;
5. what was not searched, inaccessible, or too weak to accept.

## Four conceptual tracks

| Track | Scope | Primary purpose |
|---|---|---|
| In-domain patents | Product/domain anchors plus function and mechanism | Map disclosed implementations, actors, claims, and filing activity |
| In-domain literature | Product/domain plus function, mechanism, method, and parameter | Map experiments, mechanisms, performance evidence, and limitations |
| Cross-domain patents | Generalized SVOP function plus transfer-relevant mechanisms | Find comparable implementations outside the target product domain |
| Cross-domain literature | Generalized SVOP function plus mechanism, conditions, and parameter | Find transferable scientific results and failure conditions |

Additional evidence tracks may include:

- standards and technical roadmaps;
- regulatory or safety documents;
- engineering deployments and product documentation;
- capital and funding events;
- manufacturing and cost evidence;
- new or cross-industry entrants;
- credible negative or contradictory evidence.

Keep each evidence type separate. Do not score a press release as a patent or a paper.

## Verified PatSnap patent support

When available, use:

- `advanced_patent_search`: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing`: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Use the currently exposed schemas. The source names generic `patsnap_search`, `patsnap_fetch`, paper search, family modules, valuation fields, citation modules, and legal modules. Do not claim any of those interfaces unless the execution environment actually exposes and verifies them.

PatSnap MCP is not automatically a scientific-literature, standards, market-news, funding, or regulatory connector. Use appropriate primary sources for those tracks.

## Research preparation

Create one packet per unit:

- unit ID and parent hierarchy;
- specific product/domain terms;
- generalized SVOP terms;
- mechanism terms;
- parameter names, units, and comparable conditions;
- synonyms, acronyms, spelling variants, and translations;
- relevant classifications when known;
- named actors only when inclusion is justified;
- exclusions and false-positive patterns;
- geographies and languages;
- time coverage;
- target evidence types;
- confidentiality review;
- reviewer and approval state.

## Patent query design

Build queries in layers:

1. **Recall query** — function, mechanism, synonyms, and broad classifications.
2. **Domain query** — product or application context plus the function.
3. **Cross-domain query** — generalized function and mechanism without the target-product anchor.
4. **Parameter query** — metric names, units, conditions, and claimed ranges where relevant.
5. **Actor query** — validated applicants, assignees, inventors, or organizations when needed.
6. **Gap-check query** — synonyms, adjacent classifications, citation paths, and alternative mechanisms around a candidate gap.

Use claims, title/abstract, description, classifications, applicants, dates, and jurisdictions only as supported by the connector. Search logs must preserve the exact fields and syntax used.

Do not assume:

- “active” or “granted” means technically important;
- an expired or abandoned publication is irrelevant to evolution history;
- one country set fits every decision;
- a publication count equals a family count;
- a search hit means the claim covers the analyzed feature;
- citation count is directly comparable across fields and ages;
- a missing patent means a missing product or technology.

## Literature query design

Literature retrieval prioritizes technical relevance and evidence quality:

- use natural-language mechanism and research-question queries;
- add methods, materials, operating conditions, and parameter terms;
- use controlled terms or subject classifications where available;
- inspect abstract, methods, results, and limitations;
- distinguish primary research, review, conference paper, preprint, thesis, dataset, and editorial material;
- record peer-review or editorial status;
- search contradictions, failure modes, negative results, and boundary conditions;
- use citation information as context rather than the primary relevance order.

The source reports that absolute citation sorting produced irrelevant cross-disciplinary “super-cited” results. Preserve that lesson. Citation distributions are field-, age-, and document-type dependent.

Do not assume papers consistently lead patents by 1–3 years. Compare actual dates and maturity for the project.

## Evidence acceptance

Accept a record only when:

- its identity and stable source are recorded;
- it is inside the declared scope or explicitly retained as a cross-domain analogy;
- sufficient text is available for the claimed finding;
- mechanism and conditions are interpretable;
- the record is not a duplicate under the chosen normalization rule;
- the analyst records relevance, limitations, and review depth;
- the record date does not exceed the evidence cutoff;
- confidential data was not improperly disclosed during retrieval.

Reject or quarantine:

- title-only records used for detailed route labeling;
- inaccessible records with unverifiable summaries;
- duplicate family/publication records presented as independent evidence;
- secondary reports that distort or omit the primary result;
- content farms or unattributed claims;
- current claims outside the evidence cutoff;
- records whose mechanism is incompatible with the target conditions unless retained as a clearly bounded analogy.

## Search log contract

```json
{
  "search_id": "S1",
  "unit_id": "P4.2",
  "track": "cross_domain_literature",
  "source_or_tool": "Publisher or connector name",
  "searched_at": "2026-08-08T10:00:00Z",
  "query": "full exact query",
  "filters": {},
  "languages": ["English"],
  "date_coverage": {"from": null, "to": "2026-07-31"},
  "requested_limit": 50,
  "returned_count": 34,
  "reviewed_ids": ["E12", "E13"],
  "rejected_count": 32,
  "pagination_or_truncation": "No truncation observed",
  "deduplication": "DOI and normalized title",
  "limitations": "Database and language coverage disclosed here"
}
```

Returned count, reviewed count, accepted count, publication count, family count, and estimated result total are different quantities.

## Patent evidence record

Minimum fields:

- evidence ID;
- publication number and jurisdiction;
- title and stable record link;
- earliest priority date and publication date;
- applicant and current assignee when available;
- simple family ID and count unit;
- legal status with “as of” date when relevant;
- claims or description location reviewed;
- functional unit and search track;
- mechanism and parameter evidence;
- route-label readiness;
- confidence and limitations.

## Literature evidence record

Minimum fields:

- evidence ID;
- title and DOI or stable repository/publisher link;
- authors and affiliations;
- publication date and venue;
- document type and review status;
- methods and system conditions;
- quantitative or qualitative results;
- limitations and contradictions;
- functional unit and search track;
- route-label readiness;
- confidence and review depth.

## Standards and engineering evidence

Record:

- issuing body or responsible organization;
- document or project identifier;
- version, date, and status;
- clause, section, test, or implementation location;
- geography or system scope;
- relevance and limitations;
- whether the item is mandatory, voluntary, draft, withdrawn, or superseded.

Do not turn a draft standard into proof of adoption.

## Current-awareness and web evidence

The source adds five sentinels: capital, maturity, standards, regulation, and cross-industry entrants. Localize them as evidence questions:

### Capital and funding

- What documented funding, acquisition, investment, or public-budget event affects the path?
- Is the source a filing, investor announcement, official grant, or secondary report?
- Does funding concern the exact technology or a broader company story?

### Maturity and deployment

- What prototype, pilot, qualification, manufacturing, certification, or commercial evidence exists?
- Is maturity self-declared or independently reviewed?
- Are scale, operating conditions, reliability, and cost comparable?

### Standards

- Has a standards body opened, drafted, balloted, published, revised, or withdrawn a relevant work item?
- What is the exact document and status date?

### Regulation and safety

- What official rule, guidance, enforcement action, certification requirement, or safety event changes feasibility or timing?
- What jurisdiction and effective date apply?

### Cross-industry entrants

- Has an organization outside the established actor set produced a relevant patent, paper, product, filing, partnership, or acquisition?
- Is the activity technically linked to the target mechanism?

Web evidence remains outside patent scoring and receives source-quality, directness, independence, recency, and applicability review.

## Confidence

Confidence is not encoded by red/yellow/green alone. Record:

- source authority;
- directness to the claim;
- independence from other sources;
- method transparency;
- recency relative to the decision;
- applicability to target conditions;
- contradiction status;
- analyst review depth.

## Sparse tracks

Do not force a minimum paper percentage or a fixed number per bucket.

When a track is sparse:

1. inspect synonyms, classifications, languages, and date coverage;
2. inspect adjacent mechanisms and citation paths;
3. record access or licensing limits;
4. distinguish a genuinely small research field from retrieval failure;
5. retain the sparse state in the report;
6. avoid lowering relevance merely to fill a quota.

## Cross-domain transfer screen

Before accepting an analogy, compare:

- governing mechanism;
- scale and geometry;
- material and medium;
- operating temperature, pressure, frequency, load, or data rate;
- manufacturing process;
- safety and regulatory constraints;
- reliability and lifetime;
- cost and supply chain;
- interface and integration requirements;
- intellectual-property and licensing constraints;
- evidence maturity.

Label analogies as direct, conditional, speculative, or rejected.

## Source-case observations

The source contains fixed headphone hit counts, technology examples, applicant claims, and query outcomes. They are not migrated as current facts. Their reusable lessons are:

- generalized cross-domain queries can be much noisier than product-bound queries;
- large fields need stronger relevance and normalization controls;
- paper retrieval should not be dominated by absolute citation sorting;
- patent/publication lag and literature maturity should be measured, not assumed;
- standards, regulatory, product, and capital signals can change timing interpretation;
- actor and inventor movement may be useful only when supported by lawful, relevant evidence.

## Stage gate

Do not advance until:

- all approved units have attempted tracks or explicit omissions;
- search logs are reproducible;
- evidence IDs and stable links resolve;
- evidence cutoff is enforced;
- patent family/publication units are disclosed;
- evidence types remain separate;
- rejected records and reasons are retained;
- sparse/failed/truncated searches are visible;
- no title-only record is treated as detailed technical evidence;
- cross-domain records have transfer conditions;
- confidential-search authorization is documented.

## Outputs

- evidence register by type;
- rejected-record register;
- complete search log;
- per-unit coverage matrix;
- sparse and failed-track register;
- normalization and deduplication rules;
- current-awareness signal register;
- query refinement history;
- Stage 4 handoff with no invented fixed quota.

## Limitations

- Database, language, classification, licensing, and full-text coverage vary.
- Patent applications publish with delay and legal status changes.
- Literature may not be peer reviewed or reproducible.
- Product announcements and funding events may be promotional.
- Standards and regulation are jurisdiction-specific and time-sensitive.
- Search recall cannot normally be measured exactly; document any estimate method.
- Absence from the reviewed dataset does not establish global absence.
