# Sequence Search Protocol for mAb FTO Screening

## Purpose

Define a reproducible sequence-search workflow for conventional antibodies, fragments, multispecifics, and antibody conjugates. Sequence similarity is a discovery signal. It is not a legal conclusion, an infringement probability, or evidence that every limitation of a claim is met.

## Tool and access gate

Use an authorized patent-linked biological sequence search service only when it is actually available in the execution environment. Record:

- service and database name;
- tool/version where exposed;
- access date and database coverage date;
- query options and filters;
- export identifier;
- whether unpublished candidate sequences may be disclosed to the service.

Do not invent a tool name or connection. If no sequence-search service is available, request an authoritative export, continue only the non-sequence modules that remain meaningful, mark M1 incomplete, and withhold any claim that the sequence-led FTO screen is complete.

## Sequence preparation

### Accepted inputs

- FASTA or validated one-letter amino-acid sequence;
- sequence listing extract with exact SEQ ID NO and publication source;
- controlled internal sequence record with version and checksum;
- nucleotide sequence where nucleic-acid, vector, or expression claims matter.

### Required metadata

| Field | Requirement |
|---|---|
| Query ID | Stable, non-secret identifier |
| Candidate version | Version/freeze date |
| Molecule/arm | Conventional mAb, arm A/B, common light chain, fragment, Fc, linker, etc. |
| Region | VH, VL, CDR, full chain, Fc, hinge, construct, nucleotide, other |
| Alphabet | Amino acid or nucleotide |
| Length | Residue/base count |
| Checksum | SHA-256 or approved equivalent where possible |
| Numbering scheme | IMGT, Kabat, Chothia, AHo, EU, other, or not numbered |
| Signal peptide | Included, removed, unknown, not applicable |
| Source | File/document/database and locator |
| Confidentiality | Authorized service and restrictions |

Reject or quarantine sequences containing unexplained stop symbols, gap characters, ambiguous residues, non-biological annotations, mixed alphabets, or copy/paste truncation.

## Numbering and CDR definition

Prefer a validated numbering tool or expert-supplied annotation. IMGT is a widely used default, but do not use fixed residue ranges as a substitute for numbering because insertions, deletions, chain type, and framework length vary.

For every CDR query, record:

- numbering scheme and version;
- chain and domain;
- start/end positions under that scheme;
- extracted sequence;
- extraction method;
- reviewer or validation result.

If results from IMGT, Kabat, Chothia, or another system differ, retain separate query IDs and explain the difference. Do not silently merge them.

## Query inventory

Prepare all applicable units:

| Query type | Typical purpose | Requirement |
|---|---|---|
| VH | Variable-heavy discovery | Required when available |
| VL | Variable-light discovery | Required when available |
| CDR-H3 | High-specificity discovery | Strongly recommended |
| CDR-H1/H2 | Complementary heavy-chain discovery | Recommended |
| CDR-L1/L2/L3 | Complementary light-chain discovery | Recommended |
| Full heavy chain | Constant-region/isotype and construct claims | When relevant |
| Full light chain | Light-chain/construct claims | When relevant |
| Hinge/Fc | Fc engineering and mutation claims | When relevant |
| Each multispecific arm | Arm-specific claims | Required for multispecifics |
| Paired architecture | Pairing/common-chain claims | Search by sequence plus text/structure evidence |
| Peptide linker | Conjugate/fusion claims | When peptide-based |
| Nucleic acid/vector | Encoding and expression claims | When planned acts include production |

For ADCs, run antibody sequence searches, then separately route chemical linkers/payloads and conjugation features through the modification/structure workflow. A chemical payload is not meaningfully searched as an amino-acid sequence.

## Threshold design

Thresholds are search-recall settings, not universal risk thresholds. Select and record them per region, sequence length, database behavior, and decision stage.

Suggested starting tiers for query testing:

| Query | Narrow pass | Expansion pass | Notes |
|---|---:|---:|---|
| CDR-H3 | exact and high-identity | lower identity with length/gap controls | Short sequences create chance matches; inspect context |
| Other CDRs | high identity | broader identity with paired context | Never interpret alone |
| VH/VL | high identity | broader identity | Inspect framework/CDRs and full claim |
| Full chain | high identity | region/domain search | Constant-region similarity is widespread |
| Fc/hinge | exact mutation and motif | broader domain search | Pair with numbering-aware mutation text |
| Peptide linker | exact/high identity | motif/domain expansion | Short motifs may be non-specific |

The source thresholds (for example, 95% CDR-H3 or 85–90% variable-region searches) may be used as initial tests where technically appropriate, but must not be hard-coded as legal cutoffs. Conduct at least one sensitivity pass above and below the selected threshold for high-impact matters.

## Search execution

For each query unit:

1. Validate sequence and metadata.
2. Submit one versioned query with documented threshold and filters.
3. Preserve the raw export or immutable result identifier.
4. Capture patent publication/member, sequence identifier, alignment, identity, positives, gaps, coverage, orientation, and database source.
5. Repeat with planned sensitivity/variant queries.
6. Resolve publication numbers to family and jurisdictional members.
7. Retrieve the claim and specification context for shortlisted sequences.
8. Determine whether the sequence is claimed, merely disclosed, cited, or present only in a listing.
9. Map actual claim limitations to the candidate.

Do not merge VH and VL results as if the same molecule is disclosed until pairing or construct evidence supports that inference.

## Result record

```json
{
  "query_id": "VH-A-v3",
  "candidate_version": "candidate-v3",
  "query_region": "VH",
  "numbering_scheme": "IMGT",
  "query_checksum": "sha256:...",
  "service": "authorized sequence-search service",
  "database_version": "reported coverage date",
  "search_date": "YYYY-MM-DD",
  "threshold": {"identity_min": 0.90, "coverage_min": 0.90},
  "publication_number": "US...",
  "family_id": "provider family identifier",
  "sequence_source": "SEQ ID NO: 17",
  "claim_context": "claimed|disclosed|listing_only|unknown",
  "identity_percent": 94.2,
  "query_coverage_percent": 100.0,
  "alignment_length": 118,
  "gap_count": 0,
  "mismatches": ["A23V", "G45S"],
  "source_locator": "export row or record URL",
  "review_status": "pending_claim_review"
}
```

Do not store secrets in the record. Use controlled references for confidential raw sequences.

## Interpretation hierarchy

### Retrieval relevance

- **Exact sequence**: prioritize claim-context review.
- **High identity/high coverage**: prioritize if matched region is material to the candidate.
- **Partial or motif match**: inspect alignment length, chance-match risk, context, and claim language.
- **Constant-region-only match**: generally weak unless the claim specifically limits the relevant Fc/hinge feature.
- **Listing-only hit**: does not establish that the sequence is claimed.

### Claim mapping

A literal sequence issue exists only when the controlling claim, correctly construed, contains a limitation that may read on the candidate sequence or a defined variant class. Check:

- exact SEQ ID reference;
- percentage-identity definition and calculation method;
- allowed substitutions/deletions/insertions;
- CDR definitions and numbering;
- functional limitations such as binding, affinity, competition, or activity;
- required pairing of heavy/light sequences;
- species, isotype, format, conjugate, composition, method, or use limitations;
- open versus closed claim language;
- jurisdiction and current claim version.

Sequence identity alone cannot answer these questions.

### Equivalents

Where literal mapping is absent or uncertain, identify the fact and the jurisdiction-specific legal question for counsel. Function–way–result may be one US analytical frame, but it is not a universal test and must not be applied mechanically across jurisdictions. Consider prosecution history, claim amendments, dedication/disclosure, foreseeability, prior art, and local law as directed by counsel.

## Multispecific and ADC handling

### Multispecifics

- Search each arm separately.
- Search shared/common light chains separately.
- Search Fc and pairing mutations with numbering-aware text.
- Search geometry, linker, valency, and assembly concepts.
- Confirm whether matched arms appear in the same claimed construct.
- Do not treat two hits in separate documents as one claimed multispecific.

### ADCs

- Search the antibody component as above.
- Search linker/payload structures and names separately.
- Search attachment site, conjugation chemistry, DAR, release mechanism, formulation, use, and manufacturing text.
- Confirm whether claims require the full conjugate, a component, a method, or a use.

## Design-around hypotheses

Do not recommend a residue change merely because it lowers identity. A defensible hypothesis must specify:

- exact claim/member/jurisdiction;
- limitation being changed;
- proposed sequence or architecture difference;
- predicted effect on literal mapping;
- unresolved equivalents and other-claim issues;
- target binding, developability, immunogenicity, efficacy, safety, manufacturability, regulatory, and CMC validation;
- new search triggered by the revised sequence.

Framework changes, CDR grafting, epitope changes, isotype switching, Fc mutations, or arm re-pairing may create new risks and must be re-screened.

## Common quality failures

| Failure | Consequence | Control |
|---|---|---|
| Signal peptide included inconsistently | Misleading alignment/coverage | Preserve both versions and label them |
| Fixed CDR positions | Wrong extracted CDR | Validate numbering |
| Kappa/lambda confusion | Wrong light-chain interpretation | Confirm chain type |
| VH and VL searched as one string | Invalid alignment | Separate queries |
| Bispecific arms collapsed | Missed architecture claims | Separate arm and construct analysis |
| Identity treated as risk score | Unsupported legal conclusion | Require claim mapping |
| Patent listing treated as claim | False blocking candidate | Retrieve claims/context |
| Translation substitutes original | Claim nuance lost | Preserve original claim |
| Threshold not recorded | Search not reproducible | Store query parameters |
| Database coverage unknown | False completeness | Disclose coverage/gap |

## Completion checklist

- [ ] Every candidate sequence has a version, region, source, checksum, and disclosure authorization.
- [ ] CDR numbering was validated and recorded.
- [ ] Applicable VH, VL, CDR, full-chain, Fc, multispecific, linker, and nucleotide units were considered.
- [ ] Search service, database coverage, date, filters, and thresholds are reproducible.
- [ ] Sensitivity/variant queries were considered for material regions.
- [ ] Raw exports or immutable result references are preserved.
- [ ] Sequence hits were resolved to publications, families, and target jurisdictions.
- [ ] Claim/disclosure/listing context is known or marked unknown.
- [ ] No similarity value is presented as infringement probability.
- [ ] Missing sequence-search access remains a visible coverage gap.
