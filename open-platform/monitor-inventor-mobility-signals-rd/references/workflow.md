# Inventor Mobility Signals — Complete Workflow

## Purpose and boundary

This workflow identifies public patent-record signals that may justify human review of inventor identity, organizational association and technical adjacency. It does not determine employment status, resignation, movement dates, ownership, confidentiality breach, non-compete status, misconduct or legal risk.

Use only for a legitimate organizational purpose, the minimum necessary personal data and applicable privacy, employment, works-council, discrimination and monitoring requirements. Do not create automated adverse employment decisions or covert surveillance.

## Two stages

1. **Evidence collection and review** — retrieve scoped patent records, normalize organizations/families and resolve inventor identities.
2. **Report generation** — validate reviewed JSON and render a static, escaped HTML briefing.

## Stage 1 — Evidence collection

### Step 0: authorize and define scope

Record the decision, lawful/legitimate purpose, users, retention/access controls, focal organization, jurisdictions, date fields, cutoff date, technology definition, languages, family/counting unit and review cadence. A supplied inventor list must be handled under the same controls.

### Step 1: build the focal-organization corpus

Use `advanced_patent_search` only when live PatSnap search is requested and authorized:

https://open.patsnap.com/marketplace/mcp-servers/patent-search

Search normalized applicant/assignee names, subsidiaries, former names, transliterations and relevant dates. Paginate to the stated coverage limit and save the query log. Use `patent_briefing` for record, family, bibliography and claim/description context when needed:

https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Extract inventor names exactly as published, publication/application numbers, earliest priority, filing/publication dates, applicants, family identifiers, classifications, technical text and returned global URLs.

### Step 2: identify inactivity signals, not departures

An absence of later visible filings for the focal organization is only an inactivity signal. It may reflect publication lag, role changes, name variants, entity changes, patenting strategy, project timing, incomplete coverage or no invention activity. Use exact dates where available; never infer a resignation year from the last patent filing.

The source's `inactive_years` threshold may be used as a transparent screening parameter, but not as a fact classifier. Report sensitivity to alternative windows when it affects the list.

### Step 3: resolve inventor identity

For each candidate, compare:

- full name and spelling/transliteration variants;
- co-inventor network;
- applicant/assignee and address/geography;
- technical topics, classifications and chronology;
- cited/citing or family context where useful;
- public professional evidence only when lawful, necessary and sourced.

Assign `resolved`, `probable`, `ambiguous` or `unresolved`. Do not merge records solely by name. Exclude or quarantine ambiguous records from person-level conclusions.

### Step 4: retrieve later public patents

Search each identity candidate across the monitoring window and relevant jurisdictions. Do not filter only by focal keywords before establishing identity, because that can hide counterevidence and bias similarity. Separate:

- later records at the focal organization;
- records at apparently different organizations;
- joint/academic/collaborative records;
- uncertain applicant relationships;
- records outside the scoped technology.

Organization difference in a patent record does not establish current employment.

### Step 5: assess technical adjacency

Compare claim-relevant functions, problems, mechanisms, architectures, components, materials and applications. IPC/CPC overlap and keyword overlap are discovery features, not a legal or technical conclusion. Record both supporting and counterevidence.

Use the following triage labels:

| Label | Meaning |
|---|---|
| Priority review | Identity is sufficiently supported and multiple direct technical signals merit prompt qualified review. |
| Review | Some direct adjacency exists, but evidence, identity or scope remains incomplete. |
| Watch | Weak/indirect signal suitable only for periodic re-checking. |
| Insufficient evidence | Identity unresolved, retrieval incomplete, no visible record, or evidence cannot support a level. |

These are review priorities, not risk scores and not findings of wrongdoing. Never label “low risk” merely because no publication was found.

### Step 6: qualified review

IP counsel or another qualified reviewer should independently assess material claim scope, ownership/assignment, contracts, jurisdiction and official records. HR/employment specialists must handle any employment inference. The monitoring report itself must not recommend action against an individual.

## Stage 2 — Report generation

Prepare JSON conforming to `references/data_schema.json`, then run:

```text
python scripts/generate_report.py --data reviewed-data.json --output inventor-mobility-signals.html
```

The generator validates key fields, recomputes summary counts, escapes all untrusted content and refuses overwrite unless `--force` is supplied.

## Review checklist

- [ ] Legitimate purpose, access, retention and regional privacy/employment review documented.
- [ ] Search queries, variants, cutoff, date fields, pagination and coverage recorded.
- [ ] Publication lag and unavailable records are visible.
- [ ] Organization and family/entity normalization reviewed.
- [ ] Person identity is not based on name alone.
- [ ] Employment or resignation is not inferred from patent records.
- [ ] Technical adjacency uses claim/function/mechanism evidence, not IPC/keywords alone.
- [ ] Triage labels are review priorities, not legal risk.
- [ ] Counterevidence and unresolved identities remain visible.
- [ ] PatSnap links are exact returned global URLs.
- [ ] HTML contains escaped content and a prominent limitations notice.

## Cadence

Choose cadence based on decision need, publication lag and proportionality. The source suggested quarterly monitoring, but quarterly is not a universal default. Recheck material records after publication-lag windows and when new evidence appears.
