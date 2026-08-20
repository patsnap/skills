# Detailed Workflow Steps

## Overview

```text
Step 0    Define candidate, acts, countries, timing, evidence, and confidentiality
Step 1    Search biological sequences (M1)
Step 1.5  Search modifications, Fc engineering, conjugates, and structures (M1.5)
Step 2    Search technical concepts (M2–M8)
Step 3    Expand competitors and related entities (M9)
Step 4    Normalize records; verify status, term, family, and continuity
Step 5    Triage, then screen controlling claims
Step 6    Build claim-limitation and jurisdiction risk matrices
Step 7    Produce evidence artifacts and a review-ready report
```

Every step must preserve sources, retrieval timestamps, candidate version, jurisdiction, reviewer, and unresolved gaps.

## Step 0 — Define the matter

### 0-A Intake

Apply `user-intake-protocol.md`. Capture:

- candidate identity/version and sequence provenance;
- target, epitope, mechanism, species, format, and isotype;
- Fc/glycan/modification or ADC features;
- expression, manufacturing, purification, analytics, and formulation;
- indication, population, biomarker, dose, route, schedule, and combinations;
- planned acts, manufacturing sites, launch countries, and dates;
- owned/licensed rights, known competitors, prior searches, and counsel instructions;
- confidentiality and approved tools.

### 0-B Scope and assumptions

Define:

- target jurisdictions and actual European validated/unitary states;
- analysis cutoff and expected commercial horizon;
- granted, pending, and historical status treatment;
- product, process, use, formulation, and supply-chain scope;
- source/database coverage and languages;
- what would constitute a preliminary versus complete screen.

Do not silently default to any territory or fixed date range.

### 0-C Candidate feature model

Create `tech_profile.md` with stable feature IDs:

```text
SEQ-H-001    heavy-chain sequence/version
SEQ-L-001    light-chain sequence/version
TGT-001      target and species
EPI-001      epitope/competition group
FMT-001      antibody architecture
FC-001       Fc subclass/mutations/glycoform
ADC-001      linker/payload/attachment/DAR
MFG-001      expression/manufacturing feature
FORM-001     formulation/presentation
USE-001      indication/population/regimen
ACT-001      planned jurisdictional act
```

Each feature needs value, status, source, version, locator, and confidentiality classification.

### 0-D Filter plan

Convert the scope into per-module filters. Do not force identical filters across incompatible search services. Record jurisdiction, date, legal status, language, applicant, classification, and technical concepts separately.

### 0-E Optional drug/asset context

Use supplied evidence or the verified global `drug_asset` MCP only when authorized. Retrieve public asset identity, target, organizations, and milestones to improve aliases and competitor context. Do not treat pipeline data as patent ownership, license scope, claim evidence, or legal status.

Output: `tech_profile.md` and an intake/gap table.

## Step 1 — Sequence search (M1)

Read `sequence-search.md`.

### 1-A Prepare queries

- validate alphabet, length, chain, signal peptide, and version;
- calculate checksum;
- number variable domains with the selected scheme;
- extract CDRs through validated numbering;
- split multispecific arms and common chains;
- prepare Fc/hinge/full-chain/nucleotide queries when relevant;
- confirm authorization for external disclosure.

### 1-B Execute tiers

Run exact/high-identity discovery, then broader sensitivity routes. The source's CDR-H3, other CDR, VH/VL, full-chain, hinge, and Fc tiers remain starting points, but thresholds must be documented and adapted to length/database behavior.

### 1-C Normalize hits

Record alignment metrics, sequence source, publication, family, result route, and raw export reference. Resolve each hit to claim/disclosure/listing context.

### 1-D Review

Prioritize exact and high-coverage hits for claim retrieval. Never assign legal risk solely from identity, CDR-H3 match, or number of sequence tracks.

Outputs: `sequence_alignment_log.md`, `patent_pool.json` additions, and the M1 coverage record.

## Step 1.5 — Modification search (M1.5)

Read `modification-search.md`.

### 1.5-A Glycosylation

Search fucosylation/afucosylation, glycoforms, glycosyltransferases, glycan engineering, host/process controls, and functional effects when present in the candidate.

### 1.5-B Half-life/fusion modifications

Search PEG, albumin, FcRn, XTEN and other candidate-relevant extension formats by name, concept, structure, and process where available.

### 1.5-C Fc substitutions and multispecific assembly

Expand every explicit substitution across one-letter, three-letter, source/destination, position, numbering scheme, and locally relevant languages. Search named mutation sets, functional descriptions, Fc receptors, effector effects, heterodimerization, and chain-pairing technologies.

### 1.5-D ADC/conjugate technology

Search linker, payload, cleavage, spacer, attachment site, conjugation chemistry, DAR, purification, analytics, release, method, formulation, and use. Use exact/substructure/similarity search where an authorized chemistry tool exists.

### 1.5-E Other structures

Search labels, chelators, radionuclide precursors, imaging conjugates, or other chemical features relevant to the actual candidate.

Do not use ADMET predictions as patent-risk evidence.

Output: `patent_pool.json` additions tagged with applicable M1.5 submodules.

## Step 2 — Technical search (M2–M8)

Read `search-modules.md`.

### M2 Target and binding

Search target/antigen aliases, gene/protein names, species, epitope, competition, affinity, binding, blockade, neutralization, agonism, depletion, and mechanism.

### M3 Architecture/platform

Search humanization, fully human discovery, display/transgenic platforms, fragments, nanobodies, bispecific/multispecific formats, pairing, valency, fusions, and construct architecture.

### M4 Engineering

Search Fc/hinge/glycan modifications, cell engineering, gene editing, sequence variants, and functional engineering actually relevant to the candidate.

### M5 Formulation/delivery

Search composition ranges, buffers, excipients, stabilizers, surfactants, concentration/viscosity, lyophilization, SC/IV presentation, hyaluronidase, containers, devices, and storage.

### M6 Combination/regimen

Search specific partners, classes, sequence/timing, synergy language, route, dose, and regimen—not only generic “combination” terms.

### M7 Use

Search disease/subtype, biomarker, line, prior treatment, response state, population, dose, schedule, route, companion diagnosis, and method/use claim conventions by jurisdiction.

### M8 Expression/manufacturing

Search nucleic acids, vectors, promoters, signal peptides, host cells, production, culture/media, purification, viral clearance, conjugation, analytics, and quality attributes.

Output: module-tagged additions to `patent_pool.json` and a query history.

## Step 3 — Competitor/entity expansion (M9)

### Entity tiers

1. user-named competitor and product owner;
2. parent, subsidiary, former name, and acquired entity;
3. co-developer, licensor, licensee, collaborator, and contract manufacturer;
4. inventors and assignee variants from high-relevance records.

Verify every relationship with source and effective date. A ten-year acquisition window may be a useful starting test, not a fixed rule.

### Search routes

- applicant/assignee plus target/technology;
- applicant/assignee without technical constraint for classification review;
- inventors plus relevant technology;
- asset/development code and aliases;
- acquired entity names through relevant filing periods;
- continuity, family, citations, assignments, and ownership events.

Output: `competitor_entity_map.md` and M9-tagged results.

## Step 4 — Normalize, verify, and group

### 4-A Exact-record normalization

- normalize publication/application/grant identifiers;
- preserve country and kind code;
- deduplicate exact publications;
- retain all source routes and module tags;
- keep application, publication, and grant records distinct.

### 4-B Jurisdiction and status verification

For material members, retrieve current official-register evidence. Record status category, event, event date, source, retrieval date, uncertainty, and reviewer.

Do not automatically delete inactive records. Determine whether a live relative, priority, prosecution, estoppel, ownership, term, or historical issue remains relevant.

### 4-C Family and continuity

Use `patent-family-merge.md`. Preserve:

- simple/extended family identifiers and provider definition;
- priority chain;
- US continuation/divisional/CIP/reissue links;
- PCT national stages;
- EP grant/validation/unitary/opposition/limitation relationships;
- material pending and granted claim versions.

### 4-D Term

Estimate ordinary term only where data supports it. Verify maintenance, lapse/restoration, PTA/PTE, SPC, pediatric extensions, disclaimers, terminal disclaimers, and post-grant changes separately. Label estimated and verified dates.

Outputs: `patent_pool_filtered.json` and `patent_pool_family.json`.

## Step 5 — Two-stage screening

### 5-A Triage

For each record/family/member, record `retain`, `exclude_from_claim_queue`, or `monitor`, plus:

- reason code;
- cited claim/record/status evidence;
- jurisdiction;
- reviewer/date;
- assumptions and reopening condition.

Valid reasons may include no target-territory member, no technical claim overlap, verified expiry/lapse with no relevant live branch, or a counsel-confirmed license for the defined scenario. Applicant identity alone is not a valid exclusion.

### 5-B Claim screening

- retrieve controlling claims and prosecution source;
- identify independent claims and material dependent claims;
- retain dependency relationships;
- segment limitations without changing legal meaning;
- map candidate evidence and planned acts;
- record literal mapping and open construction/equivalents questions;
- analyze every material jurisdiction/member separately.

Output: `blocking_candidates.json`.

## Step 6 — Claim and risk matrices

Build `claim_diff_matrix.md` with:

```text
Jurisdiction/member | status/source date | claim/version | claim type/dependency
limitation ID | exact excerpt/locator | candidate feature/source/version
literal mapping | uncertainty | construction/equivalents question | next action
```

Build `risk_summary.json` with:

- matter/candidate/version/cutoff;
- family/member/claim identifiers;
- planned act and jurisdiction;
- priority category and rationale;
- decisive mapped/unmapped/unknown limitations;
- status/term confidence;
- evidence gaps;
- monitoring trigger;
- counsel and technical actions.

Do not encode infringement percentages. Multiple search-module hits affect discovery confidence, not claim coverage.

## Step 7 — Reporting

Read `output-contract.md`.

### Required report checks

- all ten source-defined artifacts are present when applicable;
- report scope reconciles to intake and candidate version;
- queries and search funnel reconcile;
- family/member counts reconcile;
- granted/pending and original/translated claims are distinct;
- every priority statement has claim/status/technical evidence;
- all patent links use global Patsnap or official-register URLs;
- no API keys or confidential raw data are embedded;
- HTML is self-contained, semantic, accessible, responsive, and printable;
- assumptions, exclusions, blind spots, and monitoring are visible;
- qualified counsel review is recommended for material decisions.

## Final release gate

The analyst may release a preliminary screen only after:

- intake and scope gate are satisfied;
- applicable modules are complete or visibly waived;
- material claims and official status are available or gaps are prominent;
- query history, coverage matrix, and exclusions are reproducible;
- claim mappings have source locators;
- legal statements are jurisdiction-specific and current or explicitly reserved for counsel;
- report and intermediate artifacts pass the output contract;
- a reviewer records release type: `preliminary evidence screen`, `updated monitor`, or `counsel support package`.

Never label the output “FTO cleared.”
