# Input Scoping Prompt

## Task

Determine whether the user's topic is specific enough for a reproducible patent-opportunity assessment. Normalize the accepted scope without silently changing the business question.

## Decision rules

### Reject or request refinement

Reject a broad sector label when it appears without a technical mechanism, material, device, process, function, problem, or application boundary. Examples include:

- artificial intelligence;
- clean energy;
- semiconductors;
- biopharma;
- batteries;
- materials;
- robotics;
- quantum technology;
- software; and
- the internet.

Do not use a fixed blacklist mechanically. A phrase is acceptable when the surrounding request supplies enough technical and decision context to construct and validate a search.

### Accept a technology subfield

Require at least two of the following:

- technical mechanism or method;
- material or composition;
- device, component, or architecture;
- manufacturing or operating process;
- measurable function or performance target;
- technical problem; and
- end-use application.

Example: `pre-sodiation of hard-carbon anodes for sodium-ion batteries` is suitable. `battery anode materials` is normally too broad.

### Accept a concrete technical solution

Accept a solution that identifies a technical implementation and problem, such as `a fluorinated-polymer artificial SEI for lithium-metal batteries`. Normalize it to a technology direction while retaining the concrete solution as an included concept.

### Borderline cases

Use `accept_with_note` only when a defensible search boundary can be stated. Otherwise request one concise clarification covering the missing technical or business boundary.

## Required localization

- Use English as the report and connector language.
- Build multilingual search concepts only when they improve coverage in material jurisdictions.
- Preserve source-language keywords and document translations.
- Do not automatically add China as a benchmark; use regions relevant to the user's markets, R&D base, competitors, or decision.
- Ask for or infer the decision type: R&D exploration, commercialization, licensing, partnership, investment screening, or portfolio planning.
- Record target jurisdictions, date range, application/publication basis, family rule, and cutoff.

## Output schema

```json
{
  "decision": "accept | reject | accept_with_note",
  "refined_topic": "normalized English technology direction",
  "original_topic": "verbatim user topic",
  "input_type": "subfield_direction | specific_solution | borderline",
  "domain": "energy | life_sciences | materials | electronics | chemistry | software | other",
  "decision_context": "R&D | commercialization | licensing | partnership | investment_screen | portfolio",
  "technical_boundary": {
    "mechanism": [],
    "materials_or_components": [],
    "processes": [],
    "functions_or_metrics": [],
    "applications": [],
    "explicit_exclusions": []
  },
  "geographic_scope": [],
  "time_scope": {"start": null, "end": null, "basis": "application | publication | priority"},
  "family_counting_rule": "publication | simple_family | extended_family | INPADOC",
  "rejection_reason": null,
  "clarification_suggestions": [],
  "scope_note": null,
  "keyword_concepts": [
    {"concept": "", "english": [], "source_language_terms": [], "exclusions": []}
  ],
  "classification_candidates": [{"system": "IPC | CPC | other", "code": "", "reason": ""}],
  "subfield_candidates": [{"name": "", "definition": "", "exclusions": []}],
  "assumptions": [],
  "open_questions": []
}
```

## Quality checks

- The refined topic is narrower than a sector label.
- Search concepts cover both the mechanism and technical object.
- Exclusions are explicit enough to test precision.
- Geographic and temporal choices support the decision.
- Subfield candidates are technically meaningful rather than marketing labels.
- No unsupported IPC/CPC code, translation, or business requirement is invented.
- A rejected request receives three to five concrete refinement examples.
