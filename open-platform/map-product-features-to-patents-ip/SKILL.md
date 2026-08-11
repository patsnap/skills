---
name: map-product-features-to-patents-ip
description: Research a product feature from current public sources, decompose it into stable technical dimensions, retrieve and review related patents, map each patent’s disclosed technical evidence to those dimensions, rank relevance under a transparent rubric, and generate a self-contained interactive HTML report. Use when a user asks which patents relate to a product feature, wants a product-feature-to-patent map, or needs patent results filtered by technical dimension.
---

# Map Product Features to Patents

## Purpose

Convert a natural-language product-feature description into:

1. a cited public-evidence summary of the feature;
2. a stable T1–TN technical decomposition;
3. a deduplicated set of related patent records;
4. evidence-backed record-to-dimension mappings and relevance priorities; and
5. one self-contained HTML report with an accessible dimension filter.

This workflow identifies technical correspondence in patent disclosures. It does not
establish that a product implements a patent, that a claim covers a product, that an
organization owns a feature, or that infringement, validity, or freedom to operate
exists.

## Inputs

Required:

- `product_feature`: natural-language description of the product capability, behavior,
  component, architecture, process, or user-visible feature.

Optional:

- `product_name`, `model`, `version`, and release period;
- `manufacturer` or responsible organization;
- `assignee_or_owner_filter`;
- `jurisdictions`;
- `filing_date_from` and `filing_date_to` in ISO form;
- `priority_or_publication_date_scope` where relevant;
- `language_scope`;
- `display_limit` or review budget;
- `family_deduplication` method;
- `research_question` and audience; and
- confidentiality and web/MCP data-sharing boundary.

Do not apply a filter merely because the source default used one. Confirm what the
user means by assignee, jurisdiction, and date. If the product/model or technical
feature is materially ambiguous, clarify before live research.

## Verified PatSnap MCP services

Inspect the installed live schema before calling an operation. Record connector key,
operation, material request parameters, date, record IDs, and limitations.

### Advanced Patent Search — required

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use for fielded keyword, concept/semantic-capable, classification, organization,
  jurisdiction, and date retrieval where exposed by the active contract.

### Patent Briefing — required for selected records

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use for selected-record bibliography, family, legal-status context, claims,
  descriptions, translations, images, and verified record URLs where returned.

### Deep Patent Mining — recommended

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use for technical problem, means, effect, component, material, process, and
  application extraction when supported.

### Global Core Patent Database — optional

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Use for deeper family, status/event, citation, and full-text evidence where needed.

Do not use generic source-era patent-tool names or construct a patent URL from an
undocumented template. If no verified global record link is returned, display the
identifier and source without a fabricated hyperlink.

## Step 1 — Research and decompose the product feature

### 1A. Resolve the product context

Identify:

- exact product/model/version and geography;
- feature name and synonymous marketing/technical terms;
- release or documentation dates;
- user-visible behavior;
- known architecture, components, interfaces, inputs, outputs, and constraints; and
- which details are publicly documented versus inferred or unknown.

Do not merge different product generations or regional variants without disclosure.

### 1B. Research current public evidence

When web research is authorized, prioritize:

1. official product documentation and technical specifications;
2. regulatory filings, standards, and certification materials;
3. official developer, engineering, or safety documentation;
4. peer-reviewed/technical publications and credible teardowns; and
5. reputable secondary reporting for context.

For every material source record title, publisher, URL, publication/update date,
access date, relevant passage/topic, and evidence state.

Use evidence states:

- `Official product statement`;
- `Independent technical evidence`;
- `Secondary report`;
- `Analytical inference`; and
- `Unknown or conflicting`.

Manufacturer marketing claims are not proof of internal implementation or performance.
Current sources must be verified at execution time.

### 1C. Handle product images

Embed an image only when:

- the source and license/permission permit the intended use;
- the image is genuinely relevant;
- a stable safe URL or authorized local asset is available; and
- attribution, caption, and alt text are provided.

Otherwise provide a source-page link or state “No embeddable product image verified.”
Do not use random stock imagery or a fake product placeholder.

### 1D. Create T1–TN technical dimensions

Create the number of dimensions justified by the feature. Possible axes include:

- sensing/input;
- signal conditioning and feature extraction;
- inference/recognition/control;
- data fusion and state estimation;
- system architecture and communications;
- mechanical, optical, electrical, or material implementation;
- interface/interaction and feedback;
- safety, calibration, reliability, privacy, and resource constraints; and
- product/application integration.

Each dimension contains:

| Field | Requirement |
|---|---|
| `dimension_id` | Stable `T1`, `T2`, … identifier |
| `name` | Clear international English technical label |
| `definition` | One-to-three sentences with system boundary |
| `include` | Positive mechanisms/features |
| `exclude` | Nearby concepts that should not map |
| `evidence` | Product-source IDs and evidence state |
| `search_concepts` | Terms, synonyms, classifications, and relations |
| `overlap_policy` | Whether cross-dimension mapping is legitimate |
| `uncertainty` | Hidden implementation or source gaps |

Primary dimensions should be discriminative, but technical layers can overlap. Do not
force mutual exclusivity or claim that public sources fully describe a proprietary
implementation.

## Step 2 — Retrieve, review, and map patents

### 2A. Build complementary search strategies

For each dimension and for the integrated feature, construct:

1. fielded keyword branches;
2. concept/semantic-capable branches if the live schema supports them;
3. classification-assisted branches derived from verified seed patents and official
   IPC/CPC definitions;
4. functional/problem-effect branches; and
5. optional assignee, jurisdiction, or date filters requested by the user.

Record exact query/request, connector operation, filters, query version, raw count,
retrieval cap, screening sample, and limitations. Search multiple relevant languages
and transliterations when needed.

Do not call a Top-K result set comprehensive. A display limit controls workload and
presentation, not the search universe.

### 2B. Merge and deduplicate

- Preserve every query/dimension hit.
- Resolve publication, application, grant, and family identifiers.
- Deduplicate under a declared family method for display when appropriate.
- Keep jurisdiction-specific rights separate for legal/status context.
- Choose a representative publication by a stated rule.
- Reconcile result and selected-record counts.

### 2C. Retrieve evidence for selected records

For every displayed record obtain, where available:

- publication identifier and verified link;
- title;
- original and normalized applicant/assignee;
- publication, filing, and priority dates kept distinct;
- jurisdiction;
- dated legal-status signal;
- abstract;
- relevant claim/description passages for ambiguous or high-priority mappings;
- family/provenance; and
- translation state.

Missing data remain unavailable. Do not infer current ownership from applicant alone
or treat a database status as an enforceability conclusion.

### 2D. Apply a transparent relevance rubric

Score or prioritize only after defining the rubric. Recommended dimensions:

| Dimension | Question |
|---|---|
| Technical-means correspondence | Does the record disclose a materially similar mechanism, architecture, component, process, or relation? |
| Feature/function correspondence | Does the disclosure address the relevant behavior or function? |
| Product/application context | Is the operating context comparable or merely adjacent? |
| Evidence depth | Title only, abstract, claim-assisted, or description-reviewed? |
| Dimension coverage | Which defined dimensions have direct evidence? |
| Uncertainty/noise | Are terms broad, translated, ambiguous, or only background? |

If a numeric scale is useful, disclose anchors, weights, missing-data treatment, and
sensitivity. The source’s 0–10 bands may be adapted, but do not imply false precision.
Prefer controlled priorities such as `high technical correspondence`, `relevant`,
`partial/adjacent`, `weak`, and `excluded`, each with evidence and uncertainty.

Relevance is not legal claim coverage, patent quality, commercial implementation, or
infringement risk.

### 2E. Map technical dimensions

For each record/dimension:

1. compare the dimension definition and inclusion/exclusion boundary;
2. cite abstract, claim, or description evidence;
3. assign one state:
   - `directly disclosed`;
   - `partially disclosed`;
   - `context only`;
   - `not observed`; or
   - `unknown`;
4. map `tech_dimensions` only for direct/qualified partial disclosure under the
   report’s declared rule; and
5. preserve evidence ID, field/passage, translation state, and reviewer depth.

A record may map to multiple T dimensions when each mapping has evidence. Do not map a
dimension because the patent is merely in the same broad field. A low-ranked/noise
record need not receive a dimension, but its exclusion reason should remain auditable.

### 2F. Write the relevance explanation

Use one to three concise sentences:

```text
The record discloses [technical means] in [context], corresponding to T2 and T4 based
on [abstract/claim/description evidence]. It differs from the documented product
feature in [material boundary]; product implementation and claim coverage are unknown.
```

Do not repeat a score without explaining the technical relationship.

## Step 3 — Generate the HTML report

### Report structure

```text
Header: title, product/model, decision question, generated date, patent-data cutoff
Scope and limitations
Part 1 — Product-feature evidence
  Original user description
  Public-evidence summary
  T1–TN technical dimensions and definitions
  Product image or source/unavailable state
Part 2 — Related patent evidence
  Search and selection method
  Accessible dimension filter and result count
  Records ordered by transparent relevance priority
  Identifier/link, title, entity, status/date, priority, T mappings, explanation, evidence
Sources and evidence register
Method, uncertainty, and legal boundary
```

### Patent links

- Use a link only when returned by the active connector or documented by a current
  official global source.
- Preserve exact identifier text.
- Validate `https` scheme and host.
- Add `rel="noopener noreferrer"` to new-tab links.
- If no verified link exists, show identifier, connector/operation, and evidence ID.

### Dimension filter

Provide an “All dimensions” control and one control per T dimension.

- Buttons must be real `<button>` elements with visible focus and ARIA pressed state.
- Clicking a dimension filters or highlights records mapped under the declared rule.
- Clicking the active dimension again or “All dimensions” restores all records.
- Update a live result-count/status message.
- Keep every record visible and readable when JavaScript is disabled.
- Do not rely on color alone; show T IDs and names.
- Preserve stable dimension-color mapping across cards, buttons, and records.

Use an accessible categorical palette sized to the actual dimensions. When categories
exceed distinguishable colors, reuse hue only with additional labels/patterns; do not
cycle colors without a non-color cue.

### Scientific/executive styling

- Use semantic HTML and system fonts.
- Use a white/neutral canvas, navy/slate hierarchy, restrained teal emphasis, and
  accessible category colors.
- Prefer tables or flat evidence cards, whitespace, and rules over nested cards.
- Avoid gradients, stock imagery, decorative hero sections, 3D charts, and vendor UI.
- Use responsive grids and horizontal overflow for wide evidence tables.
- Include print/PDF styles and meaningful page breaks.

### Security and self-containment

- Embed CSS and minimal filter JavaScript in the single file.
- Load no external JavaScript framework, CDN, font, tracker, iframe, or remote data.
- Escape all user, web, and patent text.
- Never inject retrieved HTML or JSON as executable code.
- Validate image and source URLs; do not embed untrusted active formats.
- Do not expose API keys, raw connector payloads, confidential input, or local paths.

Use the active environment’s approved file-editing/writing workflow. For a large file,
write in validated bounded operations as needed; do not depend on source-specific
writer operation names or arbitrary character limits.

## Evidence and legal language

Use:

- “public product documentation states…”;
- “the patent disclosure describes…”;
- “technical correspondence to T3 under the defined mapping rule”;
- “database status signal as of [date]”; and
- “product implementation and claim coverage require additional evidence/review.”

Avoid:

- “this is the patent behind the feature”;
- “the product uses this patent”;
- “the patent covers the product”;
- “the assignee owns the product feature”;
- “infringing/non-infringing”; and
- “free to operate.”

## Quality gate

### Product research

- Product/model/version and feature boundary are explicit.
- Every material product fact has a current cited source and evidence state.
- Marketing claims, independent evidence, inference, and unknowns are distinct.
- Image source/license/alt text passes or an unavailable state is shown.

### Technical dimensions

- T IDs are stable and definitions include inclusion/exclusion boundaries.
- Overlap and cross-cutting behavior are explicit.
- Dimensions map to product evidence and search concepts.
- No hidden implementation is invented.

### Patent search and mapping

- Queries, filters, versions, caps, dates, and family method are reproducible.
- Display limit is not described as completeness.
- Every displayed patent identity/status/date/link is source-backed and dated.
- Every T mapping cites abstract/claim/description evidence.
- Relevance rubric, evidence depth, uncertainty, and exclusions are visible.
- No mapping is represented as claim coverage, implementation, or FTO.

### HTML

- One self-contained file opens locally with no remote dependency.
- Semantic headings, controls, tables/cards, focus, ARIA state, and no-JS view work.
- Filter state and counts are correct for every dimension.
- T labels remain understandable without color.
- Layout works on desktop, mobile, print, and grayscale.
- Content/URLs are escaped and safe; no broken/fabricated link or image remains.

## Stop conditions

Stop or narrow when:

- product identity or feature scope cannot be resolved;
- current credible product evidence is unavailable or contradictory;
- image rights/source cannot be verified;
- the global patent connector or required field/operation is unavailable;
- retrieval caps prevent the requested completeness claim;
- patent text is insufficient to map a dimension;
- confidentiality rules prevent necessary research;
- a global record link cannot be verified;
- HTML validation fails; or
- the user requests a legal coverage/infringement/FTO conclusion from this workflow.

Return completed research, missing evidence, affected mappings, residual uncertainty,
and the exact next action. Do not fill gaps with plausible product or patent claims.

