# Applicant Analysis Prompt

## Task

Analyze the applicant landscape only from a verified population-level aggregation or a clearly bounded partial ranking. Keep representative patents separate and use them only as examples.

## Inputs

- applicant aggregation state: `available`, `partial`, or `unavailable`;
- applicant rows and reported denominator;
- query version, date range, jurisdiction, document type, and family/count rule;
- applicant-name normalization table;
- representative patent sample for examples only; and
- source IDs and limitations.

If the aggregation is unavailable, output an evidence-gap record and do not create an applicant ranking, concentration metric, or chart.

## Analysis dimensions

### 1. Entity normalization

For every displayed applicant:

- preserve the source name;
- map verified aliases and transliterations;
- distinguish current assignee from original applicant;
- distinguish parent, subsidiary, affiliate, university, and research institute;
- state the normalization date and source; and
- keep unresolved entities separate.

Do not merge corporate groups without evidence or across periods when ownership changed.

### 2. Applicant type

Classify only when supported:

- company;
- university;
- public research institution or national laboratory;
- individual;
- consortium or joint applicant;
- government body; or
- unknown.

Do not infer headquarters, nationality, size, or commercial success from a name.

### 3. Concentration

Compute CR3 or CR5 only when:

- the numerator and denominator use the same population;
- the ranking covers at least the relevant top rows;
- aliases are normalized consistently; and
- the count unit is explicit.

Do not calculate HHI from Top 20 rows unless the complete distribution or an explicitly modeled residual is available. Do not apply universal CR5 labels. Interpret concentration relative to coverage, technology boundaries, filing behavior, and the decision context.

### 4. Technical positioning

Identify leaders only using evidence such as:

- population-level filing/family counts;
- classification or subfield coverage under comparable queries;
- recent-period activity under a complete period series;
- representative patents illustrating technical routes; and
- verified collaboration or co-application records.

Call an entity a `high-volume filer`, not a technology or market leader, unless additional evidence supports the broader term.

### 5. New entrants and momentum

Identify a new entrant only when the full time-bounded applicant data shows a first relevant filing or an explicitly defined return after inactivity. Account for name changes, acquisitions, publication lag, and incomplete recent years.

### 6. Collaboration

Analyze joint applications only from applicant records that expose all co-applicants. Separate:

- co-application;
- licensing;
- research funding;
- inventor mobility; and
- corporate affiliation.

Do not infer one relationship from another.

## Output schema

```json
{
  "applicant_analysis": {
    "state": "available | partial | unavailable",
    "scope": {
      "query_version": "",
      "period": {},
      "jurisdictions": [],
      "count_unit": "",
      "denominator": null,
      "coverage": ""
    },
    "normalization": [
      {"source_name": "", "canonical_name": "", "aliases": [], "relationship": "", "source_id": "", "confidence": ""}
    ],
    "rows": [
      {
        "rank": 1,
        "canonical_name": "",
        "source_names": [],
        "count": null,
        "share": null,
        "entity_type": "company | university | research_institution | individual | consortium | government | unknown",
        "technical_positioning": [],
        "representative_patents": [],
        "source_ids": [],
        "limitations": []
      }
    ],
    "cr3": {"value": null, "state": "calculated | unavailable", "method": ""},
    "cr5": {"value": null, "state": "calculated | unavailable", "method": ""},
    "hhi": {"value": null, "state": "calculated | unavailable", "method": ""},
    "new_entrants": [],
    "collaboration_patterns": [],
    "observations": [],
    "evidence_gaps": [],
    "limitations": []
  }
}
```

## Writing rules

- Use `applicant` for filing records and `current assignee` only when that field was retrieved.
- Qualify Top-N coverage.
- Do not use sample frequencies as shares.
- Do not call patent volume market share.
- Do not split “domestic” and “international” without a defined focal region.
- Attach a claim ID and source ID to every material conclusion.
- If unavailable, explain what connector capability or denominator is missing.

## Quality checks

- Entity aliases are documented.
- Numerators and denominators reconcile.
- Partial rankings are labeled partial.
- HHI is not computed from incomplete rows.
- Representative patents are illustrative only.
- Filing leadership is not equated with commercial leadership.
- Recent-period observations include a publication-lag caveat.
- All displayed facts have source IDs.
