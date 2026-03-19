# Novelty Report Template

Load this template only when the user wants a saved memo or formal report.
Use it to expand `novelty_report.md` into a formal memo.

## Required Sections

1. Matter under review
2. Target claim(s), jurisdiction, and critical date
3. Claim decomposition summary
4. Search summary
5. Highest-risk references
6. Element-by-element mapping
7. `claim_diff_matrix.md` summary
8. Novelty conclusion
9. Facts / inferences / unknowns
10. Open risks and next actions

## Executive Summary

Include:

- matter under review
- target claim(s)
- jurisdiction
- filing or priority date
- final result: `novelty_rejected`, `novelty_preserved`, or `uncertain`
- strongest D1 candidate
- defeating reference or missing elements
- one-sentence reason

## Citation Format

Use one compact location format throughout:

- `US20240123456A1, claim 1`
- `EP3456789A1, para [0042]`
- `CN114567890A, Fig. 3`
- `Product page, archived snapshot dated 2024-02-11`

## Mapping Table

| Element | D1 disclosure | Type | Evidence location | Comment |
| --- | --- | --- | --- | --- |
| E1 | yes | explicit | para 18 | low risk |
| E2 | yes | inherent | Fig. 2 + para 22 | medium risk |
| E3 | no | n/a | n/a | novelty preserved if this stays missing |

## Claim Difference Summary

Mirror the strongest D1 comparison:

| Element | D1 status | Evidence location | Why it matters |
| --- | --- | --- | --- |
| E1 | matched | US20240123456A1, para [0032] | baseline |
| E2 | partial | US20240123456A1, para [0035] | overlap only |
| E3 | missing | n/a | keeps novelty alive |

## Conclusion Block

Always separate:

- facts
- inferences
- unknowns

Required wording:

- If novelty is rejected:
  - `Conclusion: novelty_rejected. Under [jurisdiction], claim [X] is defeated by [reference].`
- If novelty is preserved:
  - `Conclusion: novelty_preserved. No reviewed single reference discloses all limitations of claim [X]; the remaining missing elements are [list].`
- If novelty is uncertain:
  - `Conclusion: uncertain. The current record does not support a definitive novelty conclusion because [blocker].`

If novelty is rejected, state the single reference that supports the conclusion.
If novelty is preserved, state which element(s) remain missing across all reviewed references.
If novelty is uncertain, state the blocking unknown and the next evidence needed.
