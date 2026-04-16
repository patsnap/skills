---
name: rd-initiation-review
description: >
  R&D project initiation pre-screen and proposal audit for go/no-go decisions,
  public novelty boundary review, innovation-point assessment, and evidence-backed
  project rating. Use when the user asks for project initiation pre-screening,
  initiation review, proposal review, R&D project evaluation, proposal-package
  review, novelty pre-screening, innovation-point review, project rating, or
  wants a formal review around a concrete project, proposal, or research-package
  material set — even if they only provide the proposal and do not explicitly
  say "review".
argument-hint: "[project proposal, initiation report, or review request]"
provider: "Patsnap Eureka"
compatibility: "Designed for Claude Code, Codex, and similar agent runtimes that can read/write local files and call whatever search tools are available."
deliverable-default: "Structured Markdown review report plus novelty note and traceable evidence files; docx/pdf export is optional."
fallback-policy: "Start from proposal materials; prefer structured patent/paper retrieval when available; otherwise downgrade through domain-specific sources, Exa, Tavily, Brave, web, and a known-URL reader without blocking the run."
---

# R&D Initiation Review

Provided by Patsnap Eureka.

Use this skill when the decision object is a concrete project, proposal,
innovation package, or initiation document set. The goal is to judge whether
it should move forward, how similar it is to public prior work, which
innovation claims still stand, and what evidence or materials are still missing.

The customer-visible value should land first on four questions:

1. Is this project worth advancing?
2. How close is it to public prior work?
3. Do the innovation claims hold up?
4. What is still missing before the next gate?

## Use When

- The user provides a project or proposal and asks whether it is worth advancing
- Formal initiation review report for a concrete project
- Pre-screening / public novelty pre-check / client-facing pre-screen
- Go/no-go or budget-release recommendation around a proposal
- Project-level novelty / feasibility / trend / risk review
- Innovation-point-by-innovation-point assessment
- Management-ready review bundle with evidence pack

## Do Not Use

- Pure technology-route comparison with no concrete project object → route to
  `tech-route-comparison`
- Company-by-topic technical profile or player landscape → route to
  `company-tech-profile` or `competitive-landscape`
- Legal patent opinion, FTO, infringement, or litigation analysis
- Drafting the original proposal from scratch (this skill reviews, not writes)
- Generic company overview with no project-level review depth

## Review Modes

| Mode | When To Use | Typical Output |
|------|------------|----------------|
| `screen` | Pre-screening, early-stage review, customer-facing presales | Quick go/no-go + novelty boundary + key gaps (6-8 pages) |
| `review` | Standard initiation review | Full review report + novelty note + evidence pack (10-14 pages) |
| `innovation` | Innovation-point deep review | Point-by-point innovation assessment + differentiation table (8-12 pages) |
| `assurance` | Expert review, committee-ready package | Deep evidence-sufficiency audit + rating logic + stage-gate matrix (12-18 pages) |

Default mode selection:

- If the request is for pre-screening, novelty pre-check, overlap check,
  "is it worth advancing", or an early customer-facing review → default to `screen`
- If the request is for expert review, go/no-go, budget release, evidence
  sufficiency, or committee-ready bundle → default to `assurance`
- Otherwise → default to `review`

## Core Principles

### Proposal As Input, Not Truth

The proposal is the starting point for extraction, not a source of verified
facts. A proposal claim does not become a review conclusion unless it is either
corroborated externally or explicitly labeled as proposal-only.

### Four-Layer Evidence Separation

Every substantive claim in the review must be tagged as one of:

1. **Proposal-stated**: what the proposal says (quoted or summarized)
2. **Externally corroborated fact**: confirmed by patent, paper, or official source
3. **Evidence-backed inference**: reasonable conclusion from multiple signals
4. **Open gap**: insufficient evidence — state what is missing and what would resolve it

Do not let proposal-stated claims silently become review conclusions.

### Novelty As First-Class Visible Module

Novelty search is not a side effect of baseline retrieval. The review must
clearly state:

- Novelty-search scope (databases, time window, field scope)
- Main comparison objects (prior art, prior routes, existing solutions)
- Point-by-point overlap assessment
- Residual differentiators
- Explicit novelty judgment level for each major claim
- Search limitations and unsearched areas

When novelty is downgraded because of prior art, build a structured
differentiation-boundary table showing overlap, residual differentiators,
and replacement risk.

### Material Completeness As First-Class Module

Even when the platform cannot solve the client's full data governance problem,
the report should clearly say which missing materials or data are currently
blocking:

- novelty or overlap boundary judgment
- feasibility judgment
- next-step initiation actions

If internal archives or non-public project databases are not available, say so
explicitly. Do not imply that a public-only retrieval pass proves exhaustive
internal duplicate-project exclusion.

## Tool Routing And Fallback

This skill works across multiple tool environments. Before retrieval, detect
which capabilities are available and select the highest tier that is reachable.

### Tier 0 (Always First): Proposal Materials

- User-provided proposal, initiation report, innovation package
- Extract project summary, research theme, innovation points, promised outputs,
  and proposal-stated claims BEFORE any external search
- Evidence grade: proposal-stated (not externally verified)

### Tier 1 (Recommended): Structured Patent/Paper Retrieval

- Use the host's best structured patent and paper retrieval stack to test
  novelty, feasibility, and frontier evidence around normalized innovation points.
- This usually means structured search plus record-level deep fetch.
- Evidence grade: S/A

### Tier 2 (Fallback): Exa Search + Companion Skills

- Use the host's best broad web research tool plus scholarly or finance
  companion lanes when available.
- Exa, Tavily, Brave, official filings, and domain-specific research databases
  are good examples, not hard requirements.
- Evidence grade: A/B
- Coverage loss vs Tier 1: no structured patent field search, no assignee
  filtering, novelty conclusions less precise

### Tier 3 (Fallback): Generic Web Tools

- Use generic web search and page/PDF reading tools available in the host.
- Evidence grade: B/C

### Tier 4 (Minimum): Pure LLM + Proposal Materials

- No external tools required
- Evidence grade: C/U
- The review can still extract and organize proposal claims, identify logical
  gaps, and flag what external evidence would be needed

### Routing Rules

- Always start from proposal materials (Tier 0) regardless of tool availability.
- Select the highest available external tier for verification.
- When a tier is unavailable, explicitly state the downgrade.
- Do not pretend a public-only pass equals full duplicate-project exclusion.
- When using Tier 3 or 4, increase explicit gap statements and reduce
  confidence on novelty and completeness claims.

## Minimum Working Files

Create or update these files in a writable run folder:

- `request.md`
- `workplan.md`
- `method_decisions.md`
- `query_log.csv`
- `source_index.csv`
- `claim_ledger.csv`
- `report.md`
- `novelty-note.md`

Recommended subfolders are described in [references/workflow.md](references/workflow.md).

## Default Workflow

### Step 0: Freeze Scope

Confirm or infer the following before any retrieval:

- `project_name`: the concrete project or proposal object
- `topic`: the research theme (infer from materials if not stated)
- `decision_gate`: pre-approval / go-no-go / budget release / expert review
- `mode`: screen / review / innovation / assurance
- `deliverable`: brief / report / docx / pdf / evidence-pack
- `audience`: client / internal / committee / management
- `time_window`: default last 3-5 years
- `review_focus`: novelty / feasibility / trend / risk / rating (can be multiple)
- `innovation_scope`: extract from materials or user-specified innovation points

If the user supplied materials but did not name the research theme, infer a
provisional theme from the materials and log that it is provisional.

If the user did not provide a concrete project object at all, do not force
this skill — redirect to `tech-route-comparison` or `company-tech-profile`.

### Step 1: Extract Proposal Materials

Before any external search:

1. Read the proposal and extract:
   - Project summary and research theme
   - Stated innovation points (normalize into a short comparison set)
   - Promised outputs and deliverables
   - Proposal-stated claims about novelty, feasibility, and market
   - Technical path description (main chain, dependencies, measurement approach)
2. Build an innovation register: each innovation point as an atomic item with
   the proposal's own language preserved.
3. Identify what the proposal does NOT address: missing data, unstated
   assumptions, logical gaps.
4. Tag everything as `proposal-stated` at this stage.

### Step 2: Retrieve External Evidence

1. Search for prior art and prior routes around each normalized innovation point.
   - Tier 1: structured patent/paper search around each innovation point
   - Tier 2: web research plus scholarly companion search
   - Tier 3/4: generic web or proposal-only reasoning
2. For each innovation point, run a dedicated novelty check:
   - Search scope: patents + papers + standards in the topic area
   - Record: database/source scope, time filter, field scope, linked novelty
     point, screening rule
   - Identify: closest prior art, overlap degree, residual differentiators
3. Search for feasibility and frontier support:
   - Are the proposed technical approaches validated elsewhere?
   - What is the current state of the art?
   - Are there known failure modes or blockers?
4. Search for trend and policy context when relevant:
   - Industry direction, regulatory environment, standards status
   - Only use web sources for current-status claims (standards, regulation,
     launch status, productization proof)

### Step 3: Build Analysis By Mode

Select modules based on the current mode:

| Module | screen | review | innovation | assurance |
|--------|--------|--------|------------|-----------|
| Proposal extraction | ✓ | ✓ | ✓ | ✓ |
| Novelty boundary | ✓ | ✓ | ✓ | ✓ |
| Innovation-point assessment | light | standard | deep | deep |
| Feasibility check | light | standard | light | deep |
| Trend/frontier context | optional | standard | optional | standard |
| Material completeness | ✓ | ✓ | ✓ | ✓ |
| Scoring/rating | skip | optional | optional | required |
| Stage-gate matrix | skip | skip | skip | required |
| Counterevidence pass | skip | optional | optional | required |
| Governance review | skip | skip | skip | optional |

### Step 4: Synthesize And Draft

Write the report following the mode-appropriate output skeleton.

For customer-facing or presales deliverables, put the visible value on the
front pages in this order:

1. Recommendation
2. Novelty and overlap boundary
3. Key issues and risks
4. Missing materials, data, and next steps

Do not let deep technical decomposition crowd out these questions in the
main narrative.

## Output Skeletons

### Screen Mode

1. Executive recommendation (proceed / proceed with conditions / hold)
2. Novelty boundary summary (1-2 paragraphs)
3. Key risks and blockers
4. Missing materials and next steps

### Review Mode

1. Executive recommendation
2. Project scope and proposal-stated claims
3. Novelty and overlap judgment (with comparison table)
4. Feasibility and evidence sufficiency
5. Main risks and material gaps
6. Recommendation and conditions

### Innovation Mode

1. Executive summary of innovation assessment
2. Innovation-point-by-point analysis (each point: proposal claim → external
   evidence → overlap → residual differentiator → judgment)
3. Differentiation boundary table
4. Risks to innovation claims
5. Recommendation

### Assurance Mode

1. Executive recommendation with confidence level
2. Project scope and proposal coherence assessment
3. Novelty and overlap (with detailed comparison attachment)
4. Feasibility, evidence sufficiency, and technical decomposition
5. Scoring and rating logic (with explicit rubric)
6. Stage-gate matrix (conditions, owners, timelines, non-fulfillment consequences)
7. Material gaps and data readiness
8. Counterevidence and weakening conditions

Every claim must cite its source type and identifier, e.g., `[Patent: CN1234567B]`,
`[Paper: DOI or title]`, `[Web: source name]`, `[Proposal: section/page]`.

## Formal Output Rules

For formal review audiences such as large enterprises, public-sector bodies,
and research institutions:

1. Remove empty opening filler such as trend-setting or era-setting lead-ins.
2. Remove promotional language and replace it with concrete review judgments.
3. Replace vague attribution with named evidence and explicit citations.
4. Rewrite formulaic paired constructions into direct standalone judgments.
5. Do not leak control-plane jargon such as `proposal-only`, `prior-art`,
   `assurance`, `gate`, or `owner` into the main report unless the term is
   necessary and clearly explained.

Headings and body text should use plain formal wording suitable for a written
review or committee memo.

When novelty is a live decision question, promote the method and point-by-point
comparison into `novelty-note.md`. A suitable file title is
`Public Novelty and Prior-Art Review Note` or `Novelty and Benchmarking Appendix`.

## Completion Gates

### All Modes

- [ ] Concrete project object identified (not just a topic)
- [ ] Proposal-stated claims extracted before external search
- [ ] Four-layer evidence separation maintained throughout
- [ ] Tool tier and coverage limitations explicitly stated
- [ ] Material completeness assessment present
- [ ] If internal archives are unavailable, the duplicate-project boundary is marked as unverified

### Screen Mode Additional

- [ ] Go/no-go recommendation present with conditions
- [ ] Novelty boundary summary present
- [ ] Key gaps and next steps identified

### Review Mode Additional

- [ ] At least 2 patent searches and 1 paper search executed per innovation point
- [ ] Novelty comparison table present
- [ ] Every major claim has a traceable source citation

### Innovation Mode Additional

- [ ] Each innovation point assessed individually
- [ ] Differentiation boundary table present
- [ ] Residual differentiators explicitly stated per point

### Assurance Mode Additional

- [ ] Scoring rubric explicit and traceable
- [ ] Stage-gate matrix with conditions, owners, and consequences
- [ ] Counterevidence pass completed
- [ ] Technical decomposition covers main chain, dependencies, and failure modes

## Guardrails

- The proposal is an input object, not a source of truth. Do not let proposal
  rhetoric substitute for external evidence.
- Do not imply that a public-only retrieval pass proves exhaustive coverage or internal
  duplicate-project exclusion.
- Do not let raw search hit counts or internal ledger jargon become the main
  management-facing argument.
- Treat proposal promises, roadmap claims, and commercialization statements as
  signals until corroborated.
- Keep scoring as a support layer, not the main selling point. Prefer direct
  judgments (proceed / proceed with conditions / hold) over dense weighted scoring tables
  in the main body.
- When novelty is downgraded, do not stop at prose caution — build a structured
  differentiation-boundary table.
- Do not force a strong go/no-go when the evidence base is thin — prefer
  conditional recommendations with explicit next-evidence-gathering steps.
- Separate the novelty methodology (scope, queries, limitations) from the
  novelty conclusion.
- Do not mix proposal-stated claims with externally verified facts without
  clear labeling.
- For formal reports, do not leak control-plane jargon into the
  management-facing narrative.
- Treat internal duplicate-project exclusion as data-dependent — do not promise
  it when internal project history is unavailable.

## Load These Files Only As Needed

- [references/method-benchmark.md](references/method-benchmark.md)
- [references/domain-playbooks.md](references/domain-playbooks.md)
- [references/workflow.md](references/workflow.md)
- [references/source-routing.md](references/source-routing.md)
- [references/deliverables.md](references/deliverables.md)
- [references/evidence-schema.md](references/evidence-schema.md)
- [references/quality-gates.md](references/quality-gates.md)
- [templates/request-template.md](templates/request-template.md)
- [templates/workplan-template.md](templates/workplan-template.md)
- [templates/report-outline.md](templates/report-outline.md)
