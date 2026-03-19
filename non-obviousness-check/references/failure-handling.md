# Non-obviousness Failure Handling

Use this file when the baseline, combination logic, or evidence chain is incomplete.

## Core Rule

- If the blocker could change the inventive-step result, do not force a definitive conclusion.
- Prefer a targeted follow-up request when one missing fact would unlock the analysis.
- Otherwise downgrade to `uncertain` and name the blocker explicitly.

## Scenario Matrix

| Scenario | Required behavior | Output impact |
| --- | --- | --- |
| No stable D1 | derive D1 first or ask for more baseline material | no final inventive-step conclusion |
| Missing jurisdiction but target market is known | state the assumed jurisdiction and label it `assumption` | provisional only |
| Missing jurisdiction and no target market | ask follow-up or output `uncertain` | no definitive legal conclusion |
| Date issue changes the framework or prior-art set | stop short of strong/weak conclusion | `uncertain` |
| Abstract-only D2/D3 | do not use it as a strong path anchor | replace or downgrade |
| Duplicate-heavy search results | record the recall gap and run one more targeted round | if still weak, `uncertain` |
| Fetch failure for a key D2/D3 | replace candidate or record `blocked` | strength may drop to `uncertain` |
| Same field but no concrete motivation | do not treat field proximity as enough | at most `weak`, often `uncertain` |
| Compatibility is mixed or negative | record the mismatch explicitly | strength cannot be `strong` |
| Expectation of success is unsupported | record the gap | strength cannot be `strong` |
| Secondary considerations lack nexus | mention them only as weak rebuttal evidence | do not let them drive the result |

## Required Notes

When downgrading:

- name the exact blocker
- state which artifact reflects the blocker
- say what additional fact or document would resolve it

## Examples

- D1 is obvious as a novelty baseline but may not be the closest prior art for EP PSA:
  - pause the conclusion
  - re-evaluate D1 before scoring path strength
- D2 supplies the missing feature but the interface is incompatible:
  - mark compatibility as `mixed` or `incompatible`
  - explain the engineering conflict
  - do not call the path `strong`
