# Scenario: Competitor Portrait

Use this scenario to analyze selected applicants, competitor groups, or key players in a technology domain.

## When To Use

Use when the user asks:

- What selected players are doing in a technology field.
- Which branches each player emphasizes.
- Whether a player has strengths, weak areas, or emerging focus.
- How recent patents may indicate product, R&D, or portfolio direction.
- How players compare with the broader industry.

## Business Questions

- Which players are most active and in which branches?
- Are the selected players continuously investing or only filing sporadically?
- Which branches look like strengths or gaps for each player?
- Which product, component, scenario, or technical-effect signals appear recently?
- Which representative patents deserve manual reading?

## Required Inputs

| Input | Notes |
|---|---|
| `selected_players` | Required for competitor portraits |
| `assignee_expansion_required` | Default true |
| `include_subsidiaries` | Default true, mark uncertain relations |
| `technology_domain` | Required |
| `date_range` | Use same scope as landscape |
| `comparison_mode` | Player vs player, player vs industry, or player deep dive |

## Data And MCP Capabilities

| Task | Preferred Capability |
|---|---|
| Player patent set | `search_patents` |
| Bibliographic details | `bibliography` |
| Family and jurisdiction layout | `family` |
| Citation signal | `forward_citation` |
| Legal status signal | `get_patent_legal_status` |
| Claims and description for representative patents | `claims`, `description` |
| Transfer, license, pledge, customs, award clues | `transfer_data`, `license_data`, `pledge_data`, `customs_data`, `award_data` |

## Analysis Flow

1. Expand player names:
   - Parent company.
   - Subsidiaries.
   - Historical names.
   - Acquired entities.
   - Local-language aliases.
2. Mark uncertain aliases as `to_confirm` rather than force-merging.
3. Pull each player set under the same technology and time scope.
4. Normalize counting method across players.
5. Compare:
   - Total scale.
   - Recent trend.
   - Technology branch distribution.
   - Product/component/scenario tags if available.
   - Forward citation or family coverage signals.
   - Legal or asset signals.
6. Select representative patents for each player.
7. Write cautious strategic implications.

## Report Blocks

| Block | Content |
|---|---|
| Player scope table | Included aliases, excluded aliases, uncertainty |
| Player KPI cards | Scale, recent filings, branch concentration, active jurisdictions |
| Technology branch distribution | Strengths and gaps |
| Recent focus | Last 3 to 5 years by branch or product scenario |
| Product/scenario matrix | Product or component relevance, if tagged |
| Representative patent cards | Problem, solution, effect, why it matters |
| Strategic signal summary | What the evidence may imply |

## Charts And Tables

| Output | Recommended Format |
|---|---|
| Player ranking | Bar chart |
| Player trend | Small multiple lines |
| Player x branch | Heatmap |
| Player x product/scenario | Matrix |
| Recent focus | Stacked bar or heatmap |
| Representative patents | Comparable patent cards |
| Assignee normalization | Appendix table |

## Evidence Rules

- A player strength should be supported by scale, sustained activity, citation/family/legal signal, or representative patent quality.
- A player gap should be framed as “not prominent under current search scope”, not as absence of capability.
- Product direction predictions must cite recent patents, product/scenario tags, or public product context if used.
- Legal and asset events are signals only.

## V0 Boundary

V0 can support assignee-normalized comparison, simple portfolio portrait, and representative patent reading.

Be careful with:

- Subsidiary and acquisition ambiguity.
- Different filing strategies across jurisdictions.
- Over-reading patents as product launch certainty.
- Missing data if selected players use unusual assignee names.

## Quality Checklist

- Assignee expansion rules are documented.
- All player comparisons use the same date, geography, and counting method.
- Uncertain aliases are not silently merged.
- Player predictions use cautious language.
- Each recommended representative patent has a reason.
- No real confidential competitor set from source materials is retained as an example.
