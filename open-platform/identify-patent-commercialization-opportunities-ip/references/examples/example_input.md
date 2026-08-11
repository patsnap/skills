# Example Inputs

These examples illustrate routing and evidence discipline. They do not contain real search results or recommendations.

## Example 1 — Specific technology subfield

**User input**

```text
Assess the patent and commercialization opportunities for pre-sodiation of hard-carbon anodes in sodium-ion batteries.
```

**Expected behavior**

1. Accept the topic as a bounded technology subfield.
2. Record the decision context, markets, period, date field, and family rule.
3. Build and test concept blocks for sodium-ion batteries, hard carbon, and pre-sodiation mechanisms.
4. Validate classifications and false-positive exclusions.
5. Freeze a versioned global query.
6. Use Advanced Patent Search count capabilities discovered at runtime for complete period buckets when available.
7. Define four to eight independently searchable subfields, such as chemical, electrochemical, contact, and sacrificial-additive approaches, subject to evidence.
8. Retrieve a representative patent sample only for technical illustration and evidence mapping.
9. Use Patent Briefing to verify bibliography, families, status, claims, descriptions, and translations.
10. Use Deep Patent Mining when technical-topic, problem/solution/effect, material, or application-domain enrichment is useful.
11. Generate all ten report artifacts only after metrics and sample data pass their separate gates.

**Example concept structure**

```text
("sodium-ion" OR "sodium ion")
AND ("hard carbon" OR nongraphitizable carbon)
AND (presodiat* OR "pre-sodiat*" OR "sodium compensation")
```

Convert this concept structure into the live connector's tested syntax. Do not claim it is executable before validation.

**Localization note**

Do not automatically generate a China-versus-global chart. Include China or another benchmark only when relevant to the user's manufacturing, market, competitor, or portfolio decision and when the series are comparable.

---

## Example 2 — Concrete technical solution

**User input**

```text
Evaluate the patent and commercialization opportunity for a fluorinated-polymer artificial SEI used on lithium-metal anodes.
```

**Expected behavior**

1. Accept the request as a concrete solution.
2. Normalize the broader direction as `artificial interphase materials for lithium-metal anodes`.
3. Retain fluorinated polymers as an included solution route, not the entire population definition.
4. Define exclusions for unrelated natural SEI characterization and non-lithium systems.
5. Record material jurisdictions, intended commercialization decision, and technical requirements.
6. Continue through the full workflow with evidence-qualified opportunity and risk statements.

---

## Example 3 — Topic requiring refinement

**User input**

```text
Analyze clean-energy patent opportunities.
```

**Expected behavior**

1. Reject the topic as too broad for a reproducible technology search.
2. Do not generate report artifacts.
3. Explain which technical boundary is missing.
4. Offer focused examples such as:
   - hard-carbon pre-sodiation for sodium-ion batteries;
   - encapsulation barriers for perovskite solar cells;
   - sulfide solid electrolytes with improved moisture tolerance;
   - fatigue-life sensing for composite wind-turbine blades; and
   - immersion-cooling interfaces for grid-scale battery systems.

**Example response**

```text
“Clean energy” spans multiple unrelated technologies and cannot support a reproducible patent-opportunity assessment as written. Please specify a mechanism, material/device, process, technical problem, or application. For example: “moisture-tolerant sulfide electrolytes for all-solid-state batteries.”
```

## Acceptance checks

- Accepted examples identify a technical object and mechanism/problem.
- The broad example generates no report.
- No example assumes an undocumented aggregation MCP.
- No example presents synthetic counts, scores, or patent facts as real.
- Representative samples remain separate from full-scope metrics.
