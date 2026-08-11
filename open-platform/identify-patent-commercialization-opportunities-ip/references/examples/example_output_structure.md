# Example Output Structure

## Generated report directory

```text
output/
├── index.html
├── patents.html
├── evidence.html
├── subfields.html
├── methodology.html
├── intermediate_data.json
├── patent_list.csv
├── evidence_mapping.csv
├── README.md
└── quality_check.md
```

The skill package contains no Python files or `scripts/` directory, and the generated report must not add them. Generated artifacts stay outside the skill package.

## Artifact roles

| Artifact | Role |
|---|---|
| `index.html` | Executive 15-module assessment with reproducible metrics, evidence-qualified recommendation, risks, and validation gates |
| `patents.html` | Representative patent sample with safe search, filtering, and pagination |
| `evidence.html` | Claim-to-evidence register with assumptions, counterevidence, and limitations |
| `subfields.html` | Four to eight subfield assessments with overlap and evidence gaps |
| `methodology.html` | Search versions, count semantics, sample boundary, scoring, QA, and limitations |
| `intermediate_data.json` | Authoritative structured report data and source register |
| `patent_list.csv` | Representative patent records only |
| `evidence_mapping.csv` | Stable claim-to-evidence rows |
| `README.md` | User instructions, data boundaries, and artifact manifest |
| `quality_check.md` | Completed release audit and unresolved limitations |

## Example final handoff

```text
Patent-opportunity assessment completed: [Technology topic]

Screening recommendation: [Prioritize for next-stage diligence / Proceed selectively / Monitor / Deprioritize / Insufficient evidence]
Patent-evidence confidence: [High / Medium / Low]
Commercial-evidence confidence: [High / Medium / Low]
Decision cutoff: [YYYY-MM-DD]
Count basis: [publication/application/family rule]

Core findings
1. [Bounded finding] [T001]
2. [Bounded finding] [S001]
3. [Bounded finding] [O001]
4. [Bounded risk] [K001]
5. [Next validation gate] [R001]

Generated artifacts
- index.html — executive assessment
- patents.html — representative sample
- evidence.html — claim/evidence register
- subfields.html — subfield assessment
- methodology.html — methods and limitations
- intermediate_data.json — structured data
- patent_list.csv — representative patents
- evidence_mapping.csv — evidence mapping
- README.md — usage and data notes
- quality_check.md — completed QA audit

Data statement
- Population metrics: [verified aggregation / complete buckets / unavailable]
- Representative sample: used only for examples and qualitative evidence
- Omitted aggregations: [applicant/geography/status/etc.] because [coverage reason]
- Publication-lag period: [periods]
- Main evidence gaps: [list]

Open index.html for the executive report, evidence.html for traceability, and methodology.html for the full data definition.
```

## Handoff rules

- Do not claim a fixed score when dimensions are unavailable.
- Do not call patent filing growth market growth.
- Do not claim “all data” without defining the population and denominator.
- Do not mention a chart that was omitted.
- Do not state a minimum patent count was achieved when fewer valid records exist.
- List exactly the files that were actually generated.
- Link findings to stable claim IDs.
- State both patent and commercial evidence confidence.
- Preserve limitations and next validation gates.

## Output verification

- Exactly ten required artifacts exist.
- All five HTML pages navigate to each other.
- JSON and CSV parse.
- Every displayed claim ID resolves.
- Every displayed patent resolves in the representative data.
- The QA decision supports the completion statement.
