# Handoff to Non-obviousness

Use this file when the task moves from novelty to inventive-step analysis.

## Minimum Handoff Package

Pass these artifacts or their equivalent content:

- `claim_elements.md`
- `prior_art_catalog.json`
- `element_mapping.md`
- `claim_diff_matrix.md`
- `novelty_report.md`

## What the Downstream Skill May Assume

- element IDs are stable
- the named strongest D1 candidate is the current best novelty baseline
- cited evidence locations were actually read
- missing or partial elements in `claim_diff_matrix.md` are the first-pass inventive-step hooks

## What the Downstream Skill Must Recompute

- whether D1 is still the closest prior art for inventive-step purposes
- the objective technical problem
- D2/D3 combination paths and motivation
- reasonable expectation of success
- teaching away, incompatibility, and secondary considerations

## Special Case

If `novelty_report.md` ends in `novelty_rejected`:

- do not automatically run inventive-step analysis
- continue only if the user wants fallback arguments, narrower claim focus, or jurisdiction-specific alternative positions
