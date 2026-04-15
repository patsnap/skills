# Method Benchmark

This skill should stay aligned with high-confidence public methods for company
technical profiling, patent analytics, and reproducible evidence handling.

## External Benchmark Sources

- WIPO, *Guidelines for Preparing Patent Landscape Reports* (2015)
- WIPO, *The Patent Analytics Handbook* (2022)
- OECD, *OECD Patent Statistics Manual* (2009)
- DHS S&T, *Technology Scouting* process description

## Top-Tier Method Requirements

1. Freeze scope before retrieval:
   - company entity
   - topic boundary
   - time window
   - decision use
2. Normalize the entity before counting:
   - parent vs subsidiary
   - Chinese vs English alias
   - brand vs legal entity
3. Use more than one evidence family:
   - patents
   - papers
   - official or product/public signals
4. Treat patent statistics cautiously:
   - counts need caveats
   - office bias and scope bias must be stated
   - family/equivalent issues must be acknowledged if relevant
5. Keep the analysis reproducible:
   - query log
   - source index
   - claim ledger

## What "Leading" Looks Like In This Skill

- the report does not confuse patent volume with technical strength
- the report does not confuse company messaging with verified capability
- route conclusions come from converging signals, not one source family
- downgraded runs explicitly reduce confidence and claim strength

## Upgrade Triggers

Refresh the skill when one of these happens:

- a new public benchmark source changes patent-analysis best practice
- a recurring industry-specific misread appears in real runs
- a new public data lane materially improves company capability evidence
