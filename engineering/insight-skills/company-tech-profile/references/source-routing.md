# Source Routing

Use the highest-confidence lane that is actually available.

## Default Order

1. structured patent and paper retrieval
2. domain-specific scholarly or filing databases when available
3. `Exa` for public-web discovery
4. `Tavily` when available and useful
5. `Brave` search as an additional fallback
6. `web` search as a generic fallback
7. `Jina` or another known-URL reader for pages or PDFs after discovery

## Route By Information Need

| Need | Preferred lane | Fallback |
| --- | --- | --- |
| company aliases and legal scope | official materials + structured assignee evidence | `Exa` then `web` |
| patent footprint | structured patent retrieval | `Exa` + official-domain `web` |
| paper footprint | structured paper retrieval or scholarly databases | `Exa` + `web` |
| product or release signals | official materials + `Exa` | `web`, then `Jina` to read pages |
| listed-company disclosures | official filings or finance databases | official-domain `web` |

## Downgrade Rule

If structured retrieval is not available:

- say so in `method_decisions.md`
- switch to domain-specific sources, `Exa`, `Tavily`, `Brave`, `web`, and `Jina`
- lower confidence on scale, route breadth, and novelty-style conclusions where appropriate

Do not pretend a downgraded run has the same evidence quality as a structured-data-backed run.
