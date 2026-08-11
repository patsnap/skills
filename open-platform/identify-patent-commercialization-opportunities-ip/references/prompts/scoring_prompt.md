# Scoring Prompt

## Task

Create a transparent decision-support score without converting patent metrics into a definitive investment, market-entry, or commercialization verdict.

## Governing rules

- Use a score only when the user wants a prioritization aid.
- Preserve raw metrics and narrative findings beside every score.
- Treat missing evidence as missing, not zero.
- Do not reweight available dimensions silently to hide missing dimensions.
- Document weights, thresholds, transformations, directionality, and sensitivity.
- Separate patent evidence from technical, market, regulatory, supply-chain, financial, and strategic evidence.
- Label the result a screening score, not expected return, market attractiveness, or probability of success.

## Source six dimensions

Preserve the six source dimensions but localize their meaning:

### 1. Patent activity direction — source maximum 20

Consider complete period counts, growth calculation quality, base size, publication lag, and volatility. Do not use universal CAGR bands. Define context-specific anchors and show the raw series.

### 2. Applicant activity and diversity — source maximum 15

Use only verified population-level applicant data. Distinguish volume, diversity, concentration, and new entrants. If unavailable, mark the dimension unavailable; do not use representative sample frequencies.

### 3. Patent influence and evidence quality — source maximum 15

Use age- and jurisdiction-aware citations, family coverage, claim/status evidence, and representative record review. Do not call this technical quality or product quality. Do not calculate an active rate from a sample.

### 4. Subfield opportunity evidence — source maximum 20

Use validated subfield counts, trends, technical problems, search sensitivity, commercial evidence, and risk gaps. Do not score scarcity as positive by default.

### 5. Competitive/IP risk — source maximum 15, direction reversed

Use valid concentration data, relevant current claims, portfolio density, FTO questions, litigation/licensing signals, standards exposure, and uncertainty. Patent count alone is not an entry barrier.

### 6. International and commercialization signals — source maximum 15

Separate international patent-family behavior from verified commercialization evidence. PCT or multi-jurisdiction filings are cost-bearing intent signals, not proof of sales, adoption, licensing, or market demand.

## Evidence completeness gate

For each dimension classify:

- `scored`: sufficient comparable evidence;
- `provisional`: material evidence gaps but a bounded score is useful;
- `unavailable`: insufficient evidence; or
- `not_applicable`: irrelevant to the decision.

Do not produce a single total without showing missing weight. Report:

- achieved points;
- scored-weight denominator;
- missing or provisional weight;
- normalized score only if requested; and
- sensitivity across plausible assumptions.

## Recommendation states

Use evidence-qualified states:

- `Prioritize for next-stage diligence`;
- `Proceed selectively with defined validation gates`;
- `Monitor pending additional evidence`;
- `Deprioritize under current assumptions`; or
- `Insufficient evidence to prioritize`.

Do not map fixed totals such as 75/50 to universal investment decisions. If a user-approved policy contains thresholds, cite that policy and preserve the raw score.

## Output schema

```json
{
  "scoring_result": {
    "rubric_version": "",
    "decision_context": "",
    "dimensions": [
      {
        "id": "D1",
        "name": "Patent activity direction",
        "source_weight": 20,
        "applied_weight": 20,
        "state": "scored | provisional | unavailable | not_applicable",
        "raw_metrics": [],
        "score": null,
        "transformation": "",
        "reasoning": "",
        "source_ids": [],
        "limitations": []
      }
    ],
    "achieved_points": null,
    "scored_weight": null,
    "missing_or_provisional_weight": null,
    "normalized_score": null,
    "normalization_note": "",
    "sensitivity": [
      {"scenario": "conservative | base | optimistic", "score": null, "changed_assumptions": []}
    ],
    "recommendation_state": "",
    "recommendation_reason": "",
    "patent_evidence_confidence": "high | medium | low",
    "commercial_evidence_confidence": "high | medium | low",
    "main_opportunities": [],
    "main_risks": [],
    "evidence_gaps": [],
    "next_validation_gates": [],
    "limitations": []
  }
}
```

## Confidence rules

Use high confidence only when every material metric is reproducible, complete, semantically comparable, and supported by source IDs. Bucketed counts can be high-confidence when complete and consistent; aggregation is not inherently superior.

Lower confidence for:

- partial applicant/geography/status coverage;
- query sensitivity;
- family duplication;
- publication lag;
- sparse or age-biased citations;
- unverified commercialization claims;
- inferred technical readiness;
- missing regulatory or market evidence; and
- large score sensitivity.

## Quality checks

- The source six dimensions remain visible.
- Weight and score arithmetic reconcile.
- Missing data is not zero.
- No sample statistic enters a population dimension.
- Patent activity is not called market growth.
- Patent influence is not called product quality.
- International filings are not called commercialization.
- Recommendation state follows evidence and stated policy.
- Sensitivity and missing weight are visible.
- Every dimension cites sources and limitations.
