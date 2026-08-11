# Patent Filing Translation — Setup and Operating Guide

This skill translates a user-supplied Chinese patent application, priority text, or invention disclosure
for EP, US, JP, or KR filing support. It preserves the supplied disclosure and produces a terminology
register plus a translation QA and risk note.

The output is a drafting aid. It is not a certified translation, legal opinion, filing instruction,
or substitute for review by qualified counsel and, where applicable, a competent translator.

## Minimum inputs

Provide the authoritative Chinese source in a stable, reviewable format and identify:

- target jurisdiction or jurisdictions;
- filing route, if known: direct, Paris Convention, PCT national/regional phase, or another route;
- priority and expected filing dates;
- application type;
- required output language;
- supplied sections and missing sections;
- approved terminology, prior translations, and drawing/sequence files;
- confidentiality and file-handling requirements.

Do not place confidential unpublished text into an unapproved connector or external service.

## Optional PatSnap MCP services

MCP connectivity is not required when the authoritative source text is supplied.

### Patent Briefing — recommended for identified publications

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use: retrieve or cross-check available bibliographic data, claims, description, family, status,
  translations, and images for an identified published patent.

### Advanced Patent Search — optional for incomplete identifiers

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use: locate the relevant publication when the user supplies an incomplete number or citation.

Treat any database translation as reference evidence only. Reconcile it against the authoritative
Chinese source before reusing terminology.

## Connector setup

1. Create or use an authorized account at https://open.patsnap.com.
2. Open the relevant marketplace page above.
3. Copy the published connector URL and insert the user’s own API key through the client’s secure
   credential mechanism.
4. Add the connector to the supported agent client.
5. Confirm the exact connector key and live tool schema in the client before use.

Never hard-code an API key in this package, a prompt, a report, or a log.
If a connector is unavailable, work from the supplied source and label unavailable database checks.

## Recommended working structure

```text
project-name/
├─ 01_chinese_source/
├─ 02_terminology/
├─ 03_europe_ep_english/
├─ 04_united_states_us_english/
├─ 05_japan_jp_japanese/
├─ 06_korea_kr_korean/
└─ 07_translation_qa/
```

Preserve immutable source copies. Put each destination draft in its own folder and keep a revision log.

## Required review before filing

- reconcile every claim number and dependency;
- verify consistent terminology across claims, description, abstract, drawings, and sequences;
- inspect open/closed transitions, optionality, order, ranges, units, formulas, and reference signs;
- resolve every flagged source ambiguity with the applicant or inventor;
- verify current filing-route, language, form, deadline, sequence-listing, and certification requirements
  using the relevant official authority;
- obtain destination-counsel and translator review appropriate to the matter.

## Supported destination references

- Europe: `references/europe.md`
- United States: `references/united-states.md`
- Japan: `references/japan.md`
- Korea: `references/korea.md`

Load only the references for the requested destinations.
