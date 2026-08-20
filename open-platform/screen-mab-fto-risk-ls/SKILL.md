---
copyright: "Copyright © Patsnap. All rights reserved."
name: screen-mab-fto-risk-ls
description: Conduct an evidence-backed freedom-to-operate risk screen for monoclonal antibodies, bispecific antibodies, and antibody-drug conjugates across user-selected markets. Use when a user provides antibody sequences or a defined biologic candidate and asks for patent clearance, claim coverage screening, jurisdiction-specific risk triage, or design-around questions.
---

# Screen mAb FTO Risk

## Purpose and boundary

Screen whether enforceable or potentially enforceable patent claims in selected jurisdictions may cover the planned making, use, sale, offer for sale, importation, manufacturing, formulation, or treatment activities of a monoclonal antibody, bispecific antibody, antibody fragment, or antibody-drug conjugate.

This is an evidence and triage workflow. It does not deliver a legal opinion, guarantee freedom to operate, decide infringement or equivalents, validate a patent, or replace jurisdiction-qualified counsel.

## Trigger boundary

Use this skill when:

- a user supplies VH, VL, CDR, full-chain, or construct sequences and requests an FTO screen;
- a defined mAb, bispecific, fragment, radioconjugate, or ADC needs patent clearance;
- a user asks for a jurisdiction-specific blocking-claim shortlist;
- a team wants claim-feature comparison or evidence-grounded design-around hypotheses.

Do not use it for:

- small-molecule-only FTO;
- patentability or novelty of one invention;
- a general competitor pipeline or clinical landscape;
- a final legal conclusion without qualified counsel and current official-register verification.

## Read these package resources

Read in this order before executing:

1. `references/user-intake-protocol.md`
2. `references/search-modules.md`
3. `references/modification-search.md`
4. `references/workflow-steps.md`
5. `references/search-loop.md`
6. `references/sequence-search.md`
7. `references/patent-family-merge.md`
8. `references/output-contract.md`

Use `scripts/mab_fto_recall_estimator.py` only as a diagnostic for observed track overlap, incremental yield, and declared coverage gaps. It does not estimate recall or authorize a completeness claim.

## Intake gate

Collect all material facts in one structured request. Do not force the user through serial questions.

### Minimum basis for a complete screen

- the product or process embodiment to be cleared;
- at least one usable antibody sequence or a sufficiently precise public asset identity;
- target/antigen and relevant species;
- intended indication/use and material regimen or combination features;
- target country or validated-state territory;
- planned acts and timing, including research, manufacture, import, sale, and treatment where relevant;
- analysis date/cutoff;
- available structure, sequence, formulation, manufacturing, conjugation, and licensing information.

If only a sequence is supplied, sequence searching may begin as a documented preliminary module, but do not label the result an FTO conclusion.

### Candidate architecture

Capture, where applicable:

- antibody format, isotype, heavy/light chain and chain pairing;
- VH/VL and CDR sequences with numbering scheme and provenance;
- target, epitope, affinity, mechanism, and species reactivity;
- Fc sequence, glycoform, mutations, effector function, and FcRn properties;
- bispecific geometry, heterodimerization, common-light-chain, assembly, and valency;
- ADC linker, payload, attachment chemistry/site, drug-to-antibody ratio, and release mechanism;
- expression construct, host cell, media, production, purification, analytical and formulation features;
- dose, route, schedule, population, biomarker, combination, and indication;
- planned manufacturing sites, supply chain, markets, launch window, and development stage;
- owned/licensed patents and known competitors.

Label each value `confirmed`, `provisional`, `unknown`, or `not applicable`, with source and date.

## Jurisdiction and legal-status gate

Never default silently to China, the United States, or Europe. Ask for the commercial and manufacturing countries. Treat:

- a PCT/WO publication as an international application record, not an enforceable worldwide right;
- an EP grant as a bundle whose validation, unitary effect, opposition, limitation, lapse, and national status require verification;
- US continuations, divisionals, continuations-in-part, reissues, post-grant proceedings, PTA, PTE, terminal disclaimers, and Orange/Purple Book context where relevant;
- national supplemental protection, patent term extension, pediatric extension, regulatory safe-harbor, experimental-use, and Bolar-type rules as jurisdiction-specific;
- pending claims as changeable and not presently enforceable, but potentially material to launch risk;
- expired, lapsed, revoked, abandoned, and disclaimed rights as still relevant to family history, priority, claim construction, estoppel, design history, or a live related member.

Do not exclude a record solely because an aggregated database says “inactive.” Verify material candidates in the official register and preserve the retrieval date.

## MCP and evidence routing

No MCP is required when the user supplies complete, authoritative records and official-register evidence.

For live work, use only available, authorized, verified global Patsnap MCPs:

| Need | MCP | Use |
|---|---|---|
| Broad/nested/semantic/applicant/number search | `advanced_patent_search` | Primary patent discovery and query refinement; marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search |
| Claims, description, bibliography, family, legal status, translations, drawings | `patent_briefing` | Primary-document enrichment and family verification; marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing |
| Drug identity and milestones | `drug_asset` | Optional candidate/competitor context only; marketplace: https://open.patsnap.com/marketplace/mcp-servers/drug-asset |

The global marketplace page named `chemistry-small-molecule` currently advertises no callable tools, so it is not mapped as an operational structure-search dependency. Sequence alignment and chemical structure search remain required when relevant, but do not invent connector names. Use an authorized service only if it is actually exposed in the environment; otherwise request a Patsnap or other authoritative export and document the gap.

Always verify material legal status and prosecution events against the relevant official register. A Patsnap status field is a discovery aid, not the final legal-status authority.

## Evidence hierarchy

1. issued claims and current official-register status in each target jurisdiction;
2. current pending claims and complete prosecution record;
3. specification, sequence listing, drawings, priority documents, certificates, disclaimers, and post-grant decisions;
4. verified family and bibliographic data;
5. candidate technical records and controlled internal data;
6. court decisions, statutes, rules, and current jurisdiction-specific guidance;
7. secondary analysis and news, clearly labeled.

Never fill missing claim text from memory. If the controlling claim version cannot be retrieved, mark the record `claim text unavailable` and withhold claim-coverage conclusions.

## Standard workflow

### Step 0 — Define the clearance question

- freeze candidate version and source files;
- define jurisdictions, acts, timing, cutoff, legal-status scope, and deliverables;
- create a feature inventory and evidence ledger;
- state excluded activities and unresolved inputs;
- distinguish preliminary screen from counsel-grade opinion support.

Output: `tech_profile.md`.

### Step 1 — Sequence search (M1)

Use `references/sequence-search.md`.

Search separate, versioned inputs where available:

- VH and VL;
- CDR-H1/H2/H3 and CDR-L1/L2/L3;
- full heavy and light chains;
- hinge and Fc regions;
- each arm/pairing architecture for multispecifics;
- peptide linker or peptide payload elements for applicable conjugates.

Record query sequence, checksum, numbering scheme, threshold, database, date, result identifier, aligned region, identity, positives, gaps, length, and mismatch positions. Similarity is a retrieval signal only, never an infringement score.

Outputs: `sequence_alignment_log.md` and additions to `patent_pool.json`.

### Step 1.5 — Modification and structure search (M1.5)

Use `references/modification-search.md` after initial sequence retrieval and before final keyword convergence.

Cover when applicable:

- glycosylation, afucosylation, and glycoengineering;
- PEGylation, albumin fusion, half-life extension, and related formats;
- Fc substitutions and named mutation sets;
- bispecific assembly and Fc heterodimerization;
- ADC linker, payload, attachment site, conjugation chemistry, and DAR;
- labels, chelators, radionuclide conjugates, and other chemical modifications.

Expand amino-acid substitutions to one-letter, three-letter, source/residue/destination, position-only, numbering-scheme, and relevant language variants. Do not infer a missing source residue. Preserve the exact numbering scheme.

Do not use ADMET prediction to determine patent relevance, infringement, or enablement. It may support a separately labeled R&D question only.

Output: additions to `patent_pool.json` with `source_modules` including the applicable M1.5 submodule.

### Step 2 — Technical keyword and semantic search (M2–M8)

Use `references/search-modules.md` to cover:

- M2 target, antigen, epitope, and mechanism;
- M3 antibody/platform architecture;
- M4 Fc, cell, and genetic engineering;
- M5 formulation, presentation, and delivery;
- M6 combination and regimen;
- M7 indication, biomarker, population, dose, and method of treatment/use;
- M8 nucleic acid, vector, host cell, expression, manufacturing, and purification.

Build jurisdiction-appropriate English queries plus locally relevant languages. Treat classifications as expansion tools, not fixed truth; confirm current CPC/IPC scope and date ranges.

### Step 3 — Competitor and entity search (M9)

- search known competitors and product/asset names;
- normalize legal names, former names, subsidiaries, acquired entities, licensors, licensees, co-developers, and inventors;
- record the source/date/basis of each relationship;
- do not assume corporate affiliation or license scope;
- search by applicant/assignee and technical concepts together and separately;
- review continuation/divisional/national-stage branches and recent unpublished blind spots explicitly.

Output: `competitor_entity_map.md`.

### Step 4 — Normalize records, status, and families

Use `references/patent-family-merge.md`.

- deduplicate exact publications while preserving every search-route hit;
- retrieve priority, family, continuity and jurisdictional members;
- verify material members in official registers;
- retain both controlling granted claims and material pending claim versions;
- identify oppositions, reexaminations, disclaimers, limitations, revocations, SPC/PTE/PTA, lapse/restoration, and ownership events when relevant;
- calculate estimated term only from documented dates/rules and label uncertainty;
- never use one family-level risk label as a substitute for member-by-member territorial analysis.

Outputs: `patent_pool_filtered.json` and `patent_pool_family.json`.

### Step 5 — Two-stage screening

#### Triage

Exclude from the claim-comparison queue only with a documented reason, reviewer, and evidence:

- no target-market live or potentially live member;
- no technically material claim overlap after claim review;
- activity outside the claimed act or territory;
- verified license/covenant/exhaustion analysis makes the claim non-blocking for the defined scenario;
- duplicate publication already represented without losing claim-version differences.

Do not exclude merely because the applicant is the user's company or partner. Ownership and license scope must be verified.

#### Claim screening

- identify every relevant independent claim and any dependent claim that adds a feature material to the candidate;
- use the claim version controlling on the analysis date;
- segment each claim into legally meaningful limitations without losing relationships;
- map candidate evidence to every limitation;
- distinguish present fact, planned fact, unknown fact, and inferred fact;
- analyze each claim, member, jurisdiction, and planned act separately.

Output: `blocking_candidates.json`.

### Step 6 — Claim coverage and legal-issue matrix

For each claim:

| Field | Requirement |
|---|---|
| Jurisdiction/member | Exact publication or patent number and status date |
| Claim/version | Claim number, type, source, version/event, and retrieval date |
| Limitation | Short exact excerpt or faithful paraphrase with locator |
| Candidate evidence | Source/version/locator or `unknown` |
| Literal mapping | mapped / not mapped / uncertain / not assessed |
| Equivalents issue | question for counsel; jurisdiction-specific and never probability-scored by the model |
| Prosecution/validity context | separately labeled; not used to erase a live claim automatically |
| Next action | evidence, search, engineering, license, monitoring, or counsel task |

One missing limitation can defeat literal coverage of that claim, but do not convert that observation into a final non-infringement opinion. Dependent claims are not skipped: they inherit all parent limitations and may be independently material.

Outputs: `claim_diff_matrix.md` and `risk_summary.json`.

### Step 7 — Report

Use `references/output-contract.md` to produce the listed intermediate artifacts and `fto_report.html` when requested.

The report must disclose:

- candidate/version and planned acts;
- target jurisdictions and cutoff;
- sources, queries, modules, languages, date ranges, and database timestamps;
- search funnel and known blind spots;
- family/continuity and status method;
- claim-by-claim evidence mapping;
- jurisdiction-level priority and uncertainty;
- actionable monitoring, evidence, engineering, licensing, and counsel next steps;
- limitations and a non-reliance statement.

## Search convergence

Run keyword, semantic, sequence, classification, applicant/entity, citation/family, and modification routes as applicable. Maintain `query_history` and a module/jurisdiction coverage matrix.

Use the supplied script after each round. Its `manual_stop_review` decision means only that observed incremental yield is low and required declared coverage has no recorded gap. Before stopping, a human reviewer must confirm:

- all applicable modules executed or waived with reason;
- every jurisdiction and locally relevant language covered;
- key claims and status verified;
- assignee, family, continuation/divisional, citation, inventor, and competitor branches reviewed;
- synonyms, sequence variants, classifications, and false-negative tests documented;
- known gaps accepted by the user and counsel.

Never state a numerical recall percentage from track overlap.

## Risk communication

Use priority categories rather than infringement probabilities:

- **Critical review** — a live target-market claim appears to map to all material planned features, or a decisive fact is unresolved before an imminent act;
- **High review** — substantial mapping with one or more legally/technically material uncertainties;
- **Monitor** — pending claims, uncertain status/term, incomplete mapping, or a plausible future branch;
- **Low current relevance** — documented non-mapping or territorial/timing mismatch, subject to stated assumptions;
- **Resolved for defined scenario** — counsel-verified license, covenant, expiration/lapse, or other basis, with scope/date recorded.

Do not use “70% infringement,” “safe,” “clear,” “non-infringing,” or similar definitive labels unless quoting qualified legal advice.

Multiple search-route hits increase retrieval confidence, not legal risk. Exact CDR-H3 or high sequence identity triggers claim review; it does not itself establish coverage. Likewise, structural similarity, shared target, same indication, or same applicant is not infringement.

## Design-around work

Treat design-around ideas as hypotheses tied to specific claim limitations. For each idea:

- identify the claim/member/jurisdiction;
- identify the limitation targeted;
- explain the proposed technical change;
- identify effects on literal mapping and the open equivalents question;
- check other independent/dependent claims and family members;
- identify efficacy, safety, manufacturability, regulatory, CMC, and new-patentability validation;
- require counsel and experimental review before implementation.

Do not recommend arbitrary residue substitutions, isotype switching, framework changes, epitope shifts, formulation changes, or supply-chain moves as “safe” without this analysis.

## Mandatory failure paths

- **Missing candidate definition:** restrict output to intake gaps and a preliminary protocol.
- **No sequence service:** run non-sequence modules if authorized, label M1 uncovered, and do not issue a complete sequence-led screen.
- **Claim text missing:** retain the record, mark the claim analysis pending, and do not infer text.
- **Status uncertain:** retain/monitor and verify in the official register.
- **Translation only:** cite the original-language claim and label translation; obtain local-language review for material conclusions.
- **Large result set:** preserve counts/query, refine transparently, and sample only for query testing—not for final clearance.
- **Conflicting data:** show both sources and timestamps; do not silently choose.
- **Pending/unpublished blind spot:** disclose it and define monitoring cadence.
- **Counsel unavailable:** deliver an evidence pack and unresolved-issue list, not a final FTO opinion.

## Quality gates

- [ ] Candidate version, planned acts, territories, launch/manufacturing timing, and cutoff are explicit.
- [ ] All applicable M1–M9 and M1.5 modules are complete or waived with reasons.
- [ ] Sequence inputs have provenance, checksums, numbering schemes, and per-query thresholds.
- [ ] Search queries, languages, classifications, applicants, date ranges, and timestamps are reproducible.
- [ ] Exact publications are deduplicated without collapsing material family/claim differences.
- [ ] Every material member has official-register status verification or a visible gap.
- [ ] Granted and pending claim versions are distinguished.
- [ ] Independent and material dependent claims are mapped limitation by limitation.
- [ ] Missing facts are not treated as non-mapping.
- [ ] Similarity and multi-route hits are not treated as infringement scores.
- [ ] Equivalents analysis is framed as a jurisdiction-specific counsel question.
- [ ] Terms, extensions, disclaimers, post-grant events, ownership, and licenses are evidence-backed.
- [ ] PCT and EP territorial effects are described correctly.
- [ ] Patent links use exact global Patsnap or official-register destinations, never a legacy domestic product domain.
- [ ] HTML is self-contained, accessible, responsive, printable, and visually restrained.
- [ ] No credentials, sensitive sequences beyond authorized scope, fabricated patents, claims, cases, or legal citations appear.
- [ ] Conclusions state assumptions, uncertainty, next action, owner, and timing.

## Confidentiality and output boundaries

- Minimize exposure of unpublished sequences and product details; use approved systems and access controls.
- Do not place secrets or API keys in queries, artifacts, logs, or links.
- Do not fabricate claim text, status, term, ownership, licenses, litigation, or technical evidence.
- Do not use stale hard-coded date windows.
- Do not quote long claims unnecessarily; preserve precise source locators.
- Do not describe database coverage as exhaustive.
- Recommend qualified patent counsel for all material jurisdiction-specific conclusions.
