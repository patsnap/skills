# Small-RNA Patent Tag Taxonomy

## Purpose and use

Use this controlled taxonomy for company- and portfolio-level small-RNA patent analysis. Maintain two connected layers:

- **Stakeholder-readable direction** — default timeline lanes and executive summaries;
- **Expert subdivision** — precise target, disease, platform, chemistry, delivery, process, or use interpretation.

Do not preassign a source-case tag to a new portfolio. Apply only evidence-supported tags, preserve multi-label assignments, and record source, locator, confidence, and reviewer state.

## Tag record

```json
{
  "dimension": "mechanism",
  "tag_id": "MECH-SPLICE-INCLUSION",
  "display_name": "Splice switching / exon inclusion",
  "evidence": [{"source_id": "PAT-001", "locator": "claim 1"}],
  "evidence_level": "claim|description|abstract|inferred",
  "confidence": "high|medium|low",
  "review_status": "reviewed|provisional|rejected",
  "notes": ""
}
```

Title-only classification must remain provisional.

## 1. Stakeholder-readable technology directions

Select from the following patterns or create a portfolio-specific direction using the same level of abstraction:

| Direction pattern | Meaning and evidence gate |
|---|---|
| Targeted protein upregulation ASO | Splicing/NMD or other ASO mechanism intended to restore/increase protein; target/disease should be explicit |
| Targeted transcript reduction ASO | RNase H/gapmer or other ASO-mediated reduction; target and sequence/functional basis should be explicit |
| RNA interference therapeutics | siRNA/miRNA pathway assets, with target, duplex/guide and delivery context where available |
| RNA replacement or expression | mRNA and related expression/replacement technology |
| Splicing and exon-modulation platform | Platform-level splice switching, exon inclusion/skipping, cryptic/poison exon, or NMD-escape claims |
| Oligonucleotide chemistry platform | Broad backbone, sugar, base, conjugate, sequence-selection, or synthesis claims not limited to one asset |
| Delivery and tissue targeting | Conjugates, carriers, local/systemic delivery, biodistribution, uptake, endosomal escape, or tissue selectivity |
| Formulation, dosing, and productization | Formulation, stability, concentration, route, dose, regimen, presentation, patient selection, or diagnostics |
| Manufacturing and analytical control | Oligonucleotide synthesis, purification, characterization, impurity control, scale-up, or release testing |
| Disease/asset program | A clearly defined target–disease program that is more informative than a platform lane |

### Mapping precedence

1. If a record primarily claims formulation/dosing/patient selection/manufacturing, use that productization layer.
2. Otherwise map to a well-supported disease/asset program where stakeholder-relevant.
3. Otherwise map to a mechanism or delivery platform.
4. Otherwise use broad chemistry/sequence/manufacturing platform.
5. Use `Unresolved — evidence review required` rather than force-fitting.

## 2. Expert primary subdivision

Construct as:

```text
<TARGET or PLATFORM> / <DISEASE or TECHNICAL SCOPE> / <MODALITY or MECHANISM>
```

Examples retained as examples, not defaults:

- `SCN1A / Dravet syndrome / Nav1.1 upregulation ASO`
- `OPA1 / dominant optic atrophy / splice modulation ASO`
- `PKD target / polycystic kidney disease / transcript modulation`
- `SYNGAP1 / neurodevelopmental disorder / protein upregulation ASO`
- `NMD-sensitive AS exon / platform`
- `LIPA / lysosomal acid lipase deficiency / ASO`
- `PRPF31 / retinitis pigmentosa / ASO`
- `TSC target / tuberous sclerosis / oligonucleotide`
- `JAG1 / Alagille syndrome / oligonucleotide`

Verify target, disease, and mechanism independently. Do not infer the program merely from a company pipeline.

## 3. Mechanism tags

| Tag ID | Display name | Evidence examples |
|---|---|---|
| `MECH-SPLICE-INCLUSION` | Splice switching / exon inclusion | Claim/description defines inclusion or productive splicing |
| `MECH-EXON-SKIPPING` | Exon skipping | Defined exon/event and oligonucleotide intervention |
| `MECH-CRYPTIC-POISON-EXON` | Cryptic or poison exon modulation | Explicit aberrant/poison exon event |
| `MECH-NMD-ESCAPE` | NMD suppression or escape | NMD-sensitive transcript and stabilization/upregulation |
| `MECH-RNASE-H` | RNase H-mediated degradation | Gapmer/RNase H recruitment or functional degradation |
| `MECH-RNAI` | RNA interference / RISC silencing | siRNA/guide/passenger/RISC evidence |
| `MECH-STERIG-BLOCK` | Steric-blocking oligonucleotide | Binding without cleavage to alter processing/translation |
| `MECH-TRANSLATION-UP` | Translation/protein upregulation | Direct evidence of increased translation/protein |
| `MECH-GENE-EXPRESSION` | mRNA expression/replacement | Delivered RNA encodes functional product |
| `MECH-PATIENT-SELECTION` | Patient selection / diagnostic enablement | Genotype/biomarker eligibility or response prediction |
| `MECH-DOSE-REGIMEN` | Dose/regimen optimization | Claimed dose, interval, route, or schedule |
| `MECH-OTHER` | Other defined mechanism | Document definition and evidence |

## 4. RNA modality tags

- `MOD-ASO-SSO` — single-stranded ASO/splice-switching oligonucleotide;
- `MOD-GAPMER` — gapmer/wingmer ASO;
- `MOD-PMO` — phosphorodiamidate morpholino oligomer;
- `MOD-SIRNA` — duplex siRNA;
- `MOD-MIRNA` — miRNA mimic/inhibitor;
- `MOD-MRNA` — messenger RNA;
- `MOD-APTAMER` — aptamer;
- `MOD-GRNA` — guide RNA/editing RNA;
- `MOD-OTHER-OLIGO` — other specified oligonucleotide;
- `MOD-UNRESOLVED` — modality not established.

Do not equate “small RNA” with siRNA. Confirm strand count, mechanism, chemistry, and construct.

## 5. Chemistry and structure tags

| Tag | Required evidence |
|---|---|
| Phosphorothioate backbone | Explicit linkage or structure |
| Phosphodiester/mixed backbone | Explicit linkage pattern |
| 2'-MOE | Explicit 2'-O-methoxyethyl substitution |
| 2'-OMe | Explicit 2'-O-methyl substitution |
| 2'-F | Explicit 2'-fluoro substitution |
| 5-methylcytosine | Explicit modified base |
| LNA/BNA/cEt constrained nucleotide | Explicit constrained chemistry; do not merge variants without evidence |
| PMO backbone | Explicit morpholino phosphorodiamidate chemistry |
| Gapmer/wingmer architecture | Explicit central/wing arrangement |
| Sequence-defined candidate | Claim/description provides sequence/SEQ ID |
| Stereopure/stereodefined linkage | Explicit stereochemical control |
| Conjugate/ligand | Explicit GalNAc, lipid, peptide, antibody, aptamer, polymer, or other ligand |
| Chemistry not reported | Reviewed source does not establish modification |
| Chemistry not retrieved | Required source/section unavailable |

Maintain specific chemistries as multi-tags rather than a vague “modified RNA” label.

## 6. Delivery and tissue tags

- CNS / intrathecal;
- CNS / intracerebroventricular or other local route;
- ophthalmic / intravitreal;
- ophthalmic / subretinal or other local route;
- kidney / renal targeting;
- liver / hepatocyte targeting;
- muscle / cardiac;
- lung / inhaled or systemic;
- tumor / local or systemic;
- immune-cell targeting;
- systemic unconjugated;
- ligand/conjugate-mediated delivery;
- nanoparticle/lipid/polymer carrier;
- formulation/excipient-enabled delivery;
- delivery not central;
- delivery not reported;
- delivery evidence missing.

Separate tissue, route, carrier/conjugate, and formulation in the structured layer even if combined in a stakeholder label.

## 7. Productization-stage tags

These describe the patent portfolio layer, not the clinical development phase:

- foundational platform family;
- core target/asset composition or sequence;
- national/regional prosecution branch;
- granted claim protection;
- continuation/divisional claim refinement;
- chemistry/conjugate extension;
- manufacturing/analytical extension;
- formulation/delivery extension;
- clinical dose/regimen extension;
- patient-selection/diagnostic extension;
- lifecycle/combination/use extension;
- status unresolved.

Record actual clinical phase separately using an authorized drug/trial source.

## 8. Patent and claim-type tags

- sequence/composition claim;
- chemistry/backbone/nucleotide claim;
- conjugate/delivery claim;
- platform/mechanism claim;
- target/use/method claim;
- formulation/dose/regimen claim;
- patient-selection/diagnostic claim;
- synthesis/manufacturing/process claim;
- analytical/quality-control claim;
- nucleic-acid/vector/expression claim;
- claim text unavailable;
- description-only evidence.

## 9. Review priority

Use text categories with a numeric display level only for sorting:

- `3 — Priority review`
- `2 — Material`
- `1 — Context`
- `0 — Low current relevance`

Consider:

- claim centrality and specificity;
- target/technology overlap with the defined project;
- target-jurisdiction live/pending claims;
- family/continuity breadth;
- status and claim-version confidence;
- productization/commercial relevance;
- evidence completeness;
- decision urgency.

Do not automatically elevate priority because of family size, one country, a grant, a sequence hit, or multi-tagging. Do not automatically lower priority because an aggregated status appears inactive; inspect live branches and official evidence.

## 10. Evidence strength dimensions

Keep separate:

- **Claim evidence:** strong / moderate / weak / missing;
- **Family/territory evidence:** strong / moderate / weak / conflicting;
- **Legal-status evidence:** verified / database-only / conflicting / missing;
- **Technical tag confidence:** high / medium / low;
- **Design-around assessment:** counsel/technical review required / preliminary / not assessed.

Never label design-around difficulty solely from sequence, indication, delivery, formulation, or dose difference.

## 11. Trend tags

Use complete/partial-period-aware rules:

- sustained growth;
- recent acceleration;
- recently active;
- historically concentrated;
- declining in observed data;
- isolated filing;
- episodic/unclear;
- insufficient observation window.

State period boundaries, family/publication unit, incomplete years, and small-number caveats.

## 12. Opportunity taxonomy

Opportunity markers may cover:

- indication/target expansion;
- mechanism-platform transfer;
- chemistry optimization;
- tissue/route/delivery expansion;
- formulation/stability/concentration;
- manufacturing/analytical control;
- patient selection/diagnostic enablement;
- dose/regimen/lifecycle;
- family/territory/prosecution gap;
- evidence gap requiring experiment/search.

Each marker requires:

- observed portfolio evidence;
- comparator/peer evidence where used;
- gap statement;
- R&D/IP hypothesis;
- validation experiment/search;
- business relevance;
- patentability/FTO caveat;
- confidence;
- owner/timing.

Source-case examples such as CNS, ophthalmic, renal, NMD, cryptic-exon, splice-switching, formulation, or patient-selection gaps are prompts for consideration only. Do not render them unless evidence supports them.

## QA checklist

- [ ] Every tag has a controlled ID/name and evidence locator.
- [ ] Stakeholder and expert tags are mapped but not conflated.
- [ ] Original and translated terminology are distinguishable.
- [ ] Chemistry, modality, mechanism, delivery, tissue, route, and stage are separate dimensions.
- [ ] Missing/not reported/not applicable remain distinct.
- [ ] Title-only tags remain provisional.
- [ ] Review priority is evidence-based and not a legal conclusion.
- [ ] Trends disclose period/counting limits.
- [ ] Opportunities are generated from portfolio evidence, not preloaded defaults.
