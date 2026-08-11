# Subfield Analysis Prompt

## Task

Divide the accepted technology scope into four to eight decision-useful subfields and assess each using independently validated, scope-consistent evidence.

## Subfield design

Choose dimensions appropriate to the domain:

- materials: chemistry, structure, functional property, manufacturing, application;
- energy: component, mechanism, performance problem, process, integration;
- life sciences: modality, target/mechanism, indication, delivery, formulation, manufacturing;
- chemistry: reaction route, catalyst, feedstock, product form, end use;
- electronics: device, architecture, protocol, algorithm, manufacturing, application;
- software: technical mechanism, data flow, system architecture, deployment, measurable technical effect.

Create four to eight subfields when the evidence supports that resolution. Do not force mutual exclusivity if the technology is inherently cross-cutting. Instead, document overlap and prohibit summing overlapping counts.

Each subfield requires:

- concise English name;
- operational definition;
- included concepts;
- explicit exclusions;
- independently tested query;
- known overlaps;
- comparable period/jurisdiction/family rules; and
- validation sample.

## Evidence collection

For each subfield:

1. retrieve a population count or mark it unavailable;
2. retrieve a complete comparable time series when available;
3. retrieve applicant distribution only from a verified aggregation;
4. select representative patents for technical illustration only;
5. record publication lag, count semantics, and query version;
6. identify search sensitivity and overlap; and
7. gather non-patent commercialization evidence when a commercial recommendation is requested.

## Assessment dimensions

Evaluate separately:

- observable patent activity;
- activity direction over complete periods;
- applicant concentration when valid;
- technical differentiation and unresolved problems;
- representative patent relevance and evidence quality;
- technical readiness evidence;
- market/customer evidence;
- regulatory and standards dependencies;
- supply-chain and manufacturing constraints;
- FTO or blocking-right uncertainty; and
- fit with the user's capabilities and decision.

Patent scarcity is not automatically white space. It may reflect poor search construction, terminology, low feasibility, alternative protection, weak economics, regulatory barriers, or an immature field.

## Recommendation states

Use:

- `Prioritize for validation`;
- `Monitor / targeted diligence`;
- `Deprioritize under current assumptions`; or
- `Insufficient evidence`.

Do not issue `enter` or `do not enter` from patent metrics alone.

## Output schema

```json
{
  "subfield_analysis": [
    {
      "subfield_id": "SF01",
      "name": "",
      "definition": "",
      "included_concepts": [],
      "exclusions": [],
      "query_version": "",
      "query": {},
      "overlap_with": [{"subfield_id": "", "note": ""}],
      "count": {"value": null, "state": "available | partial | unavailable", "count_unit": "", "source_ids": []},
      "trend": {"state": "available | partial | unavailable", "cagr": null, "description": "", "source_ids": []},
      "applicant_landscape": {"state": "available | partial | unavailable", "description": "", "source_ids": []},
      "representative_patents": [],
      "technical_opportunities": [],
      "technical_risks": [],
      "commercial_evidence": [],
      "commercial_gaps": [],
      "regulatory_or_standards_factors": [],
      "manufacturing_or_supply_factors": [],
      "fto_questions": [],
      "assessment": {
        "state": "prioritize_validation | monitor_targeted_diligence | deprioritize_current_assumptions | insufficient_evidence",
        "reason": "",
        "confidence": "high | medium | low",
        "next_validation": []
      },
      "source_ids": [],
      "limitations": []
    }
  ]
}
```

## White-space rules

Call an area a `candidate opportunity` rather than white space unless:

- the query is validated;
- adjacent terminology and classifications were searched;
- relevant jurisdictions and periods are covered;
- low counts persist under sensitivity tests;
- representative patents were reviewed;
- non-patent barriers were considered; and
- the conclusion is framed as bounded and time-sensitive.

## Quality checks

- There are four to eight meaningful subfields or a documented reason for another number.
- Every subfield has a tested query and exclusions.
- Counts have identical semantics where compared.
- Overlap is explicit.
- Overlapping counts are not summed.
- Sample patents do not determine population trends.
- Recommendations include commercial and technical evidence gaps.
- Each conclusion has claim and source IDs.
