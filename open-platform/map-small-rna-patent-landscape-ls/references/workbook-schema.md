# Small-RNA Patent Landscape Workbook Schema

## Purpose

Create an XLSX workbook that serves both as an analyst evidence file and a stakeholder-facing appendix. Derive it from the same structured JSON/CSV layer used by the HTML timeline.

## Full workbook

Use these English sheet names unless the user requests localized labels:

1. `Strategy Summary`
2. `Priority Patent Evidence`
3. `Portfolio Gap Matrix`
4. `R&D Hypothesis Cards`
5. `Peer Filing Playbooks`
6. `Patent Strategy Master`
7. `Timeline Tag Data`
8. `Methodology`

## Light first-pass workbook

When explicitly scoped as a lighter deliverable:

1. `Patent Analysis`
2. `Tag Summary`
3. `Timeline Data`
4. `Roadmap View`
5. `Methodology`

Do not omit methodology, sources, missing-data status, or counting rules.

## Common controls

Every analytical sheet should include or inherit:

- matter/project ID;
- company/portfolio and entity-normalization date;
- analysis cutoff and generation time;
- patent/family counting unit and family definition/provider;
- target jurisdictions/languages;
- candidate/technology scope;
- source/database cutoffs;
- reviewer and release status.

Use Excel tables, filters, frozen panes, wrapped text, stable date formats, explicit units, and source hyperlinks. Avoid decorative merged-cell layouts.

## `Patent Strategy Master`

One row per selected analytical unit, normally a family with nested/member detail represented in columns or linked evidence sheets. If one row per publication is used, state it.

### Input and identity

| Column | Requirement |
|---|---|
| Input Order | Preserve the user's sequence |
| Original Input | Exact supplied identifier |
| Resolution Status | matched / ambiguous / not found / invalid / pending review |
| Resolution Attempts | Structured or concise log; do not silently append kind codes |
| Matched Publication | Exact country-number-kind code |
| Application Number | Where available |
| Grant Number | Where available |
| Stable Source URL | Exact returned/official URL |
| Record Markdown | Relative local path |
| Retrieval Date | ISO date/time |

### Bibliography and family

| Column | Requirement |
|---|---|
| Title | Original or labeled translation |
| Original Language | ISO language code |
| Applicants | Names as published |
| Normalized Applicants | Verified English legal names |
| Assignees | Current/original distinction where available |
| Inventors | Source-backed |
| Priority Date | Earliest claimed priority with source |
| Filing Date | Current member |
| Publication Date | Current member |
| Grant Date | Current member, if any |
| Family Definition | Simple/INPADOC/custom etc. |
| Family ID | Provider/control identifier |
| Earliest Family Publication | Verified date |
| Family Member Count | Under stated definition |
| Family Members | Exact identifiers or linked child sheet |
| Jurisdictions | Codes and optional full names |
| Continuity Notes | Continuations/divisionals/national stages/EP states |

### Text and legal status

| Column | Requirement |
|---|---|
| Abstract | Original or labeled translation |
| Current Claims | Exact member/version or controlled local reference |
| Claims Source | current member / alternate family member / missing |
| Claims Substitution Note | Required if alternate text is shown |
| Current Member Status | Normalized plus raw event/source |
| Status Effective Date | If available |
| Status Verification | official / database-only / conflicting / missing |
| Family Status Summary | Member-level granted/pending/inactive/unknown counts |
| Estimated Term | Clearly labeled estimate |
| Term/Extension Notes | Maintenance, PTA/PTE/SPC, disclaimers, etc. |

### Patent and technical classification

| Column | Requirement |
|---|---|
| Patent/Claim Type | Controlled tag(s) |
| Stakeholder Technology Direction | Default timeline lane |
| Expert Primary Subdivision | Target/disease/platform detail |
| Mechanism Tags | Semicolon-separated controlled IDs/names |
| RNA Modality Tags | Controlled multi-label |
| Chemistry/Structure Tags | Controlled multi-label |
| Delivery/Tissue Tags | Controlled multi-label |
| Disease/Tissue Area | Separate from delivery |
| Productization Stage Tags | Portfolio layer, not clinical phase |
| CPC/IPC | Codes plus scheme caveat |
| Tag Evidence | Source IDs/locators |
| Tag Confidence | high / medium / low |
| Tag Review Status | reviewed / provisional / rejected |

### Strategic evidence

| Column | Requirement |
|---|---|
| Review Priority | Priority review / Material / Context / Low current relevance |
| Priority Rationale | Claim/status/technical evidence and uncertainty |
| Key Finding | Why the record matters under defined scope |
| Claim Evidence Strength | strong / moderate / weak / missing |
| Claim Evidence Basis | Claim/version/locator |
| Family/Territory Evidence | strong / moderate / weak / conflicting |
| Family Evidence Basis | Definition, countries, branches, sources |
| Status Evidence | verified / database-only / conflicting / missing |
| Status Evidence Basis | Official/database source/date |
| Portfolio Layer | Foundational platform / core asset / extension / defensive etc. |
| Design-Around Assessment | not assessed / preliminary / counsel review required |
| Design-Around Basis | Claim-limitation and technical caveats |
| Project Relevance | high / medium / low / unresolved |
| Project Relevance Basis | Defined project overlap, not generic competition |
| Reusable Filing Insight | Evidence-based learning |
| Differentiation Hypothesis | Testable opportunity, not a conclusion |
| Recommended Action | Search/review/R&D/IP/monitoring action |
| Action Owner | Role/team |
| Timing/Trigger | Actual decision-based date or event |
| Known Gaps | Missing source/data/analysis |

## `Tag Summary`

One row per tag/dimension:

| Column | Notes |
|---|---|
| Dimension | Controlled dimension |
| Tag ID | Stable ID |
| Display Name | English/localized label |
| Meaning | Definition |
| Analytical Unit | publication/family |
| Assignment Count | Patent-tag relationships |
| Unique Patent/Family Count | Deduplicated count |
| Priority Review Count | Count under defined priority |
| Average Family Count | With missing-data handling |
| Earliest Year | Verified timeline basis |
| Latest Complete Year | Exclude/flag partial current year |
| Recent Period Count | Period boundaries shown |
| Trend | Controlled trend label |
| Trend Basis | Counts/period/small-number caveat |
| Evidence Coverage | reviewed/provisional/missing |

Trend labels:

- Sustained growth;
- Recent acceleration;
- Recently active;
- Historically concentrated;
- Declining in observed data;
- Isolated filing;
- Episodic/unclear;
- Insufficient observation window.

## `Timeline Tag Data`

Use one row per patent/family–tag relationship:

| Column | Requirement |
|---|---|
| Dimension | Active dimension name |
| Tag ID | Controlled tag |
| Tag Display Name | Stakeholder label |
| Analytical Record ID | Stable ID |
| Publication/Family ID | Display identifier |
| Timeline Year | Earliest verified family publication or declared fallback |
| Timeline Date Source | Source/field |
| Review Priority | Text category and optional level |
| Family Count | Null when unavailable |
| Jurisdictions | Codes |
| Title | Source title |
| Entity | Normalized applicant/assignee |
| Source IDs | Evidence links |
| Confidence | Tag confidence |

This sheet is the direct HTML data contract. Do not manually recode HTML tags separately.

## `Strategy Summary`

One row per strategy finding:

| Column | Notes |
|---|---|
| Finding ID | Stable link across workbook/HTML |
| Strategy Type | Portfolio gap / R&D hypothesis / filing playbook |
| Finding | Executive conclusion |
| Evidence | Patent/family/tag/source IDs |
| Counterevidence | Contradiction or limitation |
| Recommended Action | Concrete next step |
| Priority | high / medium / low |
| Owner | Role/team |
| Timing/Trigger | Date/event-based |
| Confidence | high / medium / low |
| Review Status | draft / reviewed / accepted / rejected |

## `Priority Patent Evidence`

Make the reasoning trace visible:

- Review Priority;
- Publication/Family ID;
- Title;
- Stakeholder Technology Direction;
- Expert Subdivision;
- Key Finding;
- Claim Evidence Strength and Basis;
- Family/Territory Evidence and Basis;
- Status Evidence and Basis;
- Portfolio Layer;
- Design-Around Assessment and Basis;
- Project Relevance and Basis;
- Reusable Filing Insight;
- Differentiation Hypothesis;
- Recommended Action;
- Sources, gaps, reviewer/date.

## `Portfolio Gap Matrix`

Rows should cover evidence-relevant dimensions such as:

- disease/indication/target;
- mechanism;
- modality;
- chemistry/structure;
- conjugate/delivery/tissue/route;
- formulation/stability/dose;
- manufacturing/analytics;
- patient selection/diagnostics;
- productization;
- geography/family/prosecution.

Columns:

| Column | Requirement |
|---|---|
| Gap ID | Stable ID |
| Dimension | Controlled dimension |
| Observed Portfolio Coverage | Evidence-based |
| Coverage Strength | strong / moderate / weak / unknown |
| Comparator | Peer/source if used |
| Gap Statement | Precise and bounded |
| Business/Technical Relevance | Why it matters |
| Risk/Opportunity | Separate observed fact from inference |
| Recommended Validation | Search/experiment/counsel review |
| Potential Filing Theme | Hypothesis only |
| Evidence | Source IDs |
| Counterevidence | If any |
| Confidence | high / medium / low |
| Owner/Timing | Actionable |

Do not prepopulate source-case CNS, ophthalmic, renal, NMD, exon, formulation, or patient-selection gaps unless the portfolio supports them.

## `R&D Hypothesis Cards`

| Column | Requirement |
|---|---|
| Hypothesis ID | Stable ID |
| Direction | Technical idea |
| Observed Evidence | Portfolio/scientific evidence |
| Hypothesis | Falsifiable statement |
| Proposed Experiment | Model, control, endpoint, success/failure criterion |
| Potential Patent Theme | Subject to novelty/FTO review |
| Technical Risks | Safety, efficacy, delivery, chemistry, manufacturing etc. |
| Search Needed | Patent/literature/competitor search |
| Priority | high / medium / low |
| Owner/Timing | Role and trigger |
| Confidence | Evidence-based |

## `Peer Filing Playbooks`

Possible playbook categories:

- core sequence-family protection;
- chemistry/backbone/conjugate layering;
- delivery/formulation extension;
- manufacturing/analytical protection;
- patient-selection/clinical-use layering;
- continuation/divisional/geographic strategy;
- platform-to-new-target transfer.

Columns:

- Playbook ID;
- Playbook;
- Peer Practice and Source;
- Current Portfolio Evidence;
- Difference/Gap;
- Applicability Conditions;
- Proposed Action;
- Legal/technical caveat;
- Confidence;
- Owner/Timing.

Do not recommend copying a competitor's claimed implementation. The comparison informs filing architecture and research questions, subject to independent novelty/FTO analysis.

## `Methodology`

Document:

- objective, scope, cutoff, jurisdictions, languages;
- source files, MCPs/tools, exact marketplace mappings, database cutoffs;
- input normalization and identifier-resolution rules;
- family definition/counting unit;
- status/term source hierarchy;
- claim-version and alternate-family-text rules;
- taxonomy version/date and evidence/confidence method;
- trend windows and partial-year treatment;
- strategy/opportunity derivation method;
- missing-data semantics;
- workbook/HTML generation versions;
- QA/rendering performed;
- limitations and monitoring/update plan.

## Spreadsheet formatting

- Use a restrained light scientific palette and system fonts.
- Freeze top row and identity columns where useful.
- Add filters to every data table.
- Wrap long evidence cells and set readable widths.
- Use ISO date cells rather than date-like text where possible.
- Use true hyperlinks with descriptive display text.
- Use data validation for controlled categories when editing is expected.
- Use conditional formatting only as a secondary cue.
- Avoid emoji-only statuses and red/green-only meaning.
- Avoid hidden sheets/columns unless documented.
- Protect formulas only when requested; do not prevent normal review.

## Formula and data QA

- Recalculate formulas with a compatible engine where possible.
- Check for `#REF!`, `#VALUE!`, `#DIV/0!`, `#N/A`, and broken named ranges.
- Confirm counts reconcile to unique IDs and declared units.
- Confirm multi-tag expansion does not inflate patent/family counts.
- Confirm blank, zero, unknown, not reported, and not applicable remain distinct.
- Confirm date windows exclude or flag partial years.
- Confirm source hyperlinks and local Markdown paths exist.

## Visual QA

Render or inspect every sheet. Verify:

- sheet names/order;
- visible title/metadata;
- row/column dimensions;
- frozen panes and filters;
- header contrast;
- no clipped/wrapped unreadable cells;
- no blank-looking formula results caused by unsupported calculation;
- useful print area/repeat rows where requested;
- no source/confidential fields accidentally hidden or exposed.

## Release checklist

- [ ] Workbook derives from the reviewed structured analysis layer.
- [ ] All required full/light sheets are present.
- [ ] Main row unit and family definition are explicit.
- [ ] Source/member/claim/status versions are traceable.
- [ ] Taxonomy assignments include evidence/confidence.
- [ ] Strategy findings include counterevidence/gaps.
- [ ] Opportunity hypotheses are not presented as patents or facts.
- [ ] Counts and timeline rows reconcile.
- [ ] Formulas, links, formatting, rendering, and errors were checked.
- [ ] English terminology is professionally localized.
