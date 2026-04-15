# Source Routing

Use the highest-confidence lane that is actually available.

## Default Order

1. structured patent and paper retrieval for arena discovery and assignee evidence
2. domain-specific scholarly or filing databases when available
3. `Exa` for public-web discovery and official pages
4. `Tavily` when available and useful
5. `Brave` as an additional fallback
6. `web` search as a generic fallback
7. `Jina` or another known-URL reader for pages or PDFs after discovery

## Route By Information Need

| Need | Preferred lane | Fallback |
| --- | --- | --- |
| candidate player discovery | structured retrieval + `Exa` | `web` |
| per-player technical evidence | structured retrieval | `Exa` + official-domain `web` |
| papers and affiliations | structured retrieval or scholarly databases | `Exa` + `web` |
| listed-player disclosures | official filings or finance databases | official-domain `web` |
| official pages, launches, and public signals | `Exa` | `web`, then `Jina` |

## Downgrade Rule

If structured retrieval is not available:

- say so in `method_decisions.md`
- use domain-specific sources, `Exa`, `Tavily`, `Brave`, `web`, and `Jina`
- lower confidence on completeness, player ranking, and route-breadth claims

Do not present a downgraded run as a complete market map unless the evidence truly supports that level of confidence.
