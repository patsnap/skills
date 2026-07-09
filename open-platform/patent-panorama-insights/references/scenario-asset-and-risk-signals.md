# Scenario: Asset And Risk Signals

Use this scenario for high-value asset clues, legal-status overview, legal-event clues, transaction clues, and follow-up review items.

## When To Use

Use when the user asks:

- Which patents may be high-value assets.
- Which patents may deserve acquisition, licensing, monitoring, or legal review.
- Whether there are transfer, license, pledge, customs, award, invalidation, or legal-event clues.
- How to summarize risk signals without giving a legal opinion.

## Business Questions

- Which patent families have stronger value signals?
- Are there small-entity, university, or non-core-owner assets worth monitoring?
- Are there legal events that require follow-up?
- Are transfers, licenses, pledges, customs, or awards visible as asset signals?
- Which items should be escalated to patent counsel or IP operations?

## Required Inputs

| Input | Notes |
|---|---|
| `candidate_pool` | Cleaned patent set or recommended package |
| `asset_goal` | Monitor, acquire, license, portfolio build, risk review, or invalidation watch |
| `legal_opinion_allowed` | Must be false for this skill |
| `review_threshold` | Optional value-signal threshold |

## Data And MCP Capabilities

| Task | Preferred Capability |
|---|---|
| Legal status | `get_patent_legal_status` |
| Legal events | `legal_data` |
| Reexamination or invalidation | `reexamination_invalidation` |
| Transfer clues | `transfer_data` |
| License clues | `license_data` |
| Pledge clues | `pledge_data` |
| Customs clues | `customs_data` |
| Award clues | `award_data` |
| Family coverage | `family` |
| Citation signal | `forward_citation` |
| Claims for follow-up scope reading | `claims` |

## Signal Types

| Signal | Meaning | Output Language |
|---|---|---|
| Legal status | Active, pending, expired, abandoned, or other simple status | Status clue only |
| Legal event | Event history requiring review | Follow-up review item |
| Reexamination or invalidation | Challenge or stability clue | Needs legal verification |
| Transfer | Ownership movement | Asset movement signal |
| License | Commercialization or access signal | Licensing clue |
| Pledge | Financing or asset-backed signal | Asset operation clue |
| Customs | Border protection clue | Enforcement-related signal |
| Award | Recognition signal | Value clue |
| Family coverage | Geographic protection breadth | Value proxy |
| Forward citation | Technical influence proxy | Value proxy |

## Analysis Flow

1. Start from a cleaned candidate pool.
2. Pull value signals:
   - Remaining term proxy.
   - Legal status.
   - Family coverage.
   - Citation count.
   - Owner type.
   - Technology centrality.
   - Product/scenario relevance.
3. Pull legal and asset-event signals where tools are available.
4. Score or bucket candidates as high, medium, or watchlist, with transparent criteria.
5. Separate business follow-up from legal follow-up.
6. Write signal language, not legal conclusions.

## Report Blocks

| Block | Content |
|---|---|
| Signal methodology | Value dimensions and available tools |
| High-value candidate table | Candidate, signal, reason, next action |
| Asset movement clues | Transfer, license, pledge, customs, award clues |
| Legal event clues | Status, events, invalidation or reexamination clues |
| Follow-up plan | Business review, technical read, legal review |
| Limitations | Missing data and non-legal-opinion statement |

## Charts And Tables

| Output | Recommended Format |
|---|---|
| Value score distribution | Bar or table |
| Candidate ranking | Table with transparent criteria |
| Signal matrix | Patent x signal type |
| Owner type split | Bar chart |
| Follow-up queue | Action table |

## Safe Language

Use:

- “legal event signal”
- “asset movement clue”
- “candidate for follow-up legal review”
- “input for later FTO or validity review”
- “worth monitoring”

Avoid:

- “infringing”
- “not infringing”
- “valid”
- “invalid”
- “free to operate”
- “SEP essential”
- “enforceable”

## V0 Boundary

V0 can identify signals if the relevant MCP tools return data.

V0 should not output:

- Legal opinions.
- Litigation strategy.
- Formal FTO or invalidity conclusion.
- Purchase or licensing decision without expert review.

## Quality Checklist

- Each signal cites the data source or capability used.
- Missing signal data is marked unavailable, not assumed absent.
- Legal conclusions are not stated.
- High-value ranking criteria are visible.
- Next actions separate business, technical, and legal review.
- No confidential source examples or real historical patent identifiers appear.
