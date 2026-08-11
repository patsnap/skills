# Sample Workbook Guide

The package does not include real patent records because exports may be
licensed, confidential, or decision-sensitive. Build a synthetic or authorized
`.xlsx` workbook using the contract below.

## Required format

- File type: Excel `.xlsx`
- First row: column headers
- One publication record per row
- One active worksheet for the report input
- UTF-8-compatible text values
- No macros required

CSV is not the preferred format because it does not preserve embedded images,
cell hyperlinks, workbook metadata, or review formatting.

## Required columns

| Canonical field | Common accepted header | Description | Example |
|---|---|---|---|
| `publication_number` | `Publication number` | Published application or grant identifier | `US20260000001A1` |
| `title` | `Title` | Patent title | `Adjustable roof-tile mounting connector` |
| `applicant` | `Current applicant` | Applicant or assignee string from the source | `Example Solar Inc.` |

Column names are mapped by the topic configuration. If an export uses another
header, add an approved alias rather than changing data by column position.

## Recommended patent fields

| Canonical field | Common accepted header | Purpose |
|---|---|---|
| `legal_status` | `Legal status` | Status label; must be paired with source/as-of review |
| `application_date` | `Application date` | Filing/application timing |
| `publication_date` | `Publication date` | Publication timing |
| `normalized_title` | `Normalized title` | Reviewed concise English title |
| `technical_problem` | `Technical problem` | Problem stated or supported by the record |
| `technical_solution` | `Technical solution` | Technical approach stated or supported by the record |
| `technical_effect` | `Technical effect` | Reported effect, not assumed performance |
| `abstract` | `Abstract` | Discovery and review text |
| `independent_claims` | `Independent claims` | Claim text or reviewed claim notes |
| `family_id` | `Simple family ID` | Explicit family-normalization value |
| `source_url` | `Source URL` | Stable HTTP(S) patent-record link |

## Fields added by tagging

`scripts/tag_relevant.py` appends or updates:

| Header | Initial content |
|---|---|
| `Discovery disposition` | Candidate, likely out of scope, or no configured signal |
| `Inclusive terms matched` | Configured inclusive terms observed |
| `Exclusion terms matched` | Configured exclusion terms observed |
| `Review status` | `Requires human review` or `Unreviewed` |
| `Reviewer` | Optional CLI value |
| `Review date` | Optional ISO CLI value |

The reviewer may add:

| Header | Content |
|---|---|
| `Reviewed category IDs` | One or more configured category IDs separated by `|`, comma, or semicolon |
| `Review rationale` | Evidence-based inclusion or exclusion reason |
| `Status source` | Source used for a material status statement |
| `Status as of` | ISO date of the status check |
| `Claim notes` | Independent claim and relevant limitations reviewed |

Only the fields defined in the scripts are required for rendering; additional
review fields improve auditability.

## Review values accepted for publication

The renderer includes a record only when all conditions are met.

### Discovery disposition

Use one of:

- `Included`
- `Include`
- `Included — reviewer confirmed`

Other values are withheld.

### Review status

Use one of:

- `Reviewed`
- `Approved for briefing`
- `Complete`

The reviewer and a valid ISO review date are also mandatory.

## Minimal synthetic example

The following values are fictional and for schema testing only.

| Publication number | Title | Current applicant | Legal status | Application date | Publication date | Technical problem | Technical solution | Technical effect | Simple family ID | Source URL |
|---|---|---|---|---|---|---|---|---|---|---|
| `US20260000001A1` | Adjustable roof-tile mounting connector | Example Solar Inc. | Pending | `2025-06-01` | `2026-01-15` | Roof-tile alignment and weatherproofing | Adjustable connector with flashing | Reported reduction in installation steps | `EXAMPLE-F1` | `https://patentscope.wipo.int/` |
| `EP4000000A1` | Temperature control for a beverage preparation unit | Example Appliance GmbH | Application | `2025-05-20` | `2026-02-10` | Temperature variation during extraction | Closed-loop heater control | Reported temperature stability | `EXAMPLE-F2` | `https://worldwide.espacenet.com/` |

Do not cite these identifiers or facts as real evidence.

## Create a synthetic workbook with Python

```python
import pandas as pd

records = [
    {
        "Publication number": "US20260000001A1",
        "Title": "Adjustable roof-tile mounting connector",
        "Current applicant": "Example Solar Inc.",
        "Legal status": "Pending",
        "Application date": "2025-06-01",
        "Publication date": "2026-01-15",
        "Technical problem": "Roof-tile alignment and weatherproofing",
        "Technical solution": "Adjustable connector with flashing",
        "Technical effect": "Reported reduction in installation steps",
        "Simple family ID": "EXAMPLE-F1",
        "Source URL": "https://patentscope.wipo.int/",
    }
]

frame = pd.DataFrame(records)
frame.to_excel("synthetic_patents.xlsx", index=False)
```

## Add patent links

Preferred method:

1. include a `Source URL` column;
2. use a stable HTTP(S) patent-record URL;
3. verify the URL before release;
4. do not use local paths or session URLs.

The renderer uses the explicit URL field. Existing cell hyperlinks may remain in
the copied tagged workbook but are not trusted automatically as report links.

## Add embedded figures

If rights and confidentiality permit:

1. place a figure in the same row as its publication record;
2. anchor it to any cell in that row;
3. keep the image below 5 MB;
4. use PNG or JPEG;
5. verify association after rendering;
6. retain figure provenance outside the image itself.

The localized renderer associates images by row and publication header, not a
fixed column. It embeds at most 200 reviewed images. Unmatched or oversized
images are omitted.

## Data-source preparation

When using PatSnap or another database:

1. confirm export and reproduction rights;
2. save the exact search query and filters;
3. save execution date and database;
4. record matched, returned, reviewed, and exported counts separately;
5. disclose jurisdiction and language scope;
6. choose publication or family count treatment;
7. export stable identifiers and links;
8. include claim text or notes for material claim-relevance review;
9. retain status source and as-of date;
10. document exclusions and deduplication.

## Verified optional PatSnap connectors

- Patent search: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Patent briefing: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Use only the current exposed schemas. The workbook may also be prepared from an
authorized manual export.

## Data-size guidance

There is no analytical rule requiring 10–50, 100–500, or 500–2,000 records.
Select a review universe that answers the decision question and disclose limits.

Operationally:

- test schema changes with a small synthetic workbook;
- review large exports in controlled batches when necessary;
- avoid publishing hundreds of embedded images without a usability review;
- report truncation or sampling explicitly;
- never describe a convenience sample as exhaustive.

## Data-quality checks

### Identity

- publication numbers are non-empty;
- included publication numbers are unique;
- family IDs are explicit rather than inferred from number similarity;
- applicant strings are normalized when organization analysis is material.

### Dates

- dates use ISO format where possible;
- application and publication dates are not conflated;
- status as-of date is separate;
- report date and evidence cutoff are explicit.

### Technical text

- problem, solution, and effect reflect the record;
- expected effects remain distinct from measured results;
- translated text is reviewed;
- claim notes identify the claim reviewed.

### Links and images

- links use HTTP(S);
- URLs resolve to the intended record;
- embedded images map to the correct publication;
- image reuse is authorized;
- no local absolute path is present.

### Review provenance

- disposition is explicit;
- status is an accepted reviewed value;
- reviewer is named;
- review date is valid;
- category IDs resolve;
- rationale is retained for material exclusions.

## Common problems

### Missing optional normalized title

The report falls back to the original title.

### No embedded figure

The report shows `No reviewed embedded figure`. It does not download a generic
replacement.

### No family ID

The family metric displays an unavailable state. Do not infer family count.

### Unsafe URL

Non-HTTP(S) URLs are omitted from the HTML.

### Candidate does not appear

Confirm disposition, review status, reviewer, review date, and category ID.

### CSV-only source

Convert to `.xlsx` after verifying encoding and values. CSV links and images
cannot be preserved.

## Security and confidentiality

- Do not include confidential records in a public test fixture.
- Do not commit real exported workbooks.
- Do not send the workbook to external tools without authorization.
- Review generated HTML before distribution.
- Remember that Base64 images remain extractable from HTML.
- Remove temporary fixtures and cache files after testing.

## Next documentation

- `SKILL.md` — authoritative workflow
- `IMPROVEMENTS.md` — implementation and localization decisions
- `DISTRIBUTION.md` — release and packaging checks

The frozen source mentions a README that does not exist. No additional README is
created in this migration.
