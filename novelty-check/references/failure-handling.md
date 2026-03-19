# Novelty Failure Handling

Use this file when the evidence chain is incomplete, degraded, or legally unstable.

## Core Rule

- If the blocker could change the legal result, do not force a definitive conclusion.
- Prefer a targeted follow-up request when one missing fact would unlock the analysis.
- Otherwise downgrade to `uncertain` and name the blocker explicitly.

## Scenario Matrix

| Scenario | Required behavior | Output impact |
| --- | --- | --- |
| No readable claim source | Ask for claim text or a readable filing source | stop before final conclusion |
| Missing jurisdiction but target market is known | state the assumed jurisdiction and label it `assumption` | provisional only |
| Missing jurisdiction and no target market | ask follow-up or output `uncertain` | no definitive legal conclusion |
| Unknown filing date or unresolved priority chain | continue only as a provisional search view | final result becomes `uncertain` |
| Abstract-only reference | do not treat it as defeating prior art | replace or downgrade |
| Duplicate-heavy search results | record the recall gap and run one more targeted round | if still weak, `uncertain` |
| Fetch failure for a high-priority candidate | replace the candidate or record `blocked` in the catalog | final result may stay `uncertain` |
| Public-disclosure route is unclear | do not assume public availability | `uncertain` unless clarified |
| Grace-period issue may save the claim | flag the issue and stop short of rejection | `uncertain` unless resolved |
| Inherency is plausible but not necessary | mark as `inference`, not as proven disclosure | no `novelty_rejected` |
| Strongest D1 covers only part of the claim | list missing elements in `claim_diff_matrix.md` | `novelty_preserved` or `uncertain` |

## Required Notes

When downgrading:

- name the exact blocker
- state which artifact reflects the blocker
- say what additional fact or document would resolve it

## Examples

- Public-use evidence exists only as a product page summary with no stable date:
  - record the source as supplemental only
  - do not use it as the defeating reference
  - write `uncertain` if the date matters to the result
- A reference appears to imply a parameter but does not make it necessary:
  - map the element as `uncertain`
  - explain why inherency fails the necessity test
  - keep `novelty_rejected` unavailable
