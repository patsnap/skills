# FTO Report Quality Assessment Checklist

Version: 9.0 localized international edition  
Use: record `Pass`, `Partial`, `Fail`, or `N/A` for every item, cite evidence,
and explain every deduction. `N/A` requires a reason; absence is not evidence of
non-applicability.

---

## Review controls

| Field | Entry |
|---|---|
| Report reviewed | |
| Report version and issue date | |
| Reviewer and review date | |
| Target product/process and version | |
| Intended commercial activity | |
| Target jurisdiction(s) | |
| Search cutoff | |
| Legal-status cutoff | |
| Claim version(s) reviewed | |
| Family/counting convention | |
| Intended decision and audience | |
| Scenario matrix cell | |

### Status vocabulary

| Status | Meaning |
|---|---|
| Pass | Evidence fully supports the criterion |
| Partial | Some evidence exists, but a material gap remains |
| Fail | Criterion is unmet or contradicted |
| N/A | Criterion is genuinely inapplicable and the reason is documented |

---

## Fatal-defect gate

Evaluate this gate before numerical scoring. Continue the complete assessment
even if a fatal condition is triggered.

| ID | Fatal condition | Status | Evidence and consequence |
|---|---|---|---|
| FTL-01 | Target product/process or technical version cannot be identified | | |
| FTL-02 | Target market or jurisdiction cannot be identified | | |
| FTL-03 | A material conclusion relies on fabricated, mismatched, or unverifiable patent evidence | | |
| FTL-04 | A material infringement conclusion has no claim-level basis | | |
| FTL-05 | Material claim/status evidence is missing while the report gives a definitive conclusion | | |
| FTL-06 | A known higher-risk finding is omitted or contradicted without explanation | | |
| FTL-07 | The report gives an unsupported absolute non-infringement assurance | | |

**Fatal override:** Yes / No  
**Fatal evidence:**  
**Required cure before reliance:**

---

## Dimension A — Search-strategy quality (25 points)

### A0. Evidence-layer entry gate

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| A0.1 | Target market and jurisdiction are explicit | | | |
| A0.2 | Target product/process, configuration, and version are explicit | | | |
| A0.3 | Intended activity is defined: make, use, sell, offer, import, export, supply, or launch | | | |
| A0.4 | Search cutoff and legal-status cutoff are stated separately | | | |
| A0.5 | Family unit and result-counting convention are stated | | | |
| A0.6 | Claim text version and translation source are stated for material patents | | | |

### A1. Source and jurisdiction coverage (8 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| A1.1 | Sources cover the identified target jurisdictions | | | |
| A1.2 | PCT and regional routes are covered when relevant to the family or market | | | |
| A1.3 | National registers or authoritative status sources are used where a material conclusion requires them | | | |
| A1.4 | Commercial/global databases supplement rather than obscure source provenance | | | |
| A1.5 | Database limitations, update lag, translations, and family normalization are disclosed | | | |
| A1.6 | Source selection is justified for the technology and right type | | | |

Do not grade by a fixed database count. One authoritative source may be adequate
for a narrow question; several broad databases may still be inadequate for a
multi-jurisdiction launch.

**A1 score:** ___ / 8

### A2. Query and route design (6 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| A2.1 | Essential and optional technical features are decomposed | | | |
| A2.2 | Keywords include synonyms, acronyms, spelling variants, and translations as relevant | | | |
| A2.3 | Boolean, proximity, phrase, field, and truncation logic is reproducible | | | |
| A2.4 | IPC/CPC or other applicable classifications are justified and versioned | | | |
| A2.5 | Assignee/inventor/citation/known-player routes are used only where they add coverage | | | |
| A2.6 | Semantic and exact-query routes are compared rather than conflated | | | |
| A2.7 | Queries identify database, fields, filters, date run, and result count | | | |
| A2.8 | Exclusions are technically justified and testable | | | |

**A2 score:** ___ / 6

### A3. Time and prosecution coverage (5 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| A3.1 | Time scope is justified against patent term, priority, and technology history | | | |
| A3.2 | Search cutoff is sufficiently current for the stated decision date | | | |
| A3.3 | Publication delay and unpublished-application blind spots are explained | | | |
| A3.4 | Recently published and pending applications are maintained as a watchlist | | | |
| A3.5 | Re-review triggers reflect launch timing, prosecution, design, and market change | | | |

No universal 20-year lookback or fixed freshness interval applies. Record the
reasoning for the selected window.

**A3 score:** ___ / 5

### A4. Reproducibility and screening (6 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| A4.1 | A qualified reviewer can rerun every material query | | | |
| A4.2 | Inclusion, exclusion, and relevance criteria are documented | | | |
| A4.3 | Screening stages and reviewer decisions are traceable | | | |
| A4.4 | Deduplication and family consolidation are reproducible | | | |
| A4.5 | Raw, screened, and retained counts reconcile | | | |
| A4.6 | Search changes and iterations are versioned | | | |
| A4.7 | Negative findings are distinguished from missing or unsearched evidence | | | |

**A4 score:** ___ / 6

**Dimension A score:** ___ / 25

---

## Dimension B — Patent-analysis depth (30 points)

### B1. Claim-comparison rigor (10 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| B1.1 | Correct jurisdictional member and current enforceable claim set are identified | | | |
| B1.2 | Independent claims are analyzed individually | | | |
| B1.3 | Material dependent claims are included where they affect exposure | | | |
| B1.4 | Every claim limitation is mapped to product/process evidence | | | |
| B1.5 | Missing limitations and disputed interpretations are explicit | | | |
| B1.6 | Product evidence is dated, versioned, and traceable | | | |
| B1.7 | Claim quotations identify source, language, and translation basis | | | |
| B1.8 | Literal analysis is distinguished from equivalents or analogous doctrines | | | |
| B1.9 | Means-plus-function, functional, sequence, composition, numerical, or process limitations receive field-appropriate treatment | | | |
| B1.10 | Conclusions do not rely on title, abstract, classification, or figure similarity alone | | | |

**B1 score:** ___ / 10

### B2. Infringement-risk reasoning (8 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| B2.1 | Analysis applies the law of each target jurisdiction | | | |
| B2.2 | The relevant commercial act and actor are identified | | | |
| B2.3 | Direct, indirect, induced, contributory, or divided infringement is addressed only when factually relevant | | | |
| B2.4 | Claim construction uncertainty is stated | | | |
| B2.5 | Equivalents analysis is jurisdiction-specific and not presumed | | | |
| B2.6 | Infringement is kept distinct from validity and enforceability | | | |
| B2.7 | Risk level and confidence are separately explained | | | |
| B2.8 | Conclusions are tied to the defined product/process version | | | |

**B2 score:** ___ / 8

### B3. Risk tiering and materiality (4 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| B3.1 | Higher, moderate, and lower risk labels have written criteria | | | |
| B3.2 | Tiering reflects claim fit, status, jurisdiction, activity, and uncertainty | | | |
| B3.3 | Pending applications are not scored as current enforceable claims | | | |
| B3.4 | Commercial materiality is distinguished from legal likelihood | | | |
| B3.5 | Color is not the sole carrier of the risk label | | | |

**B3 score:** ___ / 4

### B4. Status, ownership, and validity context (5 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| B4.1 | Material legal status is supported by a named source and date | | | |
| B4.2 | Expected expiry, lapse, term adjustment/extension, and maintenance events are handled where relevant | | | |
| B4.3 | Ownership and recorded assignments are checked where decision-material | | | |
| B4.4 | Family members are not assumed to share identical claims or status | | | |
| B4.5 | Opposition, reexamination, post-grant review, litigation, disclaimers, or prosecution history are reviewed where relevant | | | |
| B4.6 | Validity observations cite prior art and procedural posture | | | |
| B4.7 | A validity concern is not presented as automatic freedom to operate | | | |

**B4 score:** ___ / 5

### B5. Technology- or industry-specific coverage (3 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| B5.1 | Field-specific claim types and evidence are identified | | | |
| B5.2 | Relevant standards, sequences, formulations, manufacturing steps, software functions, materials, or component interfaces are covered | | | |
| B5.3 | Technical assumptions are verified with R&D/product owners | | | |
| B5.4 | Industry-specific doctrines or regulatory interfaces are included only when applicable | | | |

**B5 score:** ___ / 3

**Dimension B score:** ___ / 30

---

## Dimension C — Legal-opinion quality (25 points)

### C1. Legal framework and sources (7 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| C1.1 | Each conclusion identifies the applicable jurisdiction | | | |
| C1.2 | Current statutes, cases, guidance, or official sources are cited where material | | | |
| C1.3 | Legal propositions are separated from factual assumptions | | | |
| C1.4 | Claim construction and equivalents standards are accurately qualified | | | |
| C1.5 | Territoriality and cross-border acts are addressed | | | |
| C1.6 | Exceptions, exhaustion, licence, safe harbour, repair, or experimental use are considered only when relevant | | | |
| C1.7 | SEP/FRAND is assessed only for an identified standard-essentiality question | | | |

**C1 score:** ___ / 7

### C2. Conclusion reliability (7 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| C2.1 | Conclusions follow from the claim chart and cited evidence | | | |
| C2.2 | Contrary evidence and plausible alternative interpretations are addressed | | | |
| C2.3 | Confidence and residual uncertainty are explicit | | | |
| C2.4 | Scope, status, claim version, translation, and data limits are visible | | | |
| C2.5 | No absolute assurance exceeds the evidence | | | |
| C2.6 | Pending claims and future prosecution are separately qualified | | | |
| C2.7 | Counsel-review boundary and reliance restrictions are clear | | | |

**C2 score:** ___ / 7

### C3. Risk mitigation and decision options (6 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| C3.1 | Every material risk has at least one concrete response option | | | |
| C3.2 | Design-around advice identifies the claim limitation affected | | | |
| C3.3 | Licence, acquisition, opinion, challenge, monitoring, supplier, and business options are distinguished | | | |
| C3.4 | Recommendations identify priority, owner, timing, trigger, and dependency | | | |
| C3.5 | Residual risk after each action is stated | | | |
| C3.6 | Recommendations align with the intended decision and risk tolerance | | | |

**C3 score:** ___ / 6

### C4. Professional qualification and communication (5 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| C4.1 | Author/reviewer roles and qualifications are transparent | | | |
| C4.2 | Facts, assumptions, analysis, conclusion, and recommendation are distinguishable | | | |
| C4.3 | Executive language remains accurate and does not overstate certainty | | | |
| C4.4 | Defined terms and professional terminology match local practice | | | |
| C4.5 | Limitations and disclaimer are prominent enough for the intended audience | | | |

**C4 score:** ___ / 5

**Dimension C score:** ___ / 25

---

## Dimension D — Documentation completeness (20 points)

### D1. Search record (6 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| D1.1 | Sources, queries, fields, filters, and dates are retained | | | |
| D1.2 | Raw, screened, retained, and family counts reconcile | | | |
| D1.3 | Screening and exclusion decisions are traceable | | | |
| D1.4 | Family normalization and identifier mapping are documented | | | |
| D1.5 | Independent-search route provenance is retained | | | |
| D1.6 | Search limitations and unsearched areas are stated | | | |

**D1 score:** ___ / 6

### D2. Analysis traceability (5 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| D2.1 | Every material statement has a citation or evidence reference | | | |
| D2.2 | Patent identifiers resolve to the correct document and jurisdiction | | | |
| D2.3 | Claim text, translation, product evidence, and conclusion are linked | | | |
| D2.4 | Status and ownership evidence include source and date | | | |
| D2.5 | Reviewer judgments and unresolved questions are recorded | | | |

**D2 score:** ___ / 5

### D3. Annexes and evidence package (4 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| D3.1 | Search strings and search log are included or referenced | | | |
| D3.2 | Result list and family map are included or referenced | | | |
| D3.3 | Material claim charts and cited patent extracts are included or referenced | | | |
| D3.4 | Status, ownership, and prosecution evidence is included where material | | | |
| D3.5 | Product/process evidence and version are retained | | | |

**D3 score:** ___ / 4

### D4. Version control and format (5 points)

| ID | Criterion | Status | Deduction | Evidence / notes |
|---|---|---|---:|---|
| D4.1 | Report version, issue date, author, reviewer, and approval are present | | | |
| D4.2 | Change history identifies material scope/evidence/conclusion changes | | | |
| D4.3 | Superseded conclusions are clearly controlled | | | |
| D4.4 | Headings, tables, captions, labels, and links are accessible | | | |
| D4.5 | Risk and status are communicated with text, not color alone | | | |
| D4.6 | Confidentiality, privilege, distribution, and retention controls are appropriate | | | |

**D4 score:** ___ / 5

**Dimension D score:** ___ / 20

---

## Independent-verification checklist

| ID | Criterion | Status | Evidence / notes |
|---|---|---|---|
| IV-01 | Route 1 semantic search is documented | | |
| IV-02 | Route 2 keyword/nested Boolean search is documented | | |
| IV-03 | Route 3 classification search is documented | | |
| IV-04 | Route 4 assignee/inventor/citation route is documented where relevant | | |
| IV-05 | Route 5 temporal/pending watchlist is separate | | |
| IV-06 | Publication identifiers are normalized | | |
| IV-07 | Family keys and family convention are explicit | | |
| IV-08 | Route provenance is retained for every result | | |
| IV-09 | Observed union, intersections, and overlap are reported | | |
| IV-10 | Report-only and independent-only families are listed | | |
| IV-11 | Potential omissions receive claim/status/materiality review | | |
| IV-12 | Search-only differences are not automatically labeled defects | | |
| IV-13 | Numeric recall is omitted unless estimator assumptions are supported | | |
| IV-14 | Any estimator is labeled a qualified heuristic, not true recall | | |
| IV-15 | Zero results are not converted into a no-risk conclusion | | |

---

## Cross-field consistency checks

| Rule | Check | Result | Resolution |
|---|---|---|---|
| LR-01 | High A1 score is consistent with explained source coverage | | |
| LR-02 | High B2 score is supported by material claim analysis | | |
| LR-03 | High C3 score is supported by actionable recommendations | | |
| LR-04 | High B4 score has dated status/ownership sources | | |
| LR-05 | Full D4 score is consistent with reproducible queries | | |
| LR-06 | Excellent grade does not coexist with a fatal defect | | |
| LR-07 | High validity score has cited prior-art/procedural evidence | | |
| LR-08 | Numeric coverage estimate has method and assumptions | | |
| LR-09 | Every higher-risk finding has a linked response | | |
| LR-10 | Pending applications are not treated as enforceable rights | | |

---

## Consolidated score and decision

| Dimension | Maximum | Score | Principal deduction |
|---|---:|---:|---|
| A. Search-strategy quality | 25 | | |
| B. Patent-analysis depth | 30 | | |
| C. Legal-opinion quality | 25 | | |
| D. Documentation completeness | 20 | | |
| **Total** | **100** | | |

**Quality grade:** Excellent / Good / Adequate / Needs improvement / Unsatisfactory / Fatal  
**Suitable for intended decision:** Yes / With conditions / No  
**Conditions or restrictions:**  
**Required re-review trigger:**

### Priority remediation register

| Priority | Finding | Required action | Owner | Due/trigger | Dependency | Residual risk |
|---|---|---|---|---|---|---|
| Critical | | | | | | |
| High | | | | | | |
| Medium | | | | | | |
| Low | | | | | | |

---

## Reviewer declaration

I assessed the supplied report and identified evidence against the criteria
above. Scores represent report quality, not a probability of infringement and
not a guarantee of freedom to operate. Conclusions remain limited to the
defined subject, activity, jurisdiction, claim version, evidence, and review
date. Material legal or commercial decisions require qualified counsel review.

Reviewer: ____________________  
Date: ____________________  
Approval / second review: ____________________
