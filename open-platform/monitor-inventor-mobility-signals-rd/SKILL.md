---
copyright: "Copyright © Patsnap. All rights reserved."
name: monitor-inventor-mobility-signals-rd
description: Monitor public patent records for inventor identity, organizational-association and technical-adjacency signals that merit qualified review. Use when an authorized IP or R&D team asks to screen a company or named inventors over a defined period and produce an evidence-backed HTML briefing; never infer resignation, employment, misconduct or legal risk from patent records alone.
---

# Monitor Inventor Mobility Signals

## Purpose

Help authorized global IP and R&D teams identify public patent-record changes that may justify human review. Preserve the source's organization mode, named-inventor mode, inactivity window, later-patent search, technical comparison and HTML report, while correcting the central inference: patent records do not establish employment or resignation.

## Required safeguards

- Confirm a legitimate purpose and applicable privacy, employment, works-council, discrimination and monitoring requirements.
- Minimize personal data, restrict access and define retention/deletion.
- Use public professional evidence only when necessary and lawful.
- Do not make or recommend automated adverse decisions about a person.
- Do not present review priority as misconduct, leakage, ownership, FTO or legal risk.
- Require qualified IP/legal and, where relevant, HR/employment review for material decisions.

If these safeguards cannot be met, stop person-level monitoring and provide only aggregated portfolio analysis.

## Inputs

| Input | Required | Meaning |
|---|---|---|
| `company_name` | One of company/inventors | Normalized focal organization plus known aliases/subsidiaries |
| `inventor_names` | One of company/inventors | Names exactly as supplied; identity remains unresolved initially |
| `tech_domain` | Recommended | Scoped functions, mechanisms, applications and exclusions |
| `inactive_years` | Optional screening parameter | Lookback used to identify a filing-inactivity signal, not departure |
| `monitor_start`, `monitor_end` | Required | Explicit monitoring window and date semantics |
| jurisdictions/languages | Required | Search and legal/privacy scope |
| cutoff date | Required | Latest evidence included |
| counting unit | Required | Publication, application or family and deduplication rule |
| output language | Optional | Default English; retain original titles with labeled translations when needed |

## MCP and evidence plan

User-supplied reviewed exports require no MCP. For a requested live search, verified global Patsnap support is:

| Task | MCP | Marketplace page |
|---|---|---|
| Applicant/inventor/field/date patent discovery | `advanced_patent_search` | https://open.patsnap.com/marketplace/mcp-servers/patent-search |
| Bibliography, family, claims, description and status context | `patent_briefing` | https://open.patsnap.com/marketplace/mcp-servers/patent-briefing |

Use only tools actually exposed and authorized. Preserve exact returned global Patsnap URLs; do not construct record URLs. Record the query, filters, date fields, tool response counts, pagination and known coverage limits.

## Method

### 1. Define and authorize

Document decision, users, legitimate purpose, jurisdictions, personal-data controls, technology scope, organization aliases, date fields, cutoff, family/counting rule and reporting cadence.

### 2. Build the focal portfolio

Retrieve the focal organization's scoped patent corpus using normalized names and relevant languages. Paginate to the documented boundary. Extract inventor strings, dates, applicants, families, classifications, technical content and source URLs.

### 3. Detect filing-inactivity signals

Calculate the last visible relevant filing date for each inventor identity candidate. Call this a filing-inactivity signal, never “suspected resignation.” Explain that the signal may arise from publication lag, role/project changes, spelling variants, entity changes, incomplete coverage or patenting strategy.

Do not use only a calendar year if exact dates exist. Test whether alternative lookback windows materially change the screened set.

### 4. Resolve identity

Names alone are insufficient. Compare spelling/transliteration, co-inventors, applicants, addresses/geography, technical topics, classifications and chronology. Assign:

- `resolved`;
- `probable`;
- `ambiguous`;
- `unresolved`.

Keep conflicting identities separate. An unresolved identity cannot support person-level priority conclusions.

### 5. Search later public records

Retrieve later records for each candidate across scoped jurisdictions. Separate records at the focal organization, apparently different organizations, collaborations and uncertain relationships. A different applicant does not prove employment at that applicant.

### 6. Compare technical content

Assess claim-relevant functions, mechanisms, architectures, components, materials, applications and chronology. IPC/CPC and keyword similarity are screening features only. Include supporting evidence, counterevidence and alternative explanations.

### 7. Assign review priority

Use four evidence labels:

| Label | Use |
|---|---|
| `priority_review` | Supported identity plus multiple direct technical signals requiring prompt qualified review |
| `review` | Some direct adjacency but meaningful uncertainty remains |
| `watch` | Weak/indirect signal suitable for proportional re-checking |
| `insufficient_evidence` | Identity, retrieval or technical evidence cannot support a priority |

Never use `low risk` for “no result”: recent applications may be unpublished and retrieval may be incomplete. Do not translate the labels into probability or legal conclusions.

### 8. Generate and review report

Populate `references/data_schema.json`. Run:

```text
python scripts/generate_report.py --data reviewed-data.json --output inventor-mobility-signals.html
```

The report generator escapes supplied content, checks dates/levels/counts and refuses overwrite by default. Review the HTML, sources and identity decisions before distribution.

## Output contract

The briefing contains:

1. purpose, scope, jurisdictions, cutoff and coverage;
2. prominent non-employment/non-legal disclaimer;
3. counts by review priority;
4. identity status and rationale for each reviewed person;
5. focal and later public patent evidence with exact source URLs;
6. counterevidence, uncertainty and recommended qualified review;
7. methodology and publication-lag limitations.

Do not expose unnecessary home addresses, personal contact details, protected characteristics or unrelated personal information.

## Publication lag and zero results

Patent applications are often published around 18 months after filing, subject to jurisdiction, procedural choices and exceptions. State this as an approximate structural limitation, not a guarantee. A zero result means only that no matching public record was identified within the documented corpus and cutoff.

## Detailed workflow

Read `references/workflow.md` before execution. It is the operational authority for identity resolution, technical adjacency, evidence labels, report generation and review controls.

## Quality gates

- [ ] Authorization, legitimate purpose, access and retention are documented.
- [ ] Company aliases, date fields, jurisdictions and technology scope are explicit.
- [ ] Search coverage and pagination are recorded.
- [ ] Identity is supported by more than a name match.
- [ ] Inactivity is not called resignation or employment change.
- [ ] Different applicant is not called new employer.
- [ ] IPC/keyword overlap is not called legal or technical risk.
- [ ] Claims/functions/mechanisms, counterevidence and chronology are reviewed.
- [ ] Recent-publication blind spot is visible.
- [ ] No-result cases use `insufficient_evidence`, not low risk.
- [ ] Exact returned Patsnap URLs are preserved.
- [ ] HTML input is schema-checked and escaped.
- [ ] Qualified reviewers own material decisions.

## Boundaries

This skill produces public-record research signals. It does not determine employment, resignation, identity with certainty, trade-secret use, inventorship correctness, patent ownership, contract breach, competitive harm or legal risk. It must not be used for employee scoring, surveillance or adverse employment action.
