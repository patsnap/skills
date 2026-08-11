# Innovation Taxonomy

Use this taxonomy after extracting the technical problem, implementation, and effect. A label organizes review; it does not determine patent eligibility, claim category, protection type, or legal outcome.

## Classification rules

- Assign one primary type based on the differentiating technical feature.
- Add secondary types when a contribution genuinely spans categories.
- Explain the feature that supports each label.
- Do not force a category when the implementation is missing.
- Keep commercial use cases separate from technical uses.

## 1. Method

**Signal:** A new way of performing a technical operation.

Look for ordered steps, conditions, inputs, transformations, feedback, control logic, or measurement procedures.

Capture:

- step sequence and dependencies;
- trigger and termination conditions;
- inputs, outputs, and intermediate states;
- hardware or environmental constraints;
- technical effect and comparison baseline.

Example: adapt a sampling interval using measured load variation and a stability threshold to maintain accuracy while reducing energy use.

## 2. Structure or device

**Signal:** A new physical or logical arrangement of components.

Look for parts, modules, interfaces, geometry, connections, placement, layers, or cooperative relationships.

Capture:

- component identity and function;
- spatial, electrical, optical, fluidic, or data relationships;
- changed feature versus the baseline;
- variants and replaceable components;
- measured or expected effect.

Example: add an adaptive filter module between a sensor front end and controller, with a defined feedback connection and operating condition.

## 3. Parameter range or formulation

**Signal:** A composition, ratio, range, process window, threshold, or coupled parameter relationship.

Capture:

- units, endpoints, tolerances, and measurement method;
- ingredients or controlled variables;
- test matrix and baseline;
- behavior inside and outside the range;
- repeatability, uncertainty, and unexpected effects.

Do not treat a routine optimum as inventive merely because it has a number.

## 4. Technical use or effect

**Signal:** A known technology applied in a technically different context with adaptation or a newly demonstrated technical effect.

Capture:

- original and new technical contexts;
- adaptation mechanism;
- operating constraints;
- evidence of the new effect;
- why the effect was not assumed from the baseline.

A new market or customer segment alone is not a technical use.

## 5. Process or system

**Signal:** Multiple stages or modules cooperate in a changed workflow or architecture.

Capture:

- modules and responsibilities;
- material, energy, data, and control flow;
- sequencing, synchronization, and feedback;
- system-level effect not attributable to one part alone;
- failure modes and fallback behavior.

## 6. Material or substance

**Signal:** A new chemical composition, material architecture, phase, morphology, treatment, or combination.

Capture:

- identity, composition, purity, structure, and preparation;
- processing history and test conditions;
- characterization methods;
- comparative samples and controls;
- stability, reproducibility, and safety constraints.

## Cross-category decision table

| Dominant feature | Primary type | Common secondary type |
|---|---|---|
| Ordered technical operations | Method | Process or system |
| Component arrangement | Structure or device | Process or system |
| Numeric window or composition | Parameter range or formulation | Material or substance |
| Adapted technical context | Technical use or effect | Method |
| Coordinated modules or stages | Process or system | Method |
| Composition or material architecture | Material or substance | Parameter range or formulation |

## Common extraction failures

- Problem without implementation: retain as a signal and ask how it was solved.
- Implementation without effect: retain the implementation and label the effect as not provided.
- Broad optimization claim: ask what changed at component, step, parameter, or control level.
- Business feature only: exclude unless a technical implementation and effect are present.
- Generic AI, cloud, sensor, or automation use: exclude until a specific technical adaptation is described.
- Several coupled contributions: split only when each can be understood and acted on independently.

## Output fields

For each candidate record:

1. primary type;
2. secondary type or `None`;
3. differentiating feature;
4. classification rationale;
5. source location;
6. confidence and missing evidence.
