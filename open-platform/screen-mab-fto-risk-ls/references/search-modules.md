# Nine Search Modules for mAb FTO Screening

## Operating rules

This reference preserves the source nine-module architecture while making it global, reproducible, and claim-oriented.

For every module:

- adapt concepts to the actual candidate rather than running a generic fixed query;
- search English plus locally relevant languages for the selected jurisdictions;
- use current classification definitions and record scheme/version;
- preserve exact query, filters, date, database, result count, export, and reviewer;
- include claims-focused, title/abstract/claims, semantic, applicant, and classification routes as appropriate;
- distinguish discovery hits from claim relevance;
- tag every record with all source modules/routes;
- do not turn similarity, module count, target match, or applicant match into legal risk.

Placeholders use angle brackets and must be replaced or removed before execution.

## M1 — Antibody sequence search

Read `sequence-search.md` for the controlling protocol.

### Coverage

- CDR-H3, CDR-H1/H2, CDR-L1/L2/L3;
- VH and VL;
- full heavy/light chains;
- hinge and Fc domains;
- each multispecific arm, common light chain, and pairing architecture;
- peptide linkers/fusions and encoding nucleotide sequences where relevant.

### Query design

Run separate, versioned queries per region. Record identity, coverage, gaps, alignment length, mismatch positions, numbering scheme, database/version, threshold, and raw export.

The source values such as exact/high-identity CDR-H3, 80% other CDRs, 85% VH/VL, 90% full chain, and 95% hinge/Fc may be evaluated as initial search tiers. They are not legal cutoffs and must be sensitivity-tested.

### Claim gate

For every shortlisted hit, determine whether the sequence is:

- recited in a current claim;
- within a claimed identity/variant definition;
- required through CDR or functional limitations;
- disclosed but unclaimed;
- present only in a sequence listing;
- cited from another record;
- not yet verified.

No sequence match creates an infringement conclusion without the full claim and candidate mapping.

## M2 — Target, antigen, binding, and mechanism

### Concept families

- target protein/gene and approved symbols;
- former symbols, aliases, CD name, receptor/ligand, isoform, complex, domain, and species;
- soluble/membrane/activated/mutant form;
- epitope, competition, binding site, conformational/linear epitope;
- affinity, avidity, selectivity, cross-reactivity;
- blocking, neutralizing, agonist, antagonist, depletion, internalization, signaling, or trafficking mechanism;
- antibody, antigen-binding protein, immunoglobulin, fragment, multispecific, conjugate, fusion, or scaffold terms.

### Fielded pattern

```text
(<target aliases>)
AND (<antibody/binding-format terms>)
AND (<binding/mechanism terms where appropriate>)
```

Use title/abstract/claims and claims-only variants. Avoid requiring an indication in the first target search because composition claims may omit it.

### Semantic patterns

- antibody binding a defined target and blocking/activating a named pathway;
- antibody competing with a known ligand or reference antibody;
- antigen-binding molecule recognizing a specific domain or epitope;
- internalizing antibody suitable for conjugate delivery.

### Expansion

- target orthologs/species and transliterated names;
- pathway partners only when they test a documented blind spot;
- reference antibodies, competition groups, and public asset aliases;
- inventor/applicant and classification intersections;
- sequence hit families lacking target terms in the title.

### Exclusions

Do not infer same epitope from same target, same mechanism from same disease, or claim coverage from a background mention.

## M3 — Antibody architecture and platform

### Humanization and fully human discovery

Concepts:

- humanized, CDR graft, resurfacing, framework back-mutation;
- fully human antibody, phage/yeast/ribosome display;
- transgenic animal, human immunoglobulin locus, single B-cell discovery;
- affinity maturation, germlining, deimmunization.

Search platform brand names only when verified and relevant; include owner/former-owner aliases and generic functional descriptions.

### Fragments and alternative formats

- Fab, F(ab')2, scFv, diabody, tandem scFv;
- VHH, nanobody, single-domain antibody;
- minibody, fusion protein, Fc fusion;
- antibody mimetic/scaffold where within candidate scope.

### Bispecific/multispecific formats

- bispecific, multispecific, dual-targeting;
- IgG-like/non-IgG-like architecture;
- knob-into-hole, common light chain, CrossMab-type crossover, controlled Fab-arm exchange, electrostatic steering, heterodimerization;
- tandem, DART-like, BiTE-like, dual-variable-domain, two-in-one, asymmetric Fc;
- chain pairing, valency, geometry, linker, assembly, purification.

Do not assume a platform name has a stable generic meaning. Search explicit structural and functional features.

### Query pattern

```text
(<candidate target/sequence/asset>)
AND (<architecture/platform concept set>)
```

Also run architecture-only claims/classification queries for key competitors.

## M4 — Fc, glycan, cell, and genetic engineering

### Fc engineering

- effector function increase/reduction/elimination;
- Fc receptor and complement binding;
- FcRn and half-life;
- Fc substitution, deletion, insertion, motif, hinge, isotype, subclass;
- heterodimerization and chain pairing;
- aggregation, stability, protease resistance, and manufacturability.

Run exact mutation expressions and functional semantic queries. Use `modification-search.md` for numbering-aware expansion.

### Glycoengineering

- glycosylation, glycoform, N-/O-linked glycan;
- fucosylation/afucosylation, galactosylation, sialylation, bisecting GlcNAc;
- glycosyltransferases and glycosidases;
- host-cell pathway engineering;
- culture/media/process control of glycan profile;
- effector-function consequences where claimed.

### Cell and gene engineering

- CRISPR, Cas, ZFN, TALEN, base/prime editing;
- knock-in/knockout and site-specific integration;
- host-cell engineering for antibody production;
- vector/cassette engineering where not fully covered in M8.

### Guardrail

Search only engineering practiced by or material to the candidate. A generic CRISPR mention does not create product FTO relevance.

## M5 — Formulation, presentation, and delivery

### Core formulation

- pharmaceutical composition/formulation;
- antibody concentration and protein concentration ranges;
- pH, buffer, ionic strength, osmolality;
- sugars/polyols/amino acids/salts;
- surfactants, stabilizers, antioxidants, chelators, preservatives;
- aggregation, particles, viscosity, opalescence, stability;
- liquid, frozen, lyophilized, reconstituted, and ready-to-use forms;
- storage temperature and shelf life.

### Administration and presentation

- IV, SC, IM, intratumoral, ocular, inhaled, or other actual route;
- high-concentration and low-volume delivery;
- hyaluronidase/co-formulation;
- prefilled syringe, autoinjector, on-body injector, vial, cartridge, infusion bag;
- container closure, silicone oil, tungsten, stopper, device compatibility;
- dose preparation, dilution, and administration method.

### Query pattern

```text
(<asset/target/antibody or distinctive sequence>)
AND (<specific formulation component/range/presentation>)
```

Search exact ranges and combinations from the candidate. Generic formulation keywords alone create excessive noise.

### Claim review

Map every required component, range, ratio, pH, concentration, container, storage, and method step. Do not collapse overlapping numeric ranges into a conclusion without claim construction and local law.

## M6 — Combination treatment and regimen

### Concepts

- named partner drug/biologic/device/radiation/surgery;
- drug class and target class;
- simultaneous, sequential, prior, maintenance, induction, neoadjuvant/adjuvant;
- dose, schedule, cycle, route, duration, and sequence;
- synergy/additivity and biomarker-defined combination;
- fixed-dose/co-formulation versus separate administration;
- checkpoint, chemotherapy, targeted therapy, cell therapy, vaccine, or other relevant partners.

### Query routes

1. candidate/target + exact partner;
2. candidate/target + partner class;
3. mechanism + indication + regimen;
4. competitor asset + combination;
5. claims-focused dose/schedule/sequence search.

### Guardrails

- same two drugs in a specification is not necessarily a claimed combination;
- a Markush list requires claim-scope review;
- a treatment method may have country-specific enforceability and actor/divided-infringement issues;
- preserve patient, biomarker, line, and timing limitations.

## M7 — Indication, population, biomarker, and use

### Disease concepts

- formal disease name and abbreviations;
- histology/subtype/stage/grade;
- organ site and metastatic setting;
- molecular alteration, expression threshold, biomarker, companion diagnostic;
- resistant/refractory/relapsed, treatment-naive, prior therapy;
- line of treatment and patient subgroup;
- response or risk classification.

### Use/regimen concepts

- treatment, prevention, diagnosis, selection, monitoring;
- therapeutically effective amount;
- dose, route, interval, loading/maintenance, duration;
- monotherapy and combination;
- method-of-treatment, Swiss-type, purpose-limited product, and local claim forms.

### Query pattern

```text
(<target/asset/antibody>)
AND (<disease/subtype/biomarker>)
AND (<use/regimen concepts>)
```

Run broader disease-only semantic queries where asset names did not exist at filing.

### Jurisdiction gate

Analyze whether the claim form and planned actor/activity matter in each country. Do not apply US method-claim reasoning to EP, JP, CN, or other jurisdictions without local-law review.

## M8 — Nucleic acid, vector, expression, manufacturing, and analytics

### Nucleic acid and vector

- encoding polynucleotide, codon optimization;
- promoter, enhancer, UTR, intron, polyadenylation signal;
- signal peptide/leader;
- expression cassette/vector and copy number;
- selectable marker, amplification system, site-specific integration;
- separate versus combined heavy/light-chain constructs.

### Host cell and production

- CHO and exact host derivative, HEK, NS0, SP2/0, PER.C6 or actual host;
- stable/transient expression;
- cell-line engineering and clone selection;
- fed-batch, perfusion, continuous culture;
- medium/feed, temperature shift, pH, dissolved oxygen, osmolality;
- productivity and product-quality control.

### Purification and analytics

- Protein A or alternative capture;
- low-pH viral inactivation, filtration, chromatography, polishing;
- aggregate/fragment/charge/glycan removal;
- ultrafiltration/diafiltration;
- conjugation and post-conjugation purification;
- potency, purity, DAR, glycan, charge, aggregation, binding, or release assays;
- process sequence and parameter ranges.

### Query pattern

```text
(<candidate/target/sequence/antibody concept>)
AND (<specific vector/host/process/purification/analytical feature>)
```

Search process steps independently when platform patents may omit the product target.

### Territorial/supply-chain gate

Map each claimed process to where the step occurs. Consider importation of a product made by a patented process only under jurisdiction-specific law and counsel direction.

## M9 — Competitor, entity, inventor, and classification expansion

### Entity graph

Capture:

- legal name and historical names;
- parent/subsidiary and effective dates;
- acquired/divested entities;
- licensor/licensee/co-developer;
- university/research partner;
- contract manufacturer where process scope matters;
- key inventors from relevant families.

Store relationship type, source, date, confidence, and relevant technology. Do not infer ownership or license rights from news alone.

### Applicant/assignee queries

- entity alone + relevant classifications;
- entity + target/format/modification/process/use;
- former entity name during historical filing period;
- inventors + technology;
- current assignee versus original applicant, where supported.

### Classification expansion

Use current CPC/IPC definitions. Candidate starting areas may include:

| Area | Typical relevance |
|---|---|
| C07K 16 | Immunoglobulins/antibodies and formats |
| A61K 39 | Medicinal preparations containing antigens/antibodies |
| C12N | Nucleic acid, host cell, genetic engineering, production |
| A61P | Therapeutic activity/use |
| A61K 47 | Carriers/conjugates/formulation-related subject matter |

Do not assume classification coverage is complete or unchanged. Record searched subclasses and definitions.

### Date strategy

Do not use a fixed “last ten years” or hard-coded 2015–2025/2022–2025 window. Search through the matter cutoff, include foundational filings, and use recent windows only as explicit supplemental views. Disclose the unpublished-application blind period.

## Cross-module integration

### Record identity

Normalize publication numbers with country and kind code. Preserve application/grant identities and exact source record.

### Source tags

```json
{
  "publication_number": "US...",
  "source_modules": ["M1", "M1.5-C", "M2", "M9"],
  "source_routes": ["sequence", "claims_keyword", "applicant"],
  "query_ids": ["Q-001", "Q-014", "SEQ-VH-03"]
}
```

Multiple tags show retrievability and may support prioritization for review. They do not increase claim scope or legal risk.

### Triage fields

Every record should include:

- publication/application/grant identifiers;
- title, applicant, assignee, inventors;
- priority/application/publication/grant dates;
- family/continuity identifiers;
- target jurisdictions and status verification state;
- source modules/routes/query IDs;
- candidate features implicated;
- claim text/version availability;
- preliminary relevance and confidence;
- exclusion/retention reason;
- sources and retrieval timestamps.

## Module completion checklist

- [ ] M1 covered all applicable sequence units with provenance and sensitivity tests.
- [ ] M2 covered target aliases, binding, epitope, and mechanism.
- [ ] M3 covered actual architecture/platform and generic equivalents.
- [ ] M4 covered actual Fc/glycan/cell/gene engineering.
- [ ] M5 mapped the real formulation, ranges, presentation, and delivery.
- [ ] M6 mapped exact partners and regimen dimensions.
- [ ] M7 mapped disease, subgroup, biomarker, dose, and local claim forms.
- [ ] M8 mapped constructs, hosts, process, purification, analytics, and sites.
- [ ] M9 verified entity relationships, inventor, classification, and continuity routes.
- [ ] Every module has query history, counts, exports, and reviewer.
- [ ] Fixed dates, generic defaults, and unsupported risk weights are absent.
- [ ] Claim relevance is verified separately from retrieval relevance.
