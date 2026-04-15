---
name: tech-route-comparison
description: >
  Evidence-backed comparison of two or more technical routes, architectures, or
  solution paths. Use when the user asks for technical pre-research, technical
  route comparison, route selection, TRL assessment, maturity assessment,
  readiness evaluation, opportunity mapping, or any management-grade technical
  report deliverable — even if they only ask for initiation analysis,
  committee-ready materials, feasibility, or "which route is better".
argument-hint: "[topic + route set + optional scenario/purpose]"
provider: "Patsnap Eureka"
compatibility: "Designed for Claude Code, Codex, and similar agent runtimes that can read/write local files and call whatever search tools are available."
deliverable-default: "Structured Markdown comparison report plus traceable evidence files; docx/pdf export is optional."
fallback-policy: "Prefer structured patent/paper retrieval when available; otherwise downgrade through domain-specific sources, Exa, Tavily, Brave, web, and a known-URL reader without blocking the run."
---

# Tech Route Comparison

Provided by Patsnap Eureka.

Use this skill when the decision object is a route set rather than a company,
a market arena, or a concrete proposal package. The goal is to compare routes
on evidence, normalize the comparison basis, and end with a recommendation the
user can act on.

## Use When

- The user asks which technical route is better, more mature, or lower risk
- Route comparison across two or more technical approaches
- Maturity, readiness, feasibility, or TRL evaluation
- Scenario-specific route recommendation (e.g., "which route for EV use?")
- Opportunity map or white-space scan across routes
- Management-ready technical pre-research report

## Do Not Use

- The real question is one company in one topic → route to `company-tech-profile`
- The real question is a multi-player arena or player map → route to
  `competitive-landscape`
- The real question is a concrete proposal or initiation package → route to
  `rd-initiation-review`
- The task is pure market sizing or commercial comparison with no technical core
- Legal patent opinion, FTO, or infringement analysis

## Modes

| Mode | When To Use | Focus |
|------|------------|-------|
| `overview` | Broad technical landscape for a topic | Route inventory, frontier scan, ecosystem structure |
| `compare` | Direct comparison of named routes | Head-to-head comparison matrix, ranking, recommendation |
| `maturity` | Readiness or TRL assessment | Maturity rubric, stage gates, deployment evidence |
| `opportunity` | White-space or opportunity scan | Gap analysis, emerging routes, entry paths |

Default mode: `compare` when routes are named, `overview` when only a topic is given.

## Core Principles

### Scope Freeze Before Retrieval

Freeze these parameters before wide retrieval to prevent evidence drift:

- `topic`: the technology domain
- `decision_question`: what the user needs to decide
- `decision_use`: directional route scan / go-no-go / diligence-grade
- `application_scenario`: the specific use case or context (e.g., EV battery,
  data center cooling, edge inference)
- `comparison_level`: material-level / component-level / system-level
- `known_routes`: user-provided or discovered route set
- `time_window`: default last 3-5 years

### Comparison Basis Must Be Explicit

Before ranking routes, write down:

- What routes are being compared (frozen definitions)
- What dimensions are used for comparison (performance, cost, maturity,
  risk, scalability, etc.)
- What normalization rules apply (same application scenario, same
  comparison level, same time window)

Do not compare shifting route buckets. Do not mix material-level evidence
with system-level evidence as if they were the same layer.

### TRL And Maturity Require Explicit Rubric

Do not write TRL labels, readiness levels, or maturity claims without an
explicit rubric that defines what each level means in the current context.
A route with many weak signals is still weak — do not confuse volume with
confidence.

### Counterevidence Is Required

For every route recommendation, actively search for and document:

- Evidence that contradicts the recommendation
- Conditions under which the recommendation would change
- Update triggers that should prompt re-evaluation

## Tool Routing And Fallback

This skill works across multiple tool environments. Before retrieval, detect
which capabilities are available and select the highest tier that is reachable.

### Tier 1 (Recommended): Structured Patent/Paper Retrieval

- Use the host's best structured patent and paper retrieval stack.
- This usually means fielded patent/paper search plus record-level deep fetch.
- Evidence grade: S/A
- Required capabilities: per-route search, keyword or semantic route discovery,
  and deep-read of shortlisted records.

### Tier 2 (Fallback): Web Research + Scholarly Companion Lane

- Use the host's best broad web research tool plus a scholarly companion lane
  when available.
- Exa, Tavily, Brave, and domain-specific scholarly databases are good examples,
  not hard requirements.
- Evidence grade: A/B
- Coverage loss vs Tier 1: route breadth and patent-structure claims are less precise.

### Tier 3 (Fallback): Generic Web Search And Page Reading

- Use generic web search and page/PDF reading tools available in the host.
- Evidence grade: B/C

### Tier 4 (Minimum): User Materials + Reasoned Synthesis

- No external tools required
- Evidence grade: C/U

### Routing Rules

- Detect available capabilities at the start of the workflow.
- Select the highest available tier as the primary retrieval channel.
- When a tier is unavailable, explicitly state the downgrade.
- If the tool stack is degraded, lower confidence on route breadth and frontier claims.

## Minimum Working Files

Create or update these files in a writable run folder:

- `request.md`
- `workplan.md`
- `method_decisions.md`
- `comparison_basis.md`
- `query_log.csv`
- `source_index.csv`
- `claim_ledger.csv`
- `report.md`

Recommended subfolders are described in [references/workflow.md](references/workflow.md).

## Default Workflow

### Step 0: Freeze Scope

Confirm or infer the following before any retrieval:

- `topic`, `decision_question`, `decision_use`
- `mode` (overview / compare / maturity / opportunity)
- `application_scenario`, `comparison_level`
- `known_routes` (user-provided or to be discovered)
- `time_window`, `audience`, `deliverable`

If the user did not specify routes, proceed with route discovery in Step 1.
If the user named routes, freeze them and proceed to Step 2.

If the topic is broad and not route-frozen yet, write a provisional route
taxonomy into `comparison_basis.md` before retrieval starts.

### Step 1: Build Route Taxonomy (When Routes Not Given)

1. Run 2-3 broad topic searches to discover candidate routes.
   - Tier 1: structured patent/paper search around the topic
   - Tier 2: targeted web research plus scholarly companion search
   - Tier 3/4: generic web or user-provided materials
2. Extract candidate routes from patent IPC clusters, paper themes, and
   review articles.
3. Freeze the route set in `comparison_basis.md` before proceeding.
4. If the route set is still too fuzzy, stop and narrow it with the user
   instead of writing a superficial ranking.

### Step 2: Freeze Comparison Basis

Write to `comparison_basis.md`:

- Route definitions (what each route means, technically)
- Comparison dimensions (performance, cost, maturity, risk, scalability,
  deployment readiness, etc.)
- Normalization rules:
  - Same application scenario for all routes
  - Same comparison level (do not mix material-level with system-level)
  - Same time window
- Scoring approach (if maturity or TRL mode):
  - Explicit rubric with level definitions
  - Evidence requirements per level

### Step 3: Retrieve Evidence Per Route

For each route independently:

1. Run 2-3 searches focused on the route's technical specifics.
   - Tier 1: structured patent/paper search for the route
   - Tier 2: targeted web research plus scholarly companion search
   - Tier 3/4: generic web or user-provided materials
2. Collect evidence across dimensions:
   - Patent activity and key technical approaches
   - Paper frontier and recent breakthroughs
   - Standards, specifications, and regulatory status
   - Product deployments, benchmarks, and commercial signals
3. Deep-read 2-3 representative patents/papers per route for technical detail.
4. Record all searches in `query_log.csv` with per-route tagging.

Do not mix evidence across routes during collection. Keep per-route evidence
buckets separate until the normalization step.

### Step 4: Normalize And Compare

1. Build the comparison matrix: routes (rows) × dimensions (columns).
   Fill each cell with evidence-backed assessments.

Example format:

| Dimension | Route A | Route B | Route C |
|-----------|---------|---------|---------|
| Performance | High — [Patent: X] demonstrates Y | Moderate — lab-scale only | High — [Paper: Z] benchmark |
| Cost | High — mature supply chain | Unknown — no production data | Low — expensive precursors |
| Maturity (TRL) | TRL 7 — pilot production | TRL 4 — lab validation | TRL 5 — prototype |
| Risk | Low — well-understood failure modes | High — scaling unknowns | Moderate — IP concentration |

2. Apply the scoring rubric (if maturity or TRL mode):
   - Score each route per dimension using the explicit rubric
   - Show the rubric alongside the scores
   - Do not assign TRL or maturity labels without evidence

3. Run the counterevidence pass:
   - For each route recommendation, search for contradicting evidence
   - Document weakening conditions and update triggers
   - If counterevidence is strong, adjust the recommendation

4. Separate every claim into:
   - **Verified fact**: directly supported by patent, paper, or official source
   - **Evidence-backed inference**: reasonable conclusion from multiple signals
   - **Open gap**: insufficient evidence, state what is missing

### Step 5: Synthesize And Draft

Write the report following the mode-appropriate output skeleton.

## Output Skeletons

### Overview Mode

1. Executive summary: topic landscape and main route families
2. Route taxonomy and definitions
3. Per-route profile cards (2-3 paragraphs each)
4. Frontier signals and emerging directions
5. Key evidence references

### Compare Mode

1. Executive summary: which route is recommended and why
2. Scope and comparison basis (explicit)
3. Route-by-route profile cards
4. Comparison matrix (routes × dimensions)
5. Recommendation with conditions, tradeoffs, and update triggers
6. Counterevidence and weakening conditions
7. Key evidence references

### Maturity Mode

1. Executive summary: maturity landscape and readiness gaps
2. Scope and maturity rubric (explicit)
3. Per-route maturity assessment with evidence
4. Maturity comparison matrix
5. Stage-gate or readiness roadmap
6. Risks and deployment blockers
7. Key evidence references

### Opportunity Mode

1. Executive summary: where the opportunities are
2. Route landscape and current coverage
3. Gap analysis (sparse coverage + technical value + entry path)
4. Emerging routes and early signals
5. Recommended investigation priorities
6. Key evidence references

Every claim must cite its source type and identifier, e.g., `[Patent: CN1234567B]`,
`[Paper: DOI or title]`, `[Web: source name]`.

## Completion Gates

All must pass before delivering the final answer:

- [ ] Route set is frozen before wide retrieval
- [ ] Comparison basis is explicit and written to `comparison_basis.md`
- [ ] Comparison level is consistent (not mixing material/component/system)
- [ ] At least 2 searches per route executed with results analyzed
- [ ] Per-route evidence collected independently before cross-route comparison
- [ ] Comparison matrix present with evidence backing per cell
- [ ] If TRL or maturity labels are used, explicit rubric is present
- [ ] Counterevidence pass completed for the main recommendation
- [ ] Every major claim has a traceable source citation
- [ ] Verified fact / evidence-backed inference / open gap clearly separated
- [ ] Tool tier and coverage limitations explicitly stated
- [ ] If evidence is insufficient for confident ranking, stated explicitly
      with next-evidence-gathering directions

## Guardrails

- Do not confuse volume with confidence. A route with many weak signals is
  still weak.
- Do not let vendor or company marketing outrank patents, papers, standards,
  or directly inspectable technical evidence.
- Do not turn raw patent or paper counts into maturity claims without dedup
  and scope caveats.
- Do not write TRL, readiness, or maturity labels without an explicit rubric.
- Do not compare material-level, component-level, and system-level evidence
  as if they were the same layer.
- Do not force a strong conclusion when the user only gave a broad topic and
  the evidence base is thin.
- Do not skip the counterevidence pass — every recommendation needs at least
  one documented weakening condition.
- If paper or patent coverage is inadequate for a route, say so explicitly
  before making strength claims.
- Do not present a route ranking as definitive when the comparison basis is
  incomplete or the scoring rubric is missing.
- Keep the recommendation tied to the stated scenario — a route that is best
  for one application may not be best for another.

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
- [templates/comparison-basis-template.md](templates/comparison-basis-template.md)
- [templates/report-outline.md](templates/report-outline.md)
