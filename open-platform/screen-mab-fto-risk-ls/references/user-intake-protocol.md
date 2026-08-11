# User Intake Protocol

## Purpose

Collect the technical, commercial, territorial, and timing facts needed to define a monoclonal-antibody FTO screen. Ask once in a structured form, accept partial answers, and distinguish what can proceed from what remains blocked.

## When to use this protocol

Use it when the user provides only a sequence, an asset name, or an incomplete product description. Do not launch a full FTO workflow when the relevant embodiment, territory, activity, or timing is undefined.

## Execution levels

| Level | Minimum information | Permitted output |
|---|---|---|
| Intake only | A general request with no defined candidate | Completed/missing field matrix and search plan |
| Preliminary sequence screen | At least one versioned, usable sequence | Sequence-search evidence and limitations only |
| Technical patent landscape | Target plus defined technical concepts and countries | Discovery/screening results; no FTO conclusion |
| FTO risk screen | Defined embodiment, planned acts, countries, timing, and sufficient technical evidence | Claim-level risk triage with explicit gaps |
| Legal opinion support | FTO screen evidence plus current official records and counsel instructions | Evidence package for qualified counsel |

## One-pass intake form

Ask only questions relevant to the candidate. Preserve `unknown` and `not applicable`; do not force guesses.

### A. Matter definition

- Matter or project name:
- Requestor/team:
- Decision to support:
- Required delivery date:
- Analysis cutoff date:
- Development stage:
- Expected launch or first commercial act:
- Confidentiality classification and handling restrictions:
- Prior FTO work or counsel instructions:

### B. Planned activities

For each country, state whether the team plans to:

- research or develop;
- make or have made;
- use;
- offer for sale;
- sell;
- import/export;
- conduct clinical trials;
- obtain regulatory approval;
- formulate, fill/finish, package, or distribute;
- practice a diagnostic or treatment method.

Record manufacturing sites, contract manufacturers, supply routes, and launch countries separately. Patent risk attaches to acts and territories, not merely to a target market label.

### C. Candidate identity

- Public/nonproprietary name, development code, and aliases:
- Molecule type: conventional mAb / fragment / nanobody / bispecific or multispecific / fusion / ADC / radioimmunoconjugate / other:
- Target/antigen, gene symbol, aliases, species, and target form:
- Binding epitope or competition group:
- Mechanism and intended functional effect:
- Isotype/subclass and light-chain type:
- Valency, geometry, chain pairing, and format:
- Public comparators and closest known competitors:
- Candidate version identifier and freeze date:

### D. Sequence evidence

For every sequence, provide:

- sequence ID and version;
- amino-acid or nucleotide type;
- VH, VL, full heavy/light chain, CDR, Fc, linker, payload-associated peptide, vector, or other region;
- raw sequence or approved file path;
- numbering scheme: IMGT, Kabat, Chothia, AHo, EU, or other;
- species and germline where known;
- signal peptide/propeptide inclusion;
- source document, laboratory record, or database record;
- checksum if available;
- whether disclosure to external services is authorized.

Do not extract CDRs from fixed residue ranges without validated numbering. For multispecifics, capture every arm and pairing arrangement.

### E. Fc, glycan, and modification features

- Fc sequence and subclass:
- Named or explicit substitutions, deletions, insertions, or engineered motifs:
- Numbering scheme and source/destination residue:
- Effector-function objective:
- FcRn/half-life objective:
- Glycoform, fucosylation, sialylation, galactosylation, or other glycoengineering:
- PEG, albumin, XTEN, label, chelator, radionuclide, or fusion features:
- Site-specific or enzymatic conjugation technology:

### F. ADC-specific features

- Antibody component and target:
- Payload name, class, structure, stereochemistry, salt, and identifier:
- Linker name, structure, cleavage mechanism, and spacer:
- Attachment site and chemistry:
- Drug-to-antibody ratio target and distribution:
- Release/metabolism mechanism:
- Free payload, linker-payload, and conjugate manufacturing steps:
- Analytical and purification controls:

### G. Manufacturing and CMC

- Encoding nucleic acids and vectors:
- Promoter, signal peptide, selectable marker, and host cell:
- Cell-line generation or editing:
- Culture/media/feed/perfusion features:
- Capture, polishing, viral clearance, conjugation, purification, and analytical methods:
- Formulation composition and concentration:
- Excipients, buffer, pH, surfactant, stabilizer, lyophilization, viscosity, and container closure:
- Route and presentation: IV, SC, prefilled syringe, autoinjector, vial, or other:
- Contract manufacturer and site-specific processes:

### H. Clinical and use features

- Disease/indication and clinically relevant synonyms:
- Patient population, line of therapy, biomarker, and exclusions:
- Dose, route, schedule, loading/maintenance, and treatment duration:
- Monotherapy or combination partners:
- Diagnostic, selection, monitoring, or companion-test steps:
- Claimed or planned treatment sequence and endpoints:

### I. Territories and timing

List countries individually. For Europe, identify target validated states and whether Unitary Patent/UPC issues matter. For each country:

- planned activity;
- earliest relevant date;
- commercial/manufacturing importance;
- search language requirements;
- acceptable status scope: granted only, granted plus pending, or broader historical review;
- monitoring horizon and refresh cadence.

`WO/PCT` may be included for family discovery and future national-stage monitoring, but it is not a stand-alone infringement territory.

### J. Ownership, licenses, and relationships

- Owned patent families:
- Inbound/outbound licenses, covenants, settlements, or collaboration rights:
- Scope by product, field, indication, activity, country, sublicensing, and term:
- Partners, licensors, licensees, contract manufacturers, and affiliates:
- Competitors, former names, subsidiaries, acquired entities, and co-developers:
- Known disputes, oppositions, challenges, or legal opinions:

Do not assume a partner patent is harmless. Obtain the operative agreement or record the license question as unresolved.

## Intake response matrix

Convert answers into this structure:

| Field | Value | Status | Source/version | Effect if missing | Action owner |
|---|---|---|---|---|---|
| Candidate version |  | confirmed/provisional/unknown/N/A |  |  |  |
| Planned acts |  |  |  |  |  |
| Countries |  |  |  |  |  |
| Relevant dates |  |  |  |  |  |
| VH/VL/CDRs |  |  |  |  |  |
| Target/epitope |  |  |  |  |  |
| Fc/modifications |  |  |  |  |  |
| ADC structure |  |  |  |  |  |
| Manufacturing |  |  |  |  |  |
| Formulation |  |  |  |  |  |
| Indication/regimen |  |  |  |  |  |
| Competitors/entities |  |  |  |  |  |
| Licenses/owned rights |  |  |  |  |  |
| Cutoff/confidentiality |  |  |  |  |  |

## Search-filter injection

Translate confirmed intake data into a versioned search plan rather than a single opaque query.

### Jurisdictions

- Apply country filters to discovery where supported.
- Run a broader family/WO search to identify future or related members.
- Verify each material national member separately.
- Do not use `EP` alone as a substitute for validated national coverage.

### Legal status

- Include granted/live rights for present-risk screening.
- Include pending applications when future claim risk is relevant.
- Retain expired/lapsed/abandoned/revoked records where they illuminate a live family, priority, prosecution, estoppel, ownership, or design history.
- Do not rely on a single normalized status label for exclusion.

### Dates

- Use the current analysis cutoff, not a fixed historical window.
- Search older foundational filings as required by priority and family chains.
- Account for the publication blind period and possible unpublished applications.

### Languages

- Search English plus official/local-language synonyms appropriate to the selected countries.
- Expand target, disease, company, mutation, formulation, and process variants.
- Label machine translation and preserve original-language claims.

## Gate decision

Before retrieval, issue one of these decisions:

- `ready_for_full_screen` — embodiment, acts, countries, timing, and technical evidence are sufficient;
- `ready_with_declared_gaps` — work may proceed, but named modules/conclusions remain provisional;
- `preliminary_module_only` — only sequence or landscape work is supported;
- `blocked_by_missing_definition` — retrieval would not answer a defined FTO question;
- `blocked_by_confidentiality_or_access` — required data cannot be handled or retrieved safely.

State the missing fields, affected modules, and permitted next output.

## Data-protection gate

- Confirm authorization before sending unpublished sequences or structures to an external service.
- Minimize candidate detail in queries where possible.
- Never include API keys, personal data, agreement terms, or privileged advice in query strings or report links.
- Record access restrictions in the matter file.
- If the environment is not approved, work from redacted or local exports and disclose the coverage limitation.

## Quality checklist

- [ ] All questions were asked in one relevant, structured request.
- [ ] Unknown and not-applicable fields remain distinct.
- [ ] Candidate version and source provenance are frozen.
- [ ] Planned acts, manufacturing countries, sales countries, and dates are separate.
- [ ] Europe is resolved to actual territorial coverage where needed.
- [ ] WO/PCT is not treated as an enforceable territory.
- [ ] Sequences have regions, numbering scheme, version, and disclosure authorization.
- [ ] Modification, ADC, CMC, formulation, use, and combination features are captured when applicable.
- [ ] Owned/licensed/partner rights are not assumed cleared.
- [ ] Legal-status scope supports the decision horizon.
- [ ] The gate decision and its consequences are explicit.
