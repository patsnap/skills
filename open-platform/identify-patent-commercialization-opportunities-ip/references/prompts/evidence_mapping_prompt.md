# Evidence Mapping Prompt

## Task

Create a reproducible mapping between every material report claim and the exact evidence, calculation, reasoning, assumptions, and limitations supporting it.

## Evidence record

```json
{
  "claim_id": "T001",
  "claim_type": "trend | applicant | region | influence | subfield | opportunity | score | risk | recommendation",
  "claim_text": "bounded report statement",
  "evidence_state": "supported | partially_supported | unsupported | conflicting",
  "source_ids": ["SRC001"],
  "data_values": [{"metric": "", "value": null, "unit": "", "scope": ""}],
  "supporting_patents": ["US..."],
  "calculation": "",
  "reasoning": "",
  "assumptions": [],
  "counterevidence": [],
  "limitations": [],
  "confidence": "high | medium | low",
  "report_locations": []
}
```

## Source record

Every `source_id` must resolve to a source register containing:

- connector and live tool or external source;
- exact query/request and filters;
- query version;
- execution/access timestamp;
- date field and period;
- jurisdictions and document types;
- publication/family count unit;
- returned versus matched counts;
- patent number, claim, page, paragraph, or record locator when applicable;
- language and translation provenance;
- coverage; and
- limitations or errors.

## Required claim coverage

Create claims only when relevant and supported. Do not force a minimum claim from an unavailable metric.

### Trend claims

- activity direction;
- growth or change calculation;
- publication-lag limitation; and
- relevant regional comparison.

### Applicant claims

- concentration or diversity only from valid aggregation;
- technical positioning with correct qualification; and
- normalization limitations.

### Region claims

- state whether the basis is authority, priority origin, applicant origin, or another field;
- do not call it market share or technology-source share without additional evidence.

### Influence claims

- use age/jurisdiction-adjusted metrics where possible;
- call the result patent influence, not technical quality or commercial success.

### Subfield and opportunity claims

- link each prioritized subfield to count/trend/search evidence;
- link each candidate opportunity to search sensitivity and non-patent evidence gaps;
- preserve overlap and uncertainty.

### Score and recommendation claims

- map each dimension to raw metrics and transformation;
- record missing weight and sensitivity;
- distinguish screening recommendation from investment advice.

## Confidence rubric

### High

- source population and denominator are defined;
- retrieval is reproducible;
- data is complete and semantically comparable;
- reasoning is direct;
- no material counterevidence is unresolved.

### Medium

- evidence is partial or requires a bounded inference;
- some comparability or coverage limitations remain;
- representative patents illustrate but do not establish population behavior.

### Low

- claim depends mainly on analyst hypothesis, indirect data, partial coverage, or unresolved conflict.

Never label an unsupported claim as low-confidence evidence. Mark it `unsupported` and remove or reframe it.

## Identifier rules

Use prefixes:

- `T` — trend;
- `A` — applicant;
- `G` — geographic;
- `I` — influence;
- `S` — subfield;
- `O` — candidate opportunity;
- `R` — score/recommendation;
- `K` — risk; and
- `M` — methodology.

IDs must be stable across HTML, JSON, and CSV. They need not be globally consecutive across types, but no ID may be duplicated or orphaned.

## Output requirements

- Populate `intermediate_data.json.evidence_mapping`.
- Populate `evidence_mapping.csv` with one row per claim and serialized stable-ID lists.
- Show the full mapping in `evidence.html`.
- Place the claim ID and concise source note next to every material statement in `index.html` and `subfields.html`.
- Link representative patents to stable global PatSnap or public patent URLs when available.

## Quality checks

- Every material claim has one stable ID.
- Every source ID resolves.
- Data values preserve units and scope.
- Calculations are reproducible.
- Assumptions and limitations are explicit.
- Counterevidence is not omitted.
- Sample evidence is labeled sample evidence.
- Unsupported claims are removed or reframed.
- Claim IDs reconcile across HTML, JSON, and CSV.
- No real API key, local path, or unstable signed URL appears.
