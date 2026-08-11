# Candidate patent white-space evaluation framework

Use this reference in Stage 1 to rank candidate sparse areas and in Stage 3 to evaluate the value of the underlying problem.

## Contents

1. Candidate-ranking dimensions
2. Preliminary interpretation types
3. Problem-value dimensions
4. Contradiction-diagnosis checklist
5. Confidence standard
6. Guardrails

## 1. Candidate-ranking dimensions

Score each candidate on six dimensions from 1 to 5.

Attach evidence to every score.

Treat the scale as ordinal decision support, not a calibrated probability.

| Dimension | Core question |
|---|---|
| Observed sparsity | Is the actual patent count low under the stated map construction, counting unit, and period? |
| Adjacent attractiveness | Are the technologies, effects, applications, or routes on both sides active and decision-relevant? |
| Need signal | Is there evidence of an important unmet task or constraint? |
| Contradiction signal | Do existing routes appear unable to satisfy competing objectives or bridge a missing mechanism? |
| Strategic relevance | Does the candidate fit the user’s markets, capabilities, and decision objective? |
| False-space risk | Could terminology, classification, family handling, data coverage, secrecy, or another artifact explain the gap? Higher score means lower observed artifact risk. |

Record:

- Score.
- Supporting evidence.
- Counter-evidence.
- Assumptions.
- Confidence.
- Evidence that would most change the score.

Do not calculate an expected patent count from row and column totals.

Do not calculate an actual-to-expected percentage.

Those calculations usually assume independence and can create false precision.

Do not announce an opportunity from the total score.

Use the score only to order candidates for user selection.

## 2. Preliminary interpretation types

Assign one or more provisional interpretation types.

| Type | Meaning |
|---|---|
| Structural-contradiction space | The problem appears important, but existing routes face a difficult trade-off. |
| Route-break space | Related routes exist independently, but an effective connection, conversion, or feedback mechanism is missing. |
| Emerging-combination space | Adjacent capabilities are maturing but have not been combined for the target outcome. |
| Currently intractable space | The problem appears important, but no plausible enabling condition is visible yet. |
| Weak-demand space | Patent sparsity may reflect low problem value or limited demand. |
| Apparent space | Classification, terminology, search, data, time-window, or family treatment likely creates the signal. |
| Hidden-activity space | Relevant know-how may be protected through trade secrecy, process control, contracts, or other non-patent means. |

State that each type is provisional.

Allow multiple explanations.

Include the strongest alternative explanation.

## 3. Problem-value evaluation

Use this only after the user selects a candidate.

Evaluate six dimensions from 1 to 5.

| Dimension | Weaker evidence | Stronger evidence |
|---|---|---|
| Severity | Minor inconvenience | Material cost, safety, compliance, performance, or strategic consequence |
| Frequency | Rare edge case | Frequent or systemic occurrence |
| Affected scope | Narrow or declining niche | Large, growing, or strategically important population |
| Existing alternatives | Effective and reasonably priced | Ineffective, expensive, slow, risky, or unavailable |
| Motivation to solve | Little willingness or pressure | Clear regulatory, operating, customer, or strategic pressure |
| Future trajectory | Importance declining | Urgency, scale, or consequence increasing |

For each dimension record:

- Stakeholder.
- Job to be done.
- Current alternative.
- Measurable consequence.
- Direct evidence.
- Contrary evidence.
- Score and rationale.
- Confidence.

Do not infer problem value from patent count alone.

Patent activity is a map signal, not a direct measure of demand, harm, or willingness to pay.

Proceed to contradiction diagnosis only when the problem appears sufficiently valuable or the user explicitly elects to explore it.

## 4. Contradiction-diagnosis checklist

Check every question:

1. Do existing routes optimize different outcomes?
2. Does improving one outcome degrade another?
3. Are there two routes that do not connect?
4. What exact connection, conversion, control, sensing, data, material, or feedback mechanism is missing?
5. Which conflict best explains why the sparse area persists?
6. Which conflicts affect performance but do not primarily create the gap?
7. Is the central barrier technical, economic, regulatory, resource-based, ecosystem-based, or behavioral?
8. Can the gap be explained through a testable causal mechanism?
9. Does each proposed resolution act on that mechanism?
10. Is TRIZ being applied after diagnosis rather than used to invent a post-hoc problem statement?

Define the primary contradiction in a testable form:

> To improve [A], the system must change [X], but that change degrades [B]; the objective requires improving both [A] and [B] under constraint [C].

Identify:

- Primary contradiction.
- Secondary contradictions.
- Technical contradiction.
- Physical contradiction where applicable.
- Nontechnical barriers.
- Route break.
- Root-cause confidence.

## 5. Confidence standard

| Level | Standard |
|---|---|
| High | Multiple independent sources and direct evidence support the conclusion; major alternatives have been tested. |
| Medium | The conclusion is reasonable and supported, but one or more material assumptions remain. |
| Low | The conclusion relies mainly on inference, incomplete map data, or missing domain evidence. |

Always state:

- Why the confidence level was assigned.
- Which evidence is direct.
- Which statements are inference.
- Which new evidence would most likely change the conclusion.

## 6. Guardrails

- Use actual counts only.
- State the family definition and counting unit.
- State the date basis and cut-off.
- State map dimensions and classification rules.
- Keep user expertise in the decision loop.
- Treat low density as a hypothesis.
- Test search, classification, language, family, time, and database artifacts.
- Consider trade-secret and non-patent activity.
- Do not use expected-count or actual/expected-ratio fields.
- Do not convert ordinal scores into probabilities.
- Do not use a score as proof that an innovation opportunity exists.
- Do not continue through either mandatory user gate without explicit confirmation.
