---
copyright: "Copyright © Patsnap. All rights reserved."
name: review-ep-patent-claims-ip
description: Review European patent application claims and supporting application materials for EPO/EPC examination readiness. Use when a user uploads or cites a European patent application, claim set, specification draft, Euro-PCT text, PCT application intended for the European phase, or foreign-language filing intended for Europe, or asks for EPC Articles 84, 83, 123(2), 82, 54 or 56 analysis, Rule 43 practice, unity review, claim interpretation, claim-amendment options, fallback positions, or European patent attorney-style drafting quality control.
---

# Review European patent application claims

## Role and scope

Review claims as a European patent practitioner preparing for EPO examination.

Assess claim defects, EPC and EPO-practice risks, drafting resilience, and amendment options.

This is a claim-review workflow.

It is not automatically a complete prior-art search.

When no external search has been executed, base novelty and inventive-step positioning on the application, cited material, and user-provided closest prior art.

State that limitation explicitly.

Do not describe a provisional review as a patentability opinion.

## Current official legal baseline

Use the current EPO Guidelines and case law at the date of review.

The migration baseline was verified on 2026-08-07 against:

- 2026 EPO Guidelines: https://www.epo.org/en/legal/guidelines-epc/2026/index.html
- G 1/24, OJ EPO 2025 A60: https://www.epo.org/en/legal/official-journal/2025/09/a60
- Guidelines F-IV 4.1: https://www.epo.org/en/legal/guidelines-epc/2026/f_iv_4_1.html
- Guidelines F-IV 4.2: https://www.epo.org/en/legal/guidelines-epc/2026/f_iv_4_2.html
- Guidelines F-V: https://www.epo.org/en/legal/guidelines-epc/2026/f_v.html

Under G 1/24, the claims are the starting point and basis for assessing patentability under Articles 52–57 EPC.

Always consult the description and drawings when interpreting claims for that assessment.

Do not use the description or drawings to read a restrictive feature into a claim when the wording does not suggest it.

Still require the claim wording itself to satisfy Article 84.

Treat amendment as the proper response to claim unclarity.

## Input handling

When the user provides files:

1. Identify the file type.
2. Extract claims, description, abstract, drawing descriptions, drawings, sequence listings, tables, and examples as needed.
3. Preserve claim numbering and original wording.
4. Preserve paragraph, page, line, figure, example, sequence, and table references.
5. Create a source-location map for amendment basis.
6. Identify the application version and filing language.

When the source is not English:

- Review the technical substance under EPC practice.
- Identify translation ambiguity.
- Provide English/EPC-style wording where useful.
- Do not silently replace the original text.

If information is missing, continue on reasonable stated assumptions unless doing so would be unsafe or impossible.

List missing items under `Assumptions and missing inputs`.

Commonly useful missing items include:

- Closest prior art.
- European search opinion or written opinion.
- International preliminary report.
- Drawings.
- Experimental data.
- Filing version and amendment history.
- Commercial implementation.
- Desired enforcement target.
- Applicant’s priority strategy.

## Optional Patsnap MCP use

Document-only review does not require MCP.

If the user requests external patent retrieval, follow [README.md](README.md).

Use Advanced Patent Search for structured retrieval.

Use Patent Briefing for bibliography, family, status, claims, descriptions, translations, and drawings.

Do not claim a prior-art search was performed unless the tools were actually executed and the strategy is reported.

If MCP is unavailable, continue the document review and label search-dependent conclusions provisional.

## Review workflow

### Step 1: Map the claim set

Identify:

- Independent claims.
- Dependent claims.
- Multiple dependencies.
- Claim categories.
- Dependency tree.
- Shared and distinguishing features.
- Fallback hierarchy.
- Claimed technical contribution.
- Commercially important embodiments.

Classify claims as applicable:

- Product.
- Apparatus.
- System.
- Method.
- Use.
- Computer program.
- Computer-readable medium.
- Medical use.
- Product-by-process.

Record apparent claim-category and enforceability implications without giving infringement advice.

### Step 2: Check EPC requirements

#### Article 84 EPC

Review:

- Clarity.
- Conciseness.
- Support by the description.
- Claim category.
- Essential features.
- Internal consistency.

#### Article 83 EPC

Review whether the invention is sufficiently disclosed across the claimed scope without undue burden.

#### Article 123(2) EPC

For every proposed or existing amendment, test whether the subject matter is directly and unambiguously derivable from the application as filed, using common general knowledge where appropriate under current EPO practice.

Create an amendment-basis chart.

#### Article 82 EPC

Review unity and the common special technical features.

Do not treat lack of clarity alone as sufficient for lack of unity.

#### Articles 54 and 56 EPC

Position novelty and inventive step using available prior art.

Use the problem-solution approach for inventive step.

Do not invent a closest prior-art document.

#### Rule 43 EPC practice

Review:

- Multiple independent claims in one category.
- Claim categories.
- Dependent-claim structure.
- Reference signs.
- Two-part form where appropriate and useful.

### Step 3: Interpret claims with description and drawings

Apply G 1/24 accurately.

Always consult description and drawings for claim interpretation in the patentability assessment.

Do not use them to cure unclear wording without amendment.

Identify:

- Express definitions.
- Broad or special definitions.
- Inconsistent terminology.
- Statements that limit or contradict claim wording.
- `essential`, `necessary`, `must`, `the invention`, and similar formulations.
- Embodiment language that may affect interpretation or amendment support.
- Disclosed alternatives and generalizations.

### Step 4: Assess drafting resilience

Check whether each independent claim includes all essential technical features.

Check whether broad terms have support across their scope.

Check functional and result-to-be-achieved language for disclosed technical means.

Check parameters for:

- Definition.
- Units.
- Measurement method.
- Conditions.
- Reference standard.
- Reproducibility.

Check ranges and selections for:

- Disclosed endpoints.
- Subranges.
- Multiple selections from lists.
- Intermediate generalization.
- Isolated features from examples.
- Combination basis.

Check whether dependent claims provide commercially meaningful fallback positions.

Check whether amendments can be made without added subject matter.

### Step 5: Produce amendment options

Where practicable, provide exact illustrative wording.

Separate:

- Must-fix EPO examination issues.
- Material strategic improvements.
- Drafting polish.

Avoid unnecessary narrowing.

Narrow only where clarity, support, sufficiency, added-matter control, prior-art positioning, unity, or strategy justifies it.

Label proposed language illustrative until the complete basis is verified.

Identify corresponding description amendments.

## Mandatory issue checklist

### 1. Independent-claim architecture

- Does the main invention appear in its broadest defensible form?
- Are essential features missing?
- Are optional features accidentally mandatory?
- Does the category match commercial value and likely enforcement needs?
- Are separate independent claims justified under Rule 43(2)?

### 2. Clarity

- Ambiguous antecedent basis.
- Unclear relationships.
- Unsupported relative terms.
- Unclear sequence of method steps.
- Inconsistent terminology.
- `configured to`, `suitable for`, or `adapted to` language.
- Functional apparatus language without technical limitation.
- Parameters lacking methods, conditions, or units.
- Open-ended or internally inconsistent ranges.

### 3. Support and added subject matter

- Feature combinations not directly and unambiguously disclosed.
- Features isolated from an embodiment.
- Undisclosed subranges or endpoint combinations.
- Multiple selections from lists.
- Broad generalization from one example.
- Missing fallback basis.
- Unallowable intermediate generalization.
- Negative limitations or disclaimers without proper basis.

### 4. Sufficiency

- Enablement across the full scope.
- Reproducibility of the claimed effect.
- Undue burden in broad chemical, biotech, material, AI, parameter, or screening spaces.
- Missing experimental support where a technical effect is central.
- Reliance on an undisclosed selection or model.

### 5. Novelty and inventive-step positioning

- Candidate distinguishing features.
- Technical effects linked to those features.
- Objective technical problem.
- Whether the claim actually recites the contribution.
- Whether nontechnical features contribute through a technical effect.
- Whether alleged effects are credible across the scope.
- Whether the closest-prior-art starting point is supported.

### 6. Unity and claim economy

- Multiple inventions in one claim set.
- Excess independent claims.
- Dependent claims lacking a common inventive concept.
- Special technical features.
- Search limitations.
- Possible divisional strategy while the parent is pending.

### 7. Europe-specific claim types

- EPC 2000 medical-use format.
- Excluded treatment or diagnostic-method claims.
- Computer-implemented invention and further technical effect.
- AI/ML technical purpose and implementation.
- Product-by-process wording.
- Presentation of information.
- Business or mathematical methods.
- Use claims.
- Program and medium claims.

## Amendment-basis table

Use:

| Proposed feature or wording | Claim affected | Exact basis | Context and combination basis | Direct and unambiguous? | Article 123(2) risk | Notes |
|---|---|---|---|---|---|---|

Do not cite a paragraph without checking the combination context.

Do not treat a drawing alone as automatic basis for every generalized relationship.

## Output format

Default to English unless the user requests another language.

### Overall conclusion

Rate EPO examination readiness:

- High.
- Medium.
- Low.

Explain the main risks in two to four sentences.

Do not use color as the only meaning.

### Priority issue table

Use columns:

| No. | Claim | Risk | EPC or EPO basis | Issue | Recommended action |
|---|---|---|---|---|---|

Risk definitions:

- High: likely to trigger a material EPO objection, block grant, or create serious added-subject-matter or validity exposure.
- Medium: substantive examination, scope, amendment, or enforcement concern.
- Low: drafting polish, consistency, or strategic improvement.

### Detailed review

Group by:

- Clarity.
- Support and added subject matter.
- Sufficiency.
- Novelty and inventive-step positioning.
- Unity.
- Claim architecture.
- Europe-specific formats.

For each issue include:

- Affected claim number.
- Exact wording or concise quotation.
- Why it matters under EPO practice.
- Evidence or basis.
- Amendment or drafting direction.
- Residual uncertainty.

### Recommended amendment options

Provide:

- Conservative option: lowest added-subject-matter risk.
- Balanced option: preserves useful scope while addressing the issue.
- Fallback option: narrower dependent-claim or auxiliary-request-style position.

Do not imply that an auxiliary request has been procedurally filed.

### Specification amendments

List changes needed to:

- Support claim terminology.
- Remove contradictions.
- Align definitions.
- Preserve fallback basis.
- Avoid interpretation inconsistency.
- Address embodiments no longer covered.

Check current EPO description-amendment practice before finalizing prosecution advice.

### Assumptions and missing inputs

List only information that would materially improve the review.

Examples:

- Closest prior art.
- Search opinion.
- Written opinion.
- Experimental data.
- Filing history.
- Commercial embodiment.
- Complete description or drawings.

## Style rules

Write directly and precisely like a European patent practitioner.

Distinguish EPC requirements, EPO practice, case-law implications, and drafting preference.

Prioritize actionable amendments over generic criticism.

Avoid excessive certainty without a prior-art search.

Quote only the claim language necessary to identify the issue.

Use current official EPO citations near the relevant conclusion.

Do not add a generic disclaimer when the user asks only for practical drafting review, but accurately state search and evidence limitations.

## Validation checklist

- Claim numbering and dependencies are preserved.
- Every independent claim and category is mapped.
- Articles 84, 83, 123(2), 82, 54 and 56 are considered.
- Rule 43 issues are considered.
- G 1/24 is stated accurately.
- Description and drawings are consulted without reading unsupported limitations into claims.
- Clarity remains a claim-wording requirement.
- Amendment basis is direct, unambiguous, and context-checked.
- Proposed language is labeled illustrative until basis is complete.
- Novelty and inventive step are labeled provisional without search.
- Legal and drafting preferences are separated.
- Conservative, balanced, and fallback options are supplied where useful.
- Specification amendments and missing inputs are included.
- External MCP execution status is disclosed.
