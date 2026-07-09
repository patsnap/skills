# Scenario: Solution Deep Dive

Use this scenario to analyze a specific technical problem, key branch, product feature, component issue, or implementation route at patent level.

## When To Use

Use when the user asks:

- What solutions exist for a key technical problem.
- How different players solve the same problem.
- Which patents represent each solution route.
- What technical effects are claimed or described.
- What product or R&D inspiration can be drawn.

## Business Questions

- Why is this technical problem important?
- What solution clusters appear in the patent set?
- Which players take which routes?
- Which representative patents are worth reading?
- What technical effects or tradeoffs matter for product planning?

## Required Inputs

| Input | Notes |
|---|---|
| `technical_problem_or_branch` | Required |
| `technology_domain` | Required |
| `selected_players` | Optional, useful for route comparison |
| `product_or_application_scope` | Optional, useful for product relevance |
| `target_count` | Suggested 3 to 10 representative families per route |

## Data And MCP Capabilities

| Task | Preferred Capability |
|---|---|
| Focused search | `search_patents` |
| Bibliographic and abstract screen | `bibliography` |
| Claims reading | `claims` or `claim_translated` |
| Description reading | `description` or `description_translated` |
| Family context | `family` |
| Citation signal | `forward_citation` |
| Legal status signal | `get_patent_legal_status` |
| Abstract image or PDF, if useful | `abstract_image`, `pdf`, `fulltext_image` |

## Analysis Flow

1. Define the technical problem in neutral terms.
2. Build a focused candidate set using technology, problem, effect, and product/scenario terms.
3. Sample titles and abstracts to remove weakly relevant records.
4. Cluster solution types by technical means.
5. Read representative claims or descriptions for each solution type.
6. Extract:
   - Problem solved.
   - Technical means.
   - Claimed or described effect.
   - Product or implementation relevance.
   - Limitations and uncertainty.
7. Compare route differences by player if player scope is selected.
8. Recommend which patent package should be read, monitored, compared, or sent for legal review.

## Report Blocks

| Block | Content |
|---|---|
| Problem framing | Why this problem matters in product or R&D terms |
| Candidate pool | Search logic, sample size, de-noising notes |
| Solution cluster overview | Main solution families |
| Problem-solution matrix | Problem, solution, effect, representative patent |
| Player route comparison | Which players use which solution routes |
| Representative patent cards | Short technical reading and why selected |
| Implications | Product, R&D, or portfolio inspiration |

## Charts And Tables

| Output | Recommended Format |
|---|---|
| Solution cluster map | Matrix or grouped table |
| Problem x solution | Matrix |
| Player x solution | Heatmap |
| Representative patents | Patent cards |
| Technical route | Timeline or flow diagram |
| Recommendation list | Table with next action |

## Patent Card Template

| Field | Content |
|---|---|
| Representative publication | `[patent_placeholder]` |
| Normalized assignee | `[assignee_group]` |
| Problem | `[technical_problem]` |
| Solution | `[technical_means]` |
| Effect | `[technical_effect]` |
| Evidence source | Abstract, claim, description, image, or family data |
| Why selected | Relevance, representativeness, citation, family, legal status, or product fit |
| Next action | Read, monitor, compare, portfolio reference, design-around review, or legal review |

## Evidence Rules

- Problem and effect should be supported by claims, description, or abstract.
- A solution cluster should include more than one record unless clearly labeled as a single notable example.
- Do not infer infringement or design-around feasibility. Use “input for later legal review” if needed.
- A representative patent can inspire R&D, but it does not prove industry-wide adoption.

## V0 Boundary

V0 can do patent-level deep reading when claims and descriptions are available.

V0 should not output:

- Claim-scope legal opinions.
- Definitive infringement or non-infringement.
- Complete design-around strategy.
- Novelty or inventiveness conclusions.

## Quality Checklist

- Technical problem is clearly defined.
- Solution clusters are mutually understandable.
- Each patent card has evidence and a recommendation reason.
- Legal language is downgraded to signal or follow-up review.
- No real confidential patent numbers or source-report examples are retained.
