# U.S. Patent Claims Review Checklist

Use this reference for full reviews of uploaded U.S. patent application documents or complex claim sets.

## Intake

- Confirm whether the document includes claims, abstract, specification, drawings, sequence listings, examples, or prior-art discussion.
- Identify the technology field and whether special scrutiny applies: software/AI, biotech/pharma, diagnostics, chemistry/materials, mechanical devices, electronics, telecom standards, business methods.
- Identify each independent claim, its category, and its commercial target.
- Map each dependent claim to its parent and determine whether it adds a meaningful fallback limitation.

## BRI Scope Review

- Flag terms that may be read broader than intended by an examiner.
- Check whether the specification defines key terms or provides enough context to narrow broad technical nouns.
- Flag result-only limitations such as "configured to improve," "optimized," "based on," "automatically," or "intelligently" when no mechanism is recited.
- Ask whether the actual inventive distinction appears in the claim body.

## 35 U.S.C. 112(a)

- Written description:
  - Check every limitation against the specification.
  - Flag generalized claim language that exceeds disclosed embodiments.
  - Check support for ranges, alternatives, species, combinations, negative limitations, and optional features.
- Enablement:
  - Ask whether the full claim scope can be practiced without undue experimentation.
  - For software/AI, check whether the algorithm, data flow, model training, architecture, or control logic is sufficiently disclosed.
  - For chemistry/biotech/materials, check whether examples support the full genus, range, function, or therapeutic/technical effect.

## 35 U.S.C. 112(b)

- Flag missing antecedent basis: `the X` without earlier `a/an X`.
- Flag inconsistent terminology: `processor`, `controller`, `computing device`, and `server` used interchangeably without clarity.
- Flag relative terms without objective boundaries: `about`, `substantially`, `high`, `low`, `near`, `fast`, `efficient`, `optimized`.
- Flag unclear actor or step order in method claims.
- Flag mixed statutory categories, such as an apparatus claim requiring a user action as a limitation.
- Flag limitations that merely state an intended use or desired result.

## 35 U.S.C. 112(f)

- Check for `means for` and nonce words: `module`, `unit`, `component`, `mechanism`, `element`, `device`, `logic`, `engine`.
- If a limitation may invoke 112(f), identify the corresponding structure, material, or acts in the specification.
- For computer-implemented functions, check whether the specification discloses an algorithm rather than only a generic processor.
- Suggest structural language when the applicant likely does not want 112(f) treatment.

## 35 U.S.C. 101

- Software/AI/business methods:
  - Identify whether the claim is only data collection, analysis, decision-making, and output.
  - Look for concrete technical improvement to computing, networking, storage, security, sensors, manufacturing, medical devices, or another technical field.
  - Suggest adding specific data structures, transformations, hardware interactions, or control steps when support exists.
- Life sciences/diagnostics:
  - Check whether the claim risks covering a natural correlation or natural phenomenon.
  - Prefer concrete treatment, preparation, assay configuration, or transformed sample steps where supported.

## 35 U.S.C. 102/103

- Do not state that claims are novel unless a prior-art search was performed.
- Conduct structural vulnerability review:
  - Are independent claims composed of conventional elements?
  - Is the difference a predictable combination or routine optimization?
  - Are technical effects recited or at least supported by the specification?
  - Do dependent claims preserve non-obvious fallback features?
- Suggest fallback limitations that tie to technical advantage and are likely visible in the specification.

## Claim Architecture

- Prefer a layered claim set: broad independent claims, mid-level fallback dependent claims, narrow implementation dependent claims.
- Consider parallel categories where appropriate: system, method, computer-readable medium, apparatus, composition, manufacture, or kit.
- Avoid unnecessary commercial-environment limitations in independent claims.
- Avoid relying on a single narrow feature across all claims unless it is truly the invention.
- Check whether dependent claims merely repeat independent claim language without substantive narrowing.

## Restriction and Election Risk

- Identify multiple independent invention concepts, species, product/method groups, or unrelated embodiments.
- Look for linking claims that may keep groups together.
- Suggest divisional or continuation planning when claim groups are commercially important but likely to be restricted.

## Enforceability and Infringement Proof

- Ask whether each limitation can be proven from public information, product testing, documentation, source code discovery, or network behavior.
- Flag limitations requiring knowledge of a competitor's internal intent or hidden server-side logic.
- For method claims, identify divided infringement risk when steps are performed by different actors.
- Prefer system or apparatus claims when the product can be observed more easily than user behavior.
- Identify easy design-arounds and suggest broader functional or structural alternatives when supported.

## Amendment Suggestions

For each important issue, recommend one of:

- Broaden: remove unnecessary environment, user, UI, implementation, or parameter limitations.
- Clarify: add antecedent basis, objective standard, actor, sequence, or structural definition.
- Narrow strategically: add a supported technical feature that distinguishes likely prior art.
- Recast: convert result language into concrete mechanism or data flow.
- Add dependent claim: preserve fallback without over-narrowing the independent claim.
- Add specification support: only when filing has not occurred or continuation/new matter rules allow it.

## Severity Guide

- High: likely 101/112 rejection, unsupported broadening, indefinite claim boundary, missing core novelty, divided infringement, or claim scope that does not cover the commercial product.
- Medium: likely prosecution friction, obviousness vulnerability, weak fallback positions, restriction risk, or avoidable 112(f) ambiguity.
- Low: polish, formatting, style, optional strategy, or minor U.S. practice preference.
