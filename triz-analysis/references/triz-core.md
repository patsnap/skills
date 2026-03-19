# TRIZ Core Playbook

## 1. Core Concepts
- Technical contradiction: improving parameter A worsens parameter B.
- Physical contradiction: one parameter must be both X and non-X.
- IFR (Ideal Final Result): maximize useful function, minimize harm/cost/complexity.
- Resources: use existing system/internal resources before introducing new complexity.

## 2. Fast Problem Framing Template
Use this structure before selecting TRIZ principles:
1. Problem statement: What fails, where, when, and for whom?
2. Target metric: What exact metric should improve?
3. Boundary: What is in scope vs out of scope?
4. Constraint set: time, cost, safety, compliance, tooling.
5. Failure impact: what is unacceptable?

## 3. Contradiction Templates

### Technical contradiction template
- Improve: `[parameter A]`
- Degrades: `[parameter B]`
- Current workaround and side effect: `[text]`

### Physical contradiction template
- Object/parameter: `[X]`
- Must be high/large/strong when: `[condition 1]`
- Must be low/small/weak when: `[condition 2]`

## 4. Practical Principle Mapping (Engineering-Oriented)
Use as a fast heuristic, not a strict matrix replacement.

| Typical contradiction pattern | Candidate principles |
| --- | --- |
| Performance up vs cost up | Segmentation, Dynamics, Prior Action |
| Strength up vs weight up | Composite Materials, Nested Doll, Parameter Changes |
| Speed up vs quality down | Preliminary Action, Feedback, Intermediary |
| Reliability up vs complexity up | Self-service, Universality, Copying |
| Precision up vs throughput down | Another Dimension, Mechanics Substitution, Local Quality |
| Energy efficiency up vs response time down | Prior Action, Cushion in Advance, Partial/Excessive Action |

## 5. IFR Guidance
State IFR with this sentence pattern:
- "The system achieves `[target function]` while adding near-zero `[cost/complexity/risk]`, using existing resources `[resource list]`."

Then derive gap:
- Current state vs IFR delta
- Which contradiction blocks progress

## 6. Resource Analysis Checklist
Check resources in this order:
1. System resources (components, unused capacity)
2. Process resources (timing windows, sequence flexibility)
3. Environmental resources (temperature, vibration, external fields)
4. Information resources (logs, telemetry, expert heuristics)
5. Human/organizational resources (skills, workflow changes)

## 7. Option Construction Rules
Every option should contain:
1. mechanism of change
2. expected metric movement
3. required resources
4. main risk and mitigation
5. evidence anchor (patent/paper/product example)

## 8. Stop Conditions
Escalate to advanced methods (`triz-advanced.md`) when any of the following holds:
- repeated contradiction loops with no converging option
- multiple coupled subsystems produce chain side effects
- physical contradiction dominates and simple principle mapping is inconclusive
