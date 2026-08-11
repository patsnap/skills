# Follow-up Question Library

Use this library only after identifying the exact missing fields. Ask no more than three questions per candidate in the first pass. Choose questions that could change the technical boundary, evidence confidence, search, disclosure urgency, or protection path.

## Selection rules

- Use plain language suitable for an engineer or scientist.
- State why the answer matters when helpful.
- Do not ask for information already supplied.
- Request a document, drawing, result, or source location when that is more efficient than prose.
- Respect confidentiality and the authorized distribution list.
- Do not use answers to make inventorship or legal conclusions without specialist review.

## Core triage

1. What was the previous technical approach, and what specific limitation appeared under actual operating conditions?
2. What component, step, relationship, rule, material, or parameter was changed?
3. What result was observed, under which test conditions, compared with what baseline?

## Missing technical problem

1. What did the earlier system or process fail to do, and under what conditions?
2. Which technical metric or failure mode showed the problem?
3. Is the limitation documented in a test, incident, customer qualification, or prior design record?

## Missing implementation

1. Please list the changed steps or components in execution order and show how they interact.
2. What inputs, thresholds, ranges, triggers, and constraints control the change?
3. Which feature is essential, and which features are optional alternatives?

## Missing technical effect

1. What metric changed, from what baseline to what result, and in which units?
2. How was the comparison tested: samples, controls, repeats, environment, and measurement method?
3. If testing is incomplete, what effect is expected, why, and what experiment would verify it?

## Method candidates

1. What are the critical steps, and which ordering or dependency cannot be removed?
2. What triggers the method, what inputs does it require, and when does it stop or fall back?
3. Does it depend on particular hardware, data, or operating conditions?

## Structure or device candidates

1. Which component or relationship changed, and can you provide a marked drawing or schematic?
2. How are the components physically, electrically, optically, fluidically, or logically connected?
3. Which structural feature produces the effect, and what happens if it is removed or replaced?

## Parameter range or formulation candidates

1. What are the units, lower and upper bounds, tolerances, and measurement method?
2. Which tests support the range, including points inside and outside it?
3. Is the observed behavior repeatable across batches, equipment, operators, and environments?

## Technical use or effect candidates

1. What was the original technical use, and what changes were required for the new technical context?
2. How was the effect discovered and independently confirmed?
3. What constraint in the new context makes the adaptation technically different?

## Process or system candidates

1. How do material, data, energy, and control move between stages or modules?
2. Which system-level effect cannot be achieved by the modules independently?
3. What synchronization, feedback, exception, and fallback behavior is required?

## Material or substance candidates

1. What composition, structure, morphology, purity, and preparation history define the material?
2. Which characterization and comparative tests support the stated properties?
3. What happens when composition or processing moves outside the proposed range?

## Software and AI candidates

1. What data enters the system, what transformation occurs, and what technical output controls or changes?
2. What model, training, inference, scheduling, memory, latency, energy, or hardware feature differs from the baseline?
3. Which datasets, code, models, libraries, or third-party rights are involved, and what may be kept confidential?

## Experiment and evidence questions

1. Where are the raw data, protocol, calibration record, analysis script, and versioned result?
2. What controls, repeats, sample sizes, exclusions, and uncertainty measures were used?
3. Were there negative results, failed alternatives, or conditions where the effect disappeared?

## Contributor and inventorship leads

Ask for contribution facts, not conclusions:

1. Who first proposed each specific technical feature, and when is that contribution recorded?
2. Who changed the concept, selected critical parameters, or developed alternatives?
3. Who only implemented, tested, supervised, funded, or documented work designed by others?

Forward these facts to the appropriate IP professional; do not decide inventorship from the responses alone.

## Disclosure-risk facts

For every potentially time-sensitive candidate ask:

1. Has any relevant detail been submitted, published, presented, demonstrated, sold, used publicly, uploaded, standardized, or shared externally?
2. For each event, what was the exact date, audience, access control, NDA/contract status, and technical content disclosed?
3. What future disclosure, launch, standards, publication, customer, or partner date is planned?

Do not state that submission always equals publication or apply a universal grace period. Escalate facts promptly for jurisdiction-specific advice.

## Ownership and third-party facts

1. Were contractors, universities, joint-development partners, customers, suppliers, or former employers involved?
2. Which agreements, statements of work, funding terms, or open-source/data licenses may apply?
3. Does any record contain third-party confidential information or restricted data?

## Trade-secret feasibility

1. Who needs access, and what repository, contractual, physical, and cybersecurity controls exist?
2. Can the contribution be learned from the product, service behavior, documentation, testing, or reverse engineering?
3. How would unauthorized disclosure or use be detected and investigated?

## Copy-ready first-pass template

> Please help us complete the technical record for candidate **[ID/title]**:
>
> 1. [Highest-impact missing technical fact]
> 2. [Highest-impact evidence or comparison fact]
> 3. [Highest-impact disclosure/contribution/protection fact]
>
> Please link the relevant drawing, test, change record, or meeting section where possible. Do not send confidential information outside the approved channel.

## Re-questioning rule

After receiving answers:

- update source fact versus inference labels;
- reconcile the three technical elements;
- reassess query readiness and confidence;
- ask another round only if a remaining gap changes the decision;
- preserve unanswered questions and contradictory evidence in the report.
