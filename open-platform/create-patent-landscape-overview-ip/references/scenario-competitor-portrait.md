# Scenario: Competitor Patent Profile

Use this scenario to compare named organizations or build a focused patent profile for one organization within a defined technology domain.

## Use for questions such as

- What is each organization patenting in this field?
- Which branches receive sustained attention?
- Which areas appear prominent or underrepresented under the search scope?
- What do recent filings suggest about possible R&D or product direction?
- Which representative patents warrant expert reading?

## Required inputs

| Input | Requirement |
|---|---|
| `selected_organizations` | Required for a comparison |
| `technology_domain` | Required with inclusion and exclusion boundaries |
| `organization_resolution` | Parent, operating units, subsidiaries, acquired entities, and historical names |
| `include_subsidiaries` | Decide explicitly; preserve uncertain relationships as unresolved |
| `date_range`, `date_basis`, `jurisdictions` | Match the landscape comparison basis |
| `comparison_mode` | Organization versus organization, organization versus industry, or one-organization deep dive |
| `unit_of_analysis` | Define publication, application, or family counting |

## Global PatSnap capabilities

Use `advanced_patent_search` to construct comparable organization-specific result sets. Use `patent_briefing`, `deep_patent_mining`, or `global_core_patent_database` for selected-record bibliography, family, citation, claims, description, status, and event evidence when those fields are exposed by the installed connector. Confirm the live operation schema before execution; do not copy legacy source operation names into calls.

## Analysis flow

1. Build an organization-resolution table covering parent, subsidiaries, former names, acquisitions, transliterations, local-language names, and known name collisions.
2. Label uncertain aliases `to_confirm`; do not force-merge them.
3. Retrieve every organization under the same technology, period, jurisdiction, date, and unit rules.
4. Record query versions and organization-specific supplements.
5. Normalize the counting method and deduplicate consistently.
6. Compare:
   - portfolio scale and sustained activity;
   - recent trends with publication-lag handling;
   - validated technology branches;
   - products, components, applications, or effects when tagged;
   - family, citation, legal-status, or transaction signals when available; and
   - representative patent substance.
7. Select representative patents by declared criteria, not visual convenience.
8. Write bounded strategic implications and identify further evidence needed.

## Report blocks

| Block | Content |
|---|---|
| Organization scope table | Included and excluded names, relationship basis, unresolved aliases |
| Comparable KPI strip | Scale, recent activity, branch concentration, and filing coverage |
| Technology-branch profile | Areas prominent under the defined scope and possible gaps |
| Recent focus | Three-to-five-year view, adjusted for lag as appropriate |
| Product/application matrix | Only when supported by validated tags |
| Representative patent cards | Problem, solution, effect, evidence, and selection reason |
| Strategic signal summary | What the evidence supports, what remains uncertain, and follow-up |

Use comparable bars, small-multiple trend charts, organization × branch heatmaps, and aligned evidence cards. Avoid radar charts when heterogeneous metrics or arbitrary scaling would obscure comparison.

## Evidence rules

- Support a claimed strength with multiple indicators such as scale, persistence, representative technical substance, or explicitly defined family/citation signals.
- Describe a possible gap as “not prominent under the current search and classification scope,” never as proof that the organization lacks capability.
- Treat patents as evidence of disclosed technical and protection activity, not confirmation of a product launch or commercial strategy.
- Distinguish applicant identity from ultimate corporate ownership.
- Date legal and transactional events and keep them as L5 signals.
- Identify inference and uncertainty explicitly when connecting patent evidence to organizational direction.

## Quality gate

- The organization-resolution policy is reproducible.
- Every comparison uses the same period, jurisdictions, date basis, and unit.
- Uncertain aliases and corporate relationships remain visible.
- Every representative patent has a documented selection reason and traceable evidence.
- Rankings are not interpreted without considering different filing and ownership practices.
- Strategic implications use calibrated language.
- No confidential competitor set or China-only legacy assumption remains.

## Organization-resolution worksheet

| Field | Record |
|---|---|
| Canonical organization | Preferred display name and legal entity basis |
| Included names | Exact assignee names and transliterations used |
| Subsidiaries | Relationship source, effective period, and inclusion decision |
| Acquisitions | Pre/post-transaction ownership treatment |
| Joint ventures | Whether treated separately and why |
| Research partners | Kept separate from ownership unless evidence supports aggregation |
| Ambiguous names | Collision risk and `to_confirm` status |
| Query supplement | Organization-specific names added for recall |

### Comparability checks

1. Reconcile every organization set to the common domain query.
2. Apply the same deduplication and family representative rule.
3. Test whether one organization’s language or jurisdiction strategy reduces recall.
4. Separate current owner, original applicant, and corporate-group aggregation.
5. Compare both absolute activity and within-organization branch share.
6. Flag small denominators and missing years.
7. Verify that recent “focus” is not caused by incomplete earlier-name expansion.

### Calibrated language

Prefer:

- “more prominent in the retrieved and validated dataset”;
- “shows sustained patenting activity under the stated scope”;
- “recent disclosures suggest a possible emphasis on…”;
- “not prominent under the current search boundary”; and
- “requires product, corporate, or expert corroboration.”

Avoid “market leader,” “technology owner,” “has no capability,” “will launch,” or “controls the field” unless independent evidence and an appropriate method support the statement.

### Handoff artifacts

Preserve the organization-resolution table, per-organization query versions, comparable record sets, taxonomy version, reviewed representative records, and unresolved identity questions. These artifacts allow later reviewers to update a profile after a merger, rename, or data refresh without reconstructing hidden assumptions.
