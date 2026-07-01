# Harness Check Catalog

The executable source of truth is `scripts/validate_report.py`.

Core check groups:

- `STRUCTURE`: fixed 16-section HTML contract, heading order, required tables.
- `STYLE`: embedded fixed CSS block, no inline styles, no stylesheet links, CSS token/hash checks.
- `CONTENT`: metadata, four dimensions, score/grade consistency, high-risk mitigation consistency.
- `METHODOLOGY`: three-layer method and key method terms.
- `FORBIDDEN`: absolute safety claims, fake verification, non-patent risk overreach.

Recommended severity:

- Use `fail` for output contract breaks and trust risks.
- Use `warn` for incomplete content that may be acceptable in drafts.
- Use `pass` for satisfied checks.

When adding checks, keep output JSON stable:

```json
{
  "id": "GROUP-NNN",
  "group": "GROUP",
  "name": "Human readable name",
  "status": "pass|warn|fail",
  "severity": "info|warn|fail",
  "evidence": "...",
  "suggestion": "..."
}
```
