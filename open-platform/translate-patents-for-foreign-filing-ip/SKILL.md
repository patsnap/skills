---
copyright: "Copyright © Patsnap. All rights reserved."
name: translate-patents-for-foreign-filing-ip
description: Translate Chinese patent applications, priority texts, claims, descriptions, abstracts, drawing text, sequence-listing references, or invention disclosures into filing-support drafts for Europe, the United States, Japan, or Korea while preserving source support, claim scope, terminology, and destination-specific patent style. Use for EP, US, JP, or KR patent translation, jurisdiction formatting, terminology reconciliation, or translation QA.
---

# Translate Patents for Foreign Filing

## Objective

Create a destination-specific filing-support translation from authoritative Chinese source material.
Preserve priority support, technical meaning, claim scope, dependency, terminology, and document structure.

This skill produces a drafting aid, not a certified translation, legal opinion, filing instruction,
priority opinion, added-matter opinion, or assurance of filing compliance.
Require review by qualified destination counsel and, where appropriate, a competent patent translator.

## When to use

Use when the user provides or describes:

- Chinese claims, description, abstract, or drawing text;
- a Chinese priority or application document;
- a Chinese invention disclosure intended for a foreign application;
- terminology or translation issues in an EP, US, JP, or KR draft;
- a request for jurisdiction-specific patent-language formatting;
- a request to audit an existing translation against the Chinese source.

Supported destinations:

- Europe / EPO;
- United States / USPTO;
- Japan / JPO;
- Korea / KIPO.

Allow multiple destinations, but create and review each version independently.

## Required inputs

Collect or infer safely:

- authoritative Chinese source and its revision/date;
- supplied sections and missing sections;
- target jurisdiction or jurisdictions;
- filing route, if known;
- priority date and planned filing date;
- application type;
- required output language;
- approved terminology and prior translations;
- drawing, formula, table, and sequence-listing dependencies;
- confidentiality and file-handling constraints;
- requested output format.

If the user provides only part of the application, translate that part and identify missing dependencies.
Do not manufacture absent sections.

## Reference routing

Load only the reference files required for the requested destinations:

- Europe: `references/europe.md`
- United States: `references/united-states.md`
- Japan: `references/japan.md`
- Korea: `references/korea.md`

The common source-faithfulness rules in this file control every destination.
Jurisdiction references refine patent style and QA; they do not authorize new technical matter.

## Optional Patsnap MCP support

No MCP is required when the user supplies the authoritative source text.

### Patent Briefing — recommended for an identified publication

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use: retrieve or cross-check bibliographic data, claims, description, family, status,
  available translations, and images for a published patent.

### Advanced Patent Search — optional for incomplete identifiers

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use: locate an authoritative publication when the citation or publication number is incomplete.

Confirm the live tool schema before calling a connector.
Do not send confidential unpublished text to an unapproved service.
Treat machine translations returned by a database as reference evidence, not filing-ready text.

## Workflow

### Step 1 — Inventory and freeze the source

1. Identify each supplied file or pasted section.
2. Record document title, revision, date, page/paragraph/claim locators, and language.
3. Separate claims, description, abstract, drawings, tables, formulas, and sequence materials.
4. Preserve an immutable source copy when creating files.
5. Identify missing pages, unreadable text, inconsistent numbering, and conflicting revisions.
6. Do not translate from an unofficial OCR extract without disclosing the limitation.

Create a source inventory with these fields:

```text
source_id | file/section | revision | locator range | authority | condition | notes
```

### Step 2 — Define the destination and filing context

For each destination, record:

- office and jurisdiction;
- direct, Paris, PCT national/regional phase, or other route;
- priority date and expected filing date;
- application type;
- filing language and delivery language;
- sections to translate;
- known official forms or sequence-listing dependencies;
- counsel or translator review owner;
- current official requirements still needing verification.

If no destination is specified, ask the user to identify Europe, the United States, Japan, Korea,
or a combination. Do not silently choose a destination.

### Step 3 — Build the terminology and ambiguity registers

Extract high-impact terms before translating claims:

- invention title and core technical objects;
- component, material, composition, and process names;
- relationships, connections, directions, and spatial terms;
- algorithm, signal, data, and control terms;
- chemical, biological, and sequence nomenclature;
- measurement units, test methods, and numerical qualifiers;
- scope terms such as at least one, plurality, any, and/or, optionally, preferably,
  including, comprising, containing, consisting of, and substantially.

Use this terminology schema:

```text
term_id | Chinese source | approved destination term | context | source locators | alternatives rejected | rationale | status
```

Use this ambiguity schema:

```text
issue_id | source locator | source wording | possible readings | scope/technical impact | proposed handling | decision owner | status
```

Do not silently resolve an ambiguity that can affect claim scope, support, or technical meaning.

### Step 4 — Translate claims first

Translate independent claims before dependent claims, then reconcile the dependency tree.

For every claim:

1. preserve claim number and category;
2. preserve dependency and multiple-dependency logic;
3. map every limitation to the source;
4. preserve open or closed transitions intentionally;
5. preserve antecedent basis and singular/plural relationships;
6. preserve optionality, alternatives, and examples;
7. preserve only source- or technology-required method order;
8. preserve ranges, endpoints, units, formulas, conditions, and reference signs;
9. flag functional-language and destination-specific construction risks;
10. record unresolved choices in the ambiguity register.

Never:

- add a limitation, effect, parameter, example, definition, or fallback embodiment;
- convert an optional or preferred feature into a mandatory limitation;
- strengthen an effect to “significant,” “complete,” “always,” or “substantial” without support;
- impose a strict sequence merely for smoother prose;
- collapse distinct technical relationships into a generic connection;
- repair a source inconsistency without recording it.

### Step 5 — Translate the remaining sections

Translate the description, abstract, drawing text, tables, formulas, and sequence references using the
approved claim terminology.

Improve grammar and readability where necessary, but do not change technical content.
Keep paragraph, figure, example, table, sequence, and reference-sign locators stable where practical.
Preserve definitions, alternatives, embodiments, ranges, conditions, and negative statements.

For an invention disclosure rather than a filed application:

- label the output as a translation of the disclosure;
- do not represent it as a complete application;
- identify missing support, drawings, examples, and formal sections;
- separate translation from any later drafting or claim-development request.

### Step 6 — Apply destination formatting

Load the applicable jurisdiction reference and use its section order and patent-language guidance.

Do not invent an official form or hard-code a filing rule from memory.
At execution time, verify material route-specific requirements against current official EPO, USPTO,
JPO, KIPO, or WIPO sources as applicable.

Keep substantive translations separate from purely formal reordering.
Record any moved section, renamed heading, or destination-specific adaptation in the change log.

### Step 7 — Reconcile the complete translation

Perform cross-document checks:

- every claim term appears consistently in the description;
- claim dependencies and categories match the source;
- title, abstract, claims, and description use approved core terminology;
- drawing labels and reference signs reconcile;
- tables, equations, chemical names, sequences, ranges, and units reconcile;
- optionality and alternatives remain intact;
- no unsupported matter appears;
- every ambiguity has a status and owner;
- every intentional adaptation has a source locator and rationale.

### Step 8 — Deliver and qualify the result

For each selected destination, deliver:

```text
[Destination] patent filing-support translation

1. Source and filing-context record
2. Formatted translation
3. Bilingual terminology register
4. Ambiguity and change register
5. Translation QA and risk note
6. Items requiring counsel/translator confirmation
```

If file creation is requested, use this source-defined working convention unless the user provides another:

```text
project-name/
├─ 01_chinese_source/
├─ 02_terminology/
├─ 03_europe_ep_english/
├─ 04_united_states_us_english/
├─ 05_japan_jp_japanese/
├─ 06_korea_kr_korean/
└─ 07_translation_qa/
```

Do not create empty destination folders for jurisdictions not requested.

## Translation rules

- Claims control scope and receive first-pass priority.
- Use one approved translation for each technical term unless the context requires a documented distinction.
- Preserve open-ended language unless the source and strategy clearly require closed scope.
- Preserve optional, preferred, exemplary, alternative, and conditional features.
- Preserve method order only where linguistically, expressly, or technically required.
- Treat scope terms as deliberate drafting decisions.
- Do not exaggerate effects or certainty.
- Repair grammar without repairing the invention.
- Mark unclear source text and request a decision rather than inventing meaning.
- Preserve negative limitations and disclaimers precisely.
- Preserve source punctuation when it affects mathematical, chemical, sequence, or logical meaning.
- Distinguish translation decisions from counsel-approved substantive amendments.

## Quality gates

### Source gate

- The authoritative source and revision are identified.
- Supplied and missing sections are listed.
- OCR or extraction limitations are disclosed.

### Claim gate

- Claim numbering, category, and dependency are complete.
- Each independent-claim limitation maps to a source locator.
- Antecedent basis and singular/plural logic are consistent.
- Open/closed transitions, optionality, order, and functional wording are deliberate.

### Technical gate

- Units, ranges, endpoints, formulas, algorithms, materials, sequences, and test conditions are preserved.
- Reference signs, drawings, and drawing descriptions reconcile.
- No unsupported effect, parameter, example, or implementation was added.

### Terminology gate

- Claims, description, abstract, drawings, and sequences use consistent approved terms.
- Alternatives and rejected terms are recorded where material.
- Unresolved ambiguity remains visible.

### Destination gate

- Only the applicable jurisdiction references were used.
- Destination headings and order are consistent with the selected route.
- Current official requirements needing confirmation are listed.
- The output does not claim autonomous filing readiness.

### Professional-review gate

- Destination counsel review is identified as required.
- Translator or certification review is identified where applicable.
- Priority, support, added matter, claim interpretation, forms, and deadlines are not presented as settled
  unless verified by the responsible professional for the actual facts.

## Failure handling

If the source is incomplete, translate the available material and issue a missing-content register.
If revisions conflict, stop combining them and ask which version controls.
If text is unreadable, identify exact locators and do not guess.
If the target jurisdiction is unknown, obtain it before formatting.
If terminology is disputed, preserve alternatives and assign a decision owner.
If an MCP is unavailable, continue from user-supplied source and label unavailable database checks.
If confidential handling is not authorized, do not transmit unpublished content externally.

## Final response

State:

- source revision and sections translated;
- destination and filing context used;
- output language and document structure;
- number of unresolved terminology or ambiguity issues;
- highest-risk scope or support issue;
- files or sections delivered;
- exact counsel/translator review still required.
