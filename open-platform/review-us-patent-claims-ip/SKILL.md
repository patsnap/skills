---
copyright: "Copyright © Patsnap. All rights reserved."
name: review-us-patent-claims-ip
description: Review supplied US patent application claims and relevant specification, drawings, Office-action, and prosecution context for claim quality, prosecution readiness, 35 U.S.C. 101/102/103/112 risk, BRI, 112(f), dependency/form, restriction/election, continuation/divisional strategy, infringement observability, and amendment options. Use for US claim review, drafting quality control, amendment strategy, or a structured claim issue list.
---

# Review US patent claims

## Purpose and boundary

Provide evidence-based US patent drafting and examination-quality assistance. Do not claim to be a licensed attorney or patent agent, and do not present the output as legal advice, a filing clearance, a validity opinion, an infringement opinion, or a guarantee of allowance.

Use `references/review-checklist.md` for every full or complex review.

Current USPTO examination guidance and case law can change. Re-check the relevant official authority for the actual filing date, application route, procedural posture, technology, and review date.

## Supported materials

- pasted claims;
- DOCX, PDF, TXT, or Markdown claim sets;
- complete application/specification;
- drawings and sequence listings;
- Office actions and draft responses;
- claim amendments and redlines;
- PCT applications intended for US national-stage or continuation practice; and
- identified published US applications/patents.

If a file is unreadable, request an accessible copy or pasted text. Do not infer missing text.

## Intake

Capture:

- exact document and claim version;
- source filename and date;
- application type: provisional, nonprovisional under 35 U.S.C. 111(a), national stage under 35 U.S.C. 371, continuation, divisional, CIP, reissue, or unknown;
- application/publication/patent number if available;
- priority and filing dates;
- pre-AIA/AIA status where relevant;
- prosecution stage and deadline;
- current claims, marked-up claims, and clean claims;
- specification, abstract, drawings, examples, sequence listing, deposit/data, and prior-art discussion supplied;
- Office-action grounds and cited references;
- target commercial embodiment and likely infringing actor;
- desired breadth and fallback positions;
- jurisdictions from which language was adapted;
- whether filing already occurred; and
- whether claim amendments may add subject matter.

For AI-assisted inventions, flag inventorship facts for qualified review under current USPTO guidance. Do not decide inventorship from prompt history alone.

## Document-availability matrix

Before analysis, state:

| Material | Available | Version/date | Supports | Cannot determine without it |
|---|---|---|---|---|
| Claims | | | Scope/form/dependency | |
| Specification | | | 112(a), definitions, 112(f), amendment basis | |
| Drawings | | | Structural relationships/support | |
| Filing history | | | claim versions, estoppel, rejections, elections | |
| Cited prior art | | | reference-specific 102/103 review | |
| Business embodiment | | | coverage/observability/design-around | |

If only claims are supplied, label written description, enablement, corresponding structure/algorithm, and amendment basis as preliminary.

## Optional Patsnap connectors

No connector is required for supplied authoritative materials.

### Patent Briefing — recommended for identified publications

- https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- key: `patent_briefing`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use to retrieve or cross-check bibliography, family, status, claims, description, translations, and images. Verify against the authoritative application/prosecution record when material.

### Advanced Patent Search — recommended only for authorized search

- https://open.patsnap.com/marketplace/mcp-servers/patent-search
- key: `advanced_patent_search`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Use to resolve identifiers or conduct an authorized prior-art search. Record exact query, fields, dates, authorities, family rule, references reviewed, and claim-feature mapping.

Do not call a structural 102/103 review a novelty search.

## Current authority orientation

Use official current USPTO/MPEP material as examination-practice guidance and distinguish it from statutes, regulations, precedential case law, and litigation claim construction.

Official pages checked for migration on 2026-08-07:

- Subject-matter eligibility: https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility
- MPEP 2106: https://www.uspto.gov/web/offices/pac/mpep/s2106.html
- BRI, MPEP 2111: https://www.uspto.gov/web/offices/pac/mpep/s2111.html
- 112(f), MPEP 2181: https://www.uspto.gov/web/offices/pac/mpep/s2181.html
- Multiple dependent claims, MPEP 608.01(n): https://www.uspto.gov/web/offices/pac/mpep/s608.html
- Restriction, MPEP 802: https://www.uspto.gov/web/offices/pac/mpep/s802.html
- National restriction versus PCT/371 unity, MPEP 823: https://www.uspto.gov/web/offices/pac/mpep/s823.html

The current USPTO eligibility page identifies MPEP 2103–2106.07 as current guidance and lists later updates, including the 2024 AI eligibility update, 2025 reminders/Desjardins-related changes, and 2026 Rule 132 declaration best practices. Check the page again in a live matter.

## Workflow

### 1. Identify scope and authority

- Confirm whether review covers claims only, full application, amendment, Office-action response, or portfolio strategy.
- Identify application route and procedural posture.
- Identify review date and current authority cutoff.
- Separate pre-filing drafting suggestions from post-filing amendments.
- Identify deadlines but do not calculate a dispositive deadline without authoritative docket information.

### 2. Extract the claim set

Preserve:

- claim number;
- exact text;
- status if known (originally filed, currently pending, canceled, withdrawn, allowed, rejected, amended);
- independent/dependent/multiple-dependent form;
- statutory category;
- parent reference(s);
- dependency path;
- amendment changes; and
- source page/paragraph/locator.

Do not silently correct text before logging the issue.

### 3. Build the dependency graph

Check:

- duplicate or missing claim numbers;
- reference to nonexistent/canceled claims;
- circular or impossible dependencies;
- dependent claims that fail to further limit the parent;
- multiple dependent claims referring in the alternative only;
- a multiple dependent claim depending from another multiple dependent claim;
- mixed-category dependencies;
- inconsistent incorporation of limitations; and
- fee/claim-count implications requiring current verification.

### 4. Identify claimed inventive concepts

For each independent claim:

- statutory category;
- actor/system boundary;
- essential elements/steps;
- apparent technical problem;
- claimed technical mechanism;
- result/effect;
- likely commercial embodiment;
- likely distinguishing limitations;
- evidence/source locator; and
- uncertainty.

Do not substitute the abstract or marketing description for the claim language.

### 5. Apply BRI for pending US examination

MPEP 2111 states that pending claims receive the broadest reasonable interpretation consistent with the specification, not the broadest possible interpretation.

Review:

- ordinary/customary meaning to a person of ordinary skill;
- express definitions;
- consistent specification/drawing usage;
- preamble effect;
- transitional phrase;
- functional language;
- intended use;
- wherein/whereby clauses;
- relative terms;
- ranges; and
- open/closed language.

Do not apply prosecution BRI as though it were the issued-claim litigation standard. State the procedural context.

### 6. Review 35 U.S.C. 112(a)

#### Written description

For each limitation, identify support by paragraph/page/figure/example/sequence.

Review:

- genus/species breadth;
- ranges and endpoints;
- alternatives/Markush groups;
- combinations and subcombinations;
- negative limitations;
- optional features;
- functional results;
- newly introduced terminology;
- priority entitlement concerns; and
- new-matter risk for amendments.

#### Enablement

Review the full claimed scope and technology-specific predictability, working examples, guidance, variability, testing burden, and undue experimentation risk under current law.

For software/AI, inspect disclosed architecture, data flow, model/training/inference steps, control logic, technical improvement, and implementation detail.

For chemistry, biotech, pharma, diagnostics, and materials, inspect representative species, ranges, protocols, structure/function, endpoints, utility, and evidence across the claimed scope.

Do not conclude enablement from one example without analyzing scope.

#### Best mode

For applications subject to AIA treatment, distinguish the disclosure requirement from enforceability consequences; route matter-specific advice to qualified counsel.

### 7. Review 35 U.S.C. 112(b)

Check:

- antecedent basis;
- inconsistent terminology;
- unclear boundaries;
- subjective/relative terms;
- terms of degree and objective standards;
- optional/alternative language;
- unclear step order;
- actor ambiguity;
- mixed statutory categories;
- intended-use/result-only language;
- internally inconsistent ranges;
- claim-reference errors; and
- ambiguity introduced by translation.

Context controls the result. Words such as “about,” “substantially,” “module,” or “configured to” are not automatically indefinite.

### 8. Review 35 U.S.C. 112(f)

MPEP 2181 states application turns on claim language, not applicant intent.

For each function-associated term:

1. identify whether the claim uses “means” or “step”;
2. identify whether the term has sufficiently definite structural meaning in context;
3. identify the complete claimed function;
4. locate corresponding structure, material, or acts in the specification;
5. confirm linkage between disclosure and function;
6. for computer-implemented functions, locate a sufficient algorithm where required;
7. assess indefiniteness/scope consequences; and
8. compare structural recasting if 112(f) is not intended.

Do not treat a list of nonce words as a per se rule.

### 9. Review 35 U.S.C. 101

Use the current USPTO subject-matter-eligibility framework and current controlling law.

Analyze each claim as a whole:

- statutory category;
- judicial exception, if recited;
- Step 2A Prong One;
- Step 2A Prong Two/practical application;
- Step 2B/significantly more;
- claimed technological improvement;
- specification support for that improvement;
- additional elements and their arrangement; and
- claim-specific outcome.

For software/AI, do not use a fixed list of magic eligible terms. Evaluate concrete improvements to computer functionality or another technical field and the claim as a whole.

For diagnostics/life sciences, distinguish natural correlation/phenomenon/product concerns from supported concrete treatment, preparation, assay configuration, transformation, or other claim elements.

Do not conflate eligibility with novelty, obviousness, or disclosure.

### 10. Review 35 U.S.C. 102 and 103

#### Without an executed search

Perform only structural vulnerability review:

- conventional element aggregation;
- apparent predictable combination;
- routine optimization/range selection;
- result-only distinction;
- missing technical mechanism;
- weak nexus between feature and effect;
- likely single-reference exposure; and
- fallback limitation quality.

Label this `search_status: not_executed`.

#### With cited references or an executed search

For each ground/reference:

- verify publication date and prior-art eligibility for the relevant filing/priority context;
- map every claim limitation;
- identify explicit, implicit, or inherency theory;
- for 103, identify combination rationale, analogous art, reasonable expectation of success, teaching away, unexpected results, objective indicia and nexus where supported;
- distinguish examiner assertion from verified reference disclosure;
- record missing limitation/evidence; and
- avoid final novelty/nonobviousness conclusions without qualified review.

### 11. Review claim architecture

Assess:

- independent claim categories;
- commercial actor/product coverage;
- broad, intermediate, and narrow fallback layers;
- meaningful dependent claims;
- parallel system/method/CRM/apparatus/composition/manufacture/kit claims as appropriate;
- unnecessary environment/UI/user/parameter limitations;
- product-by-process and intended-use issues;
- unsupported breadth;
- single-point-of-failure limitations;
- continuation/divisional/CIP options; and
- double-patenting/terminal-disclaimer issues for qualified review.

Do not add a claim category merely to increase count.

### 12. Review restriction/election

For US national applications under 111(a), review current MPEP Chapter 800 principles for independent/distinct inventions, species, product/process groups, burden and linking claims.

For 371 national stage/PCT context, distinguish unity-of-invention practice under MPEP 823/Chapter 1800.

Identify:

- invention groups;
- species/genus structure;
- design/operation/effect relationship;
- linking/generic claims;
- rejoinder potential;
- election consequences;
- divisional timing/35 U.S.C. 121 safe-harbor issues requiring counsel; and
- continuation strategy.

Do not predict a restriction requirement solely from multiple independent claims.

### 13. Review infringement observability and enforceability strategy

This is drafting strategy, not an infringement opinion.

Review:

- whether each limitation is externally observable;
- public documentation, testing, teardown, source-code discovery, network evidence, or manufacturing proof needed;
- single versus multiple actors;
- method-step attribution and divided-infringement risk;
- location/jurisdiction of system components or steps;
- product/system alternatives to hidden user behavior;
- easy design-arounds;
- claim differentiation and equivalents/estoppel sensitivity; and
- whether amendment language could create avoidable disclaimer.

### 14. Draft issue records

Each issue must include:

```yaml
issue_id: US-CLM-001
severity: High|Medium|Low
category: BRI|112a|112b|112f|101|102|103|form|architecture|restriction|observability|strategy
claim_numbers: []
quoted_language: ""
claim_source_locator: ""
specification_support_locator: ""
authority_or_practice_basis: ""
risk: ""
confidence: High|Moderate|Limited
recommended_action: ""
example_language: ""
scope_tradeoff: ""
new_matter_caution: ""
```

Do not assign High merely because a keyword appears.

### 15. Severity guide

- **High:** likely material rejection/indefiniteness/support problem, missing core claim coverage, serious actor/observability failure, material dependency/form defect, or amendment with substantial new-matter risk.
- **Medium:** likely prosecution friction, 103 vulnerability, weak fallback, 112(f) ambiguity, restriction/election exposure, or avoidable strategic limitation.
- **Low:** clarity polish, formatting, optional architecture improvement, or minor practice preference.

State uncertainty and procedural context.

### 16. Amendment and redline strategy

For each proposed change:

- exact claim and text;
- objective;
- support locator;
- anticipated effect on BRI/101/102/103/112;
- scope gained/lost;
- actor/observability effect;
- dependency changes;
- new-matter warning;
- prosecution-history/disclaimer concern; and
- whether a dependent claim is preferable.

Post-filing additions must not introduce new matter. If support cannot be located, do not present language as safely amendable.

## Output structure

```markdown
# US patent claims review

## Overall assessment
[Preliminary risk, document completeness, prosecution posture, and readiness boundary.]

## Scope and materials
[Document/version matrix, authority cutoff, search status.]

## Claim-set map
[Independent claims, categories, dependencies, invention groups.]

## Priority issues
| Severity | Issue ID | Claim | Category | Quoted language | Risk | Support/authority | Recommended action | Confidence |
|---|---|---|---|---|---|---|---|---|

## Claim-by-claim review
### Claim [n]
- Scope/BRI:
- Category/dependency:
- 101:
- 102/103 search status and vulnerability:
- 112(a)/(b)/(f):
- Observability/actor:
- Recommendation/support:

## Amendment strategy
[Independent claims, dependent fallback ladder, continuation/divisional options, change log.]

## Example amendment text
[Only supported representative language, with additions/deletions clearly marked.]

## Limitations and attorney review gates
[Missing materials, search, current law, deadlines, new matter, claim construction, business facts.]
```

## Final checks

- Exact claim version identified.
- Application route and stage identified.
- Claim numbers/categories/dependencies reconcile.
- BRI is prosecution-context and specification-consistent.
- 112(a) statements have support locators or are preliminary.
- 112(f) analysis identifies function and corresponding disclosure.
- 101 uses current claim-as-a-whole guidance.
- 102/103 search status is explicit.
- Multiple-dependent format follows current US rules.
- Restriction and PCT unity are distinguished.
- Proposed amendments have basis and new-matter review.
- Observability and actor issues are separate from infringement conclusions.
- Current official authorities are rechecked.
- Output is drafting/review assistance, not legal advice.
