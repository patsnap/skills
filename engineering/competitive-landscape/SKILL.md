---
name: competitive-landscape
description: >
  Technology-sector competitive landscape analysis with player tiering, route
  differentiation, and white-space identification. Use when the user asks for
  player mapping, sector competitor analysis, technology-track player
  comparison, domestic-vs-overseas player comparison, or any multi-player
  competitive assessment in a defined technology domain.
argument-hint: "[topic + optional region/purpose/player set]"
provider: "Patsnap Eureka"
compatibility: "Designed for Claude Code, Codex, and similar agent runtimes that can read/write local files and call whatever search tools are available."
deliverable-default: "Structured Markdown landscape report plus traceable evidence files; docx/pdf export is optional."
fallback-policy: "Prefer structured patent/paper retrieval for arena discovery and per-player evidence; otherwise downgrade through domain-specific sources, Exa, Tavily, Brave, web, and a known-URL reader without blocking the run."
---

# Competitive Landscape

Provided by Patsnap Eureka.

Produce an evidence-driven competitive landscape report for a technology sector
or track. The deliverable is a structured report with player tiers, route
differentiation matrix, top-player profiles, and white-space opportunities —
conclusion first, evidence second — suitable for strategic planning, market
entry decisions, and R&D direction setting.

## Use When

- Sector or technology-track player mapping and competitive tiering
- Route differentiation analysis across multiple companies
- White-space and opportunity identification in a technology domain
- Multi-company comparison anchored to a technology topic
- Domestic-vs-overseas player comparison in a defined technical arena
- "Who are the players in X?" or "What is the competitive landscape for X?"

## Do Not Use

- Single company only, no sector scope → route to `company-tech-profile`
- Pure technology-route comparison with no player/company object → route to
  `tech-route-comparison`
- The task is a project/proposal review → route to `rd-initiation-review`
- Market or commercial analysis without technology depth (pure market sizing,
  pricing strategy, go-to-market)
- Legal patent opinion, FTO, or infringement analysis

## Tool Routing And Fallback

This skill works across multiple tool environments. Before retrieval, detect
which capabilities are available and select the highest tier that is reachable.

### Tier 1 (Recommended): Structured Patent/Paper Retrieval

- Use the host's best structured patent and paper retrieval stack.
- This usually means sector search, assignee/entity filtering, and record-level
  deep fetch.
- Evidence grade: S/A (primary structured evidence)
- Required capabilities: sector discovery, entity filtering, route faceting or
  structured narrowing, and deep-read of shortlisted records.
- Typical query count per run: 8-15 searches.

### Tier 2 (Fallback): Web Research + Companion Lanes

- Use the host's best broad web research tool plus scholarly or finance
  companion lanes when available.
- Exa, Tavily, Brave, official filings, and domain-specific research databases
  are good examples, not hard requirements.
- Evidence grade: A/B
- Coverage loss vs Tier 1: no structured assignee extraction from patent data,
  no IPC/CPC faceting, player discovery depends on web article quality

### Tier 3 (Fallback): Generic Web Tools

- Use generic web search and page/PDF reading tools available in the host.
- Evidence grade: B/C
- Coverage loss vs Tier 2: no academic-focused ranking, broader noise

### Tier 4 (Minimum): Pure LLM + User Materials

- No external tools required
- Evidence grade: C/U
- Coverage loss vs Tier 3: no current information, no verifiable citations

### Routing Rules

- Detect available tools at the start of the workflow.
- Select the highest available tier as the primary retrieval channel.
- When a tier is unavailable, explicitly state the downgrade in the output
  and in `method_decisions.md`.
- Do not pretend lower-tier results have the same coverage as higher tiers.
- If the tool stack is degraded, lower confidence on player completeness
  and white-space claims.

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

- **sector / track**: the technology domain to analyze
- **geography**: default global unless user specifies a region
- **time_window**: default last 3 years unless user specifies otherwise
- **known_players**: any companies the user already has in mind (seed set)
- **purpose**: what decision this landscape supports (market entry / R&D
  direction / investment screening / strategic planning)
- **TopN target**: default 5-10 players

Scope routing decision tree:

```
User input shape?
├─ Technology topic + multiple companies → proceed as player-set landscape
├─ Technology topic only, no companies → proceed; discover players from evidence
├─ "Who are the players in X?" → proceed as discovery landscape
├─ Only 1 company, no sector scope → redirect to company-tech-profile
├─ "Compare A with B in topic X" with 2+ companies → proceed as landscape
└─ Pure technology route, no player interest → redirect to tech-route-comparison
```

### Step 1: Build Sector Evidence Baseline

1. Run 2-3 broad sector searches with core technology terms.
   - Tier 1: structured sector search across patents and papers
   - Tier 2: targeted web research across technical reports, official pages, and
     research coverage
   - Tier 3/4: generic web or user-provided materials for initial candidate list
2. Extract candidate player set from patent assignees and paper affiliations
   in the search results. Aim for 10-20 candidates before filtering.
3. Run 1-2 sector overview searches to capture market context, recent trends,
   and players that may not appear in patent/paper data.
4. Merge candidates from all sources into a single candidate list with
   preliminary activity indicators.

### Step 2: Tier Players

For each candidate in the list:

1. Run a focused search to get patent and paper activity volume and recency.
   - Tier 1: structured entity-filtered search
   - Tier 2+: targeted web research across patent indices, official domains, and
     research pages
2. Classify each player using the tiering decision tree:

```
Player classification criteria:
├─ Tier 1 — Leader: high patent/paper activity + shipped products or
│  demonstrated capability + sustained recent growth
├─ Tier 2 — Challenger: moderate activity + clear differentiation or
│  strong niche position + growing trajectory
├─ Tier 3 — Follower: low activity or narrow focus, but present in the
│  space with identifiable technology routes
└─ Watchlist: emerging signals (recent filings, new entrants, pivoting
   companies) but insufficient evidence for confident tiering
```

3. Select top 5-7 players for deep-dive based on tier and relevance to the
   user's decision context.
4. If evidence is insufficient to tier confidently, keep the player on the
   watchlist and note the evidence gap.

Tiering evidence rule:

- Full-scope counts and route breadth must come from aggregation, not samples
- Final tiers must combine patent evidence with paper and product signals
- Do not assign tiers from one noisy search or one source family alone

### Step 3: Deep-Dive Top Players Individually

For EACH top player, analyze independently — never merge conclusions across players:

1. **Patent route analysis**: key IPC clusters, filing trend, representative patents.
   - Tier 1: structured per-player search; for large footprints, use optional
     host-specific automation if available
   - Tier 2+: targeted web research across patent indices, official domains, and
     technical publications
2. Deep-read 2-3 representative patents per player to extract route-specific
   technical detail and differentiation evidence.
3. **Paper focus**: research themes, collaboration network, publication venues.
4. **Product signals**: shipped products, benchmarks, partnerships, market presence.

Per-player sampling defaults (Tier 1 with structured retrieval):

- `k = 6` for a focused challenger or niche player
- `k = 8` for a normal Tier 1 / Tier 2 player
- `k = 10` for highly diversified leaders

Two-level sampling rule (when sampling is used):

1. **Sector sample first**: use it to understand routes, terminology, and
   ecosystem structure
2. **Player sample second**: use it to understand each shortlisted player's
   real route emphasis

Never substitute one for the other:

- Sector sample ≠ player proof
- Player sample ≠ sector white-space proof

Adjust analysis emphasis by industry type:

```
Industry type?
├─ Semiconductor → emphasize: process node, EDA/IP, foundry vs fabless split,
│  patent family breadth
├─ Biopharma → emphasize: pipeline stage, target coverage, clinical results,
│  regulatory milestones
├─ AI / Software → emphasize: model benchmarks, open-source presence, API
│  adoption, paper citation impact
├─ New Energy / Materials → emphasize: material routes, production capacity,
│  cost trajectory, supply chain position
└─ General Manufacturing → balanced patent families + standard participation
   + supply chain signals
```

### Step 4: Route Differentiation And White Spaces

1. Build a route differentiation matrix: rows = top players, columns = key
   technology routes or sub-tracks. Cells indicate strength level
   (Strong / Moderate / Emerging / Absent) with brief evidence notes.

Example format:

| Player | Route A | Route B | Route C |
|--------|---------|---------|---------|
| Company X | Strong — 50+ patents, shipped product | Emerging — 3 recent filings | Absent |
| Company Y | Moderate — 15 patents, no product yet | Strong — market leader | Emerging |

2. Identify white spaces — areas that simultaneously satisfy ALL three criteria:
   - **Sparse coverage**: few or no strong players currently active
   - **Clear technical value**: the route addresses a real technical need or
     market demand
   - **Explainable entry path**: a realistic way for a new entrant to build
     capability in this space
3. If a potential white space fails any of the three criteria, do not present
   it as an opportunity — note it as an observation instead.

### Step 5: Synthesis

Synthesize all evidence into the output skeleton. Separate every claim into:

- **Verified fact**: directly supported by patent, paper, or official source
- **Evidence-backed inference**: reasonable conclusion from multiple signals
- **Open gap**: insufficient evidence, state what is missing

## Output Skeleton

### 1. Lead With Conclusion

1-2 sentences: overall sector competitive dynamics — concentration level,
dominant routes, pace of change.

### 2. Player Tiers

Tiered list with 1-line evidence summary per player:

| Tier | Player | Key Evidence |
|------|--------|-------------|
| Leader | Company A | 150+ patents in route X, shipped product Y |
| Challenger | Company B | Growing paper output, niche in route Z |
| ... | ... | ... |

### 3. Route Differentiation Matrix

Markdown table: players (rows) × technology routes (columns).
Cells = strength indicator (Strong / Moderate / Emerging / Absent).

### 4. Top Player Profiles

2-3 paragraphs per top player covering:
- Primary technology route and focus areas
- Key differentiation from other players
- Trajectory and recent moves

### 5. White Spaces And Opportunities

2-3 identified white spaces, each with:
- What the gap is
- Why it has technical value
- How an entrant could realistically build capability there

### 6. Risks And Recommendations

- Sector-level risks (consolidation, regulatory shifts, technology disruption)
- Recommended actions aligned to the user's decision context

Every claim must cite its source type and identifier, e.g., `[Patent: CN1234567B]`,
`[Paper: DOI or title]`, `[Web: source name]`.

## Completion Gates

All must pass before delivering the final answer:

- [ ] Sector scope and geography confirmed
- [ ] At least 3 sector-wide searches executed with results analyzed
- [ ] Player candidate set built from evidence, not assumed from prior knowledge
- [ ] If sector or player patent scopes are broad, representative sampling was
      executed or explicitly skipped with reason
- [ ] If sampling was used, sector sample supported route discovery rather than
      directly deciding final player tiers
- [ ] If player sampling was used, each player was sampled independently
- [ ] Top players deep-dived individually (not merged across players)
- [ ] Route differentiation matrix present with evidence backing per cell
- [ ] White spaces satisfy all 3 criteria (sparse + valuable + entry path)
- [ ] Every major claim has a traceable source citation
- [ ] Verified fact / evidence-backed inference / open gap clearly separated
- [ ] Output follows the 6-part skeleton
- [ ] No tier assigned without patent, paper, or product evidence basis
- [ ] Tool tier and coverage limitations explicitly stated in the output
- [ ] If evidence is insufficient for a complete landscape, deliver "candidate
      tiers + evidence gaps + next evidence-gathering directions" instead of
      forcing completeness

## Guardrails

- Do not merge multiple companies into a single analytical conclusion.
- Do not assign tiers based on brand recognition alone — require patent, paper,
  or product evidence.
- Do not invent white-space opportunities without evidence of sparse coverage.
- For non-evidence dimensions (TCO, regulation, teardown, collaboration networks),
  write "evidence pending" rather than fabricating a judgment.
- Do not mix commercial players with academic institutions or upstream IP sources
  in one comparison matrix unless the split is explicitly noted.
- Keep charts or visual aids to 1-2 maximum; retain only those that directly
  support the analytical conclusion.
- Default TopN should be 5-10 companies; do not inflate the player set beyond
  what the evidence supports.
- Do not use representative sampling for FTO, infringement, or exhaustive
  legal-risk workflows.
- Do not collapse all players into one shared sampled set; sampling,
  interpretation, and synthesis must remain per-player once top players are selected.
- Do not let sector-level sampled patents dominate the narrative of a specific
  player unless that player-level evidence has been separately checked.
- Do not force a strong completeness claim when the tool stack is degraded —
  prefer explicit uncertainty over false confidence.
- Record why a player was included, excluded, or downgraded.

## Optional Host-Specific Automation

Some hosts may provide extra helpers for representative sampling, quantitative
aggregation, or patent-card normalization. These helpers are optional and are
not part of the core open-source contract.

If you use host-specific automation:

- record the helper and its role in `method_decisions.md`
- keep the final evidence compatible with `query_log.csv`, `source_index.csv`,
  and `claim_ledger.csv`
- keep sector-level and player-level helper outputs clearly separated

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
