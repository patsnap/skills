# Smart Document REST API contract

## Connection

- Method: `POST`
- Production endpoint: `https://connect.zhihuiya.com/rd-llm/v1/documents/doc_parsing`
- Authentication: `Authorization: Bearer <API_KEY>`
- Content type: `multipart/form-data`

This Skill must use the production endpoint above. Do not use a stage host or the `/mcp` endpoint.

## Request

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `file` | yes | Binary file upload | Document to parse; the filename extension determines its type |
| `output_format` | no | `markdown`, `jsonl`, `both` | Response representation; defaults to `markdown` |

Supported filename extensions are `png`, `jpg`, `jpeg`, `pdf`, `doc`, `docx`, `ppt`, `pptx`, `xls`, and `xlsx`.

The current gateway defaults allow files up to 20 MB and documents up to 200 pages. Processing times out after 300 seconds. Deployment policy can change these limits, so the returned error is authoritative.

## cURL template

Read the API Key from the caller's secure environment instead of putting it in the command or source file:

```bash
curl --fail-with-body --silent --show-error \
  -X POST "https://connect.zhihuiya.com/rd-llm/v1/documents/doc_parsing" \
  -H "Authorization: Bearer ${SMART_DOCUMENT_API_KEY}" \
  -F "file=@${DOCUMENT_PATH}" \
  -F "output_format=markdown"
```

Do not manually set the `Content-Type` header. `curl -F` creates the multipart boundary correctly.

## Success response

The API returns a JSON envelope:

```json
{
  "status": "success",
  "data": {
    "state": "success",
    "total_pages": 1,
    "file_type": "pdf",
    "results": [],
    "markdown": "..."
  },
  "error_code": 0,
  "error_msg": "success",
  "_meta": {
    "openapi_billing": {
      "version": 1,
      "multiplier": "1"
    }
  }
}
```

Output shaping:

| `output_format` | `data.markdown` | `data.results` |
| --- | --- | --- |
| `markdown` | Present | Empty array |
| `jsonl` | Absent | Page-region array |
| `both` | Present | Page-region array |

Each structured region can contain:

- `page`: zero-based page index.
- `type`: layout category such as main text, table, equation, chemical structure, or figure.
- `content`: OCR text when available.
- `url`: signed crop URL when emitted by the service.
- `bbox`: normalized `[x1, y1, x2, y2, confidence]` values in the range 0–1.

`X-Openapi-Amount` and `_meta.openapi_billing.multiplier` normally reflect the parsed page count. Avoid duplicate calls when the first response already contains the required data.

## Errors

Application errors use the same envelope with `status=error`, `data=null`, and a string `error_code`.

| HTTP/code | Action |
| --- | --- |
| `401` / `403` | Check whether the Bearer API Key exists, is valid, and has permission. Never print the Key. |
| `INVALID_FILE_FORMAT` | Supply a supported, uncorrupted file with a detectable extension. |
| `FILE_TOO_LARGE` | Reduce or split a file that exceeds the size or page limit. |
| `PDF_PARSE_FAILED` | Decrypt or re-export an encrypted/corrupted PDF. |
| `DOCUMENT_CONVERSION_FAILED` | Re-export the Office document or convert it to PDF. |
| `OCR_FAILED` | Report the OCR service failure without inventing content. |
| `LAYOUT_DETECTION_FAILED` | Report the layout service failure without inventing regions. |
| `GATEWAY_TIMEOUT` | Split the file; retry only with user agreement. |
| `INTERNAL_ERROR` | Report the service-side failure and preserve any correlation identifier. |

With `--fail-with-body`, curl returns a nonzero exit status for HTTP errors while retaining the response body for diagnosis.
