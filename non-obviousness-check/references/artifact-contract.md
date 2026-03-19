# Non-obviousness Artifact Contract

Use this file whenever you create, update, or validate required artifacts.

## General Rules

- Reuse stable element IDs such as `E1`, `E2`, `E3` across all artifacts.
- Reuse one stable D1 identifier across `jurisdiction_plan.md`, `claim_diff_matrix.md`, `combination_candidates.json`, `motivation_matrix.md`, and `inventive_step_report.md`.
- If a field is unresolved, write `unknown` or `uncertain`; do not leave silent gaps.
- Allowed inventive-step outcome strengths are:
  - `strong`
  - `weak`
  - `uncertain`

## `jurisdiction_plan.md`

Required fields:

- `Target jurisdiction`
- `Routing reason`
- `Critical date`
- `Selected framework`
- `Open routing issues`

Canonical example:

```markdown
## Jurisdiction Plan

- Target jurisdiction: EP
- Routing reason: user wants EPO filing strategy
- Critical date: 2024-05-18
- Selected framework: problem-solution approach and could-would test
- Open routing issues: none
```

## `claim_diff_matrix.md`

This is the canonical bridge artifact from novelty review or the first artifact to build when no upstream novelty package exists.

Required columns:

| Field | Meaning |
| --- | --- |
| `Element` | Stable element ID |
| `Claim text` | Short form of the limitation |
| `D1 status` | `matched`, `partial`, `missing`, or `uncertain` |
| `Evidence location` | D1 citation or `n/a` |
| `Significance` | Why the gap matters to inventive-step analysis |

## `combination_candidates.json`

Top-level fields:

- `jurisdiction`
- `baseline_reference`
- `technical_problem`
- `paths`

Allowed path `status` values:

- `candidate`
- `shortlisted`
- `discarded`
- `blocked`

Minimal shape:

```json
{
  "jurisdiction": "EP",
  "baseline_reference": "D1",
  "technical_problem": "how to automate pH control without increasing maintenance",
  "paths": [
    {
      "path_id": "D1+D2",
      "references": ["D1", "D2"],
      "supplied_elements": ["E3"],
      "motivation_source": "same problem plus explicit control-loop suggestion",
      "compatibility": "compatible",
      "expectation_of_success": "supported",
      "counter_evidence": ["no teaching away found"],
      "status": "shortlisted"
    }
  ]
}
```

## `motivation_matrix.md`

Required columns:

| Field | Meaning |
| --- | --- |
| `Path` | Combination path ID |
| `Missing feature supplied by` | D2 or D3 contribution |
| `Motivation source` | Why the skilled person would look there |
| `Compatibility check` | `compatible`, `mixed`, or `incompatible` |
| `Expectation of success` | `supported`, `uncertain`, or `unsupported` |
| `Counter-evidence` | teaching away, prejudice, mismatch, etc. |
| `Strength` | `high`, `medium`, or `low` |

Canonical example:

| Path | Missing feature supplied by | Motivation source | Compatibility check | Expectation of success | Counter-evidence | Strength |
| --- | --- | --- | --- | --- | --- | --- |
| D1 + D2 | D2 supplies E3 | same problem + explicit hint | compatible | supported | none | high |
| D1 + D3 | D3 supplies E4 | market pressure only | mixed | uncertain | interface mismatch | low |

## `secondary_considerations.md`

Required columns:

| Field | Meaning |
| --- | --- |
| `Category` | commercial success, unexpected results, etc. |
| `Evidence` | source and short description |
| `Nexus` | `established`, `weak`, `unproven`, or `not_applicable` |
| `Strength` | `high`, `medium`, or `low` |
| `Comment` | why it matters or why it fails |

## `inventive_step_report.md`

Required summary fields:

- `Matter under review`
- `Target claim(s)`
- `Jurisdiction`
- `Selected framework`
- `Strongest D1`
- `Best combination path`
- `Outcome strength`
- `Open issues`

Required outcome rules:

- `strong`: the best combination path and its motivation must be explicitly named.
- `weak`: a path exists but one or more core links remain vulnerable.
- `uncertain`: the baseline, framework, or evidence chain is not stable enough.

Canonical header block:

```markdown
## Executive Summary

- Matter under review: membrane control claim set
- Target claim(s): claim 1
- Jurisdiction: EP
- Selected framework: problem-solution approach
- Strongest D1: EP3456789A1
- Best combination path: D1 + D2
- Outcome strength: weak
- Open issues: expectation of success remains contested
```
