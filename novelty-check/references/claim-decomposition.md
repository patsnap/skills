# Claim Decomposition Guide

Use this guide before any search or legal conclusion.

## Goal

Turn each target claim into a stable list of searchable limitations.

## Workflow

1. Select the target claim set.
   - Start with the main independent claim.
   - Add only those dependent claims that materially change patentability risk.
2. Split the claim into:
   - preamble
   - transition phrase
   - individual limitations
3. Assign stable IDs such as `E1`, `E2`, `E3`.
4. Record for each element:
   - short description
   - structural, functional, parameter, or process type
   - synonyms and term variants
   - numeric ranges or thresholds
   - likely search anchors

## Special Handling

### Dependent claims

- Reconstruct the full claim by inheriting all parent limitations.
- Do not analyze the added feature in isolation.

### Functional language

- Capture both the stated function and the structure or step that appears to perform it.
- Flag means-plus-function or highly abstract language as higher-risk elements.

### Numerical ranges and Markush groups

- Keep endpoints and units exactly as written.
- Note whether novelty risk can arise from overlap, selection, or one specific embodiment.

### Preamble and environment

- Include preamble language only when it is likely limiting.
- If uncertain, mark the issue explicitly instead of silently dropping it.

## Recommended Output Shape

| Element ID | Text | Type | Key variants | Search anchor |
| --- | --- | --- | --- | --- |
| E1 | ion-exchange membrane | structural | ion exchanger, membrane | material + function |
| E2 | pore size 0.2-0.5 um | parameter | pore diameter | numeric range |
| E3 | adjusts pH automatically | functional | auto pH control | control + sensor |

## Red Flags

- Bundling multiple limitations into one element
- Dropping units or thresholds
- Ignoring inherited dependent-claim language
- Treating result language as identical to mechanism language
- Using search terms that do not map back to a claim limitation
