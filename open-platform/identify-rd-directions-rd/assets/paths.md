# Output Path Contract

This file is the single source of truth for the three generated artifacts. Do not hard-code session-specific, user-specific, operating-system-specific, or domestic-platform paths elsewhere in the package.

## Command-line placeholders

| Placeholder | Meaning | Portable default when the user does not specify a path |
|---|---|---|
| `PAYLOAD_PATH` | Reviewed canonical JSON payload | `reports/rd-directions-{YYYYMMDD}.json` |
| `HTML_PATH` | Self-contained HTML report | `reports/rd-directions-{YYYYMMDD}.html` |
| `MARKDOWN_PATH` | Markdown report generated from the same payload | `reports/rd-directions-{YYYYMMDD}.md` |

`YYYYMMDD` is the report-generation date in the user's selected time zone. The date must be resolved before calling the renderer; do not store a literal shell substitution or placeholder in the payload.

## Renderer

| Purpose | Package-relative path |
|---|---|
| Deterministic validator and renderer | `scripts/render_report.py` |

## Invocation

```bash
python scripts/render_report.py \
  --payload /path/to/reviewed-payload.json \
  --output /path/to/rd-directions.html \
  --markdown-output /path/to/rd-directions.md
```

The payload already exists before rendering. The renderer must not reconstruct research evidence from environment variables, standard input, conversation text, or hidden session state.

## User-specified paths

Explicit user paths override the defaults. Resolve each path, require a `.json`, `.html`, or `.md` suffix as applicable, refuse filesystem roots and symbolic-link targets, and create only the immediate parent directories required for the named files.

## Overwrite policy

Refuse to overwrite an existing artifact unless `--overwrite` is explicitly supplied. With overwrite enabled, replace only the three named output files. Never recursively delete or empty an output directory.

## Artifact relationship

```text
reviewed evidence and analysis
             |
             v
       canonical payload
          /       \
         v         v
   Markdown report  HTML report
```

Markdown and HTML are deterministic views of the same validated payload. Neither output is used as the source for the other, and pasted conversation content is not authoritative.
