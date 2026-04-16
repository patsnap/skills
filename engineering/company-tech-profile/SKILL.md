---
name: company-tech-profile
description: >
  Single-company technology profile and R&D assessment for a defined technology
  topic. Use when the user asks for a company technology profile, company
  technical analysis, R&D direction assessment, technical due diligence
  briefing, or any single-company-by-topic technical evaluation — even if they
  only mention a company plus a technology area without explicitly asking for a
  "profile".
argument-hint: "[company + topic + optional purpose/time window]"
provider: "Patsnap Eureka"
compatibility: "Designed for Claude Code, Codex, and similar agent runtimes that can read/write local files and call whatever search tools are available."
deliverable-default: "Structured Markdown report plus traceable evidence files; docx/pdf export is optional."
fallback-policy: "Prefer structured patent/paper retrieval when available; otherwise downgrade through domain-specific sources, Exa, Tavily, Brave, web, and a known-URL reader without blocking the run."
---

# Company Tech Profile

Provided by Patsnap Eureka.

Produce an evidence-driven technology profile for a single company in a defined
technology topic. The deliverable is a structured report — conclusion first,
evidence second — suitable for technical leaders, analysts, and investment
screeners.

## Use When

- A company's technical strength, R&D direction, or core technology layout in a topic
- Technology due diligence or partnership evaluation for a named company
- Investment screening that needs patent/paper/product evidence for one entity
- A company-only prompt where you can infer a safe technology topic from context

## Do Not Use

- Multiple companies need comparison or tiering → route to `competitive-landscape`
- Pure technology-route comparison with no company anchor → route to `tech-route-comparison`
- The task is a project/proposal review → route to `rd-initiation-review`
- Legal patent opinion, FTO, infringement, or litigation analysis
- Generic company overview with no technology depth requirement

## Tool Routing And Fallback

This skill works across multiple tool environments. Before retrieval, detect
which capabilities are available and select the highest tier that is reachable.

### Tier 1 (Recommended): Structured Patent/Paper Retrieval

- Use the host's best structured patent and paper retrieval stack.
- This usually means fielded search with company/entity filtering plus
  record-level deep fetch.
- Evidence grade: S/A (primary structured evidence)
- Required capabilities: company/entity filtering, topic search, structured
  patent/paper retrieval, and deep-read of shortlisted records.
- Typical query count per run: 4-8 searches.

### Tier 2 (Fallback): Web Research + Companion Lanes

- Use the host's best broad web research tool plus scholarly or finance
  companion lanes when available.
- Exa, Tavily, Brave, official filings, and domain-specific research databases
  are good examples, not hard requirements.
- Evidence grade: A/B (web-sourced but structured)
- Coverage loss vs Tier 1: no structured assignee filtering, no IPC/CPC faceting,
  and weaker paper-graph style coverage

### Tier 3 (Fallback): Generic Web Tools

- Use generic web search and page/PDF reading tools available in the host.
- Evidence grade: B/C (unstructured web)
- Coverage loss vs Tier 2: no academic-focused ranking, broader noise

### Tier 4 (Minimum): Pure LLM + User Materials

- No external tools required
- Evidence grade: C/U (LLM knowledge + user-provided only)
- Coverage loss vs Tier 3: no current information, no verifiable citations

### Routing Rules

- Detect available tools at the start of the workflow.
- Select the highest available tier as the primary retrieval channel.
- When a tier is unavailable, explicitly state the downgrade in the output
  and in `method_decisions.md`.
- Do not pretend lower-tier results have the same coverage as higher tiers.
- When using Tier 3 or 4, increase the proportion of explicit gap statements
  and reduce confidence language in conclusions.

## Minimum Working Files

Create or update these files in a writable run folder:

- `request.md`
- `workplan.md`
- `method_decisions.md`
- `query_log.csv`
- `source_index.csv`
- `claim_ledger.csv`
- `report.md`

Recommended subfolders are described in [references/workflow.md](references/workflow.md).

## Default Workflow

### Step 0: Freeze Scope

Confirm or infer the following before any retrieval:

- **company_name**: the primary entity to profile
- **topic**: the technology area to anchor the analysis
- **purpose**: what decision this profile supports (orientation / due diligence /
  partnership / investment screening)
- **time_window**: default last 3 years unless user specifies otherwise

Scope routing decision tree:

```
User input shape?
├─ Company + technology topic → proceed as single-company profile
├─ Company only, no topic → infer topic from company's main business domain;
│  confirm with user if ambiguous
├─ Multiple companies mentioned → redirect to competitive-landscape
├─ Technology topic only, no company → redirect to tech-route-comparison
└─ "Compare company A with B" → redirect to competitive-landscape
```

If the user only names a company without a topic, do not stall — infer the most
likely technology topic from the company's known domain and state the inference
explicitly.

### Step 1: Anchor The Entity

1. Normalize the company name: resolve parent vs subsidiary, Chinese vs English
   aliases, brand name vs legal entity.
2. Run a confirmation search to verify the company has presence in the topic.
   - Tier 1: structured entity-filtered patent/paper search
   - Tier 2+: targeted web or scholarly search across patent indices, official
     domains, and research pages
3. If the company has no patent presence in the topic, note this as a finding
   and shift emphasis to papers and public signals.
4. Search for the company's official site to capture basic profile, product
   lines, and recent announcements.

### Step 2: Patent Portfolio Analysis

1. Run 2-3 patent searches varying keywords to cover the topic's sub-routes.
   - Tier 1: structured patent search with entity filters and keyword variations
   - Tier 2: targeted web research across patent indices, official domains, and
     technical publications
   - Tier 3/4: generic web or user-provided materials
2. Analyze from search results: filing volume trend (by year), IPC distribution,
   key technology clusters, filing jurisdictions.
3. Decide whether direct deep-reading is stable enough, or whether representative
   sampling is required.

Sampling decision tree (Tier 1 with structured retrieval):

```
Patent evidence shape?
├─ Scope is small and route concentration is obvious
│  └─ Skip sampler; deep-read the strongest 3-5 patents directly
├─ Scope is medium/large and route coverage matters
│  └─ Run the optional representative patent sampling script
├─ Scope is large and highly heterogeneous across time/jurisdiction/CPC
│  └─ Run the optional sampling script; treat result as default evidence pack
└─ Task is drifting toward legal completeness
   └─ Do not use sampler; redirect to a legal/FTO-oriented workflow
```

Default thresholds:

- `<= 12` patents after filtering: usually skip sampler
- `13-80` patents: sampler recommended if route interpretation is part of the goal
- `> 80` patents: sampler should be the default

4. Deep-read top 3-5 representative patents to extract: core technical
   approaches, key claims, innovation points.
5. Identify the company's primary technology routes and any emerging pivots.

### Step 3: Paper And R&D Signals

1. Run 1-2 paper searches with company name + topic.
   - Tier 1: structured paper retrieval
   - Tier 2: scholarly companion search or targeted web research
   - Tier 3/4: generic web or user-provided materials
2. Analyze: publication trend, collaborating institutions, research focus areas.
3. Cross-reference with patent routes — consistency strengthens confidence;
   divergence is a signal worth noting.

### Step 4: Product And Public Signals

1. Search for: product launches, benchmark results, partnerships, funding
   rounds, key hires, conference presentations.
2. Read 2-3 high-signal pages for deeper extraction.
3. Corroborate patent/paper findings with product reality — a strong patent
   portfolio without shipped products is a different signal than one with them.

### Step 5: Synthesis

Adjust analysis emphasis by industry type:

```
Industry type?
├─ Semiconductor / Hardware → emphasize: patent clusters by process/architecture,
│  fab vs fabless signals, IPC H01L/H04 distribution
├─ Biopharma / Medtech → emphasize: pipeline stage, clinical trial signals,
│  target coverage, IPC A61K/C07/A61B distribution
├─ AI / Software → emphasize: papers and benchmarks, open-source presence,
│  model performance, API/platform adoption signals
├─ New Energy / Materials → emphasize: material composition patents, capacity
│  signals, cost trajectory, IPC H01M/C01/H02 distribution
└─ General Manufacturing → balanced patent + product + standard participation
```

Synthesize all evidence into the output skeleton. Separate every claim into:

- **Verified fact**: directly supported by patent, paper, or official filing
- **Evidence-backed inference**: reasonable conclusion from multiple signals
- **Open gap**: insufficient evidence, state what is missing and suggest next steps

## Output Skeleton

### 1. Lead With Conclusion

1-2 sentences: the company's overall technical position and trajectory in the topic.

### 2. Technology Layout Highlights

2-4 bullet points: core technology routes, key patents or papers, differentiation
from the broader field. Use a compact markdown table when comparing 3+ dimensions.

### 3. Trend Assessment

1 paragraph: R&D direction evolution over the time window — acceleration,
deceleration, pivots, emerging focus areas. Cite specific year-over-year changes
when data supports it.

### 4. Risks And Recommendations

1 set of bullet points:
- Key risks (technology gaps, dependency, competitive pressure)
- Opportunities (white spaces, collaboration potential, emerging routes)
- Recommended next actions for the user's decision context

Every claim must cite its source type and identifier, e.g., `[Patent: CN1234567B]`,
`[Paper: DOI or title]`, `[Web: source name]`.

## Completion Gates

All must pass before delivering the final answer:

- [ ] Company entity confirmed and aliases resolved (not confused with subsidiary or homonym)
- [ ] At least 1 patent search and 1 paper search executed with results analyzed
- [ ] If patent scope is broad, representative sampling was executed or explicitly skipped with reason
- [ ] Core technology routes identified with patent or paper evidence
- [ ] Every major claim has a traceable source citation
- [ ] Verified fact / evidence-backed inference / open gap clearly separated
- [ ] Output follows the 4-part skeleton (conclusion → layout → trend → risks)
- [ ] No drift into generic company biography without technical substance
- [ ] Tool tier and coverage limitations explicitly stated in the output
- [ ] If evidence is insufficient for a confident profile, explicitly stated with follow-up suggestions
- [ ] Company marketing claims treated as signals, not verified facts, unless corroborated

## Guardrails

- Do not equate patent volume with technical strength without considering route
  quality, claim scope, and recency.
- Do not treat company marketing claims, recruiting signals, or press releases as
  verified facts until corroborated by stronger sources.
- Do not mix parent company and subsidiary data without an explicit scope note.
- This is a single-company skill — do not produce competitive comparison matrices.
  If the user needs multi-company comparison, redirect to `competitive-landscape`.
- If the company has minimal patent/paper presence in the topic, say so directly
  rather than padding the profile with tangential evidence.
- Do not use representative sampling for legal-opinion tasks or when exhaustive
  recall is required.
- Do not present the sampled patent set as "all relevant patents"; state clearly
  that it is a structured representative subset.
- Do not let the sampled set silently override full-scope facts such as total
  patent count, jurisdiction count, or exact filing volume.
- Do not force a strong conclusion when the evidence base is thin — prefer
  explicit uncertainty over false confidence.
- Keep charts or visual aids to 1-2 maximum; retain only those that directly
  support the analytical conclusion.
- For non-evidence dimensions (TCO, regulation, teardown), write "evidence
  pending" rather than fabricating a judgment.

## Optional Host-Specific Automation

Some hosts may provide extra helpers for representative sampling, quantitative
aggregation, or patent-card normalization. These helpers are optional and are
not part of the core open-source contract.

If you use host-specific automation:

- record the helper and its role in `method_decisions.md`
- keep the final evidence compatible with `query_log.csv`, `source_index.csv`,
  and `claim_ledger.csv`
- do not make the report depend on a helper that other hosts cannot reproduce

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
