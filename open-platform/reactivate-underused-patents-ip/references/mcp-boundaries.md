# MCP and Evidence Boundaries

Use this reference to select verified global PatSnap connectors and prevent a score,
search result, or missing tool from becoming an unsupported commercialization claim.

## Verified published connectors

| Connector | Role | Marketplace | Connection endpoint |
|---|---|---|---|
| `patent_monetization_valuation` | Patent transaction/monetization screening, search, status, family, claims, description, translations and images exposed by the live schema | https://open.patsnap.com/marketplace/mcp-servers/patent-monetize | `https://open.patsnap.com/marketplace/mcp-servers/patent-monetize` |
| `advanced_patent_search` | Reproducible fielded/semantic/similarity search, counts, facets, assignee expansion and candidate discovery | https://open.patsnap.com/marketplace/mcp-servers/patent-search | `https://open.patsnap.com/marketplace/mcp-servers/patent-search` |
| `global_core_patent_database` | Selected-record family, claims/full text, status/events, citation, license, transfer, pledge and challenge evidence where exposed | https://open.patsnap.com/marketplace/mcp-servers/core-patents | `https://open.patsnap.com/marketplace/mcp-servers/core-patents` |
| `patent_briefing` | Fast selected-record bibliography, technical summary, family, status, claims, description, translations and images | https://open.patsnap.com/marketplace/mcp-servers/patent-briefing | `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing` |

Inspect `tools/list` or the installed schema at runtime. A marketplace description does
not guarantee that every desired operation or field is authorized in the current session.

## Runtime-discovered optional capability

`patent_valuation_scorecard` operations are visible in the current runtime and may return
overall or component scores/indicators. The migration did not independently verify a
dedicated global marketplace page and connection contract for this server. Therefore:

- treat it as optional and runtime-discovered;
- record exact tool name, inputs, output version/date, units and limitations;
- do not include an invented marketplace URL or endpoint;
- do not make the skill fail when it is absent; and
- treat scores as model-derived screening inputs, not formal valuation, legal opinion,
  transaction price, market demand, or technical quality.

## Unavailable source dependencies

Two source-only corporate-asset and exploratory-search dependencies were not callable
in the verified current runtime, and no exact global contract was established for them.

Replace their intended roles with:

- authorized internal asset registers, contracts, product/project records and CRM;
- current official corporate, regulator, court, procurement, standards, funding and
  transaction sources when web research is authorized;
- `advanced_patent_search` for patent discovery/statistics;
- `patent_briefing` for selected technical reading; and
- `global_core_patent_database` for deeper selected-record verification.

Mark the unavailable dimension rather than inventing non-patent assets or buyers.

## Three-layer patent funnel

1. **Explore:** use Advanced Patent Search semantic/similarity/keyword capabilities and
   known seeds to understand terminology, neighboring solutions and organizations.
2. **Measure:** use a versioned Advanced Patent Search query/count/facet method with a
   documented population, cap, date, unit and family rule.
3. **Verify:** use Patent Monetization & Valuation, Patent Briefing, and/or Global Core
   Patent Database on selected records for identity, family, status, claims, description,
   events, translations and images.

Do not perform population statistics on a Top-K exploratory result set. Do not call a
selected-record score or event a portfolio-wide fact.

## Conflict rules

- Preserve every conflicting value with source and date.
- Prefer official registers/courts/contracts for dispositive ownership, status, term,
  encumbrance, license and litigation facts.
- Use patent-database values as dated research signals until verified.
- Define family and citation measures before comparing them.
- Do not merge current owner, original applicant and corporate group.
- Do not replace a missing internal-use or transaction record with “unused.”
- Do not resolve a conflict by taking the highest score or most favorable valuation.
- Record which value is displayed, why, and what review is required.

## Evidence hierarchy

| Level | Appropriate sources | Use |
|---|---|---|
| S | Official patent registers, courts, regulators, government procurement/funding records, signed internal contracts and authoritative patent facts | Primary factual evidence, still date- and scope-bound |
| A | Audited/listed-company disclosures, official company sites, recognized transaction platforms, verified structured connector results | Strong operational/commercial signal |
| B | Standards bodies, industry associations, peer-reviewed research, reputable technical/business media | Corroborating context |
| C | Ordinary media, conference material, forums or social posts with identifiable provenance | Weak lead only |
| D | Unsourced reposts, anonymous claims, generated assertions | Exclude from conclusions |

Record URL/document ID, title, publisher, date, access date, level, relevant fact, and
which conclusion uses it. A high evidence level does not remove the need for legal or
commercial interpretation.

## Language and legal boundary

Use “database status signal,” “model-derived valuation input,” “candidate counterparty,”
“underused candidate,” and “requires diligence.” Avoid “clean title,” “verified value,”
“buyer,” “demand,” “safe to abandon,” or “ready to transact” without the corresponding
authoritative evidence and professional approval.
