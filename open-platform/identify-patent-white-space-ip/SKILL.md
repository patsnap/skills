---
copyright: "Copyright © Patsnap. All rights reserved."
name: identify-patent-white-space-ip
description: Identify candidate patent white-space signals from a patent map, technology-effect matrix, technology-application matrix, cluster map, roadmap, or sparse portfolio region; test whether the signal is a search or classification artifact; assess the value of the underlying problem; diagnose route breaks and primary contradictions; and propose two to four principle-level resolution directions. Use for structured innovation-opportunity exploration from patent-map evidence. Require explicit user confirmation after candidate selection and after problem-value assessment; do not perform downstream technical validation, commercial validation, FTO, patentability, or filing-strategy justification.
---

# Identify patent white-space opportunities

## Purpose

Start from low-density or structurally unusual signals in a patent map.

Determine whether a signal may correspond to an important problem.

Explain why the sparse area may persist.

Diagnose the route break and primary contradiction.

Generate principle-level resolution directions grounded in that diagnosis.

Treat every white-space result as a hypothesis until validated.

## Required references

Read [references/evaluation-framework.md](references/evaluation-framework.md) when ranking candidates or assessing problem value.

Read [references/output-templates.md](references/output-templates.md) before presenting either confirmation point, a stage result, or the final report.

No README exists in the source package.

Do not create or depend on one.

## Core definitions

Keep four objects separate throughout the analysis.

### Candidate white-space signal

A statistically or structurally sparse area observed in a patent map or underlying dataset.

It is not yet an opportunity.

### Underlying problem

An important task, need, constraint, or outcome that may be insufficiently addressed in the sparse area.

### Primary contradiction

The conflict, trade-off, or missing mechanism that best explains why an important problem remains insufficiently solved.

### Resolution direction

A principle-level path that acts on the diagnosed contradiction.

It is not a validated technical solution, commercial opportunity, patentable invention, or filing recommendation.

## Non-negotiable rules

Do not equate low patent count with high opportunity value.

Test obvious false-space explanations before deep analysis.

Do not use TRIZ before diagnosing a causal contradiction.

Do not select a TRIZ principle and then invent a problem to fit it.

Separate facts, retrieved evidence, inference, uncertainty, and recommendation.

Show supporting and opposing explanations at every stage.

Stop at both mandatory user confirmation points.

Do not choose a candidate on the user’s behalf.

Do not continue to contradiction diagnosis without confirmation of problem value.

Do not perform technical feasibility validation.

Do not perform commercial validation.

Do not perform patentability analysis.

Do not perform FTO analysis.

Do not justify a patent filing or portfolio strategy.

## Inputs

Prefer user-provided evidence.

Request missing information only when it blocks a defensible stage.

Collect:

1. Patent map, matrix, cluster plot, roadmap, or underlying patent dataset.
2. Meaning of rows, columns, clusters, bubble size, color, and other visual encodings.
3. Time period and data cut-off.
4. Date basis: priority, filing, publication, or grant.
5. Counting unit: publication, application, simple family, extended family, or another unit.
6. Family-deduplication method.
7. Search query and exclusions.
8. Classification or tagging method.
9. Target industry, market, business context, and decision.
10. Known industry problems, incumbent routes, and expert judgments.

If only an image is supplied, state which interpretations are provisional.

Do not infer raw values that are unreadable from the image.

## Patsnap MCP plan

This skill can operate from a user-provided map without live MCP access.

Use MCP only when the user authorizes bottom-level patent validation or additional retrieval.

### Recommended: Advanced Patent Search

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-search

Verified 2026-08-07.

Configuration key: `advanced_patent_search`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Use documented capabilities as appropriate:

- `search_patent_count` for actual count checks.
- `search_patent_field` for distributions.
- `search_patents_nested` for query validation.
- `search_patents_by_semantic` for alternative-language and conceptual checks.
- `search_patent_by_pn` for known-counterexample verification.
- Assignee search for missing-player checks.
- `suggest_keywords` for terminology expansion.

### Optional: Patent Briefing

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Verified 2026-08-07.

Configuration key: `patent_briefing`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use bibliography, family, legal status, claims, descriptions, drawings, and technical summaries to examine counterexamples or representative records.

### MCP fallback

If MCP is unavailable, continue from supplied map evidence only when sufficient.

Label patent-level validation `not executed`.

List the queries and checks required to validate the signal.

Do not fabricate counts, records, families, status, or classifications.

## Workflow

### Stage 0: Define the decision objective

Clarify whether the user needs to:

- Find candidate sparse areas.
- Judge the value of an underlying problem.
- Explain why the sparse area persists.
- Diagnose a contradiction.
- Generate principle-level resolution directions.

Show:

- Decision objective.
- Scope.
- Map construction.
- Assumptions.
- Available evidence.
- Missing evidence.
- The endpoint of this analysis.
- Explicitly excluded downstream work.

### Stage 1: Identify candidate white-space signals

Use actual patent counts and map structure.

Consider:

- Zero or low observed count.
- Active adjacent dimensions with a sparse intersection.
- Small base with accelerating growth.
- A gap between technology clusters.
- A missing connection in a plausible technical route.
- Missing important applicants, applications, effects, or use cases inside an active field.

Check quickly whether the signal may result from:

- Search terms.
- Spelling or translation variants.
- Classification rules.
- Tagging method.
- Family deduplication.
- Date basis.
- Time window.
- Database coverage.
- Delayed publication.
- Trade secrecy or non-patent protection.
- A different technical expression.

When underlying data is unavailable, mark these as validation risks.

Do not claim a complete false-space search was performed.

Use the evaluation framework to rank candidates.

Display at most seven candidates unless the user asks for more.

### Candidate table

| Candidate white-space signal | Actual patent count | Selection rationale | Possible underlying problem | Main false-space risk | Preliminary priority | Confidence |
|---|---:|---|---|---|---|---|

Do not calculate or display:

- Expected count derived from row or column totals.
- Predicted count.
- Actual as a percentage of expected.
- Opportunity probability from the score.

These measures depend on assumptions that can create false precision.

### Mandatory confirmation point 1

Recommend a candidate and explain the evidence.

Do not make the selection.

Use this pattern:

> I identified the candidate white-space signals above. I recommend examining [candidate] first because [reason]. Please confirm which candidate you want to investigate in depth. You may select more than one, and I will analyze each separately.

Stop and wait for explicit confirmation.

Do not enter Stage 2 before confirmation.

### Stage 2: Rapidly test obvious false-space explanations

For each selected candidate, test:

- Terminology differences.
- Classification differences.
- Alternative technical expressions.
- Family-counting artifacts.
- Time-window artifacts.
- Database gaps.
- Clear counterexamples in adjacent areas.
- Trade-secret or non-patent explanations.

Show:

- Checks performed.
- Evidence supporting the sparse-signal hypothesis.
- Evidence opposing it.
- Unexecuted checks.
- Whether deeper analysis is justified.
- Confidence and reservations.

If the signal is clearly an artifact, stop.

Explain the cause.

Return to Stage 1.

### Stage 3: Evaluate the underlying problem’s value

Define:

- Stakeholder.
- Use context.
- Job to be done.
- Current route or alternative.
- Desired outcome.
- Measurable consequence.

Assess:

- Severity.
- Frequency.
- Affected scope.
- Economic, safety, compliance, performance, or strategic consequence.
- Weakness of existing alternatives.
- Motivation to solve.
- Future trajectory.

Use map signals, domain evidence, standards, market or operational evidence, and user expertise.

Do not use patent count alone.

Use the Problem-value brief in the output templates.

Include supporting evidence, counter-evidence, score, confidence, and the evidence that would change the result.

### Mandatory confirmation point 2

Use this pattern:

> The current assessment is that [problem] has [High/Medium/Low] value because [evidence]. The largest uncertainty is [uncertainty]. Please confirm whether this matches your domain knowledge and whether I should continue to contradiction diagnosis and resolution-direction generation.

Stop and wait for explicit confirmation.

If the user disagrees, revise the problem definition or gather more evidence.

Do not enter Stage 4 without confirmation.

### Stage 4: Diagnose causes and contradictions

Map existing solution routes.

For each route explain:

- What it improves.
- What it sacrifices.
- Which constraint it encounters.
- Which mechanism is missing.
- Why it cannot reach the target outcome.

Show the route break separately:

```text
What Route A achieves
-> missing connection, conversion, sensing, control, data, or feedback mechanism
-> what Route B cannot obtain
-> unresolved target problem
```

Write the primary contradiction in testable form:

> To improve [A], the system must change [X], but that change degrades [B]; the objective requires improving both [A] and [B] under constraint [C].

Distinguish:

- Primary contradiction.
- Secondary contradictions.
- Technical contradiction.
- Physical contradiction where applicable.
- Resource constraints.
- Cost constraints.
- Regulatory constraints.
- Ecosystem and commercial-model constraints.

Show the root-cause mechanism and confidence.

### Stage 5: Identify possible enabling conditions

Consider:

- New algorithms.
- New materials.
- New sensors.
- New data.
- New control architecture.
- New infrastructure.
- New standards.
- Falling costs.
- Increasing technology readiness.
- Cross-domain mechanisms.
- Regulatory change.
- Market incentives.
- Business-model change.

Identify conditions only.

Do not validate maturity, feasibility, cost, adoption, or regulatory acceptance.

### Stage 6: Generate resolution directions

Start from the diagnosed contradiction.

Use:

- TRIZ separation principles and inventive principles.
- Cross-domain analogy and technology transfer.
- Recombination of adjacent mature capabilities.
- Substitution.
- Virtualization.
- Closed-loop control.
- Mechanism-and-data integration.

Generate two to four directions.

For each show:

```text
Root barrier
-> resolution principle
-> possible technical mechanism
-> how the mechanism reduces the contradiction
-> limitation or new risk
```

Do not submit “use AI,” “create a digital twin,” or another broad label without a causal mechanism.

Do not present a direction as validated.

### Stage 7: Create the contradiction and resolution report

Use the output templates.

Include:

- Candidate signal and map basis.
- Map construction and actual values.
- False-space checks.
- Problem-value judgment.
- Supporting and opposing evidence.
- Existing routes.
- Route break.
- Root cause.
- Primary and secondary contradictions.
- Technical and physical contradictions.
- Nontechnical barriers.
- Possible enabling conditions.
- Two to four resolution directions.
- Logic and limitation for every direction.
- Confidence.
- Unresolved questions.
- Excluded downstream validation.

End with:

> [Candidate white-space signal] deserves further attention because it appears to correspond to [important problem]. The signal may persist because [limitations of existing routes], and the primary contradiction is [contradiction]. [Resolution principle and technical mechanism] could reduce this contradiction, but [main limitation or unknown] still requires validation.

### Stage 8: Generate a self-contained HTML report

After Stage 7, create a self-contained HTML report without requiring a separate request.

Use a safe workspace directory.

Use filename:

`whitespace-[topic-keyword]-report.html`

Do not assume `@session/reports/` exists.

The report must include:

1. Title and executive summary.
2. Analysis topic, map name, selected signal, decision scope, and analysis date.
3. Complete technology-effect or other source matrix with actual values.
4. A selected-cell annotation visible without color.
5. Complete candidate table.
6. Rapid false-space check with supporting and opposing evidence.
7. Problem-value brief and six-dimension scoring table.
8. Existing-route comparison and route-break flow.
9. Primary, physical, secondary, and nontechnical contradictions.
10. Possible enabling conditions.
11. Resolution-direction comparison.
12. Evidence chain from map anomaly to resolution direction.
13. Standardized conclusion.
14. Confidence, unknowns, sources, methodology, and excluded downstream work.

## Scientific visual standard

Use semantic HTML5.

Use `lang="en"`.

Use a white background, charcoal text, restrained blue accent, and neutral borders.

Use an English system-font stack.

Use sentence-case headings.

Use responsive navigation rather than a permanently fixed sidebar on narrow screens.

Use accessible tables with captions and headers.

Use alternating rows only when contrast remains accessible.

Highlight the selected matrix cell with a border, text label, and annotation—not color alone.

Show matrix legend, counting unit, date basis, period, and sources.

Use print CSS.

Do not use a dark technology theme.

Do not use decorative cards, gradients, emoji, or color-only priority markers.

Do not target an arbitrary 30–60 KB file size.

Let evidence and accessibility determine file size.

## Stage display requirement

At the end of every completed stage, show:

1. Scope checked.
2. Strongest supporting evidence.
3. Counter-evidence and alternative explanation.
4. Reasoning.
5. Stage conclusion.
6. Confidence and unknowns.
7. Next decision.

Keep the main conclusion concise.

Place detailed scoring and evidence tables after it.

## Validation checklist

- Source map and underlying values are traceable.
- Counting unit, family method, date basis, period, and cut-off are stated.
- At most seven candidates are shown unless requested otherwise.
- Candidate table uses actual counts only.
- No expected-count or actual/expected metric appears.
- False-space risks are tested or marked unexecuted.
- Problem value is supported beyond patent counts.
- Both user confirmation gates were honored.
- Route comparison precedes contradiction diagnosis.
- Primary contradiction is causal and testable.
- TRIZ follows diagnosis.
- Each resolution direction acts on the contradiction.
- Each direction includes a limitation or new risk.
- Technical, commercial, patentability, FTO, and filing validation remain excluded.
- HTML includes every required analytical section.
- Visual encoding remains understandable without color.
- Report path exists before being reported.

## Final response

State the selected signal, underlying problem, primary contradiction, and strongest resolution direction as a hypothesis.

State confidence and the evidence most likely to change the conclusion.

Link the HTML report.

List its chapters.

State the excluded downstream validation steps.
