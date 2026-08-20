---
copyright: "Copyright © Patsnap. All rights reserved."
name: identify-rd-directions-rd
description: Convert a concrete engineering, scientific, manufacturing, or technical project requirement into evidence-backed R&D directions, including requirement analysis, bounded technical issues, research questions, tasks, targets, deliverables, patent and literature evidence, standards and engineering cases, relevant organizations, search logs, and synchronized Markdown and HTML reports. Use when a user asks what R&D directions to pursue, how to decompose a project into research routes, or needs an evidence-led R&D direction report.
---

# Identify Evidence-Backed R&D Directions

## Role

Turn a concrete project requirement into a transparent set of research directions and validation plans. Begin with source-faithful requirement analysis, separate technical issues, formulate testable directions, retrieve and review relevant evidence when requested, and produce synchronized Markdown and HTML reports from one validated payload.

Do not treat a plausible route as proven. Do not provide a patentability, freedom-to-operate, infringement, validity, safety, regulatory, investment, or funding decision unless a qualified specialist supplies and owns that conclusion.

## Trigger and fit

Use this skill when the user:

- asks which R&D directions should be pursued for a defined problem;
- wants technical issues decomposed into research routes;
- supplies a project background, initiation brief, engineering need, or research requirement;
- needs patent, literature, standards, and engineering evidence attached to proposed directions;
- requests a structured R&D direction report for technical or management review.

Do not use it as the primary workflow for:

- reading one patent or paper;
- novelty, patentability, invalidity, or FTO analysis;
- a broad landscape with no concrete project requirement;
- an already approved direction that only needs a bibliography;
- a formal project go/no-go audit with organization-specific scoring;
- detailed experimental design or safety approval.

## Bundled authorities

Read and follow:

- `assets/workflow.md` for decomposition, evidence selection, query design, tool boundaries, and zero-result handling;
- `assets/payload-schema.md` before constructing the canonical JSON;
- `assets/report-template.md` before checking report completeness;
- `assets/paths.md` before naming or writing artifacts;
- `scripts/render_report.py --help` before rendering.

The payload schema controls fields and references. The report template controls section order. The path contract controls artifact names. The main skill controls the workflow and completion gates.

## Inputs

### Required

- `requirement_text`: a concrete technical, engineering, scientific, manufacturing, or system requirement with enough context to identify at least one issue.

### Recommended

- project and applicant/team names;
- decision to be supported;
- domain and system boundary;
- operating/use context;
- target geographies and jurisdictions;
- evidence cutoff and preferred time window;
- languages and source access;
- maximum number of directions for presentation;
- known constraints, baselines, data, targets, interfaces, standards, and risks;
- expected output directory;
- confidentiality and external-search authorization.

Do not impose a 100–400-character rule. If the source is too sparse to form a bounded issue, ask for the smallest missing information: context, baseline, observed limit, mechanism, target, or constraint.

## Deliverables

A complete run produces:

1. one reviewed canonical JSON payload;
2. one Markdown report generated from that payload;
3. one self-contained HTML report generated from that payload;
4. a concise user handoff with artifact paths, evidence cutoff, searched/unsearched sources, limitations, and specialist-review needs.

The conversation may summarize the result, but copied conversation Markdown is not an artifact authority. Markdown and HTML must be deterministic views of the same payload.

## Completion gates

Do not claim completion until:

- payload validation passes;
- every issue and direction reference resolves;
- every evidence and organization ID is unique;
- issue coverage is complete or explicitly limited;
- search counts and evidence counts reconcile;
- patent count unit is disclosed and consistently applied;
- payload, Markdown, and HTML files exist and are non-empty;
- Markdown and HTML contain every required report section;
- external links are valid or rendered as unavailable plain text;
- HTML parses and contains no external runtime dependency;
- existing files were not overwritten without explicit authorization;
- no cache, temporary package file, credential, or local user path was created.

If a gate fails, report the failed step, exact reason, remediation attempted, and reproducible command. Do not present partial artifacts as complete.

## Stage 0 — Freeze scope and evidence policy

Before analysis, record:

- project and decision context;
- system/technology boundary and exclusions;
- geographies, jurisdictions, languages, and source types;
- evidence cutoff and search dates;
- historical versus recent evidence needs;
- patent unit and family rule;
- organization identity unit;
- current baseline and target metrics;
- confidentiality and authorization for external queries;
- maximum directions as a presentation constraint;
- specialist domains required.

Do not default to recent three-year evidence, granted patents, a universal jurisdiction list, high citation counts, or a specific country. Older evidence may establish foundational constraints; applications may signal emerging work; standards and routes vary by decision.

## Stage 1 — Analyze the source requirement

Follow the three-part structure in `assets/workflow.md` and the schema.

### Demand and operating need

Extract:

- operating, scientific, manufacturing, environmental, clinical, or engineering context;
- stakeholder or system need;
- technical, safety, reliability, sustainability, throughput, quality, accessibility, or economic consequence;
- current response, workaround, or baseline.

Keep source facts separate from analyst interpretation. Do not require a catastrophic consequence for a requirement to be valid.

### Bottleneck

Extract:

- observed or specified performance limit;
- supporting source location or evidence;
- current-solution tradeoffs;
- physical, chemical, biological, algorithmic, manufacturing, integration, or system mechanism;
- missing evidence and assumptions.

Do not claim a physical ceiling unless evidence supports it.

### Solution hypothesis

Extract source-stated ideas. If a path is analyst-generated, label it `Analyst hypothesis requiring validation`. Record technical path, system concept, compatibility, target outcome, and decision criteria. A target is not an achieved result.

Use the exact missing-value phrase required by the schema when a source field is absent. Never invent a value to make the table appear complete.

## Stage 2 — Decompose technical issues

Create issue records `T1`, `T2`, and so on.

Each issue must:

- be traceable to source locations;
- name one bounded technical difficulty or uncertainty;
- distinguish symptom, root-cause evidence, and root-cause hypothesis;
- state dependencies and overlaps;
- avoid combining independent validation questions;
- avoid duplicate wording of another issue;
- carry extraction confidence.

The number of issues follows the source. Do not force a quota or manufacture mutual exclusivity where the system is coupled.

Run the issue-quality check:

- Is the issue technical rather than purely administrative or commercial?
- Is its boundary clear?
- Does it include the relevant condition or context?
- Is the source location present?
- Is it distinguishable from other issues?
- Are dependencies explicit?
- Is missing evidence visible?

## Stage 3 — Form candidate R&D directions

Create `D1`, `D2`, and so on. A direction may cover multiple coupled issues; one issue may have alternative directions.

For each direction specify:

- issue IDs addressed;
- evidence-linked rationale;
- testable core research question;
- research tasks;
- validation method per task;
- measurable success metric per task;
- task uncertainty;
- technical target and basis;
- expected deliverables;
- supporting evidence IDs;
- evidence gap;
- confidence;
- transparent priority basis.

Do not mechanically set the number of directions to `min(number of issues, max_directions)`. Use the maximum only to consolidate presentation while preserving alternative routes and full issue coverage.

### Direction-separation test

Split directions when they require materially different:

- mechanisms;
- materials or architectures;
- experimental programs;
- technical disciplines;
- validation facilities;
- standards or regulatory paths;
- deployment constraints;
- decision gates.

Merge only when the same research program and evidence logically address the issues together. Preserve sub-route alternatives in tasks or deliverables.

## Stage 4 — Prepare research packets

For every direction create separate packets for:

- patents;
- scientific/technical literature;
- standards and engineering cases;
- authoritative web evidence.

Each packet records:

- direction and issue IDs;
- problem context and mechanism;
- differentiating concepts;
- synonyms, acronyms, historical terms, translations, and classifications;
- materials, structures, functions, processes, parameters, effects, and applications;
- exclusions and common false positives;
- target dates, jurisdictions, languages, and source types;
- confidentiality-minimized wording;
- inclusion and review criteria.

Do not combine unrelated directions into one query.

## Stage 5 — Search patents with verified Patsnap MCP

Only search when the user requests research or the report scope includes evidence retrieval.

Use, when exposed:

- `advanced_patent_search` — [Patsnap Advanced Patent Search](https://open.patsnap.com/marketplace/mcp-servers/patent-search);
- `patent_briefing` — [Patsnap Patent Briefing](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing) for selected record/family details.

Use the current callable schema and English interface. Do not copy legacy domestic tool names from the source package.

Choose semantic, keyword, classification, nested, assignee, citation, similarity, patent-number, or field search according to the packet. Do not fix top-k, recent-year, status, or jurisdiction rules universally.

Record one search-log entry per direction and strategy, including:

- exact source/tool;
- timestamp and cutoff;
- query and filters;
- requested and returned counts;
- pagination or truncation;
- reviewed and retained evidence IDs;
- family/deduplication rule;
- language and jurisdiction coverage;
- false positives and limitations.

Use Patent Briefing only when record details materially affect the technical interpretation. State review depth: bibliographic, abstract, specification, or claims. Do not infer legal conclusions.

## Stage 6 — Search literature

For engineering and general science, use user-accessible primary publisher/repository records, DOI/Crossref metadata, recognized bibliographic databases, standards databases, or user-supplied literature.

Do not map general engineering paper search to Patsnap `scientific_translational_evidence`; its verified public tools concern translational medicine. Use it only for a biomedical/translational request that matches its current tool scope.

For each search record exact query, database, coverage, filters, limit, returned results, reviewed records, access restrictions, and cutoff.

Select evidence by relevance, authority, directness, method, applicability, independence, and coverage. Recency and citation count may inform review but are not quality or truth scores.

Capture:

- title, authors, affiliations, venue, DOI, URL, date, and publication type;
- peer-review status where established;
- citation count only with source and date;
- method and relevant result;
- relevance, review depth, and confidence;
- direction and organization links.

## Stage 7 — Search standards and engineering cases

Prefer primary standards bodies, regulators, government laboratories, project owners, official technical reports, and peer-reviewed cases.

Capture:

- document/project identifier;
- issuing/publishing organization;
- version, status, or stage;
- publication/event date and access date;
- system, location, scale, and operating context;
- direct URL where available;
- evidence summary and relevance;
- direction and organization links;
- review depth and confidence.

Do not label a promotional page as an independently verified engineering case. Do not treat a search snippet as a standard.

## Stage 8 — Add authoritative web evidence

Use web evidence only when the page is the primary source or a needed structured source is unavailable. Favor government, standards, university, research-institute, repository, and first-party organization pages.

The source package's China-specific platform list and hard-coded breaker queries are examples, not portable workflow requirements. Form domain-specific English or multilingual queries and document site restrictions.

Do not use `current_awareness` as a generic engineering-news MCP: its verified public scope is pharmaceutical news.

Capture publisher type, category, title, date, URL, summary, relevance, review status, confidence, and limitations.

## Stage 9 — Normalize and select evidence

Use one global evidence namespace: `E1`, `E2`, and so on, across patents, papers, standards, engineering cases, and authoritative web sources.

This intentionally resolves the source conflict in which A1 cases/standards were sometimes outside `[S#]` and elsewhere required to carry `[S#]`.

For every evidence record:

- preserve source identity and direct URL;
- normalize unambiguous dates;
- retain source language;
- link organizations and directions by stable IDs;
- state evidence type and subtype fields;
- distinguish source summary from relevance interpretation;
- record review depth, status, confidence, and access date;
- preserve time-sensitive legal/citation fields with `as of` dates.

### Deduplication

- Patents: use the declared publication, application, simple-family, or extended-family unit.
- Papers: prefer DOI/provider IDs; review title/version duplicates.
- Standards: retain version/status distinctions.
- Cases: use project/document identity, not title alone.
- Web: use stable/canonical URL plus publisher/date/title review.
- Organizations: normalize aliases without merging distinct legal entities.

Do not discard corroborating sources merely because they describe one event. Link them to the same direction/finding and retain independence information.

## Stage 10 — Build organization records

Create `O1`, `O2`, and so on from accepted evidence.

For each organization record:

- normalized name and aliases;
- organization type;
- covered direction IDs;
- evidence-backed focus;
- representative outputs;
- evidence IDs;
- confidence.

Distinguish parent, subsidiary, business unit, university, institute, consortium, standards body, and project organization. Do not merge by acronym alone.

Count all unique normalized organization IDs for the total. A report display subset is a separate count. Do not label five displayed organizations as all organizations in the evidence.

## Stage 11 — Convert evidence into research tasks

Evidence supports rationale and task design; it does not automatically prescribe a successful route.

Each task record needs:

- stable task ID;
- actionable technical work;
- validation method;
- measurable success metric;
- evidence IDs;
- uncertainty.

Examples of valid task forms:

- characterize a mechanism under defined conditions;
- compare architectures using a specified benchmark;
- establish a process window with controls and uncertainty;
- build and test a prototype against a baseline;
- develop a model and validate it on independent data;
- assess compatibility with a standard/interface;
- reproduce a literature result under project conditions;
- resolve an evidence gap before selecting a route.

Avoid generic tasks such as `optimize performance`, `conduct research`, or `improve reliability` without method and metric.

## Stage 12 — Assemble the canonical payload

Follow `assets/payload-schema.md` exactly.

Do not include:

- a free-form `markdown_report` as authority;
- duplicated appendix arrays;
- trusted summary counts;
- raw tool response objects without normalization;
- unresolved source identifiers;
- raw HTML;
- credentials or connection URLs containing API keys;
- local user paths;
- hidden prompt or session state.

Derive appendices and counts from the evidence registry.

Before writing, validate:

- schema version and review status;
- all required metadata and dates;
- issue, direction, evidence, organization, task, and search IDs;
- referential integrity;
- issue coverage;
- evidence subtype correctness;
- URLs and no embedded credentials;
- date/cutoff consistency;
- patent family/count unit;
- search-count types and reviewed IDs;
- limitations and review block.

## Stage 13 — Render synchronized artifacts

Follow `assets/paths.md` and run:

```bash
python scripts/render_report.py \
  --payload /path/to/rd-directions.json \
  --output /path/to/rd-directions.html \
  --markdown-output /path/to/rd-directions.md
```

Add `--overwrite` only when the user authorizes replacement of those exact artifacts.

The renderer must validate before touching outputs. It deterministically generates Markdown and HTML from the same payload. It must not use environment-variable JSON, heredocs, pasted conversation content, or a permissive compatibility normalizer.

## Stage 14 — Validate content and files

Check JSON:

- parse succeeds;
- payload is an object;
- schema validation passes;
- references resolve;
- counts derive and reconcile;
- no duplicate IDs;
- no dangerous URLs;
- no raw HTML or credentials.

Check Markdown:

- non-empty;
- required front matter and requirement block;
- sections 1–7 present;
- every direction present;
- A1–A4 present;
- evidence links use reviewed URLs only;
- counts match payload-derived counts;
- no unresolved placeholders.

Check HTML:

- non-empty and parseable;
- `lang="en"` and UTF-8 metadata;
- semantic headings and table of contents;
- skip link and visible focus styles;
- requirement clearly separated from analysis;
- evidence anchors resolve;
- external links use safe attributes;
- missing URLs are plain text;
- no external CSS, font, script, image, or runtime request;
- no gradients, emoji navigation, domestic fonts, raw unsafe HTML, analytics, or storage;
- responsive and print rules present;
- source register and limitations visible.

Check filesystem:

- requested suffixes and resolved paths;
- no filesystem root or symlink target;
- existing files unchanged without `--overwrite`;
- only named artifacts written;
- no package cache or temporary file.

## Evidence interpretation rules

### Patents

Patent hits and counts do not establish novelty, inventive step, patentability, infringement, validity, freedom to operate, commercial use, product mapping, technical leadership, or route success.

### Papers

A published result may not reproduce under the project's material, scale, environment, system, or data. Record method, context, and applicability limits.

### Standards

Distinguish current, draft, withdrawn, superseded, and locally adopted versions. A standard requirement is not proof that a proposed method satisfies it.

### Engineering cases

Distinguish reported, operating, independently verified, pilot, demonstration, planned, and promotional claims. Record scale and conditions.

### Web evidence

Use first-party statements for what the party announced, not as independent proof of performance.

### Organizations

Evidence volume is not technical capability, leadership, independence, or commercial readiness.

## Zero-result and failure behavior

When a direction has no retained patent record, state the search ID and limitations. Do not infer novelty.

When literature access is blocked, state database, query, accessible metadata, and review depth. Do not invent an abstract or finding.

When a standards source is unavailable, state the unavailable source and version uncertainty. Do not substitute a blog as a standard.

When a tool fails, preserve the failure in the search log, use an authorized alternative if available, and disclose coverage loss.

When the requirement is insufficient, stop evidence search for the affected issue and ask focused questions rather than producing generic routes.

When rendering fails, preserve the validated payload and do not claim the Markdown/HTML deliverable is complete. Report the reproducible command and error.

## Quality checklist — requirement fidelity

- [ ] Requirement text is authorized and traceable.
- [ ] Optional metadata rows are omitted when absent.
- [ ] Every required analysis subfield is populated or uses the exact missing-value phrase.
- [ ] Source statements and analyst hypotheses are distinguishable.
- [ ] Targets are not represented as results.
- [ ] Units, conditions, baselines, and source locations are retained.
- [ ] Confidential or personal information is handled for the intended audience.

## Quality checklist — issues and directions

- [ ] Issue IDs are unique and ordered.
- [ ] Each issue is technically bounded.
- [ ] Dependencies and overlaps are recorded.
- [ ] Every issue is covered or explicitly limited.
- [ ] Direction IDs are unique.
- [ ] Direction count is analytically justified.
- [ ] Alternatives are not hidden by forced consolidation.
- [ ] Every direction has rationale and a testable core question.
- [ ] Every task has method, metric, evidence or hypothesis label, and uncertainty.
- [ ] Targets and deliverables are concrete and evidence-aware.
- [ ] Confidence and priority bases are explained.

## Quality checklist — research evidence

- [ ] Each direction has separate search packets.
- [ ] Search logs contain exact tools/sources, queries, filters, and timestamps.
- [ ] Requested, returned, reviewed, retained, and deduplicated counts remain distinct.
- [ ] Patent unit and family rule are disclosed.
- [ ] Literature selection does not rely only on recency or citation count.
- [ ] Standards/cases use primary or clearly characterized sources.
- [ ] Web evidence is authoritative for the claim it supports.
- [ ] All evidence uses one unique E# namespace.
- [ ] Source URLs are genuine or absent.
- [ ] Review depth, status, confidence, and cutoff are present.
- [ ] Zero results and tool failures are disclosed.
- [ ] No domain-inappropriate MCP is claimed.

## Quality checklist — organizations and counts

- [ ] Organization IDs and normalized names are unique.
- [ ] Parent/subsidiary/business-unit distinctions are preserved.
- [ ] Every organization claim cites evidence.
- [ ] Unique total and displayed subset counts are separate.
- [ ] Evidence totals derive from the registry.
- [ ] Direction counts derive from linked evidence.
- [ ] A1–A4 rows equal evidence-type partitions.
- [ ] Patent aggregate count follows the declared unit.
- [ ] Search-log counts are not presented as retained evidence counts.

## Quality checklist — artifacts

- [ ] Payload validation finishes before writes.
- [ ] JSON, Markdown, and HTML paths follow the path contract.
- [ ] Existing artifacts require explicit overwrite.
- [ ] Markdown and HTML are generated from the same payload.
- [ ] Every required report section appears.
- [ ] Evidence references resolve to the source register.
- [ ] HTML text and attributes are escaped.
- [ ] URLs are allowlisted.
- [ ] HTML has no external runtime dependencies.
- [ ] Desktop, narrow-screen, and print behavior are reviewed.
- [ ] No cache, temp, credential, or local absolute path remains in the package.

## User handoff

### Review ownership

- The analyst owns source traceability, query logging, normalization, and uncertainty disclosure.
- The technical reviewer owns issue decomposition, direction logic, research-task feasibility, and metric interpretation.
- A patent specialist reviews claim-scope or legal-status conclusions when those conclusions affect a decision.
- A domain specialist reviews safety, regulatory, clinical, or standards implications beyond the analyst's competence.
- The final approver confirms that the report supports the named decision context without overstating accepted evidence.

Lead with the outcome and provide:

- payload path;
- Markdown path;
- HTML path;
- number of issues and directions;
- evidence counts by type and patent count unit;
- evidence cutoff;
- searches not run or incomplete;
- important evidence gaps;
- specialist review required;
- whether artifacts replaced existing files.

Do not paste a large duplicate Markdown report into the handoff when the user asked for files, unless they explicitly request the full report in conversation. The artifacts remain complete regardless of handoff brevity.
