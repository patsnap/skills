# API call notes

## Authentication

All endpoints use a PatSnap Open Platform API key as a Bearer token:
```
Authorization: Bearer <token>
```

## Collapse parameters

| Parameter | Value | Meaning |
|------|----|------|
| `collapse_by` | `PBD` | Select records by publication date within each collapsed set. |
| `collapse_type` | `APNO` | Collapse by application number. |
| `collapse_order` | `LATEST` | Keep the latest publication in the collapsed set. |
| `collapse_order_authority` | Optional endpoint-specific array | Jurisdiction preference. Do not send it in this skill's P002 dashboard request because the frozen source validation identified count distortion. |

## P002 endpoint

- **URL**: `https://connect.patsnap.com/search/patent/query-search-patent/v2`
- **Method**: POST
- **Query syntax**: `ANCS:(Applicant name)`
- **Response records**: `data.results`
- **Source validation date**: 2026-05-27 on the Chinese endpoint; treat the source counts as historical fixtures, not current global results.
- **Global documentation verification**: The current PatSnap MCP/API pages document this `connect.patsnap.com` query-search path and a `data.results` response convention; recheck the OpenAPI schema before release.
