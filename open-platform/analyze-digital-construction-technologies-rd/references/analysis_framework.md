# Digital Construction Analysis Framework

## Six dimensions

1. **Technology architecture** — functional stack, interfaces, maturity and subsystem relationships.
2. **Patent landscape** — families, publications, applicants, classifications, claims, citations and status context.
3. **Scientific activity** — research questions, methods, evidence maturity, institutions and translation signals.
4. **Competitive landscape** — actors, capabilities, barriers, deployment evidence and geographic reach.
5. **Translation and engineering cases** — projects, measured outcomes, implementation conditions and transfer limits.
6. **Trends and constraints** — automation, AI, digital-twin continuity, interoperability, safety, workforce and economics.

## Three-route patent search

```text
Route A: semantic
  - Describe the engineering function, mechanism or problem.
  - Use for emerging language and mechanism-led discovery.

Route B: keyword plus classification
  - Combine validated synonyms, acronyms, product terminology and IPC/CPC seeds.
  - Use for defined technology names and standards language.

Route C: entity plus date
  - Search normalized applicant/assignee names with explicit date fields.
  - Use for competitor portfolios and monitoring.
```

Validate each route with known-relevant and known-irrelevant records. Preserve exact queries, filters, tool version, run time, matched count, returned count, pagination and exclusions.

## Evidence levels

Evidence quality is multidimensional; do not infer it from source type alone.

| Level | Typical support | Appropriate use |
|---|---|---|
| A | Primary technical evidence with reproducible method or official record, directly relevant to the claim | Material factual conclusions with stated limitations |
| B | Credible patent, peer-reviewed or official evidence with partial directness or incomplete validation | Directional technical conclusions |
| C | Official vendor/project communication or reputable trade reporting | Commercial/deployment signals requiring qualification |
| D | Unverified news, exhibition material or secondary aggregation | Discovery lead only; low confidence |

Assess authority, directness, method, recency, independence and geographic applicability separately. A granted patent proves neither technical performance nor commercial deployment.

## Evidence record

Every material claim should map to:

- evidence ID;
- claim supported;
- source title, publisher and URL/identifier;
- source type and publication/access dates;
- relevant passage or structured fields;
- geography and technology scope;
- limitations and conflicts;
- analyst confidence.

## Report quality checklist

- [ ] Every material conclusion has an evidence ID.
- [ ] Patent citations use the exact returned global PatSnap URL when available.
- [ ] Counts are copied from recorded tool/export output, not typed from memory.
- [ ] Family and publication counts are clearly distinguished.
- [ ] Negative conclusions are bounded by complete documented retrieval.
- [ ] Competitor scoring has a disclosed rubric and source evidence.
- [ ] Project metrics include baseline, unit, period and measurement method.
- [ ] Vendor claims and independent evidence are labeled separately.
- [ ] Status, citations and other dynamic fields include observation dates.
- [ ] Word generation consumes reviewed structured data.

## Classification seeds

These are search starters, not an exhaustive or stable taxonomy. Confirm current IPC/CPC definitions and add technology-specific classes.

| Direction | Example seeds |
|---|---|
| Bridges and structural systems | E01D, E04B |
| Tunnels and excavation | E21D, E21B |
| Roads, paving and rail beds | E01C, E01B |
| BIM, CAD and image/geometry processing | G06F30, G06T17 and relevant current subclasses |
| Industrial or machine control | G05B, B25J |
| Measurement and monitoring | G01B, G01D and sensor-specific classes |
| AI/analytics | G06N and application-specific classes |

## Actor discovery

Do not use the source's domestic and international company lists as a fixed universe. Build the actor set from scoped evidence, then normalize subsidiaries, former names, transliterations, joint applicants and ownership changes. Include platform vendors, equipment OEMs, contractors, engineering firms, universities, public laboratories, integrators and standards bodies when relevant.

## Comparison rubric

Score only dimensions supported by evidence. Example dimensions:

- technical relevance and differentiation;
- claim/family relevance in scoped jurisdictions;
- validated deployment maturity;
- interoperability and standards participation;
- safety/cybersecurity assurance;
- ecosystem and delivery capacity;
- geographic reach;
- evidence quality and recency.

For every score provide definition, scale, evidence IDs, analyst, date, confidence and “not assessed” option. Never turn missing evidence into a low score.

## Global localization rules

- Use the terminology of the selected geography and infrastructure sector.
- Retain original-language titles/names when needed and add labeled English translations.
- Treat policies, standards, safety rules and procurement regimes as jurisdiction-specific.
- Avoid national-leadership claims without a defined metric, comparator, period and evidence.
- Treat exhibition visibility and patent filing as signals, not proof of adoption.
- Use SI units, while preserving source units and conversions.
