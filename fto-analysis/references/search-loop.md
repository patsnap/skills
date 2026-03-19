# Search Loop

## Goal

Control expansion of the FTO candidate pool with two-lane search and deterministic recall estimation instead of intuition alone.

## Required Round Inputs

Before each call to `scripts/fto_recall_estimator.py`, prepare a JSON input file:

```json
{
  "round": 2,
  "keyword_ids": ["US1", "US2"],
  "semantic_ids": ["US2", "US3"],
  "seen_ids": ["US0"],
  "recall_target": 0.85,
  "delta_n_min": 5
}
```

Field conventions:

- `round`: current round number, starting from `1`
- `keyword_ids`: unique patent IDs hit by the keyword path in this round
- `semantic_ids`: unique patent IDs hit by the semantic path in this round
- `seen_ids`: unique patent IDs already accumulated before this round
- `recall_target`: accepts either `0.85` or `85`
- `delta_n_min`: minimum new-result count that triggers diminishing-returns guidance

Optional fields:

- `overlap_correction_threshold`
- `correction_factor`

## Deterministic Estimator

Run the script before writing any round summary or stop / continue judgment:

```bash
python3 scripts/fto_recall_estimator.py --input-json <round-input.json>
```

The script outputs Chapman-style capture-recapture metrics:

- `n_k`
- `n_s`
- `n_ks`
- `n_pool`
- `delta_n`
- `universe_estimate_raw`
- `universe_estimate_adjusted`
- `recall_estimate`
- `correction_applied`
- `decision`
- `warnings`

## Interpretation Rules

- `target_met`: estimated recall has reached the target, so screening and analysis may proceed
- `diminishing_returns`: new additions are below threshold, so explain diminishing marginal value
- `continue_search`: continue to the next round
- `expand_search`: the current round is too weak, so broaden the query or add a new expression style

Only state that the recall target has been met when the script returns `target_met`.

## Query History Contract

Maintain:

```json
{
  "query_history": {
    "keywords": ["used keyword 1", "used keyword 2"],
    "semantic": [
      { "round": 1, "level": "implementation", "query": "..." },
      { "round": 2, "level": "effect", "query": "..." }
    ],
    "ipc_codes_used": ["H01M10/60"]
  }
}
```

Rules:

- new keyword queries must not repeat `query_history.keywords`
- semantic queries should move upward by abstraction level each round rather than swapping synonyms in place
- every stop / continue explanation must cite the current round metrics and `query_history`

## Query Evolution Guidance

### Keywords

- extract concrete implementation terms from highly relevant patent specifications
- add materials, structures, processes, parameters, and standard designators
- add competitor or assignee names when useful
- extend into adjacent IPC subclasses when justified

### Semantic

- use claim-style functional language
- move from implementation level toward effect, problem, and scenario levels across rounds
- avoid mixing model numbers, dimensions, or material names into semantic queries

## Failure Handling

- if both lanes are empty, the expression strategy has failed; broaden the query before continuing
- if high overlap triggers correction, explicitly warn that `R_est` may be optimistic
- if the estimated universe falls below the accumulated pool, accept the script’s floor result rather than manually rewriting it
