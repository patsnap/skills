# Requirement Decomposition, Research, and Evidence Workflow

This file supplies decision criteria and query-design guidance for the main Skill. It does not redefine the payload or report structure.

## 1. Requirement-analysis discipline

### Demand and operating need

Extract only what the source supports:

- concrete operating, scientific, manufacturing, clinical, environmental, or engineering context;
- stakeholder or system that needs a solution;
- technical, safety, environmental, reliability, throughput, cost, or other consequence;
- current baseline or workaround.

Do not require a catastrophic safety threat or enormous economic loss. Legitimate R&D can address performance, sustainability, manufacturability, measurement, scientific uncertainty, accessibility, or cost when the source supports it.

### Bottleneck

Look for:

- measured or specified limit with units and conditions;
- tradeoffs of current solutions;
- physical, chemical, biological, algorithmic, manufacturing, integration, or system mechanism;
- missing evidence and assumptions.

Do not insist that the existing route has reached an absolute physical ceiling. Many research directions improve a route through a new combination, control method, process window, material, architecture, or evidence base.

### Solution hypothesis

Separate source-stated solution ideas from analyst-generated hypotheses. Capture path, system interaction, compatibility constraints, target outcome, and validation needs. Never convert a target into a demonstrated result.

## 2. Technical issue decomposition

Create the smallest useful set of bounded technical issues:

- each issue has a distinct decision or validation question;
- source locations are retained;
- dependencies and overlaps are explicit;
- broad symptoms are separated from root-cause hypotheses;
- missing root-cause evidence is labeled;
- no issue is invented to meet a quota.

IDs use `T1`, `T2`, and so on. Every source issue is covered by a direction or a visible limitation.

## 3. Direction formulation

Directions use `D1`, `D2`, and so on. One direction may address several coupled issues, and one issue may require alternative directions. The user-specified maximum is a presentation/decision constraint, not a mathematical instruction to set `k = min(N, max)`.

A direction needs:

- rationale linked to issues;
- testable core research question;
- specific research tasks;
- validation methods and success metrics;
- technical target with basis;
- expected deliverables;
- evidence and evidence gaps;
- uncertainty and confidence;
- disclosed priority basis.

## 4. Search preparation

Build one search packet per direction:

1. problem context and mechanism;
2. differentiating concepts and synonyms;
3. relevant structures, materials, processes, functions, parameters, outcomes, or classifications;
4. exclusions and false positives;
5. languages, jurisdictions, dates, and source types;
6. historical terminology where older evidence matters;
7. confidentiality-minimized query wording;
8. decision-linked review criteria.

## 5. PatSnap MCP mapping

When actually exposed in the user's environment:

- `advanced_patent_search` — https://open.patsnap.com/marketplace/mcp-servers/patent-search — supports semantic, similarity, patent-number, nested, field, count, assignee and keyword-assistance workflows.
- `patent_briefing` — https://open.patsnap.com/marketplace/mcp-servers/patent-briefing — supports selected patent/family bibliography, family, legal-status, description, abstract and claim review.

Use the current callable schema and English interface. The source-named domestic paper/patent functions are not portable. Do not claim `scientific_translational_evidence` for general engineering literature: its verified tools concern translational medicine. Do not claim `current_awareness` for general engineering news: its verified scope is pharmaceutical news.

## 6. Patent search

Choose semantic, keyword, classification, assignee, citation, similarity, or nested strategies according to the direction. Do not impose fixed top-k, recent-three-year, granted-only, or preferred-country rules.

Historical patents may establish route evolution. Applications may show emerging work. Grants may be relevant to current claim scope. Jurisdictions follow the decision, not a universal list.

Record exact query, fields, filters, requested and returned limits, pages reviewed, family rule, cutoff, language, and rejected false positives. Patent evidence does not establish patentability, infringement, validity, FTO, commercial use, or technical superiority.

## 7. Scientific literature search

Use primary publisher/repository records, DOI/Crossref metadata, recognized bibliographic databases available to the user, standards databases, or user-supplied literature. Search by mechanism and technical vocabulary, not only the proposed direction title.

Consider foundational older work, recent advances, reviews for vocabulary, and primary experiments for evidence. Citation counts are field-, age-, database-, and date-dependent; record the source/date and never use them as the sole quality criterion.

For biomedical/translational work only, `scientific_translational_evidence` may be used when its actual tools and domain match the request.

## 8. Standards and engineering cases

Prefer issuing organizations, regulators, government laboratories, project owners, peer-reviewed case reports, official technical reports, and standards bodies. Record version/status, date, publisher, system or project context, and whether a document is normative, draft, superseded, reported, or independently verified.

Do not treat search snippets, aggregator pages, or promotional case studies as equivalent to standards or independently verified engineering evidence.

## 9. Authoritative web supplementation

Use authoritative pages only when primary structured sources are unavailable or when a web page is itself the primary evidence. Possible source classes include government agencies, standards organizations, universities, research institutes, repositories, and companies for their own announcements.

Search queries should be tailored to the technology and evidence class. Do not hard-code China-specific publishers, standards prefixes, voltage levels, or breaker examples.

Record exact URLs, page titles, publishers, publication/update dates, access dates, content category, and limitations. A site restriction is a search tactic, not evidence of authority.

## 10. Parallel execution

Patent, literature, standards/cases, and authoritative-web searches may run in parallel after direction packets are stable. Keep each direction and evidence type in a separate search log. Parallelism must not cause:

- mixed candidate queries;
- duplicate IDs;
- lost pagination state;
- hidden tool failures;
- inconsistent cutoffs;
- unsafely expanded confidential queries.

## 11. Evidence selection

Retain records based on relevance to the direction, source authority, directness, method quality, coverage, recency where material, applicability, independence, and diversity of evidence. Explain representative selection.

Do not enforce universal per-direction caps. If presentation requires a subset, preserve the complete reviewed registry in appendices and state how the subset was chosen.

Use one global `E#` sequence across all evidence types. Deduplicate patents by the declared unit and other evidence by stable identifier/canonical source logic. Preserve corroborating sources through shared event or finding relationships rather than deleting them blindly.

## 12. Organization normalization

Use stable IDs. Preserve source names and aliases. Distinguish parent, subsidiary, business unit, consortium, standards body, university, institute, and project organization. Do not merge on acronym alone or infer leadership from evidence volume.

## 13. Zero-result and failed-search states

Write:

- `No retained directly relevant record was found under search S4.`
- `Database X was unavailable; source class not searched.`
- `Full text was inaccessible; review depth limited to abstract.`

Do not write:

- `No prior work exists.`
- `The direction is novel.`
- `The platform returned no result` without query and failure details.

## 14. Quality gates before rendering

- Requirement facts and analyst hypotheses are separated.
- Every issue has source locations.
- Direction coverage and dependencies reconcile.
- Every task has evidence or an explicit hypothesis/uncertainty label.
- Search logs are reproducible.
- Evidence IDs are unique and references resolve.
- URLs are genuine or absent.
- Patent count unit and organization unit are disclosed.
- Summary counts derive from the registry.
- No domain-inappropriate MCP is claimed.
- Legal, safety, regulatory, and specialist boundaries are visible.
- The payload validates before output files are touched.
