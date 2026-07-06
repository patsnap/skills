# Dairy Protein Competitive Analysis White Paper Framework

Use this framework to generate a high-end business white paper from dairy or milk protein patent data after upstream screening and fine labeling.

## Upstream Workflow Gate

The complete business workflow is:

1. Competitor patent retrieval with `C:\Users\zhanghongyu\.codex\skills\competitor-patent-retrieval`.
   - Input: competitor company name(s).
   - Output: applicant-expanded, merged, deduplicated competitor patent dataset.
   - Principle: retrieve through the Patsnap/Zhihuiya applicant entrance, preserve applicant provenance, and deduplicate before technical screening.
2. Initial screening with `C:\Users\zhanghongyu\.codex\skills\milk-protein-patent-screening`.
   - Input: competitor patent dataset from retrieval.
   - Output: retained milk-protein deep-processing related patents.
   - Principle: high recall, retain uncertain records for review.
3. Fine labeling with `C:\Users\zhanghongyu\.codex\skills\milk-protein-patent-labeling.skill`.
   - Input: retained patents from screening.
   - Formal output dimensions: `蛋白类型`, `蛋白功能`, `分离技术手段`.
   - The analysis skill should treat these labels as the main structured input.
4. Competitive analysis with `dairy-protein-competitive-analysis`.
   - Input: screened and fine-labeled patent dataset.
   - Output: evidence-based competitive technology analysis white paper.

If the user provides only competitor names, do not proceed directly to white paper analysis; run or request competitor patent retrieval. If the provided data is not screened, run or request the screening step. If the data is screened but not fine-labeled, run or request the fine-labeling step. If labels are partially missing, analyze only complete dimensions and place missing dimensions in the research boundary.

## Report Title

Use a business-style Chinese title such as "Dairy Protein Deep-Processing Patent Competition and Strategic Opportunity White Paper" translated naturally into Chinese.

## Cover Information

Generate:

- White paper title
- Subtitle
- Intended audience
- Data scope
- Analysis basis
- Version date

## Executive Summary

Write 5-8 strategic conclusions. Each conclusion must include:

- Core finding
- Data basis
- Strategic meaning
- Evidence strength: strong / medium / weak

Do not introduce conclusions that are not supported in the body.

## Research Method and Boundary

Explain:

- Data source and time range
- Tagged fields used
- Core analytical frame: protein type x protein function, with separation technology as a process-route lens when labeled
- Dimensions supported by data
- Dimensions not analyzed due to insufficient fields
- Difference between patent-data conclusions and industry mapping references

Use this table:

| Field | Provided | Supported analysis | Unsupported analysis | Enter body analysis |
|---|---|---|---|---|

Only dimensions that are supported and logically closed should enter body chapters.

## Industry Mapping Reference

This section is reference-only. It helps interpret potential commercial value but is not itself patent evidence.

### Table 1: Protein Type to Potential High-Value Direction Mapping

| Protein type | Common technical/nutritional feature | Potential target population | Potential high-value product direction | Validation points |
|---|---|---|---|---|
| Casein / caseinate / micellar casein | Structure, gelation, emulsification, sustained release, calcium binding | Children, elderly, general nutrition | Cheese, yogurt, high-protein foods, bone-health nutrition | Product scenario, formulation role, process and evidence data |
| Whey protein / WPC / WPI / WPH | High nutritional value, digestibility, amino acid profile, muscle protein synthesis relevance | Sports users, adults, elderly | Protein beverages, protein powder, sports nutrition, elderly nutrition | Target population and product fields |
| Lactoferrin | Iron-binding glycoprotein, immune and antibacterial relevance | Infants, children, immune-health consumers | Infant formula, immune nutrition, high-value functional dairy | Evidence, dosage, product scenario |
| Alpha-lactalbumin | Amino acid balance, infant nutrition relevance | Infants, children, sleep/brain-development adjacent scenarios | Infant formula, premium nutrition products | Product scenario and evidence fields |
| Beta-lactoglobulin | Main whey protein, structure/function modification, allergen relevance | General nutrition, low-allergen scenarios | Functional protein ingredients, allergen-control formulas | Hydrolysis/allergen and evidence fields |
| CPP / casein phosphopeptide | Mineral binding, calcium absorption relevance | Children, elderly, bone-health consumers | Calcium absorption, bone-health products | Evidence and formulation fields |
| Milk-derived bioactive peptides | Potential antihypertensive, antioxidant, immune, metabolic functions | Adults, elderly, functional-food users | Functional foods, FSMP-adjacent nutrition, health management products | Peptide sequence, evidence, product fields |
| Hydrolyzed/modified milk protein | Digestibility, allergen reduction, solubility, stability | Infants, sensitive digestion groups, special nutrition users | Hypoallergenic formulas, FSMP, high-protein beverages | Process, evidence, regulatory/product fields |

### Table 2: Protein Function to Potential Market Scenario Mapping

| Protein function | Potential target population | Potential product/market direction | Evidence to validate | Note |
|---|---|---|---|---|
| Nutrition enhancement | Children, adults, elderly, sports users | High-protein milk, protein powder, nutrition supplements | Product and formulation fields | Broad function, needs scenario validation |
| Immune modulation | Infants, children, immune-health consumers | Lactoferrin products, immune nutrition, infant formula | Experimental and product evidence | Do not infer clinical efficacy from tag alone |
| Digestibility / hypoallergenic | Infants, sensitive digestion groups, FSMP users | Hydrolyzed protein formulas, hypoallergenic nutrition | Hydrolysis/process/evidence fields | Needs source and evidence validation |
| Muscle synthesis / recovery | Sports users, elderly | Sports nutrition, elderly muscle-health nutrition | Product and target-population fields | Industry mapping only unless tagged |
| Bone health / calcium absorption | Children, elderly | CPP/calcium nutrition, bone-health products | Evidence and formulation data | Needs proof beyond function tag |
| Gut health | Children, adults, elderly | Fermented dairy, functional dairy, protein-prebiotic combinations | Product and microbiome/evidence fields | Avoid overclaiming |
| Antioxidant / anti-inflammatory | Adults, elderly, functional-food users | Functional foods, healthy-aging products | Experimental evidence | Concept-only claims are weak |
| Antihypertensive / metabolic regulation | Adults, elderly, chronic-disease management users | Functional foods, FSMP-adjacent nutrition | Peptide/evidence fields | Requires strong validation |
| Texture / stability / emulsification / gelation | Product formulation users | Yogurt, cheese, protein beverages, shelf-life improvement | Process/formulation/product fields | Technical function, not health efficacy |

## Chapter 1: Overall Competitive Landscape

Analyze only with supported fields:

- Patent scale by competitor
- Protein type breadth and concentration
- Protein function breadth and concentration
- Separation-technology breadth and concentration when labels are present
- Overall hotspots
- Main competitive battlegrounds

Output:

1. Strategic overview
2. Competitor layout comparison table
3. Key findings
4. Strategic meaning

## Chapter 2: Competitor Resource Positioning by Protein Type

Answer:

- Which protein types are high-density layout directions?
- Which companies concentrate on specific protein types?
- Which companies are broader or more focused?
- Which protein types may become resource positioning points?
- Which protein types have potential high-value relevance under industry mapping?

Output:

- Protein type heatmap
- Company protein-resource positioning table
- Key findings
- Strategic meaning
- Evidence strength

Use "industry mapping suggests..." when connecting protein type to population or product direction unless data directly supports it.

## Chapter 3: Functional Value Layout by Protein Function

Answer:

- Which functions are layout hotspots?
- Which functions are shared by many companies?
- Which functions are concentrated in a few companies?
- Which functions may represent differentiated directions?
- Which functions have potential high-value market relevance under industry mapping?

Output:

- Protein function comparison table
- Function hotspot and differentiation table
- Key findings
- Strategic meaning
- Evidence strength

Do not infer clinical effectiveness or productization from function tags alone.

## Chapter 4: Protein Type x Protein Function Matrix

This is the core chapter.

Identify:

- High-density combinations
- High-growth combinations if year fields exist
- Competitor-leading combinations if company fields exist
- Multi-company overlapping combinations
- Potentially high-value but underdeveloped combinations

Use this table:

| Protein type | Protein function | Main companies | Layout density | Recent trend | Competitive crowding | Potential high-value direction from industry mapping | Data-supported conclusion | Cannot directly judge | Evidence strength | Strategic meaning |
|---|---|---|---|---|---|---|---|---|---|---|

Rules:

- Do not treat low density alone as opportunity.
- Do not treat high density alone as moat.
- If time fields are absent, omit recent trend.
- If company fields are absent, omit competitor-leading analysis.

## Chapter 4B: Separation Technology Route Pattern

Include this chapter only when the fine-labeled dataset contains `分离技术手段`.

Analyze:

- Which separation technology labels appear most often.
- Which companies concentrate on chromatography, ion exchange, membrane separation, ultrafiltration, reverse osmosis, isoelectric/electrochemical routes, hydrolysis routes, or other labeled separation paths.
- Which protein types or functions are frequently associated with each separation route.
- Whether the data supports "route concentration" or only scattered use.

Use this table:

| Separation technology label | Main companies | Associated protein types | Associated functions | Layout density | Data-supported conclusion | Cannot directly judge | Evidence strength | Strategic meaning |
|---|---|---|---|---|---|---|---|---|

Rules:

- Do not equate separation technology labels with full manufacturing-process capability.
- Do not claim process-platform leadership unless repeated, company-concentrated labels and patent text support that interpretation.
- If only a few patents contain separation labels, describe it as a signal requiring further validation.

## Chapter 5: Competitor Strategic Profiles

Use only supported positioning labels:

- Protein-type concentrated
- Function concentrated
- Protein-function combination leader
- Broad-coverage layout
- Emerging-direction accelerator
- Existing-portfolio defender

Do not use labels such as process-platform, product-formulation, infant nutrition, elderly nutrition, sports nutrition unless corresponding fields support them.

For each company:

- Core layout direction
- Key protein types
- Key functions
- Key separation technology labels if present
- Leading/concentrated protein-function combinations
- Leading/concentrated protein-function-separation combinations if data volume supports
- Layout breadth/concentration
- Time trend if supported
- Possible strategic intent
- Meaning for our company
- Evidence strength
- Data boundary

## Chapter 6: Potential Barriers and Opportunity Windows

Be conservative.

If data only has protein type and function, analyze:

- Layout concentration
- Layout density
- Potential barrier directions
- Competitive crowding
- Evidence to further validate

If separation technology labels exist, include potential route barriers, but keep the wording to "potential process-route concentration" unless legal-quality and process-depth evidence also exists.

Only assess stronger moats when legal status, grants, family, citations, claims, and continuous filing fields support it.

Potential barrier table:

| Protein type | Protein function | Leading company | Existing evidence | Missing evidence | Current judgment | Risk to us |
|---|---|---|---|---|---|---|

Opportunity window table:

| Protein type | Protein function | Current layout | Potential value from industry mapping | Possible opportunity for us | Information to validate | Priority |
|---|---|---|---|---|---|---|

## Chapter 7: Future Focus Assessment

Include this chapter only if time fields exist.

Use:

- Recent application growth
- Newly appearing protein types
- Newly appearing functions
- Growth in protein-function combinations
- Multi-company acceleration
- Single-company sustained concentration

Output:

- Future focus table
- Judgment basis
- Industry mapping reference
- Evidence strength
- Signals to monitor

## Chapter 8: R&D and Patent Layout Recommendations

Classify recommendations into:

A. Data-supported recommendations
B. Industry-mapping-inspired recommendations
C. Recommendations requiring additional data

Use this table:

| Recommendation type | Direction | Protein type | Function | Competitor status | Opportunity or risk to us | Action | Priority | Evidence strength | Information to validate |
|---|---|---|---|---|---|---|---|---|---|

Actions can include:

- Rapid patent filing
- R&D pre-research
- FTO review
- Add process/product-scenario tagging
- Deepen separation-technology route tagging if process differentiation is material
- Core competitor patent stability analysis
- Validate commercial value against product pipeline

## Closing

Write a concise business white paper closing:

- Emphasize "protein type x protein function" as the lens for identifying competitive battlegrounds.
- Emphasize data discipline and boundary awareness.
- Suggest linking patent tagging with product, process, efficacy evidence, and market data.
- Avoid slogans.

## Output Requirements

- Chinese output unless otherwise requested.
- Markdown white paper draft.
- Formal titles and clean table names.
- Do not output raw patent details unless necessary.
- Do not analyze dimensions that cannot be closed by available data.
- Put insufficient-data notes mainly in methodology/boundary sections.
- Final conclusions must be traceable and verifiable.
