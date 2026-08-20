# Modification Search Protocol (M1.5)

## Timing and purpose

Run after initial sequence searching and before final convergence of the text search. The module captures claims centered on antibody modifications, platform features, or conjugate components that sequence-only retrieval can miss.

## Routing

| Submodule | Primary routes | Optional specialized route |
|---|---|---|
| M1.5-A Glycosylation | fielded/claims/semantic patent search | glycan or biological-sequence evidence where available |
| M1.5-B PEG/fusion/half-life | fielded/claims/semantic search | exact/substructure/similarity structure search |
| M1.5-C Fc substitutions/assembly | mutation-aware text and semantic search | sequence search for defined Fc variants |
| M1.5-D ADC/conjugate | fielded/claims/semantic search | exact/substructure/similarity structure search |
| M1.5-E Other chemical modification | structure plus text search | chemical identifier normalization |

Use Patsnap `advanced_patent_search` for patent discovery and `patent_briefing` for claims, description, family, status, and translations when available. Use a chemistry or sequence service only if it is actually authorized and exposed. Do not invent the source's generic tool names.

## Global language strategy

English is required. Add local-language terminology based on selected jurisdictions and search value, for example German, French, Japanese, Korean, Simplified/Traditional Chinese, Portuguese, or Spanish. Record the language routes executed.

The source's Chinese-specific queries remain useful only when CN/TW/HK records or Chinese-language coverage is within scope. They are not mandatory for every global matter. Translate neither target names nor mutation syntax mechanically if local patent practice commonly preserves Latin symbols.

## Amino-acid substitution expansion

### Required parsing

For each mutation, capture:

- numbering scheme: EU, IMGT, Kabat, Chothia, AHo, sequence-native, or unknown;
- original/source residue if supplied;
- position;
- replacement/destination residue;
- chain/domain;
- candidate source and version.

Do not infer a source residue from a shorthand such as `428L` unless candidate/reference sequence evidence confirms it. `428L` may mean “Leu at 428,” while `M428L` explicitly describes Met-to-Leu.

### One-letter and three-letter mapping

| One-letter | Three-letter | English name |
|---|---|---|
| A | Ala | alanine |
| R | Arg | arginine |
| N | Asn | asparagine |
| D | Asp | aspartic acid |
| C | Cys | cysteine |
| E | Glu | glutamic acid |
| Q | Gln | glutamine |
| G | Gly | glycine |
| H | His | histidine |
| I | Ile | isoleucine |
| L | Leu | leucine |
| K | Lys | lysine |
| M | Met | methionine |
| F | Phe | phenylalanine |
| P | Pro | proline |
| S | Ser | serine |
| T | Thr | threonine |
| W | Trp | tryptophan |
| Y | Tyr | tyrosine |
| V | Val | valine |

### Expansion example

For a verified EU-numbered `M428L`, test:

```text
M428L OR M428Leu OR Met428Leu OR methionine 428 leucine
OR position 428 leucine OR residue 428 leucine
OR EU 428 OR EU-numbered position 428
```

Combine with antibody/Fc/FcRn/half-life concepts and relevant local-language forms. Add formatting variants such as `M428 L`, `M428→L`, `Met-428-Leu`, and mutation-set names when supported by the database syntax.

For `N434S`, `M252Y`, `S254T`, `T256E`, `L234A`, `L235A`, `P329G`, `N297A`, `S239D`, `I332E`, and other explicit source examples, apply the same logic. Do not limit searches to this list.

### Mutation sets

Search both individual substitutions and verified combinations:

- LALA and LALA-PG-type effector-reduction sets;
- aglycosylating N297 variants;
- YTE-type and LS-type half-life sets;
- ADCC-enhancing substitutions;
- candidate-specific Fc or heterodimerization sets.

Platform names and acronyms may be trademarks or ambiguously used. Pair them with explicit substitutions and functional descriptions.

## M1.5-A — Glycosylation and glycoengineering

### Coverage

- N-linked and O-linked glycosylation;
- fucosylation and afucosylation;
- galactosylation, sialylation, high-mannose, bisecting GlcNAc;
- glycoform composition and percentage ranges;
- glycosyltransferases, glycosidases, and pathway genes;
- host-cell engineering and culture/process control;
- Fc receptor binding, ADCC/ADCP/CDC effects;
- analytical and release methods for glycan profiles.

### Query concept set

```text
(glycosylat* OR glycoengineer* OR glycoform* OR fucosylat* OR afucosylat*
 OR sialylat* OR galactosylat* OR N-glycan OR O-glycan
 OR FUT8 OR MGAT3 OR glycosyltransferase)
AND (antibody OR immunoglobulin OR Fc OR <target/asset>)
```

Add candidate glycan values, host cell, process parameters, relevant classifications, claims-only variants, applicant routes, and local languages.

### Claim questions

- Is the claim directed to the antibody/product, cell, enzyme, process, composition, method, or use?
- Are glycan ranges measured by a defined method?
- Does the candidate fall within every structural, process, functional, and use limitation?
- Where is the relevant making/use/import activity performed?

## M1.5-B — PEG, albumin, fusion, and half-life technologies

### Coverage

- PEGylation/polyethylene glycol, molecular weight, branching, attachment site, linker, and process;
- albumin fusion/binding, Fc fusion, XTEN-like or other half-life extension;
- FcRn binding and pH dependence;
- reversible/non-covalent half-life extension;
- candidate-specific route and formulation implications.

### Query concept set

```text
(PEGylat* OR polyethylene glycol OR PEG linker OR half-life extens*
 OR albumin fusion OR albumin binding OR FcRn OR neonatal Fc receptor
 OR <specific fusion/extension technology>)
AND (antibody OR binding protein OR <target/asset>)
```

### Structure search

For an actual PEG/linker structure, record normalized structure, repeating-unit treatment, attachment points, molecular-weight distribution, exact/substructure/similarity mode, threshold, stereochemistry, salts, and database date. `OCCOCCO` alone is an illustrative fragment, not a universal PEG query.

## M1.5-C — Fc substitutions, functions, and assembly

### C1 Effector reduction or elimination

Search:

- L234/L235, P329, D265, N297 and candidate-specific variants;
- effector-silent/reduced-effector language;
- Fc receptor, C1q, CDC, ADCC, ADCP binding/activity;
- glycosylation-dependent and independent mechanisms.

Example concept group:

```text
(LALA OR L234A OR L235A OR LALAPG OR P329G OR D265A
 OR N297A OR N297G OR N297Q OR effector silent OR reduced effector function)
AND (antibody OR Fc OR immunoglobulin)
```

### C2 Effector enhancement

Search explicit substitutions such as S239D, I332E, G236A when relevant, plus Fc-gamma receptor binding, NK-cell activity, ADCC/ADCP/CDC enhancement, and afucosylation concepts.

### C3 FcRn/half-life

Search YTE (`M252Y/S254T/T256E`), LS (`M428L/N434S`), other candidate substitutions, FcRn/neonatal receptor, pH-dependent binding, recycling, clearance, and half-life.

Verify numbering system. The same residue number can differ across schemes or constructs.

### C4 Multispecific Fc assembly

Search:

- knob-into-hole and other heterodimerization motifs;
- asymmetric Fc, electrostatic steering, strand exchange;
- crossover/common-light-chain/orthogonal pairing;
- homodimer byproduct reduction and purification;
- platform names plus explicit structural features.

### Sequence route

If an authorized sequence service supports Fc queries, search the exact candidate Fc and mutation-bearing segments. Do not convert a protein sequence to SMILES for an “exact structure” patent search as the source suggested; that is not an adequate replacement for biological sequence search.

## M1.5-D — ADC and other antibody conjugates

Activate for ADCs, antibody–oligonucleotide conjugates, radioimmunoconjugates, imaging conjugates, immune-stimulating conjugates, or other defined conjugates.

### D1 Linker and spacer

- cleavable/non-cleavable;
- protease, acid, disulfide, beta-glucuronide, or other trigger;
- maleimide, succinimide stabilization, click, enzymatic, or other chemistry;
- MC-VC-PABC, SMCC, SPDP, GGFG and candidate-specific named linkers;
- hydrophilicity, masking, self-immolation, bystander effect, release kinetics;
- attachment handles and spacer structure.

### D2 Payload/warhead

- MMAE/MMAF and other auristatins;
- DM1/DM4 and other maytansinoids;
- SN-38, exatecan/DXd-like topoisomerase payloads;
- calicheamicin, PBD, duocarmycin and other actual classes;
- immune agonists, degraders, oligonucleotides, radionuclides, or other candidate payloads;
- stereochemistry, prodrug state, metabolites, and linker-payload intermediate.

Do not assume payload name equivalence; verify structure and definitions.

### D3 Attachment and DAR

- lysine/cysteine/random/site-specific conjugation;
- engineered cysteine, non-natural amino acid, selenocysteine;
- transglutaminase, glycan remodeling, enzyme tags, click chemistry;
- conjugation site and occupancy;
- drug-to-antibody ratio target, range, average/distribution, and measurement;
- unconjugated antibody/free payload controls.

### D4 Manufacturing, purification, analytics, and formulation

- conjugation sequence and reaction conditions;
- quench, purification, free payload removal, aggregate control;
- DAR/charge/size/purity assays;
- stability, storage, formulation, reconstitution, administration;
- scale, batch mode, and product-quality attributes.

### Query routes

Run component, full-conjugate, process, claims-only, structure, target, applicant, and semantic searches separately. A linker or payload hit does not show that the complete candidate is claimed.

## M1.5-E — Other chemical modifications

Cover only actual candidate features, including:

- fluorescent labels and imaging probes;
- bifunctional chelators such as DOTA/NOTA and related structures;
- radionuclide precursors and attachment chemistry;
- photo-crosslinkers, affinity tags, masking groups, polymers, lipids, or other modifications.

### Structure workflow

1. Obtain the authoritative structure and identifiers.
2. Normalize salt/solvate, isotope, stereochemistry, tautomer, aromaticity, charge, and attachment points.
3. Preserve the original structure and normalization log.
4. Run exact search.
5. Run substructure search with justified query atoms/bonds.
6. Run similarity search with recorded fingerprint/threshold where available.
7. Link hits to patent claims and target jurisdictions.
8. Review component versus conjugate/process/use claim scope.

Chemical-property or ADMET prediction may support separate R&D analysis, but cannot validate claim scope, infringement, patent validity, or commercial feasibility.

## Local-language mutation examples

Use these only when the corresponding language/jurisdiction is in scope. Preserve Latin one-letter and three-letter expressions alongside the translation because patent documents frequently retain them.

| Search language | Example variants for verified M428L | Notes |
|---|---|---|
| English | `M428L`, `M428Leu`, `Met428Leu`, `methionine at position 428 replaced by leucine` | Include `EU numbering` where applicable |
| German | `Methionin an Position 428 durch Leucin ersetzt`, `Aminosäureaustausch M428L` | Test inflection and compound terms |
| French | `méthionine en position 428 remplacée par une leucine`, `substitution M428L` | Preserve accents and unaccented variants if database normalization is unknown |
| Spanish | `metionina en la posición 428 sustituida por leucina`, `mutación M428L` | Combine with Fc/antibody concepts |
| Portuguese | `metionina na posição 428 substituída por leucina`, `mutação M428L` | Confirm database tokenization |
| Other local language | Obtain a verified translation of “Met at position 428 replaced by Leu” and preserve `M428L`, `M428Leu`, and `Met428Leu` unchanged | Record translator/source and original-script query in the matter query log, not this English package |

For every translated query:

1. retain the verified mutation expression unchanged;
2. pair it with local antibody/Fc/function terms;
3. record the translator/source or analyst basis;
4. test whether the database indexes machine translations or originals;
5. review unique local-language hits against the original document;
6. do not elevate legal priority solely because only one language route found the record.

## Numbering conversion control

Do not automatically convert EU positions to IMGT/Kabat/Chothia positions with a fixed arithmetic offset. Alignment and domain context are required. When the candidate uses one scheme and the patent another:

- preserve both original annotations;
- align the relevant reference and candidate domains;
- cite the numbering/conversion method;
- record insertions and gaps;
- search both verified expressions;
- mark the conversion uncertain if the reference sequence or domain boundary is unavailable.

## Integration

Each hit must retain:

```json
{
  "publication_number": "...",
  "source_modules": ["M1.5-C"],
  "query_ids": ["M15C-007"],
  "modification_type": "Fc substitution",
  "candidate_feature_ids": ["FC-001"],
  "retrieval_basis": "exact mutation text",
  "claim_context": "pending_review",
  "jurisdiction_status": "pending_verification",
  "sources": []
}
```

Deduplicate exact publications without dropping module/query provenance. Merge families later under `patent-family-merge.md`.

## Prioritization

Prioritize claim review when:

- the exact candidate modification is recited in a target-market claim;
- a claimed combination of sequence plus modification appears relevant;
- a platform/process claim maps to planned manufacturing;
- an ADC claim combines the relevant antibody/target, linker/payload, attachment, DAR, use, or process;
- controlling claim/status evidence is incomplete but the commercial impact is material.

Do not automatically elevate risk because M1 and M1.5 both retrieve a family, because a similarity threshold is exceeded, or because a local-language query found a unique record. Those facts affect review priority and search confidence only.

## Claim review questions

- Which current claim and member are relevant?
- Is the feature structural, functional, process, composition, use, or result-defined?
- What numbering, measurement, identity, range, or test method controls?
- Does the claim require a component or the complete antibody/conjugate?
- Are all other limitations mapped to versioned candidate evidence?
- Where is the relevant act performed?
- Is status/term verified officially?
- What prosecution or construction question needs counsel?

## Completion checklist

- [ ] Applicable glycan, PEG/fusion, Fc, multispecific, ADC, and other chemical modules were selected from actual candidate features.
- [ ] Mutation source residue, destination residue, position, chain/domain, and numbering scheme are preserved.
- [ ] One-letter, three-letter, named-set, function, and local-language variants were considered.
- [ ] Structure searches preserve normalization, mode, algorithm/threshold, and database date.
- [ ] Full conjugate, component, process, formulation, and use claims are distinguished.
- [ ] Sequence services are not replaced by protein-to-SMILES shortcuts.
- [ ] ADMET or technical-property predictions are not used as legal evidence.
- [ ] Every hit retains module/query/candidate feature/source provenance.
- [ ] Multi-route hits and similarity are not converted into infringement probability.
