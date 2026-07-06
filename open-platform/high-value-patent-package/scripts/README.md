# Reference Implementation — high-value-patent-package

These scripts are a **reference implementation** of the workflow described in
`../SKILL.md`. The skill itself is tool-agnostic: an agent can reproduce the same
result with any HTTP client. These Python scripts are provided so you can run the
pipeline directly or use it as a worked example.

## Setup

```bash
pip install requests python-docx
```

Provide credentials and the search query (never hard-code the key into artifacts):

```bash
# API key — option A (recommended): environment variable
export ZHIHUIYA_API_KEY="sk-xxxxxxxx"
# option B: a key file path
export ZHIHUIYA_API_KEY_FILE="/path/to/key.txt"
# option C: a file named api_key.txt in the working directory

# Search query — option A: environment variable
export HVP_QUERY='tac_all:(virtual reality) AND all_an:("Meta Platforms, Inc.") AND PBD:[20250101 to *]'
# option B: a file named query.txt in the working directory
```

## Run

```bash
python run_all.py          # HTML report only (default deliverable)
python run_all.py --word   # also generate the optional Word report
```

The HTML report is the required deliverable. The Word report is optional: it runs
only with `--word`, or by calling `hv_8_word.py` directly. `python-docx` is only
needed for the Word report.

Or run stage by stage (each writes a JSON checkpoint, so stages are restartable):

| Stage | Script | Output |
| --- | --- | --- |
| 1 | `hv_1_fetch.py` | `cand_raw.json` — all candidates (P002, paged 500/call) |
| 2 | `hv_2_numeric.py` | `enrich_num.json` — P014 family size, P015 cited-by |
| 3 | `hv_3_legal.py` | `enrich_legal.json` — P034/P027/P028/P029 events |
| 4 | `hv_4_score.py` | `scored.json` — 30/30/20/20 scores, top-5 inventors, selection |
| 5 | `hv_5_display.py` | `enrich_display.json` — P021 drawing, P025 AI elements, P041 status (selected only) |
| 6 | `hv_6_assemble.py` | `final_records.json` + `高价值专利包筛选数据.json` (trace; includes `patent_id` and `view_url`) |
| 7 (required) | `hv_7_html_a.py` | `高价值专利包筛选报告.html` — publication numbers link to the Zhihuiya patent page |
| 8 (optional) | `hv_8_word.py` | `高价值专利包筛选报告.docx` — same content + links, embeds abstract drawings |

`hv_8_word.py --noimg` skips downloading/embedding drawings (smaller, faster file).

## Notes

- **Inventor parsing.** PatSnap formats inventors as `LASTNAME, FIRSTNAME|...`.
  Split on `|`, `;`, `；`, and line breaks only — never on commas, or names get
  fragmented. See the core-inventor rule in `../references/screening-standard.md`.
- **Numeric scores** use percentile rank within the candidate set (>=10 candidates).
  Recent publication years often have few forward citations, so the cited-by
  indicator may have low discrimination; family size, core inventor, and legal
  events then carry the selection.
- **No fabricated data.** Missing fields are kept as `未获取` and preserved in the
  trace JSON so the report is auditable.
- Abstract-image URLs (P021) are signed and expire (~1 hour); the Word builder
  downloads them at generation time.
- **Clickable publication numbers.** Both reports turn the publication number into
  a link to the Zhihuiya patent-view page, built as
  `https://analytics.zhihuiya.com/patent-view/abst?patentId=<patent_id>&q=<pn>`
  (template `VIEW_TMPL` in `hv_6_assemble.py`). This minimal form has no share
  signature, so it never expires; the reader must be logged into Zhihuiya. To
  target a different Zhihuiya/PatSnap product line, edit `VIEW_TMPL`.

## Tuning

- Selection ratio defaults to 10% (`ceil(n*0.10)`). To widen toward the 15% cap,
  edit `sel_count` in `hv_4_score.py`.
- To re-weight indicators, edit the `s_cited / s_fam / s_inv / s_legal` terms in
  `hv_4_score.py`.
