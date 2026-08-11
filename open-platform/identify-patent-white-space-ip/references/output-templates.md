# Patent white-space output templates

## Contents

1. Stage result
2. Candidate white-space table
3. Mandatory confirmation point 1
4. Problem-value brief
5. Mandatory confirmation point 2
6. Existing routes and contradiction map
7. Resolution-direction comparison
8. Final contradiction and resolution report

## 1. Stage result

### Stage conclusion

State the stage conclusion and why it matters in one concise paragraph.

| Item | Content |
|---|---|
| Scope checked | Data, map, time period, counting unit, dimensions, and comparisons used |
| Supporting evidence | Strongest evidence supporting the conclusion |
| Counter-evidence | Evidence or alternative explanation opposing the conclusion |
| Reasoning | How the evidence supports the stage conclusion |
| Confidence | High, Medium, or Low, with rationale |
| Unknowns | Missing evidence most likely to change the conclusion |
| Next decision | Next analysis step or user decision |

Separate observed facts, retrieved evidence, inference, and recommendation.

## 2. Candidate white-space table

| Candidate white-space signal | Actual patent count | Selection rationale | Possible underlying problem | Main false-space risk | Preliminary priority | Confidence |
|---|---:|---|---|---|---|---|

Display no more than seven candidates unless the user requests more.

After the table, recommend one candidate and explain why.

Do not select on the user’s behalf.

Prohibited fields include:

- Expected patent count.
- Predicted patent count.
- Actual as a percentage of expected.
- Opportunity probability derived from the score.

## 3. Mandatory confirmation point 1

Use this pattern:

> I identified the candidate white-space signals above. I recommend examining [candidate] first because [evidence-based reason]. Please confirm which candidate you want to investigate in depth. You may select more than one, and I will analyze each separately.

Stop and wait for explicit user confirmation.

Do not start the false-space check or deeper problem analysis before confirmation.

## 4. Problem-value brief

### Problem definition

> For [stakeholder] performing [job to be done] in [context], current [alternative] does not adequately achieve [desired result], causing [measurable consequence].

### Value evidence

| Dimension | Evidence | Score 1–5 | Confidence | Counter-evidence |
|---|---|---:|---|---|
| Severity | | | | |
| Frequency | | | | |
| Affected scope | | | | |
| Alternative inadequacy | | | | |
| Motivation to solve | | | | |
| Future trajectory | | | | |

Include:

- Evidence supporting problem value.
- Evidence opposing problem value.
- Provisional conclusion.
- Largest uncertainty.
- Evidence that would change the result.
- The second mandatory confirmation question.

Do not average scores without explaining weighting and missing data.

Do not convert the scores into a financial value without separate evidence.

## 5. Mandatory confirmation point 2

Use this pattern:

> The current assessment is that [problem] has [High/Medium/Low] value because [evidence]. The largest uncertainty is [uncertainty]. Please confirm whether this matches your domain knowledge and whether I should continue to contradiction diagnosis and resolution-direction generation.

Stop and wait for explicit user confirmation.

If the user disagrees, revise the problem definition or gather more evidence before continuing.

## 6. Existing routes and contradiction map

### Route comparison

| Existing route | Outcome improved | Outcome sacrificed | Why the target remains unmet | Evidence | Confidence |
|---|---|---|---|---|---|

### Route break

```text
What Route A achieves
-> missing connection, conversion, sensing, control, data, or feedback mechanism
-> what Route B therefore cannot obtain
-> unresolved target problem
```

### Root cause

State the causal mechanism that appears to maintain the sparse area.

### Primary contradiction

> To improve [A], the system must change [X], but that change degrades [B]; the objective requires improving both [A] and [B] under constraint [C].

### Secondary contradictions

List conflicts that affect the result but do not best explain the gap.

### Technical contradiction

State the improving and worsening parameters in domain language.

### Physical contradiction

State why the same property appears to need opposing states, if applicable.

### Nontechnical barriers

Address cost, resources, regulation, infrastructure, ecosystem, incentives, adoption, and business model where supported.

### Evidence and confidence

State direct evidence, inference, alternative explanations, and tests.

## 7. Resolution-direction comparison

| Direction | Resolution principle | Possible technical mechanism | How it acts on the contradiction | Limitations and new risks |
|---|---|---|---|---|

Provide two to four directions.

Each direction must show the complete logic chain:

```text
Root barrier
-> resolution principle
-> possible technical mechanism
-> effect on the contradiction
-> limitation or new risk
```

Do not use labels such as “use AI,” “build a digital twin,” “apply blockchain,” or “use smart materials” without explaining the causal mechanism.

Do not present the directions as validated solutions.

## 8. Final contradiction and resolution report

### Core judgment

State whether the candidate sparse area appears connected to an important problem, why it may persist, and which contradiction best explains it.

### Evidence chain

```text
Patent-map anomaly
-> rapid false-space check
-> valuable underlying problem
-> existing routes and limitations
-> primary contradiction
-> possible enabling conditions
-> targeted resolution directions
```

### Required report content

**Candidate signal and map basis:**

**Map construction, counting unit, period, and limitations:**

**Underlying problem and value assessment:**

**Evidence supporting and opposing the value judgment:**

**Existing routes and limitations:**

**Route break:**

**Root cause of the sparse signal:**

**Primary and secondary contradictions:**

**Technical and physical contradictions:**

**Nontechnical barriers:**

**Possible enabling conditions:**

**Resolution directions and mechanisms:**

**Limitations and new risks for each direction:**

**Confidence and unresolved questions:**

**Excluded downstream work:**

- Technical feasibility validation.
- Commercial validation.
- Patentability assessment.
- FTO analysis.
- Filing strategy or portfolio justification.

### Standardized conclusion

> [Candidate white-space signal] deserves further attention because it appears to correspond to [important problem]. The signal may persist because [limitations of existing routes], and the primary contradiction is [contradiction]. [Resolution principle and technical mechanism] could reduce this contradiction, but [main limitation or unknown] still requires validation.

## Presentation requirements

Use text labels in addition to any visual encoding.

Show actual matrix values.

Highlight the selected cell with a border, label, and pattern or annotation—not color alone.

Include captions, legends, counting units, date basis, and source notes.

Make tables responsive and printable.

Keep detailed evidence after the concise stage conclusion.
