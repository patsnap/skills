# Evidence Search Guide (Patents + Papers)

This skill is evidence-driven. Do not deliver final recommendations without external support unless the user explicitly asks for brainstorming only.

## 1. Minimum Evidence Contract
- Collect at least 3 credible sources per analysis.
- Each of the 3 options must map to at least 1 source.
- Prefer sources from the last 5 years.
- Add 1-2 classic references when foundational methods are relevant.

## 2. Source Priority
1. Patent full-text pages (Google Patents, WIPO, USPTO/EPO public pages)
2. Peer-reviewed publishers (IEEE, ACM, Springer, Elsevier, Nature family)
3. Reputable preprints (arXiv) when peer-reviewed alternatives are limited
4. High-quality technical standards or vendor technical notes (as supporting evidence)

Avoid low-trust blogs unless they lead to primary references.

## 3. Query Building Framework
Build queries from four blocks:
- Problem object: component/system/process
- Contradiction pair: improve X while not worsening Y
- Mechanism terms: candidate solution principles/materials/architectures
- Context constraints: industry, scale, environment

## 4. Query Templates
Use bilingual terms when helpful.

### Patent-focused templates
- "[core system] [contradiction mechanism] patent"
- "[problem function] [target metric] [technical approach] patent"
- "[CPC/IPC if known] [key concept]"

### Paper-focused templates
- "[problem statement] [method] [benchmark metric] paper"
- "[domain] [tradeoff] optimization review"
- "[key mechanism] experimental validation"

## 5. Search Flow
1. Broad pass: 2-4 queries, collect candidate pool.
2. Narrow pass: focus on most relevant mechanism and constraints.
3. Verification pass: check publication year, relevance, and technical closeness.
4. Coverage check: ensure all 3 options can be evidence-linked.

## 6. Evidence Record Format
For each source, capture:
- title
- URL
- source type (patent/paper/standard)
- year
- one-sentence relevance note
- mapped option (Conservative/Balanced/Breakthrough)

## 7. Handling Evidence Gaps
If high-quality evidence is insufficient:
1. state insufficiency explicitly
2. provide expanded query suggestions
3. mark recommendation confidence down
4. still deliver options, but separate "evidence-backed" vs "hypothesis"

## 8. Conflict Handling
When sources conflict:
- identify disagreement point
- check scenario mismatch (scale/material/context)
- prioritize evidence with stronger experimental or deployment validation
- reduce confidence and surface decision risk
