# Source Routing

Use the highest-confidence lane that is actually available.

## Default Order

1. structured patent and paper retrieval
2. domain-specific scholarly databases when available
3. `Exa` for public-web discovery and official pages
4. `Tavily` when available and useful
5. `Brave` as an additional fallback
6. `web` search as a generic fallback
7. `Jina` or another known-URL reader for pages or PDFs after discovery

## Route By Information Need

| Need | Preferred lane | Fallback |
| --- | --- | --- |
| route definitions and candidate evidence | structured retrieval | `Exa` + `web` |
| frontier papers and DOI support | structured retrieval or scholarly databases | `Exa` + `web` |
| standards, launches, and official public status | `Exa` | `web`, then `Jina` |
| detailed page or PDF reading | `Jina` after discovery | any equivalent known-URL reader |

## Downgrade Rule

If structured retrieval is not available:

- say so in `method_decisions.md`
- use domain-specific sources, `Exa`, `Tavily`, `Brave`, `web`, and `Jina`
- lower confidence on route breadth, novelty-style claims, and frontier completeness

Do not pretend a downgraded run is exhaustive if the route evidence is clearly thinner.
