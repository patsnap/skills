# Fallback Example

If structured patent/paper retrieval is unavailable, the skill should still proceed like this:

1. Start from proposal materials and extract claims carefully.
2. Record in `method_decisions.md` that the highest-confidence structured source is not available.
3. Use any available scholarly databases, official filings, or domain-specific sources where possible.
4. Use `Exa` for broad public-web discovery.
5. Use `Tavily` or `Brave` if available for supplementary discovery.
6. Use generic `web` search as a fallback.
7. Use `Jina` or another known-URL reader to read the specific official pages or PDFs that matter.

The final report should clearly state that novelty and overlap conclusions were produced on a downgraded evidence path.
