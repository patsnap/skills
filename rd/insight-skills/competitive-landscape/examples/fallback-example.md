# Fallback Example

If structured patent/paper retrieval is unavailable, the skill should still proceed like this:

1. Record in `method_decisions.md` that the highest-confidence structured source is not available.
2. Use any available scholarly databases, official filings, or domain-specific sources where possible.
3. Use `Exa` for broad public-web discovery.
4. Use `Tavily` or `Brave` if available for supplementary discovery.
5. Use generic `web` search as a fallback.
6. Use `Jina` or another known-URL reader to read the specific official pages or PDFs that matter.

The final report should clearly say that player completeness and route breadth are based on a downgraded evidence path.
