# Handoff from Novelty

Use this file when `non-obviousness-check` starts from an upstream novelty package.

## Minimum Accepted Package

Prefer these artifacts:

- `claim_elements.md`
- `prior_art_catalog.json`
- `element_mapping.md`
- `claim_diff_matrix.md`
- `novelty_report.md`

## What May Be Reused Directly

- stable element IDs
- the strongest D1 candidate as the first inventive-step baseline
- reviewed evidence locations already read in the novelty stage
- missing or partial elements in `claim_diff_matrix.md` as candidate difference features

## What Must Be Recomputed

- whether the novelty D1 is also the closest prior art for the selected jurisdiction
- the objective technical problem
- which D2/D3 path is strongest
- motivation, compatibility, and expectation of success
- teaching away, prejudice, and secondary considerations

## Boundary Rule

If the upstream package already ends with `novelty_rejected`:

- do not assume inventive-step analysis is still needed
- continue only if the user wants fallback arguments, narrower claim positions, or jurisdiction-specific alternative analysis
