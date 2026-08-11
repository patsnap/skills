# PatSnap MCP Search Guide

Use an external patent search only when the user asks for research or when the requested innovation screen expressly includes patent evidence. Do not search merely because a document was supplied.

## Verified global mapping

- `advanced_patent_search` — [PatSnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- `patent_briefing` — [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

Use the exact callable schema exposed in the current environment. Do not invent legacy domestic tool names, parameters, response fields, or record URLs. Use English interface parameters and English queries unless the technical vocabulary or source evidence requires multilingual searching.

## Search-readiness gate

A candidate is query-ready when:

- the technical problem or operating context is defined;
- at least one differentiating implementation feature is specific;
- generic business outcomes have been removed;
- the query can distinguish the contribution from the baseline.

A measured effect is desirable but not always required for an initial search. If the effect is expected or missing, label that limitation.

Do not search a fragment such as `uses AI to improve accuracy`. Ask what data, model, architecture, training/control step, hardware constraint, and technical effect are involved.

## Strategy by source type

| Source | Default approach |
|---|---|
| R&D update | Search query-ready candidates; ask about fragments first |
| Meeting notes | Search decisions with specific old/new technical features |
| Technical design | Search every independently query-ready candidate |
| Experiment record | Search reproducible mechanism or parameter candidates |
| Incident/fix record | Search the technical root cause and implemented remedy |

Do not impose an arbitrary maximum candidate count. Prioritize transparently if time or tool limits apply.

## Prepare one search packet per candidate

Record:

1. candidate ID;
2. technical field and intended function;
3. baseline and limitation;
4. differentiating components, steps, relationships, ranges, or conditions;
5. demonstrated or expected effect;
6. synonyms, abbreviations, translations, and entity names;
7. candidate classifications;
8. exclusions and known false positives;
9. target jurisdictions, languages, and dates;
10. confidential details omitted from external queries.

Never combine unrelated candidates into one semantic paragraph.

## Initial search

Use semantic discovery when terminology is uncertain or the contribution is best expressed as a functional combination. Use structured keyword, classification, assignee, inventor, date, jurisdiction, or legal-status filters when they improve reproducibility or precision. A robust screen may require both, plus citation and family review.

The source package's fixed semantic-only `topk: 8` setting is not a global rule. Choose result limits according to query breadth, tool constraints, and review capacity; record both requested and returned counts.

## Result review

Review enough records to support the stated screening confidence. Rank is a discovery aid, not a legal conclusion.

For each reviewed record capture:

- publication number and stable record identifier;
- title and applicant/assignee as returned;
- earliest priority and publication dates where available;
- jurisdiction and language;
- simple or extended family identity;
- relevant passages or claims, with location;
- features apparently disclosed;
- differences and unresolved interpretation;
- relevance rationale;
- review depth: bibliographic, abstract, specification, or claim-level;
- global PatSnap record link when returned;
- reviewer and review date.

Normalize families before reporting portfolio or evidence counts. State whether a number represents publications, applications, grants, simple families, extended families, or reviewed samples.

## Deeper record briefing

Use `patent_briefing` only for selected records where deeper understanding would change triage. Review the relevant specification and claims within the available evidence, but do not issue an infringement, validity, patentability, or FTO conclusion.

Escalate to a qualified patent professional when:

- a record appears to disclose the differentiating feature combination;
- claim interpretation matters;
- a filing or disclosure deadline may exist;
- ownership, inventorship, priority, or legal status affects the decision;
- the user requests a legal conclusion.

## Empty, sparse, or failed results

If few or no relevant results appear:

- record the exact search and tool response;
- broaden terminology, classifications, languages, and functional expressions where justified;
- inspect whether confidential shorthand or an over-specific query reduced recall;
- state `no close record found under the documented search`;
- retain `systematic prior-art review required`.

Never convert a zero-result search into a novelty finding.

If the connector is unavailable, do not fabricate results. Produce the extraction and follow-up sections, mark external evidence as not searched, and explain how a later search can be attached.

## Reproducibility log

| Field | Required |
|---|---|
| Search ID | Stable ID linked to candidate |
| Tool and version/schema | Current exposed connector |
| Search timestamp | Include time zone |
| Evidence cutoff | Date through which results were reviewed |
| Query | Exact text and filters |
| Strategy | Semantic, keyword, classification, citation, or combined |
| Coverage | Jurisdictions, languages, dates, source types |
| Limit / returned | Keep distinct |
| Family rule | Deduplication method |
| Reviewed set | IDs of records actually assessed |
| Limitations | Recall, truncation, translation, lag, unavailable fields |

## Multi-candidate reporting

Report candidate counts consistently:

- detected;
- query-ready;
- searched successfully;
- not searched due to missing evidence;
- search failed or incomplete;
- escalated for specialist review.

Do not say `all candidates were searched` unless the search log proves it.

## Safety and confidentiality

Obtain authorization before sending confidential technical details to an external service. Minimize query content, follow organizational data-handling rules, and do not place credentials in reports or files. Treat returned links and metadata as external evidence that still needs review.

## Language for conclusions

Use:

- `apparently discloses`;
- `relevant to feature`;
- `difference not established from reviewed material`;
- `screening signal`;
- `requires specialist review`.

Avoid:

- `blocks the invention`;
- `must design around`;
- `infringes`;
- `is valid/invalid`;
- `is novel`;
- `will be granted`.
