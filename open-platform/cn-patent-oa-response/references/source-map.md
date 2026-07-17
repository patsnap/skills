# Source Map - Patent OA Response

> **Tool Tier Classification**
> - `[Core]` = Tier 1: Fixed in workflow steps. Default choice.
> - `[Extended]` = Tier 2: Conditional branch tools. Activated by specific conditions.
> - `[Reference]` = Tier 3: On-demand tools. Loaded via ToolSearch when needed.
>
> **Invocation Method**
> - **Local API Wrappers (AI60)**: Invoked via **Bash tool** with CLI commands. NOT an MCP tool — do NOT search via ToolSearch, do NOT call via DeferExecuteTool.
> - **MCP Tools** (all other entries): Invoked via **ToolSearch + DeferExecuteTool**.
> 
> Tools without a tier label are unclassified — treat as Reference.

Use this file as the factual basis for tool/API capability statements.

## Local API Wrappers [Core]

API wrappers are in `$USERPROFILE/.workbuddy/api-wrappers/`. Invoke via Bash using the managed runtimes.

### AI60 Cloud OCR (Step 1 — scanned/image-based input only)

- CLI: `$USERPROFILE/.workbuddy/api-wrappers/ai60/cli.py`
- Node.js backing client: `$USERPROFILE/.workbuddy/api-wrappers/ai60/cli.mjs`
- **Bash invocation** (API key required — AI60/AI32/AI37 共用 Bearer Token):
  ```bash
  # URL mode (recommended — works as long as AI60 service is enabled on the key):
  python "$USERPROFILE/.workbuddy/api-wrappers/ai60/cli.py" smart_doc --document "https://example.com/doc.pdf" -o output.md [--api-key KEY]
  # File mode (requires /ai/ocr/document/upload permission in API key, auto-fallbacks to RapidOCR):
  python "$USERPROFILE/.workbuddy/api-wrappers/ai60/cli.py" smart_doc --file /path/to/document.pdf -o output.md [--api-key KEY] [--no-fallback]
  ```
- **Credentials**: Pass via `--api-key` CLI arg, or set `AI_API_KEY` env var (shared by AI60/AI32/AI37).
- **AI60** is PatSnap's cloud-based document OCR service (https://connect.zhihuiya.com).
- Supports: PDF, images (PNG/JPG/TIFF/BMP), Office docs.
- Use this for scanned OA notices, scanned D1/D2, image PDFs, or handwritten/printed file images when OCR is appropriate.
- **Fallback**: AI60 云端 OCR 失败时（网络错误、权限不足、超时），**自动降级到 RapidOCR**（本地 CPU OCR 引擎，基于 ONNX Runtime，无需 GPU）。降级行为默认开启，可通过 `--no-fallback` 禁用。对于有 MCP PDF URL 的专利文献，仍建议优先使用 AI60 URL 模式。

## Relevant MCP Tools [Core]

- `mcp__zhihuiya_2b0355_logic.patsnap_fetch`
  - Fetches patent/paper Markdown from URLs or patent publication numbers.
  - Patent modules: `basic`, `citation`, `legal`, `family`.
  - Can include signed patent image links.
  - Use for public patent supplementation only when the user gives a number/URL or asks for retrieval.

- `mcp__zhihuiya_1458a4.claims`
  - Retrieves patent claim data by patent ID or publication number.
  - Includes claim text and independent-claim count.

- `mcp__zhihuiya_e5851d.annuity_get_legal_status`
  - Retrieves legal status and legal events by patent ID or publication number.

- `mcp__zhihuiya_299425.novelty_summary`
  - Extracts technical problem, solution, and effect from text.

- `mcp__zhihuiya_299425.novelty_feature_extract`
  - Extracts technical features from a summary.

- `mcp__zhihuiya_299425.novelty_feature_comparison`
  - Compares technical features with patent IDs.

- `mcp__zhihuiya_299425.novelty_lite_report_generate`
  - Generates a short novelty/inventiveness review from comparison results.

## Chemical Structure Tools [Extended] (zhihuiya_713886)

- `mcp__zhihuiya_713886.ls_structure_search`
  - Searches compounds by SMILES structure. Supports `EXT` (exact/substructure) and `SIM` (similarity with threshold).
  - Returns inchi_key, compound_name, formula, similarity. Paginated with offset/limit.
  - Use for: finding closer/farther prior-art compounds to support inventive-step arguments.

- `mcp__zhihuiya_713886.ls_structure_fetch`
  - Batch fetches full compound details by InChIKey list (max 100 per request).
  - Use after `ls_structure_search` to enrich compound data for comparison tables.

- `mcp__zhihuiya_713886.ls_patent_structure_fetch`
  - Fetches all chemical structures associated with a patent by patent_id or pn.
  - Paginated: offset + limit (max 100 per page).
  - Use for: extracting compound lists from D1/D2 to verify examiner's characterization.

- `mcp__zhihuiya_713886.ls_chemical_mcs_analyze`
  - Analyzes common fragment (MCS) distribution across a list of SMILES structures.
  - Use for: demonstrating that the applicant's compound has a structurally distinguishing scaffold vs D1/D2.

- `mcp__zhihuiya_713886.ls_sar_submit` and `ls_sar_fetch`
  - Submit/fetch SAR extraction for small-molecule patent public numbers. Async: submit returns task_id, poll with fetch.
  - Use for: extracting SAR data from D1/D2 to argue that the prior art does not teach or suggest the applicant's substitution pattern.

- `mcp__zhihuiya_713886.ls_admet_predict`
  - Predicts ADMET properties for SMILES list (1-100 per request).
  - Use for: providing supplementary evidence of unexpected technical effects (e.g., superior bioavailability, lower hERG risk).

## Biological Sequence Tools [Extended] (zhihuiya_06e741)

- `mcp__zhihuiya_06e741.ls_sequence_search_submit`
  - Submits a bio sequence search job (NUCLEOTIDE or PROTEIN). Async: returns job_id.
  - Supports database filter (ALLPATENT, CLAIMS), identity/coverage thresholds, evalue, strand, subject_length.
  - Follow with `ls_sequence_search_check_status` and `ls_sequence_search_get_results`.
  - Use for: finding closer/farther prior-art sequences to support inventive-step or novelty arguments.

- `mcp__zhihuiya_06e741.ls_sequence_search_check_status`
  - Polls status of a sequence search or modification search job. Returns SUCCESS/RUNNING/FAILED.

- `mcp__zhihuiya_06e741.ls_sequence_search_get_results`
  - Retrieves paged results from a completed sequence/modification search job.
  - Returns sequence_id, identity, coverage, evalue, alignment details, claimed status, modification info.

- `mcp__zhihuiya_06e741.ls_sequence_fetch`
  - Batch fetches full sequence details by sequence_number list (max 100 per request).
  - Returns full sequence text, organism, genes, drugs, is_antibody flag.

- `mcp__zhihuiya_06e741.ls_sequence_alignment`
  - Runs pairwise (PSA) or multiple (MSA) sequence alignment. Supports NUCLEOTIDE and PROTEIN types.
  - Use for: precisely showing sequence differences between applicant's claims and D1/D2 sequences to support distinguishing arguments.

- `mcp__zhihuiya_06e741.ls_patent_sequence_fetch`
  - Fetches all sequences associated with a patent by patent_id or pn. Paginated: offset + limit (max 100 per page).
  - Use for: extracting sequence listings from D1/D2 to verify the examiner's characterization of the prior-art sequences.

- `mcp__zhihuiya_06e741.ls_antibody_antigen_search`
  - Searches antibody-antigen relations by target_name (required). Returns antibody sequences, patent info, species.
  - Use for: surveying the antibody prior-art landscape when the OA involves antibody claims.

- `mcp__zhihuiya_06e741.ls_modification_search_submit`
  - Submits a modification search job for sequences with chemical modifications. Async: returns job_id.
  - Use for: finding prior-art for modified-sequence claims (e.g., PEGylation, lipidation) to assess novelty/inventive-step.

## User Input Boundary

The OA notice, application text, D1/D2, and previous amendment text are user-provided case documents. Public patent tools may supplement or verify, but they are not the default source for those case documents.

## Pharma Intelligence Tools [Extended] (mcp__pharma_intelligence)

- `mcp__pharma_intelligence.ls_drug_search`
  - Searches drug pipeline by drug name, target, disease, organization, drug type, mechanism of action, highest phase, ATC code, country, development status, and date range.
  - Use for: finding competing drugs in development that may support or undermine the examiner's obviousness position.

- `mcp__pharma_intelligence.ls_drug_fetch`
  - Batch fetches full drug details by drug IDs or drug names.
  - Use for: enriching drug data for OA argument support (e.g., showing the applicant's drug has unexpected advantages over prior-art drugs).

- `mcp__pharma_intelligence.ls_drug_deal_search` / `ls_drug_deal_fetch`
  - Searches drug BD deals by drug, target, disease, organization, deal type, phase, country, date range.
  - Use for: understanding the commercial significance of the claimed invention vs D1/D2 compounds.

- `mcp__pharma_intelligence.ls_clinical_trial_search` / `ls_clinical_trial_fetch`
  - Searches clinical trials by drug, target, disease, organization, phase, study status, country.
  - Use for: finding clinical data to support arguments about unexpected technical effects.

- `mcp__pharma_intelligence.ls_clinical_trial_result_search` / `ls_clinical_trial_result_fetch`
  - Searches clinical trial results by drug, target, disease, organization, phase, date range.
  - Use for: providing evidence of unexpected clinical advantages for inventive-step arguments.

- `mcp__pharma_intelligence.ls_target_fetch`
  - Batch fetches target details by target IDs or names.

- `mcp__pharma_intelligence.ls_disease_fetch`
  - Batch fetches disease details by disease IDs or names.

- `mcp__pharma_intelligence.ls_organization_fetch` / `ls_organization_pipeline_fetch`
  - Fetches organization details and drug development pipeline.

- `mcp__pharma_intelligence.ls_news_vector_search` / `ls_paper_vector_search`
  - Semantic vector search for biopharma news or academic papers. Requires `query` and `lang` (CN/EN).
  - Use for: finding recent news or publications supporting the applicant's position.

- `mcp__pharma_intelligence.ls_patent_vector_search` / `ls_patent_search`
  - Semantic or structured search for life-science patents.
  - Use for: supplementary prior-art search in biopharma-specific databases.

- `mcp__pharma_intelligence.ls_translational_medicine_search` / `ls_translational_medicine_fetch`
  - Searches translational medicine records.

- `mcp__pharma_intelligence.ls_fda_label_vector_search`
  - Semantic vector search for FDA drug label data. Requires `query` and `lang` (CN/EN).
  - Use for: finding approved drug label information for FTO or claim scope analysis.

- `mcp__pharma_intelligence.ls_ner_nor_normalize`
  - Named entity recognition and normalization for drug/target/disease names.

## Novelty Lite Complete Tools [Core] (mcp__zhihuiya_299425 additions)

- `mcp__zhihuiya_299425.novelty_lite_submit`
  - Submits a complete novelty Lite task with one call. Requires `data.text` (the technical solution text). Optionally accepts `data.search_types` (semantic, boolean, paper, website).
  - Returns `data.task_id`. Use `novelty_lite_get` to poll progress and results.
  - Use for: efficient pre-response supplementary search (Step 6).

- `mcp__zhihuiya_299425.novelty_lite_get`
  - Queries progress and results of a novelty Lite task by task_id.
  - Supports `step_ids` and `include_step_results` parameters.

- `mcp__zhihuiya_299425.novelty_lite_search`
  - Runs novelty lite search using keyword extraction output and summary output.
  - Was missing from source-map but available; use for Step 6 supplementary search.

- `mcp__zhihuiya_299425.novelty_keywords_extract`
  - Extracts keywords, synonyms, and IPC-style elements from technical features.
  - Was missing from source-map but available; use for Step 6 supplementary search keyword generation.

## Patent Content Tools [Reference] (mcp__zhihuiya_958a46)

- `mcp__zhihuiya_958a46.search_patents` — Searches patents by query. Returns patent_id, patent_number, title.
- `mcp__zhihuiya_958a46.tech_summary` — Extracts 技术三要素 from a patent. Supports cn/en.
- `mcp__zhihuiya_958a46.description` / `description_translated` — Fetches full specification text by patent_id or patent_number.
- `mcp__zhihuiya_958a46.claims` / `claim_translated` — Fetches claim text by patent_id or patent_number.
- `mcp__zhihuiya_958a46.legal_status` — Fetches legal status by patent_id or patent_number.
- `mcp__zhihuiya_958a46.family` — Fetches patent family data by patent_id or patent_number.
- `mcp__zhihuiya_958a46.bibliography` — Fetches bibliographic data by patent_id or patent_number.

## Patent Legal & Financial Tools [Extended] (mcp__zhihuiya_30096b)

- `mcp__zhihuiya_30096b.re_examination_data`
  - Fetches re-examination and invalidation data by patent_id or patent_number.
  - Returns type (re-examination or invalidation), sequence, case type, decision number, decision date, requester, legal basis.
  - Use for: understanding D1/D2 prosecution history; finding relevant invalidation decisions that may support the applicant's position.

- `mcp__zhihuiya_30096b.litigation_data`
  - Fetches litigation data by patent_id or patent_number.
  - Returns case title, case number, filing date, verdict date, court, plaintiff, defendant.
  - Use for: understanding D1/D2 enforcement history; assessing litigation risk for claim scope decisions.

- `mcp__zhihuiya_30096b.fee_info`
  - Creates a patent fee information task by application numbers.

- `mcp__zhihuiya_30096b.legal_data`
  - Fetches legal event data by patent_id or patent_number.

- `mcp__zhihuiya_30096b.license_data` / `transfer_data` / `pledge_data` / `award_data` / `customs_data`
  - Fetches license, transfer, pledge, award, customs data for a patent.

## Credential Handling

For demo execution, use configured credentials from:

- `AI_API_KEY` — Unified Bearer token for AI60, AI32, and AI37 (e.g. `sk-vOwsyw...`).
- MCP server configuration already available to Codex

Do not paste credential values into chat, generated legal documents, or source appendices. Do not invent credentials.
