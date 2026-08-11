# Taxonomy Design

## Build from evidence

1. Sample across time, source, organization, technology direction, relevance, and text completeness.
2. Extract open codes without treating them as formal labels.
3. Normalize synonyms and spelling variants.
4. Separate dimensions before creating hierarchy.
5. Resolve mixed granularity, duplicate paths, and cross-dimensional concepts.
6. Create label confirmation cards backed by representative evidence.
7. Confirm definitions before formal use.

## Required definition content

Each formal label needs a stable ID, dimension, full path, definition, inclusion boundary, exclusion boundary, status, and version. Add synonyms, confusable labels, positive examples, and negative examples when available.

## Candidate evaluation

Do not promote a concept only because it appears once. Consider business relevance, recurrence, distinctiveness, boundary clarity, and whether an existing label already covers it.

## Change operations

- `add`: introduce a confirmed new label.
- `rename`: preserve the stable ID when meaning is unchanged.
- `merge`: record predecessor IDs and relabeling impact.
- `split`: define allocation rules and identify records needing rework.
- `move`: record hierarchy and path changes.
- `deprecate`: retain history; do not delete silently.

Any semantic change creates a new taxonomy version. Before freezing, report records affected by the change.

## Label confirmation card

Show proposed definition, inclusion and exclusion rules, synonyms, classification context, representative positive examples, hard negatives, adjacent labels, evidence sources, and user actions: accept, edit, merge, split, or reject.
