# Organization Mapping and OLED Seed Universe

Use this reference to build an evidence-backed organization universe. The listed OLED organizations preserve the source example in globally recognizable English, but they are not a current ranking, exhaustive landscape, or automatic competitor set.

## Entity-governance rules

1. Assign a stable internal organization ID.
2. Preserve the legal or source-reported name.
3. Store aliases separately from the display name.
4. Distinguish parent, subsidiary, business unit, joint venture, brand, and research organization.
5. Record source IDs and dates for inclusion.
6. Separate direct competitors, suppliers, customers, research actors, entrants, and adjacent players.
7. Never infer headquarters, ownership, market participation, or competitive tier from a name alone.
8. Review merger, rename, and ownership changes at every refresh.
9. Generate slugs from stable IDs; do not use source filenames as identity evidence.
10. Resolve collisions explicitly.

## Required organization fields

| Field | Requirement |
|---|---|
| `id` | Stable ASCII identifier |
| `display_name` | Reviewed English display name |
| `legal_name` | Legal name when established |
| `aliases` | Names, abbreviations, translations, former names |
| `entity_type` | Company, business unit, university, institute, consortium, other |
| `value_chain_roles` | Reviewed role list |
| `geographies` | Relevant operating geographies, not assumptions |
| `inclusion_rationale` | Why the entity is in scope |
| `evidence_ids` | Supporting records |
| `first_evidence_date` | Earliest in-scope evidence date |
| `last_evidence_date` | Latest in-scope evidence date |
| `review_status` | Seed, checked, corroborated, or excluded |
| `confidence` | High, medium, or low with rationale |
| `relationship_notes` | Parent/subsidiary/JV/rename caveats |

## OLED seed organizations from the source package

These names are preserved only as a discovery seed. Confirm scope, entity identity, role, and current relevance from dated sources before publication.

| Seed ID | English display name | Source abbreviation | Review state |
|---|---|---|---|
| `samsung-display` | Samsung Display | SDC | Seed — evidence required |
| `lg-display` | LG Display | LGD | Seed — evidence required |
| `boe-technology` | BOE Technology Group | BOE | Seed — evidence required |
| `tcl-csot` | TCL China Star Optoelectronics Technology | CSOT | Seed — evidence required |
| `visionox` | Visionox | VNX | Seed — evidence required |
| `tianma` | Tianma Microelectronics | TM | Seed — evidence required |
| `everdisplay-optronics` | Everdisplay Optronics | EDO | Seed — evidence required |
| `sharp` | Sharp | SHARP | Seed — evidence required |
| `japan-display` | Japan Display | JDI | Seed — evidence required |
| `infovision-optoelectronics` | InfoVision Optoelectronics | IVO | Seed — evidence required |
| `auo` | AUO | AUO | Seed — evidence required |
| `innolux` | Innolux | INX | Seed — evidence required |

Names and abbreviations should be checked against the organization's current preferred English usage and the returned evidence. Do not preserve the source's inconsistent filename abbreviations as canonical identity.

## Example reviewed JSON record

```json
{
  "id": "example-display-company",
  "display_name": "Example Display Company",
  "legal_name": "Example Display Company Ltd.",
  "aliases": ["EDC"],
  "entity_type": "company",
  "value_chain_roles": ["panel manufacturer"],
  "geographies": ["Global"],
  "inclusion_rationale": "Named in reviewed route and investment records E014 and E028.",
  "evidence_ids": ["E014", "E028"],
  "first_evidence_date": "2025-02-18",
  "last_evidence_date": "2026-05-03",
  "review_status": "corroborated",
  "confidence": "medium",
  "relationship_notes": "Corporate relationship requires refresh at next cutoff.",
  "summary": "Evidence-linked summary, not a leadership claim.",
  "technology_ids": ["tandem-oled"],
  "record_ids": ["E014", "E028"],
  "patent_ids": ["P006"]
}
```

## Alias normalization

Normalize case, surrounding punctuation, common corporate suffixes, and documented abbreviations for matching, but preserve the original source string. Do not automatically remove words that distinguish subsidiaries or business units.

Match in this order:

1. stable provider/entity identifier;
2. exact reviewed legal name;
3. exact alias scoped by geography and entity type;
4. manually reviewed fuzzy candidate.

Never merge solely on acronym, transliteration, domain name, or shared parent.

## Relationship handling

Use explicit relationships:

- `parent_of`;
- `subsidiary_of`;
- `business_unit_of`;
- `joint_venture_with`;
- `formerly_named`;
- `acquired_by`;
- `brand_of`;
- `unresolved_relationship`.

Attach an evidence ID, effective date, and review status. Do not rewrite historical records to a current name without retaining the name used at the event date.

## Inclusion and exclusion

Include an organization when evidence shows material relevance to the scoped technology and decision. Exclude or demote when:

- it appears only through an ambiguous name match;
- it is mentioned as a customer or supplier but the portal scope is direct competitors;
- evidence is outside the period or geography and no historical context is needed;
- the record duplicates a parent/subsidiary already counted under the declared unit;
- the source is promotional and uncorroborated for a material claim.

Record exclusions and reasons; absence from the portal is not evidence of inactivity.

## Page rendering

The renderer creates `company-{safe-slug}.html` from `id`. A safe slug contains lowercase ASCII letters, digits, and hyphens, cannot be empty, cannot contain `..`, path separators, or a reserved filename, and must be unique after normalization.

Company cards and pages show:

- display name and role;
- inclusion rationale;
- evidence coverage dates;
- associated technology routes;
- dated current-awareness and event records;
- associated patent evidence under the declared count unit;
- missing evidence and confidence;
- no fake link when a source URL is absent.

## Refresh checks

At each portal refresh verify legal/display names, relationships, business status, route relevance, latest evidence date, stale pages, aliases, and slug collisions. Keep prior evidence and effective dates for auditability.
