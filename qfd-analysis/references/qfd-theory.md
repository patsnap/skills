# QFD Theory for This Skill

This skill implements phase-1 QFD: translating voice of customer into technical priorities.

## What the Pipeline Produces

- customer requirements and their importance
- technical features
- requirement-to-feature relationships
- feature-to-feature correlations
- conflicts and trade-offs
- benchmark gaps when competitor specs exist
- ranked recommendations

## How to Interpret the Outputs

- `requirements.json` explains what customers care about.
- `relationship_matrix.json` shows which technical features drive those needs.
- `correlation_matrix.json` and `conflicts.json` reveal engineering tensions.
- `priority_recommendations.json` ranks what to improve first.
- `qfd_report.md` provides the user-facing synthesis.

## Scope Boundary

- Use this skill for phase-1 HOQ analysis.
- If the user wants contradiction resolution after the HOQ, consider handing off to `triz-analysis`.
- If the user wants raw market research rather than structured deployment, gather or clean the inputs first instead of forcing the pipeline.
