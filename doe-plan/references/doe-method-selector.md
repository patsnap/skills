# DOE Method Selector

Select method using `phase + factor_count + resource_budget`.

## Inputs
- `phase`: `screening` or `optimization`
- number of selected factors
- resource budget (max runs)
- need for curvature modeling

## Decision Rules
1. Screening:
   - factors >= 7: choose `PB`
   - factors 4-6: choose `FFD`
   - factors <= 3: choose `FFD`
2. Optimization:
   - factors <= 5 and tight budget: choose `BBD`
   - factors <= 5 and enough budget: choose `CCD`
   - factors > 5: choose `FFD` first to reduce dimensions

## Practical Rules
- Keep center points >= 3 for optimization designs.
- Add replicates for noisy assays.
- Apply randomization with a fixed seed.
- Record why the method was selected in `selection_rationale.why_this_design`.

## Diagnostics Expectations
- Include `run_count`, `alias_risk`, and column correlation indicator.
- Mark PB/FFD alias risk as higher than BBD/CCD.
