# Setup guide

This skill can review supplied US claim/application materials without an MCP connection.

## 1. Prepare the materials

Provide the exact claim version and, where available:

- complete specification and drawings;
- application type/route, number, filing/priority dates, and stage;
- Office actions, cited references, interview summaries, amendments, and remarks;
- target commercial embodiment and desired breadth; and
- deadline/docket information from an authoritative source.

Claims-only review is supported, but 112(a), antecedent support, 112(f) corresponding structure/algorithm, and amendment basis remain preliminary.

## 2. Optional PatSnap global MCP services

### Patent Briefing

Recommended for retrieving or cross-checking an identified published application/patent's bibliography, family, status, claims, description, translations, and images.

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Key: `patent_briefing`
- Transport: `streamableHttp`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

### Advanced Patent Search

Recommended only when prior-art retrieval is authorized or an incomplete identifier must be resolved.

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Key: `advanced_patent_search`
- Transport: `streamableHttp`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Open the [PatSnap global MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers), sign in, and copy the current connection URL from the official Connect panel. Keep the real API key secret.

Do not make a mandatory connectivity call when supplied materials are sufficient.

## 3. Current US authority

Re-check current official sources for every live matter:

- USPTO subject-matter eligibility: https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility
- MPEP 2106, eligibility: https://www.uspto.gov/web/offices/pac/mpep/s2106.html
- MPEP 2111, BRI: https://www.uspto.gov/web/offices/pac/mpep/s2111.html
- MPEP 2181, 112(f): https://www.uspto.gov/web/offices/pac/mpep/s2181.html
- MPEP 608.01(n), dependent/multiple-dependent claims: https://www.uspto.gov/web/offices/pac/mpep/s608.html
- MPEP 802, restriction: https://www.uspto.gov/web/offices/pac/mpep/s802.html
- MPEP 823, PCT/371 unity distinction: https://www.uspto.gov/web/offices/pac/mpep/s823.html

These sources describe USPTO examination practice; statutes, regulations, binding precedent, prosecution records, and matter-specific facts also control.

## 4. Connection failure

If a requested connector is unavailable:

- continue from supplied authoritative materials;
- label external retrieval/search `not_executed`;
- provide a reproducible search/data request when needed; and
- do not fabricate prior art, legal status, claim text, family data, or a search conclusion.

## 5. Professional boundary

This skill provides drafting and review assistance. Filing decisions, deadlines, inventorship, new matter, legal conclusions, prosecution responses, restriction strategy, terminal disclaimers, enforceability, and infringement should be reviewed by qualified US patent counsel.

Use the [PatSnap Developer Center](https://open.patsnap.com/devportal) for current global platform documentation.
