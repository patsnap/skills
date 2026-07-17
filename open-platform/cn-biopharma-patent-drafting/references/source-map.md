# Source Map - CNIPA Patent Drafting

> **Tool Tier Classification**
> - `[Core]` = Tier 1: Fixed in workflow steps. Default choice.
> - `[Extended]` = Tier 2: Conditional branch tools. Activated by specific conditions.
> - `[Reference]` = Tier 3: On-demand tools. Loaded via ToolSearch when needed.
> 
> **Invocation Method**
> - **Local API Wrappers (AI60/AI32/AI37)**: Invoked via **Bash tool** with CLI commands. NOT MCP tools — do NOT search via ToolSearch, do NOT call via DeferExecuteTool.
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
- Supports: PDF, images (PNG/JPG/TIFF/BMP), Office docs (doc/docx/ppt/pptx/xls/xlsx).
- **Fallback**: AI60 云端 OCR 失败时（网络错误、权限不足、超时），**自动降级到 RapidOCR**（本地 CPU OCR 引擎，基于 ONNX Runtime，无需 GPU）。降级行为默认开启，可通过 `--no-fallback` 禁用。对于有 MCP PDF URL 的专利文献，仍建议优先使用 AI60 URL 模式。

### AI32 Technical Disclosure (Step 5)

- Client: `$USERPROFILE/.workbuddy/api-wrappers/ai32/patent-disclosure-client.mjs`
- CLI: `$USERPROFILE/.workbuddy/api-wrappers/ai32/cli.mjs`
- **Bash invocation** (credentials via CLI args or env vars):
  ```bash
  # One-shot: extract tech means → generate disclosure → download
  node "$USERPROFILE/.workbuddy/api-wrappers/ai32/cli.mjs" create_and_wait --tech_solution "技术方案文本" [--api-key KEY] [--language cn] [--output disclosure.docx]
  # Extract tech means only (AI32-1)
  node "$USERPROFILE/.workbuddy/api-wrappers/ai32/cli.mjs" extract_tech_means --tech_solution "技术方案文本" [--api-key KEY]
  # Check download status
  node "$USERPROFILE/.workbuddy/api-wrappers/ai32/cli.mjs" get_download_status --job_id ID [--api-key KEY]
  ```
- Credentials: pass via `--api-key` CLI arg, or set `AI_API_KEY` env var (shared by AI32/AI37).
- Endpoints: `/search/patent/patent-disclosure/tech-means`, `/generate`, `/download`, `/sse`
- AI32 generates a technical disclosure document; it is NOT an initial-claim generator.

### AI37 CNIPA Specification (Step 7)

- Client: `$USERPROFILE/.workbuddy/api-wrappers/ai37/ai37_cnipa_client.py`
- CLI: `$USERPROFILE/.workbuddy/api-wrappers/ai37/cli.py`
- **Bash invocation** (credentials via CLI args or env vars):
  ```bash
  # One-shot full flow: init → extract feature → generate report → download
  python "$USERPROFILE/.workbuddy/api-wrappers/ai37/cli.py" run_full_flow --claim "权利要求书内容" --disclosure "交底书内容" [--api-key SK] [--title "发明名称"]
  # Or step-by-step:
  python "$USERPROFILE/.workbuddy/api-wrappers/ai37/cli.py" init_summary --claim "..." --disclosure "..." [--api-key SK]
  python "$USERPROFILE/.workbuddy/api-wrappers/ai37/cli.py" extract_feature --task_id ID --category CAT [--api-key SK]
  python "$USERPROFILE/.workbuddy/api-wrappers/ai37/cli.py" generate_report --payload-json payload.json [--api-key SK]
  python "$USERPROFILE/.workbuddy/api-wrappers/ai37/cli.py" get_report_result --task_id ID [--api-key SK]
  ```
- Credentials: pass via `--api-key` CLI arg, or set `AI_API_KEY` env var (shared by AI32/AI37). `AI37_API_KEY` also supported as fallback.
- Required inputs: both `claim` and `disclosure` must be provided before running AI37.
- **`--title` limit**: Must be ≤50 characters. The CLI auto-truncates titles exceeding 50 chars to 47 chars + "...".

## Chemical Structure Tools [Core]

- `mcp__zhihuiya_713886.ls_structure_search`
  - Searches compounds by SMILES structure. Supports `EXT` (exact/substructure) and `SIM` (similarity with threshold).
  - Returns inchi_key, compound_name, formula, similarity. Paginated with offset/limit.
  - Use for: prior-art compound landscape check before drafting claims for a small molecule.

- `mcp__zhihuiya_713886.ls_structure_fetch`
  - Batch fetches full compound details by InChIKey list (max 100 per request).
  - Returns canonical_smiles, molecular_formula, compound_name, patent associations.
  - Use after `ls_structure_search` to enrich prior-art compound data.

- `mcp__zhihuiya_713886.ls_patent_structure_fetch`
  - Fetches all chemical structures associated with a patent by patent_id or pn.
  - Paginated: offset + limit (max 100 per page).
  - Use for: extracting compound lists from cited prior-art patents.

- `mcp__zhihuiya_713886.ls_chemical_mcs_analyze`
  - Analyzes common fragment (MCS) distribution across a list of SMILES structures.
  - Use for: identifying shared scaffolds to support claim scope decisions (broader vs narrower scaffold claims).

- `mcp__zhihuiya_713886.ls_sar_submit` and `ls_sar_fetch`
  - Submit/fetch SAR extraction for small-molecule patent public numbers. Async: submit returns task_id, poll with fetch.
  - Use for: understanding prior-art SAR to inform claim drafting strategy and avoid over-narrow claims.

- `mcp__zhihuiya_713886.ls_admet_predict`
  - Predicts ADMET properties for SMILES list (1–100 per request).
  - Use for: generating supporting data for inventive-step arguments (unexpected ADMET advantage over prior art).

## Biological Sequence Tools [Core]

- `mcp__zhihuiya_06e741.ls_sequence_search_submit`
  - Submits a bio sequence search job (NUCLEOTIDE or PROTEIN). Async: returns job_id.
  - Supports database filter (ALLPATENT, CLAIMS), identity/coverage thresholds, evalue, strand, subject_length.
  - Follow with `ls_sequence_search_check_status` and `ls_sequence_search_get_results`.
  - Use for: prior-art sequence search before drafting biologic/antibody claims.

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
  - Use for: aligning applicant sequence against closest prior-art to identify distinguishing regions for claim drafting.

- `mcp__zhihuiya_06e741.ls_patent_sequence_fetch`
  - Fetches all sequences associated with a patent by patent_id or pn. Paginated: offset + limit (max 100 per page).
  - Use for: extracting sequence listings from cited prior-art patents.

- `mcp__zhihuiya_06e741.ls_antibody_antigen_search`
  - Searches antibody-antigen relations by target_name (required). Returns antibody sequences, patent info, species.
  - Use for: antibody prior-art landscape before drafting CDR claims or antibody composition claims.

- `mcp__zhihuiya_06e741.ls_modification_search_submit`
  - Submits a modification search job for sequences with chemical modifications. Async: returns job_id.
  - Use for: prior-art search for modified nucleotide/peptide inventions (e.g., PEGylation, lipidation, phosphorylation).

## Relevant MCP Tools [Core]

- `mcp__zhihuiya_33072f.upload_patent_image`: upload a local JPG/PNG image under 4 MB to obtain a public URL.
- `mcp__zhihuiya_299425.novelty_summary`: summarize technical problem, solution, and effect from technical text.
- `mcp__zhihuiya_299425.novelty_feature_extract`: extract technical features from a summary.
- `mcp__zhihuiya_299425.novelty_keywords_extract`: extract keywords and IPC-style search elements.
- `mcp__zhihuiya_299425.novelty_lite_search`: multi-channel novelty search; use only with its documented inputs.
- `mcp__zhihuiya_299425.novelty_feature_comparison`: compare extracted features against patent IDs.
- `mcp__zhihuiya_299425.novelty_lite_report_generate`: generate a short novelty/inventiveness review from feature comparison and top patents.
- `mcp__zhihuiya_2b0355_logic.patsnap_search`: patent/paper semantic, keyword, and filtered search.
- `mcp__zhihuiya_2b0355_logic.patsnap_fetch`: fetch patent or paper details; patent modules include `basic`, `citation`, `legal`, `family`.

## Pharma Intelligence Tools [Extended]

- `mcp__pharma_intelligence.ls_drug_search`
  - Searches drug pipeline by drug name, target, disease, organization, drug type (Small molecule drug, Monoclonal antibody, ADC, Biological product, Gene therapy), mechanism of action, highest phase, ATC code, country, development status, and date range.
  - Use for: checking whether the invention's drug/target/disease already has competing drugs in development; informing claim scope based on pipeline stage.

- `mcp__pharma_intelligence.ls_drug_fetch`
  - Batch fetches full drug details by drug IDs or drug names.
  - Returns target associations, global highest dev status, indication details, mechanism of action, organization, milestones.
  - Use for: enriching the novelty assessment with drug development context.

- `mcp__pharma_intelligence.ls_drug_deal_search` / `ls_drug_deal_fetch`
  - Searches drug BD deals (licensing, collaboration, option, acquisition, M&A, investment) by drug, target, disease, organization, deal type, phase, country, date range.
  - Use for: understanding the commercial landscape and informing claim value assessment.

- `mcp__pharma_intelligence.ls_clinical_trial_search` / `ls_clinical_trial_fetch`
  - Searches clinical trials by drug, target, disease, organization, phase, study status, country, mechanism of action, date range.
  - Use for: understanding the clinical development stage of competing drugs; informing the level of detail needed in the specification for sufficient disclosure.

- `mcp__pharma_intelligence.ls_clinical_trial_result_search` / `ls_clinical_trial_result_fetch`
  - Searches clinical trial results by drug, target, disease, organization, phase, date range.
  - Use for: finding trial results that may support inventive-step arguments.

- `mcp__pharma_intelligence.ls_target_fetch`
  - Batch fetches target details by target IDs or names.

- `mcp__pharma_intelligence.ls_disease_fetch`
  - Batch fetches disease details by disease IDs or names.

- `mcp__pharma_intelligence.ls_organization_fetch` / `ls_organization_pipeline_fetch`
  - Fetches organization details and drug development pipeline by organization IDs or names.
  - Use for: understanding the competitive landscape when the applicant is developing drugs in the same space.

- `mcp__pharma_intelligence.ls_news_vector_search`
  - Semantic vector search for biopharma news. Requires `query` and `lang` (CN/EN). Returns top_k text chunks.

- `mcp__pharma_intelligence.ls_paper_vector_search`
  - Semantic vector search for academic papers. Requires `query` and `lang` (CN/EN). Returns top_k text chunks.
  - Use for: finding relevant academic publications for prior art during novelty assessment.

- `mcp__pharma_intelligence.ls_patent_vector_search`
  - Semantic vector search for biopharma patent text chunks. Requires `query` and `lang` (CN/EN).

- `mcp__pharma_intelligence.ls_patent_search`
  - Structured search for life-science patents by drug, target, disease, organization, patent type, country, date, legal status, sequences.

- `mcp__pharma_intelligence.ls_translational_medicine_search` / `ls_translational_medicine_fetch`
  - Searches translational medicine records by drug, target, disease, organization, mechanism of action, date range.

- `mcp__pharma_intelligence.ls_epidemiology_vector_search`
  - Semantic vector search for epidemiology data. Requires `query` and `lang` (CN/EN).
  - Use for: disease prevalence/incidence data to support indication scope and market analysis in the specification.

- `mcp__pharma_intelligence.ls_fda_label_vector_search`
  - Semantic vector search for FDA drug label data. Requires `query` and `lang` (CN/EN).
  - Use for: finding approved drug label information for claim scope analysis.

- `mcp__pharma_intelligence.ls_ner_nor_normalize`
  - Named entity recognition and normalization for drug/target/disease names.

## Novelty Lite Complete Tools [Core]

- `mcp__zhihuiya_299425.novelty_lite_submit`
  - Submits a complete novelty Lite task with one call. Requires `data.text` (the technical solution text). Optionally accepts `data.images` and `data.search_types` (semantic, boolean, paper, website).
  - Returns `data.task_id`. Use `novelty_lite_get` to poll progress and results.
  - **Why this matters**: Instead of manually calling 6 individual tools in sequence (summary → feature_extract → keywords_extract → search → feature_comparison → report_generate), `novelty_lite_submit` runs all steps automatically. Use this as an efficient alternative in Step 3 (Pre-Drafting Novelty Assessment).

- `mcp__zhihuiya_299425.novelty_lite_get`
  - Queries progress and results of a novelty Lite task by task_id.
  - Supports `step_ids` to query specific steps (novelty_summary, novelty_feature_extract, novelty_keywords_extract, novelty_lite_search, novelty_lite_candidate_patents, novelty_feature_comparison, novelty_lite_report_generate).
  - Supports `include_step_results=true` to get results of completed steps while task is still running.
  - Use after `novelty_lite_submit` to get the complete novelty assessment results.

## Patent Content Tools [Reference]

- `mcp__zhihuiya_958a46.search_patents` — Searches patents by query. Returns patent_id, patent_number, title.
- `mcp__zhihuiya_958a46.tech_summary` — Extracts 技术三要素 from a patent. Supports cn/en.
- `mcp__zhihuiya_958a46.description` / `description_translated` — Fetches full specification text by patent_id.
- `mcp__zhihuiya_958a46.claims` / `claim_translated` — Fetches claim text by patent_id.
- `mcp__zhihuiya_958a46.legal_status` — Fetches legal status by patent_id.
- `mcp__zhihuiya_958a46.family` — Fetches patent family data by patent_id.
- `mcp__zhihuiya_958a46.bibliography` — Fetches bibliographic data by patent_id.

## Material & Classification Tools [Reference]

- `mcp__zhihuiya_7cc6ae.tech_problem_benefit_summary` — Extracts technical problem/benefit/approach summaries. Supports cn/en.
- `mcp__zhihuiya_7cc6ae.technology_topic` — Gets technology topic classification for a patent.
- `mcp__zhihuiya_7cc6ae.classification_description` — Gets IPC/CPC/UPC etc. description (batch up to 10 codes).
- `mcp__zhihuiya_7cc6ae.seic_classification` — Gets strategic emerging industry classification.

## Credential Handling

API wrappers read credentials from environment variables. Set these before invoking:

- `AI_API_KEY` — Unified Bearer token for AI60, AI32, and AI37 (e.g. `sk-vOwsyw...`). `AI37_API_KEY` also supported as fallback.
- `AI37_BASE_URL` — (optional) Override AI37 base URL

MCP server credentials are handled by the MCP server configuration.

Do not paste credential values into user-facing replies or generated reports. Do not invent missing credentials.
