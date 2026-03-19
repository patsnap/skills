# Bioprocess Factor Library

Use canonical factor names in outputs.

## Core Factors
1. `temperature` (`degC`)
2. `pH` (`pH`)
3. `dissolved_oxygen` (`%`)
4. `agitation_speed` (`rpm`)
5. `aeration_rate` (`vvm`)
6. `feed_rate` (`mL_per_h`)
7. `induction_timing` (`h`)

## Metadata Expectations
- `name`
- `type` (`range|categorical`)
- `unit`
- `suggested_range`
- `mechanism_hypothesis`
- `risk_note`

## Normalization Rules
- Keep one canonical unit per factor.
- Convert source units before score aggregation.
- Keep aliases strict to avoid false positives.
