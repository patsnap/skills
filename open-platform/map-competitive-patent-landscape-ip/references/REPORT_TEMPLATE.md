# Competitive patent landscape report template

## Contents

1. Executive landscape and conclusions
2. Competitor deep dives
3. Representative patent reviews
4. Geographic strategy comparison
5. Strategic implications and opportunity windows

## Chapter 1: Executive landscape and conclusions

Place the decision summary before the charts.

Include three evidence-backed technology trends.

Include a competitor positioning table.

Include one concise synthesis statement.

Then show the competitive-landscape bubble chart and portfolio-size bar chart.

Every metric must state its counting unit, date basis, time period, jurisdiction scope, and denominator.

Do not equate document count with portfolio strength.

### Competitor positioning table

| Competitor | Main technology bets | Evidence | Relative activity | Opportunity status | Confidence |
|---|---|---|---|---|---|

Use text labels rather than color-only badges:

- `Constrained`: dense, relevant activity with corroborating evidence; entry likely requires differentiation, licensing, or further diligence.
- `Time-sensitive`: recent acceleration with identifiable but narrowing technical space; state the evidence for any estimated period.
- `Open hypothesis`: comparatively sparse observed activity; requires validation beyond the retrieved sample.
- `Monitor`: early or ambiguous signal that does not yet support action.

Never assert a fixed 12–18-month window unless filing cadence, product timing, technical maturity, and market evidence support it.

## Chapter 2: Competitor deep dives

Create one technical-strategy section per competitor.

Include:

- Resolved legal entities and aliases.
- Retrieved sample and estimated or verified portfolio scope.
- Technology-cluster distribution.
- Three leading technology bets when evidence supports three.
- Representative publication numbers.
- Technical rationale.
- Geography and family behavior.
- Implications for the named client.
- Uncertainty and counter-evidence.

Use evidence tables instead of decorative brand cards.

Do not infer product launches from patent filings alone.

Label forward-looking statements as hypotheses.

## Chapter 3: Representative patent reviews

Review two or three representative records per competitor when the dataset supports that number.

For each record, include:

- Publication number.
- Title.
- Applicant and current assignee when available.
- Earliest priority date.
- Filing and publication dates.
- Simple legal status and retrieval date.
- Family and jurisdiction path.
- Technical problem, solution, and benefit.
- Independent-claim or disclosure focus.
- Reason for selection.
- Strategic interpretation and its confidence.
- Direct source link.

Selection must combine relevance, recency, family/geographic signal, claim substance, and citation context.

Do not rank solely by forward citations.

Do not use a pill-shaped number label or decorative icon as the only identifier.

## Chapter 4: Geographic strategy comparison

Show a competitor-by-jurisdiction matrix.

Distinguish priority origin, filing office, publication authority, designated state, and commercial market.

Compare family-normalized activity where possible.

Explain whether differences reflect strategy, procedural routes, data coverage, or sample bias.

Include focused cross-market comparisons requested by the user.

Use a labeled heatmap only when cell values and denominators are available.

Provide an accessible data table alongside every heatmap.

## Chapter 5: Strategic implications and opportunity windows

Present up to three supported opportunity hypotheses.

For each, include:

- Technical space.
- Evidence of unmet or underrepresented activity.
- Competitor proximity.
- Adjacent prior art.
- Client capability fit.
- Market or product evidence.
- Key uncertainty.
- Validation action.
- Decision owner and timing.

Include a time-window table and three to five prioritized actions.

Use `Constrained`, `Time-sensitive`, `Open hypothesis`, or `Monitor` as text.

Do not use red, yellow, green, gray, or emoji as the sole meaning.

## Scientific HTML pattern

Use semantic HTML5 with a light, restrained executive-scientific design.

Use a white background, charcoal text, one muted accent color, and neutral rules.

Use a system-font stack.

Use sentence-case headings.

Avoid gradients, decorative shadows, oversized cards, emoji, and yellow callout boxes.

Give every chart a title, caption, source note, unit, denominator, and accessible companion table.

Use direct labels when practical.

Use a zero baseline for magnitude-comparison bar charts unless a justified exception is disclosed.

Make status and series distinctions understandable in monochrome.

Add responsive behavior for navigation, tables, and charts.

Add print CSS that exposes all report sections and preserves sources.

## Executive insight block

```html
<section class="executive-findings" aria-labelledby="executive-findings-title">
  <h2 id="executive-findings-title">Executive findings</h2>
  <ol class="findings-list">
    <li><strong>Finding:</strong> Evidence-backed conclusion. <span class="confidence">Confidence: medium</span></li>
  </ol>
  <table>
    <caption>Competitor positioning; family-normalized publications, retrieval cut-off YYYY-MM-DD</caption>
    <thead>
      <tr><th>Competitor</th><th>Technology bet</th><th>Evidence</th><th>Status</th><th>Confidence</th></tr>
    </thead>
    <tbody><!-- Evidence-backed rows --></tbody>
  </table>
  <p class="synthesis"><strong>Synthesis:</strong> One decision-relevant conclusion with limitations.</p>
</section>
```

## Client implication block

```html
<aside class="client-implication" aria-labelledby="client-implication-title">
  <h3 id="client-implication-title">Implication for [client name]</h3>
  <p>State the opportunity or risk, supporting evidence, confidence, and next validation action.</p>
</aside>
```

Do not copy stale client names or source examples into a new report.

Do not show a metric or conclusion without traceable supporting data.
