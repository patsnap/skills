# PatSnap IP Skills

IP skills in this directory support the core free patent-search workflow and its Chinese variant. Imported Skill Hub / Open Platform IP workflows now live in `../open-platform/`.

Install all IP skills:

```bash
npx skills add patsnap/skills/tree/main/ip --all
```

## Directory Snapshot

| Type | Count | Notes |
|---|---:|---|
| Total skill directories | 2 | `free-patent-search` and `free-patent-search-zhcn`. |
| Open Platform imported directories | 0 | Imported Skill Hub / Open Platform workflows live under `../open-platform/`. |

## Available Skills

| Skill | Chinese Variant | Description |
|---|---|---|
| `free-patent-search` | `free-patent-search-zhcn` | Patent search powered by PatSnap's free MCP, covering novelty search, FTO analysis, invalidation search, competitive intelligence, legal-status checks, and portfolio research. |

## Language Variants

Chinese versions use the `-zhcn` suffix and are separate skill directories. Use the Chinese variant when the expected interaction and output should be in Simplified Chinese.

## Primary Workflow

`free-patent-search` guides agents through:

1. API Key readiness check for PatSnap Open Platform.
2. Patent-search intent triage, such as novelty search, FTO analysis, competitive intelligence, legal-status checks, design patent risk, or premium-field requests.
3. Retrieval through the PatSnap free MCP fields when an API Key is available.
4. Clear explanation of free-tier data boundaries.
5. Product guidance for deeper workflows, including Novelty Search Agent, FTO Agent, Design FTO Agent, Patent Data API, and PatSnap Analytics.

## Data Boundary

The free patent MCP focuses on lightweight patent metadata fields, such as title, applicant, inventor, filing/publication dates, publication/application numbers, legal status, IPC class, and priority country.

Do not present free-tier results as legal advice or as a substitute for full claim analysis, semantic retrieval, patent family mapping, litigation review, or attorney-led FTO conclusions.

## Open Platform Skills

Additional patent and IP workflows imported from Skill Hub are available in `../open-platform/`, including patent quality review, FTO report generation, claims review, patent mining, lifecycle management, asset grading, technology transfer, litigation monitoring, portfolio analysis, and vertical patent intelligence workflows.

## Related PatSnap Products

| Product | Best For |
|---|---|
| Novelty Search Agent | Prior-art search, invention feasibility, invalidation search. |
| FTO Agent | Claim-level freedom-to-operate and infringement-risk workflows. |
| Design FTO Agent | Design patent and visual-similarity risk checks. |
| Patent Data API | Programmatic patent data access and system integration. |
| PatSnap Analytics | Full-field patent search, competitive intelligence, portfolio analysis. |
