# Scenario: Technology Evolution

Use this scenario to turn patent records into a technology taxonomy, route evolution view, key problem map, and future-direction hypotheses.

## When To Use

Use when the user asks:

- How a technology route has evolved.
- Which technical branches or sub-routes are rising.
- Which problems the industry is trying to solve.
- Which future R&D directions are suggested by patent signals.
- How to connect patent signals to product or technical planning.

## Business Questions

- What are the main technology branches?
- Which branches show recent growth or renewed attention?
- What technical problems are repeatedly addressed?
- What solution clusters appear in representative patents?
- Which future directions are evidence-backed enough to monitor or explore?

## Required Inputs

| Input | Notes |
|---|---|
| `technology_domain` | Required |
| `known_branches` | Optional customer-provided taxonomy |
| `product_or_application_scope` | Useful for product planning |
| `date_range` | Prefer earliest priority date for evolution |
| `depth` | `landscape` for branch-level, `deep_dive` for route-level |

## Data And MCP Capabilities

| Task | Preferred Capability |
|---|---|
| Branch candidate search | `search_patents` |
| Bibliographic fields and abstracts | `bibliography` |
| Claims for route confirmation | `claims` or `claim_translated` |
| Description for problem-solution reading | `description` or `description_translated` |
| Family context | `family` |
| Citation signal | `forward_citation` |

Use claims and descriptions selectively. Do not call full text for all records unless the dataset is tiny.

## Analysis Flow

1. Draft a three-level taxonomy:
   - Level 1: major technology category.
   - Level 2: technology branch or function module.
   - Level 3: specific method, scenario, component, problem, or effect.
2. Map search rules to preliminary branch labels.
3. Sample each branch to verify relevance and noise.
4. Generate time x branch trend.
5. Select branches for deep reading based on growth, concentration, customer relevance, and representative patents.
6. Extract technical problems, solution types, and effects from representative records.
7. Build route evolution hypotheses with uncertainty labels.

## Report Blocks

| Block | Content |
|---|---|
| Technology taxonomy | Level 1 to Level 3 definitions and boundaries |
| Branch trend | Time x branch movement |
| Problem map | Key technical problems and frequency signals |
| Solution route map | Solution clusters and representative patents |
| Technology evolution timeline | Route shifts over time |
| Future direction hypotheses | Evidence-backed and uncertainty-labeled |

## Charts And Tables

| Output | Recommended Format |
|---|---|
| Taxonomy | Hierarchical table |
| Branch trend | Stacked bar, heatmap, or small multiples |
| Time x branch | Heatmap |
| Problem x solution | Matrix |
| Route evolution | Timeline |
| Representative patents | Patent cards |

## Evidence Rules

Use this chain:

```text
branch count or trend -> sampled representative patents -> problem/solution extraction -> route hypothesis -> product or R&D implication
```

- A route cannot be called important only because one patent is interesting.
- A future direction must be phrased as a signal or hypothesis.
- Claims and descriptions are stronger evidence than title-only labels.

## V0 Boundary

V0 can support taxonomy, branch trend, route hypotheses, and representative deep reading.

V0 should not claim:

- A complete technology roadmap for the whole industry.
- Product launch certainty.
- Legal claim-scope conclusions.
- SEP or standards relevance unless separate tools are available.

## Quality Checklist

- Each taxonomy label has include/exclude guidance.
- Rule-hit labels are separated from validated tags.
- Recent-year dips are checked for publication lag.
- Future directions use cautious wording.
- Representative patents are used to support route claims.
- No confidential source wording or project-specific examples appear.
