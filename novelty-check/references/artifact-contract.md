# Novelty Artifact Contract

Use this file whenever you create, update, or validate required artifacts.

## General Rules

- Reuse stable element IDs such as `E1`, `E2`, `E3` across all artifacts.
- Reuse one stable identifier for the strongest D1 candidate across `prior_art_catalog.json`, `element_mapping.md`, `claim_diff_matrix.md`, and `novelty_report.md`.
- If a field is unresolved, write `unknown` or `uncertain`; do not leave silent gaps.
- Allowed novelty outcomes are:
  - `novelty_rejected`
  - `novelty_preserved`
  - `uncertain`

## `claim_elements.md`

Required columns:

| Field | Meaning |
| --- | --- |
| `Element ID` | Stable element label |
| `Claim source` | Claim number and inherited path if dependent |
| `Text` | Limitation text |
| `Type` | `structural`, `functional`, `parameter`, `process`, or `environment` |
| `Variants` | Synonyms, abbreviations, term variants |
| `Search anchor` | Best query hook |
| `Risk note` | Any limiting-language uncertainty |

Canonical example:

| Element ID | Claim source | Text | Type | Variants | Search anchor | Risk note |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | claim 1 | porous substrate | structural | porous base, support layer | substrate + pore | low |
| E2 | claim 1 | pore size 0.2-0.5 um | parameter | pore diameter | 0.2 0.5 um | range overlap risk |

## `prior_art_catalog.json`

Top-level fields:

- `claim_set`
- `critical_date`
- `jurisdiction`
- `queries`
- `candidates`

Allowed candidate `status` values:

- `queued`
- `fetched`
- `read`
- `excluded`
- `blocked`

Minimal shape:

```json
{
  "claim_set": ["claim 1"],
  "critical_date": "2024-05-18",
  "jurisdiction": "US",
  "queries": [
    {
      "round": 1,
      "purpose": "broad recall",
      "query": "porous substrate pore size 0.2 0.5 um"
    }
  ],
  "candidates": [
    {
      "candidate_id": "D1",
      "reference": "US20240123456A1",
      "source_type": "patent",
      "publication_or_disclosure_date": "2024-01-10",
      "apparent_elements": ["E1", "E2"],
      "readability": "full text",
      "status": "read",
      "why_it_matters": "closest process and parameter overlap"
    }
  ]
}
```

## `element_mapping.md`

Create one section per reviewed reference.

Required columns:

| Field | Meaning |
| --- | --- |
| `Element` | Stable element ID |
| `Result` | `disclosed`, `missing`, or `uncertain` |
| `Disclosure type` | `explicit`, `implicit`, `inherent`, or `n/a` |
| `Evidence location` | `reference, claim/paragraph/figure/table` |
| `Risk note` | Why the mapping is low, medium, or high risk |

Canonical example:

| Element | Result | Disclosure type | Evidence location | Risk note |
| --- | --- | --- | --- | --- |
| E1 | disclosed | explicit | US20240123456A1, para [0032], Fig. 2 | low |
| E2 | uncertain | inherent | US20240123456A1, para [0035] | inherency not yet necessary |
| E3 | missing | n/a | n/a | no control logic found |

## `claim_diff_matrix.md`

This is the canonical bridge artifact to `non-obviousness-check`.

Required columns:

| Field | Meaning |
| --- | --- |
| `Element` | Stable element ID |
| `Claim text` | Short form of the limitation |
| `D1 status` | `matched`, `partial`, `missing`, or `uncertain` |
| `Evidence location` | D1 citation or `n/a` |
| `Significance` | Why the gap matters downstream |

Canonical example:

| Element | Claim text | D1 status | Evidence location | Significance |
| --- | --- | --- | --- | --- |
| E1 | porous substrate | matched | US20240123456A1, para [0032] | baseline feature |
| E2 | pore size 0.2-0.5 um | partial | US20240123456A1, para [0035] | overlap but not exact sub-range |
| E3 | automatic pH adjustment | missing | n/a | likely inventive-step hook |

## `novelty_report.md`

Required summary fields:

- `Matter under review`
- `Target claim(s)`
- `Jurisdiction`
- `Critical date`
- `Outcome`
- `Strongest D1 candidate`
- `Defeating reference` or `Missing elements`
- `Open issues`

Required outcome rules:

- `novelty_rejected`: exactly one defeating reference must be named.
- `novelty_preserved`: missing elements across reviewed references must be listed.
- `uncertain`: a blocker to a definitive conclusion must be named.

Canonical header block:

```markdown
## Executive Summary

- Matter under review: membrane control claim set
- Target claim(s): claim 1
- Jurisdiction: US
- Critical date: 2024-05-18
- Outcome: uncertain
- Strongest D1 candidate: US20240123456A1
- Open issues: priority chain unresolved; inherency not yet necessary
```
