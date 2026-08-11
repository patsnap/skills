# Patent Family and Continuity Consolidation

## Purpose

Group related records for navigation and counting without erasing jurisdiction-specific rights, claim versions, continuity relationships, or legal status. A family is an analytical container, not one worldwide patent.

## When to consolidate

Normalize exact publications first. Expand priority, family, continuity, and national-stage relationships before final claim screening. Jurisdiction filters may guide risk analysis, but do not discard non-target members needed to understand priority, prosecution, claim evolution, ownership, or future national-stage risk.

## Family definitions

Record the provider and definition used:

- simple family;
- INPADOC/extended family;
- domestic family;
- custom priority-connected group;
- US continuity chain;
- PCT-to-national-stage group;
- EP application/grant/validation/unitary group.

Do not use earliest priority number alone as an undocumented family identifier. Different provider algorithms can group records differently.

## Data retrieval

For every material publication/application/grant, retrieve where available:

- publication, application, grant, and priority identifiers;
- country/office and kind code;
- title, applicant, assignee, inventors;
- filing, priority, publication, grant, and event dates;
- parent/child/continuation/divisional/CIP/reissue relations;
- PCT international application and national stages;
- EP validation/unitary status and designated/validated states;
- family IDs under the named definition;
- current claims and material historical claim versions;
- legal status, maintenance, lapse/restoration, opposition, limitation, revocation, post-grant proceedings;
- assignments/licenses where available;
- ordinary term and extensions/disclaimers.

Use `patent_briefing` for family/bibliography/status/claims discovery where available. Verify material status, term, and proceedings in the relevant official register.

## Member model

```json
{
  "family_group_id": "provider-or-controlled-id",
  "family_definition": "INPADOC extended family",
  "family_provider": "PatSnap",
  "earliest_priority": {
    "date": "YYYY-MM-DD",
    "application_number": "...",
    "verified": false
  },
  "members": [
    {
      "publication_number": "EP...B1",
      "application_number": "EP...",
      "grant_number": "EP...",
      "office": "EP",
      "kind_code": "B1",
      "relationship": "PCT national/regional phase",
      "target_territories": ["DE", "FR"],
      "claim_version": {
        "type": "granted",
        "event_date": "YYYY-MM-DD",
        "source": "official register or document URL"
      },
      "legal_status": {
        "normalized": "active|pending|lapsed|revoked|expired|unknown",
        "event": "...",
        "effective_date": "YYYY-MM-DD",
        "source": "...",
        "retrieved_at": "YYYY-MM-DDThh:mm:ssZ",
        "confidence": "high|medium|low"
      },
      "term": {
        "estimated_ordinary_expiry": "YYYY-MM-DD|null",
        "verified_expiry": "YYYY-MM-DD|null",
        "adjustments": ["PTA", "PTE", "SPC", "terminal disclaimer"],
        "notes": ""
      },
      "source_modules": ["M1", "M2"],
      "query_ids": ["SEQ-01", "Q-14"]
    }
  ]
}
```

Use `null`, `unknown`, and `not applicable` correctly. Do not use a dash that loses meaning in machine-readable artifacts.

## Granted and pending text

### Granted claims

Retrieve the claims currently in force after any correction, reissue, disclaimer, opposition, limitation, reexamination, post-grant amendment, or court effect. A B1/B2 kind code is a useful document clue, but does not by itself prove current enforceability or final claim text.

### Pending claims

Retrieve the latest publicly available claim set and identify its prosecution event/date. Pending claims may change and are not presently enforceable, but can be material to future launch risk.

### Multiple target jurisdictions

There is no single representative claim that substitutes for all countries. Select a display representative only for navigation; the risk analysis must use the controlling member/claim/version for each target jurisdiction.

## Representative-record selection

For a compact family table, choose a representative using this order:

1. target-jurisdiction member with a verified, controlling granted claim;
2. target-jurisdiction pending member with latest public claim set;
3. international/earliest publication for technical context;
4. another member only with an explicit reason.

Store `representative_reason`. Do not globally prefer EP grants or the earliest grant when the target country differs.

## US continuity

Preserve application-by-application relationships:

- continuation;
- divisional;
- continuation-in-part;
- national stage;
- bypass continuation;
- reissue;
- provisional/nonprovisional priority;
- terminal disclaimer and patent-term relationships.

Related US applications can contain materially different claims. Never collapse them into one claim set.

## PCT handling

- WO/PCT publication supports family discovery and future monitoring.
- It is not an enforceable global right.
- Record priority date, international filing/publication, Chapter II events where relevant, national-stage deadline assumptions, and confirmed national entries.
- Do not call a normal national-stage period a “PCT risk exemption” or infer non-entry until official evidence and deadlines support it.
- Schedule monitoring where a national-stage decision remains unobservable.

## EP handling

For EP matters, record:

- application and grant;
- opposition/appeal/limitation/revocation status;
- Unitary Patent effect where applicable;
- validated states and national status;
- translations/fees/renewals where relevant;
- SPC or pediatric extensions by country;
- UPC opt-out and litigation context if material and verifiable.

An EP grant does not create identical live rights in every EPC state indefinitely.

## Legal-status categories

Normalize for sorting, but retain raw events:

- `pending`;
- `granted_active`;
- `granted_lapsed_or_expired`;
- `abandoned_or_withdrawn`;
- `revoked_or_cancelled`;
- `unknown_or_conflicting`.

For each material conclusion, cite the raw official event, effective date, retrieval time, and source. Database status can be stale or aggregated.

## Term analysis

Do not calculate expiry as “priority date + 20 years” without qualification. Consider:

- governing filing date and transitional law;
- claimed priority versus effective filing;
- maintenance/renewal fees and restoration;
- US PTA, PTE, terminal disclaimer, reissue, and litigation effects;
- SPC/supplementary certificates and pediatric extensions;
- national patent term extension;
- disclaimers, limitation, revocation, or surrender;
- claim-specific and country-specific effects.

Store both estimated ordinary term and verified adjusted term, with formula, source, and uncertainty.

## Family-level roll-up

Allowed roll-up fields:

- highest review priority among target members;
- target jurisdictions with live/pending material claims;
- next expiry/monitoring/prosecution event;
- unresolved status/claim gaps;
- source-module coverage.

Never state “the family infringes,” “the family is active,” or “the family expires on X” without member-level qualification.

## Sorting and display

Within a family:

1. target-jurisdiction critical/high-review members;
2. other target-jurisdiction granted members;
3. target-jurisdiction pending members;
4. related technical/context members;
5. historical/expired members.

Then sort by jurisdiction and relevant event date. Use text labels with color only as a secondary cue.

## Consolidation effects on review

- Multiple module hits increase discovery confidence, not claim scope.
- A live material member keeps the family in the target-country queue.
- Expiry/lapse of one member does not resolve another member.
- A pending branch remains monitored even when an earlier grant is irrelevant.
- An owned/licensed member is resolved only after ownership/license scope is verified.
- An inactive foundational record may remain as continuity/prosecution evidence.

## Quality checklist

- [ ] Family definition and provider are recorded.
- [ ] Exact publications are deduplicated without erasing source provenance.
- [ ] Application, publication, grant, and jurisdictional members remain distinct.
- [ ] Priority and continuity relationships are evidence-backed.
- [ ] US continuations/divisionals/CIPs/reissues are not collapsed.
- [ ] WO/PCT is not treated as an enforceable territory.
- [ ] EP validation/unitary/national status is resolved where material.
- [ ] Granted and latest pending claim versions are preserved.
- [ ] Material status is verified in official registers or marked unresolved.
- [ ] Term estimates disclose adjustments and uncertainty.
- [ ] Representative claims are used only for display, not cross-country substitution.
- [ ] Family-level priority reconciles to member-level evidence.
