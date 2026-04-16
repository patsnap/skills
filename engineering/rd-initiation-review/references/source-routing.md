# Source Routing

Use the highest-confidence lane that is actually available.

## Default Order

1. proposal materials and user-provided files
2. structured patent and paper retrieval for prior-work and frontier evidence
3. domain-specific scholarly or filing databases when available
4. `Exa` for public-web discovery
5. `Tavily` when available and useful
6. `Brave` as an additional fallback
7. `web` search as a generic fallback
8. `Jina` or another known-URL reader for pages or PDFs after discovery

## Route By Information Need

| Need | Preferred lane | Fallback |
| --- | --- | --- |
| proposal claim extraction | proposal materials | ask for missing material or mark as open gap |
| novelty and overlap | structured retrieval or scholarly databases | `Exa` + `web` |
| feasibility and frontier support | structured retrieval or scholarly databases | `Exa` + `web` |
| sponsor or comparator disclosures | official filings or finance databases | official-domain `web` |
| policy, standards, and public deployment status | `Exa` | `web`, then `Jina` |

## Downgrade Rule

If proposal materials are thin or structured retrieval is unavailable:

- record the downgrade in `method_decisions.md`
- be explicit about what cannot be fully checked
- lower confidence on novelty, overlap, and completeness claims

Do not imply that a public-only pass equals full duplicate-project exclusion.
