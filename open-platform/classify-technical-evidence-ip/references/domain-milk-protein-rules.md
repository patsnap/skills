# Milk-protein processing domain rules

## Baseline and scope

Use the 222 customer answers and 60 observed paths in `20260525085204594-2.xlsx` as the v2 baseline. This historical customer fixture applies only to labeling protein types, primary functions, and key separation methods in patents concerning advanced milk-protein processing.

Do not revert to an earlier generic label chain unless the user explicitly requests reproduction of that historical version.

The formal dimensions are:

- `Protein type`
- `Protein function`
- `Separation method`

The customer baseline favors conservative labeling: identify the main object, primary effect, and key process rather than tagging every incidental concept.

The root-only paths `Protein function` and the historical `Peptide function` are dirty observations. They are not eligible leaf outputs.

The China- and Korea-heavy patent examples are translated historical fixtures. They are useful for boundary testing but are not a representative global sample.

## Evidence order

1. Independent claims
2. Abstract
3. Technical approach or solution
4. Technical effect
5. Technical problem
6. Title

PatSnap Deep Patent Mining may provide technical problem, approach, and benefit summaries. These derived fields must remain consistent with the claimed or described object and use.

Translated patent excerpts are working translations. Retain publication number, source language, and translation provenance; consult the source-language text when a translation ambiguity could change a label.

## General decision sequence

1. Identify the core milk-protein object.
2. Determine whether it is an active ingredient, prepared product, processed object, or claim-limited component.
3. Determine the primary use or technical effect.
4. Identify the key preparation, extraction, purification, concentration, or separation route.
5. Output complete label paths, evidence, reasons, confidence, and review status.

Multiple labels within one dimension are permitted only when each has independent evidence.

Weak evidence, extended uses, optional ingredients, background diseases, mechanism terms, and auxiliary process steps do not justify additional labels.

If independent claims and the abstract or technical-effect field support different core functions, retain each directly evidenced function and route the record to review. Do not ignore a claimed use merely because the abstract is more prominent.

## Protein-type boundaries

- Prefer the core active ingredient in the claims or abstract; do not label every optional ingredient.
- In bovine-colostrum or immune compositions, label immunoglobulin or growth factor only when it is a core active component, preparation target, or claim-limited object.
- `Growth factor`, `Immunoglobulin`, `Milk-derived peptide`, and `Hydrolyzed protein` are weak-trigger labels. Require both a milk-source context and explicit object evidence.
- Lactose, plant protein, and physiological indicators such as GLP-1 or IGF-1 do not trigger a milk-protein-type label.
- Prefer the most specific supported label, including soft casein micelle, kappa-casein, alpha-s1-casein, alpha-s2-casein, serum albumin, or lysozyme.

## Milk-derived peptides and hydrolyzed protein

- Casein phosphopeptide, ACE-inhibitory peptide, bioactive peptide, whey peptide, and a specific peptide obtained from milk-protein hydrolysis normally map to `Protein type > Other milk proteins > Milk-derived peptide`.
- Use `Protein type > Other milk proteins > Hydrolyzed protein` only when the object is explicitly hydrolyzed milk protein, hydrolyzed whey protein, or hydrolyzed casein and no more specific peptide object is supported.
- An enzymatic-hydrolysis step does not by itself establish a hydrolyzed-protein output. Identify the final active object.

## Function boundaries

### Immunity, antimicrobial or antiviral action, respiratory disease, and inflammation

- Prefer `Protein function > Immune modulation` when infection prevention is achieved by strengthening immune defenses.
- Apply `Protein function > Antimicrobial or antiviral` only when pathogen inhibition, infection reduction, antimicrobial activity, or viral suppression is a direct technical effect.
- Apply `Protein function > Treatment of respiratory disease` only when improvement of a respiratory symptom or disease is the central objective. Mentioning influenza alone is insufficient.
- Apply `Protein function > Anti-inflammatory` only when inflammation is a primary disease target or technical effect. Cytokine changes or inflammation terms in an immune mechanism do not trigger the label automatically.

### Digestion and bone health

- Do not label `Promotes digestion` merely because the record says “absorption.”
- Calcium absorption, bone mineral density, and bone formation normally support `Protein function > Bone health`.
- Evidence concerning digestion of proteins, peptides, or amino acids, or gastric emptying, may support `Protein function > Promotes digestion`.

### Metabolic and other functions

- Glycemic control, blood-pressure reduction, lipid reduction, weight management, and improved digestion must be a claimed use, the central title or abstract purpose, a primary technical effect, or an experimental conclusion.
- `Protein function > Tooth protection` requires central evidence concerning teeth, enamel, remineralization, caries, or protection of tooth surfaces. Oropharyngeal discomfort, immune effects, or an antimicrobial setting does not trigger it automatically.

## Separation-method boundaries

- Label only a key route used to prepare, extract, purify, concentrate, separate, or selectively obtain the target protein.
- Do not label ultrafiltration, nanofiltration, reverse osmosis, diafiltration, centrifugation, precipitation, chromatography, or enzyme treatment when it is merely a routine auxiliary step.
- If ultrafiltration, nanofiltration, or reverse osmosis forms the core separation or purification route, use `Separation method > Membrane separation > Filtration, ultrafiltration, or reverse osmosis`.
- Use `Targeted enzymatic hydrolysis` only when the step selectively produces the target peptide or hydrolysate.
- Where several steps coexist, prefer the principal step under the customer baseline. Use `Separation method > Two or more preparation methods` only when the combination itself is a technical feature.

## Manual review

Route a record to manual review when:

- only a coarse parent label is supportable and the parent is not an eligible output;
- several adjacent protein or function labels remain plausible;
- several milk-derived ingredients are present but the core active ingredient is unclear;
- many effects are asserted but the primary effect is unclear;
- many process steps are present but the key separation route is unclear;
- the record may fall outside the milk-protein scope;
- a root-only path, historical dirty label, or out-of-taxonomy path appears;
- translation ambiguity could change the decision.

## PatSnap MCP use

- Use keyword assistance to expand milk-protein, peptide, function, and process terminology, then filter noise.
- Separate keyword results into synonyms, related context terms, and noise. Product contexts, diseases, broad nutrition terms, and unrelated abbreviations must not enter the synonym list automatically.
- Use semantic or similar-patent retrieval for positive, adjacent, and high-similarity negative examples.
- Use classification descriptions, technology topics, and application domains to understand boundaries.
- Use `tech_problem_benefit_summary` to supplement the problem/approach/benefit evidence.
- Use claims and descriptions to resolve ambiguities.
- Retrieval supports recall and evidence enrichment. It cannot override the v2 label definitions or create a new formal label.
- Obtain external-data authorization before sending non-public records or excerpts.
