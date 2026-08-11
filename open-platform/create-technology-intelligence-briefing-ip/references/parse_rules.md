# Request parsing rules

## Goal

Convert a natural-language request into an explicit, reviewable research scope. Never hide a consequential assumption.

## Input patterns

Accept any combination of:

- company only: “Brief Acme’s solid-state-battery activity”;
- topic only: “Brief direct-air-capture technology”;
- company plus topic: “Compare Acme and Example Corp in silicon photonics”;
- topic plus market: “Hydrogen electrolyzers for the EU market”;
- explicit period: “from 2024-01-01 through 2025-12-31”;
- relative period: “the last six complete months”; or
- explicit patent, literature, or news constraints.

## Normalized scope

Create this structure before retrieval:

```yaml
research_question: ""
decision_context: ""
companies: []
entity_scope: pending
technology:
  core_concept: ""
  inclusions: []
  exclusions: []
patents:
  jurisdictions: []
  geographic_markets: []
  date_field: priority|filing|publication|grant
  start_date: YYYY-MM-DD
  end_date: YYYY-MM-DD
  document_types: []
  languages: [en]
  counting_unit: publication|application|simple_family|extended_family
  deduplication_rule: ""
  display_limit: null
literature:
  sources: []
  document_types: []
  start_date: YYYY-MM-DD
  end_date: YYYY-MM-DD
  display_limit: null
news:
  start_date: YYYY-MM-DD
  end_date: YYYY-MM-DD
  source_policy: primary_first
evidence_cutoff: YYYY-MM-DD
output_path: ""
assumptions: []
pending_confirmations: []
```

## Date handling

- Resolve relative dates to exact ISO 8601 dates and record the resolution date.
- “Last six months” means the six-month interval ending on the evidence cutoff unless the user says “complete calendar months.”
- Do not substitute a fixed period.
- Identify partial years in trend charts.
- Use publication date for public-availability analysis unless another field is explicitly required.

## Jurisdiction and geography

Patent jurisdiction is not the same as commercial geography. Record both when relevant.

- `jurisdictions` controls patent authorities/documents searched.
- `geographic_markets` controls the commercial or policy context.
- Do not default to CN, US, EP, JP, or KR as a mandatory set.
- If the user gives no jurisdiction and the request is exploratory, use a global scope only after stating what the connector’s “global” coverage means.
- WIPO/PCT publications are not a grant jurisdiction.

## Company handling

- Keep the user’s string as `input_name`.
- Resolve legal entities separately.
- Do not treat a brand as an assignee.
- Do not combine parent and subsidiaries without a recorded scope decision.
- If the alias reference marks a group as mixed, require selection before live retrieval.

## Technology handling

- Preserve the user’s wording.
- Add English synonyms and relevant local-language terms only when needed for recall.
- Validate acronyms because many are ambiguous.
- Record excluded meanings and noise terms.
- Treat classifications as retrieval aids, not definitions of the technology.

## Defaults

Use defaults only when they do not materially change the decision:

| Field | Default | Required disclosure |
|---|---|---|
| Interface/report language | English | State `en` |
| Evidence cutoff | Current date | Record exact date |
| News source policy | Primary sources first | List exceptions |
| Display selection | Relevance-based representative set | State method and limit |
| Unknown section | `not_executed` | State reason |

Do not default the patent counting unit, family rule, date field, or legal-entity scope silently.

## Confirmation gate

Seek confirmation when any of these remains material:

- similarly named companies;
- parent-versus-subsidiary coverage;
- technology boundary with a likely order-of-magnitude count effect;
- jurisdiction or date-field choice tied to a legal/business decision;
- population counting unit;
- confidential or access-restricted inputs; or
- intended use that could be mistaken for legal, investment, or regulatory advice.

Otherwise proceed with a clearly logged assumption and offer the user a correction point.

## Parse QA

- Dates are valid and ordered.
- Jurisdictions and markets are not conflated.
- Company scope is not inferred from brand recognition.
- Technology inclusions and exclusions are explicit.
- Population and display settings are distinct.
- Every default is visible in the trace.
