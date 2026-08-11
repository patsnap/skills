---
name: audit-catalyst-experimental-methods-rd
description: Audit catalyst preparation and evaluation methods for executability, reproducibility, controlled comparison, attribution, measurement reliability, safety-review readiness, and claim-to-evidence linkage. Use for experimental procedures, screenshots, paper methods, patent examples, draft plans, and machine-generated catalyst routes.
---

# Audit catalyst experimental methods

## Scope

Use this skill as a pre-experiment technical audit of catalyst preparation and evaluation methods. The central questions are:

1. Can a trained researcher execute the stated method safely with the information provided?
2. Are the conditions sufficient for an independent laboratory to reproduce it?
3. Do samples, variables, controls, and baselines support a fair comparison?
4. Can an observed effect be attributed to the intended variable?
5. Do the evaluation and characterization plans support each performance, structural, or mechanistic claim?
6. Are material hazards and operability questions visible for qualified EHS and laboratory review?

The skill does not authenticate results, approve laboratory safety, certify regulatory compliance, perform engineering scale-up, determine patentability or freedom to operate, or replace a catalyst specialist.

## Typical inputs

Accept the material in its current form; do not require the user to rebuild it as a formal proposal.

| Input | Audit treatment |
|---|---|
| Preparation-step procedure | Full method audit emphasizing operations, conditions, samples, controls, and missing evaluation detail |
| Complete preparation and evaluation plan | Full preparation, comparison, measurement, validation, and safety-readiness audit |
| R&D concept or machine-generated draft | Draft-level audit focused on missing evidence and executable next steps |
| Paper Methods section | Reproducibility audit; distinguish publication brevity from evidence that a step was not performed |
| Full paper | Locate preparation, characterization, catalytic testing, and supporting methods before auditing |
| Patent example or embodiment | Convert the example into a method register while retaining patent-specific context |
| Screenshot or scanned document | Faithful transcription before extraction or audit |
| Insufficient material | Issue an insufficiency notice; do not fabricate a full audit conclusion |

## Evidence discipline

- Quote or identify the source passage supporting each extracted condition and each issue.
- Write `not specified` when the submitted material is silent.
- Do not convert `not specified` into `not performed`.
- Distinguish an inferred condition from an explicit condition.
- Preserve the original units and add a normalized unit only in a separate field.
- Retain ranges, tolerances, uncertainty, significant figures, and conditional steps.
- Preserve conflicting versions and request resolution; never silently select one.
- Treat generated recommendations as method-development guidance, not facts about the experiment.

## Required execution sequence

Follow this order.

### 1. Read and classify the material

Read the complete submission. For screenshots or scanned PDFs, follow `prompts/00_faithful_transcription.md`. Preserve page order, formulas, sample identifiers, values, units, atmospheres, and instrument names. Mark illegible content; do not guess.

Classify the material with `rules/material_type_rules.yaml`. Record the material type, audit mode, confidence, and evidence for the classification.

### 2. Extract canonical method elements

Extract directly when possible. Use `prompts/01_canonical_extraction.md` only if the structure cannot be read reliably.

Capture:

- catalyst system, composition, precursor identity, purity or grade;
- operation sequence and dependencies;
- amount, concentration, solvent, pH, order and rate of addition;
- mixing mode, speed or power, duration, and geometry when outcome-sensitive;
- vessel material, volume, fill fraction, and pressure rating where relevant;
- temperature program, dwell, atmosphere, flow, purge, and cooling;
- separation, washing, drying, calcination, activation, reduction, and storage;
- sample identifiers, batches, target variables, controls, blanks, and baselines;
- reaction, reactor, catalyst charge, particle size, dilution, feed and pretreatment;
- temperature, pressure, flow, residence time or space velocity;
- sampling, analytical method, calibration, response factor, detection limit, and balance;
- characterization methods and the exact claim each method tests;
- replication, randomization, blocking, uncertainty, exclusions, and acceptance criteria;
- hazards, containment, ventilation, gas handling, equipment limits, waste, and stop-work criteria when stated;
- performance, structure, and mechanism claims.

### 3. Audit preparation executability

Review the extracted sequence against `rules/audit_dimensions.yaml` and `rules/issue_catalog.yaml`.

For each operation, determine whether a competent researcher can identify:

- material identity and amount;
- equipment and contact materials;
- sequence and endpoint;
- temperature, duration, atmosphere, and pressure;
- scale-dependent conditions;
- separation and recovery conditions;
- intermediate handling and storage;
- sample or batch identifier;
- applicable safety-review requirement.

Do not impose a detail merely because it is common. Explain why the missing detail could affect execution, reproducibility, safety, or interpretation.

### 4. Audit sample design and attribution

Create a sample-variable register. Exclude gases, solvents, equipment, solution labels, and condition strings from the sample list.

For every sample, record:

- stable identifier and batch;
- role: target, blank, support-only, unmodified, positive control, negative control, commercial baseline, literature baseline, or intermediate;
- composition and preparation route;
- intentionally changed variables;
- unintentionally changed or uncontrolled variables;
- evaluation conditions;
- evidence location.

Flag simultaneous changes that prevent attribution. Recommend a single-variable, factorial, response-surface, or explicitly qualified comparison as appropriate; do not universally require one-factor-at-a-time design.

### 5. Audit evaluation reliability

Review the complete measurement chain:

1. reactor and operating mode;
2. catalyst charge, particle size, dilution, and bed geometry;
3. pretreatment and transition to reaction conditions;
4. feed composition, purity, delivery, and flow basis;
5. temperature and pressure measurement locations and calibration;
6. residence time, GHSV, WHSV, or another justified basis;
7. steady-state definition and sampling schedule;
8. product identification and quantitation;
9. calibration model, standards, response factors, blanks, carryover, and detection limits;
10. material or elemental balance and acceptance rule;
11. independent replication and uncertainty;
12. deactivation, regeneration, and post-test characterization where relevant.

Do not treat a technique name such as `GC` or `HPLC` as a complete analytical method.

### 6. Audit claim-to-evidence linkage

Build a claim-validation matrix.

| Claim type | Required definition | Example evidence classes |
|---|---|---|
| Activity | Metric, basis, conditions, comparator, uncertainty | conversion, rate, TOF, STY, kinetic regime checks |
| Selectivity or yield | Product basis, conversion window, balance, calibration | calibrated product distribution and mass/element balance |
| Stability | Duration or cycles, deactivation metric, operating history | time-on-stream, cycling, regeneration, before/after analysis |
| Composition or loading | Target and tolerance | ICP/OES, ICP/MS, XRF, elemental analysis with controls |
| Phase or structure | Distinguishing feature and alternatives | diffraction, spectroscopy, microscopy, scattering |
| Oxidation state or active site | State under relevant conditions and competing explanations | orthogonal ex situ plus operando/quasi-in-situ evidence |
| Mechanism | Causal prediction and alternatives | kinetics, isotopes, perturbation tests, operando evidence, modeling |

A characterization technique supports only the claim it can discriminate under the stated conditions. Avoid equating correlation with mechanism.

### 7. Apply issue levels and judgments

Use `rules/judgment_level_rules.yaml` consistently.

- `HIGH` / Critical issue: can prevent safe execution, reproduction, valid comparison, or support for a core claim.
- `MEDIUM` / Material issue: materially weakens credibility, attribution, or reviewability.
- `LOW` / Documentation issue: affects operational detail, traceability, or record quality.

Use `NOT_APPLICABLE` when a dimension truly does not apply. Do not turn absence of evidence into a positive judgment.

### 8. Generate deterministic deliverables

Run the only execution entry point:

```bash
python scripts/run_audit.py --input <input_file_or_transcription> --out outputs
```

The script generates exactly:

- `outputs/report_context.json`
- `outputs/Catalyst Preparation and Evaluation Method Audit Report.html`
- `outputs/Catalyst Preparation and Evaluation Method Audit Report.docx`

Then run:

```bash
python scripts/validate_outputs.py outputs
```

Do not create ad hoc repair scripts or manually rewrite the generated report body. Correct extraction, rules, or the generator and rerun.

## Report structure

The HTML and Word reports contain:

1. Material and classification
2. Overall audit conclusion
3. Priority issues
4. Dimension-level findings
   - Preparation executability
   - Variable design and attribution
   - Controls and baselines
   - Evaluation conditions and data reliability
   - Claim-to-evidence linkage
5. Preparation-step register
6. Sample and variable register
7. Required additions
8. Audit limitations

The Word report additionally includes extracted elements, rule basis, input fingerprint, version, and generation time.

## Report language and visual system

Follow `prompts/02_formal_report_language.md`.

Use clear international scientific English. Expand acronyms on first use unless they are universally understood by the intended specialists. Preserve chemical formulas and accepted SI notation. Use decimal points in normalized values; retain source formatting in evidence quotations.

The HTML output uses a restrained light scientific/editorial design: strong typographic hierarchy, neutral surfaces, accessible contrast, compact evidence tables, responsive layout, and printable structure. Severity color is supportive, never the sole carrier of meaning. Do not use gradients, animated decoration, product chrome, or dashboard hype.

## Runtime and output safety

- Do not install packages during execution.
- DOCX reading, generation, and validation use the Python standard library.
- Stop if the input cannot be read; do not create a partial report.
- Use a dedicated output directory. Never point `--out` at a workspace root, home directory, system root, or directory containing unrelated material.
- Do not follow symlinks when validating output artifacts.
- Generated reports may contain confidential experimental material; retain and share them according to the user's access and retention rules.
- Do not send source material to an external service unless the user explicitly authorizes that transmission.

## MCP use

No PatSnap MCP service is required for auditing material supplied by the user. The source workflow is local and deterministic.

If the user separately asks for patent or scientific evidence, use only an actually available, authorized service and keep retrieved evidence separate from submitted method facts. Relevant verified global PatSnap options may include:

- `advanced_patent_search`: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing`: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- `scientific_translational_evidence` when currently exposed and appropriate

External evidence does not replace method-specific measurements or EHS review. No MCP configuration file is part of this source package, so none is added.

## Completion checks

Before reporting completion, verify:

- the entire source material was read or faithfully transcribed;
- every issue has an evidence basis and required addition;
- `not specified` is not presented as `not performed`;
- sample identifiers exclude gases, solvents, equipment, and condition strings;
- sample and issue counts reconcile across context, HTML, and DOCX;
- both reports contain every required section;
- no raw dictionary, `None`, internal enum, or unescaped user content appears;
- output files are non-empty and open as valid HTML/DOCX;
- no report claims safety approval, result authenticity, patentability, or legal clearance;
- the final chat response is concise and points to the generated artifacts.
