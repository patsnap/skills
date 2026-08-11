---
name: complete-invention-disclosures-rd
description: Guide inventors and R&D teams through a seven-step English invention-disclosure workflow, organize rough technical notes, identify missing technical support, and generate a structured draft for inventor and qualified patent-professional review. Use when a user has an idea, product note, paper abstract, experiment record, design discussion, or incomplete disclosure that must be made technically complete without drafting claims or providing legal conclusions.
---

# Complete Invention Disclosures

## Purpose

Turn fragmented, conversational or product-oriented R&D material into a technically structured invention-disclosure draft.

Typical inputs include:

- an initial idea;
- product or architecture notes;
- a paper abstract;
- laboratory or test notes;
- an R&D chat transcript;
- an incomplete invention disclosure;
- diagrams or descriptions that have not been reconciled.

The output supports continued work by inventors, in-house IP teams and qualified patent professionals.

It is not a patent application, claim set, patentability opinion, infringement opinion, FTO opinion or filing instruction.

## Primary asset

Use `assets/disclosure-guide.html` when the user asks to open, view, demonstrate or deliver the interactive guide.

The asset is the approved package deliverable.

Do not rebuild it from this Markdown, replace its layout or add a source-absent asset without user approval.

If a copy is needed outside the package, preserve the original file and use an approved output location.

## Seven-step disclosure workflow

1. **Invention context** — working title, technical field, contributors, applicant/owner context, project and contact fields.
2. **Background** — known approaches, closest alternatives and specific limitations.
3. **Core invention** — technical problem, changed feature/relationship, mechanism and measured/expected effects.
4. **Technical solution** — architecture, process sequence, interfaces, inputs/outputs, parameters, ranges and alternatives.
5. **Embodiments and evidence** — best-known implementation, experiments, examples, failures and drawings.
6. **Priorities and disclosure timing** — commercially important aspects, easy workarounds, public/private disclosures and deadlines.
7. **Review and export** — completeness warnings, structured draft, source/gap list and safe copy/download.

## What to collect

### Context

- working title in technical rather than promotional language;
- technical field and adjacent fields;
- contributors and contribution notes for later inventorship review;
- applicant/owner/employer context for qualified review;
- project/product name and revision;
- confidentiality and access restrictions.

Do not determine inventorship or ownership from the form.

### Background

- how the problem is currently solved;
- known products, papers, standards and patents;
- concrete limitations under defined conditions;
- baseline metrics, sample sizes and measurement methods;
- why an improvement matters technically.

Avoid admissions that a specific document is legally “prior art.”

Record it as a known reference for counsel to assess.

### Core invention

Express:

> Given [baseline/problem under conditions], the proposal changes [technical feature or relationship], operating through [mechanism], to produce [measurable technical effect].

Separate observed effects from expected effects.

Do not convert marketing benefits into technical effects without a mechanism and evidence.

### Technical solution

Capture:

- system components and interfaces;
- method/process steps and ordering constraints;
- data inputs, transformations, states and outputs;
- physical/material/electrical/chemical relationships;
- control logic and feedback;
- parameter values, ranges, units and selection rationale;
- required versus optional elements;
- alternatives, substitutions and fallback modes;
- dependencies, assumptions and failure modes.

### Embodiments and evidence

Capture at least one implementation in enough detail for a technical reader to reproduce or test it.

Include:

- materials/components/datasets/equipment;
- setup and initial state;
- sequence of operations;
- operating conditions;
- measurements and calculations;
- results, uncertainty and comparison baseline;
- negative or failed examples when informative;
- figures and what each figure shows;
- open experiments and missing evidence.

### Priorities and disclosure events

Ask what aspects matter commercially and technically, but do not ask the inventor to draft claims.

Record past or planned:

- publications and preprints;
- conference abstracts, posters and talks;
- standards submissions;
- product releases or demonstrations;
- customer/partner disclosures;
- offers for sale or sales;
- public repositories or source-code releases;
- grant/proposal disclosures;
- confidentiality agreements where known.

Record exact dates, jurisdictions/audiences and confidentiality status for professional review.

Do not calculate a filing deadline or legal consequence.

## Writing support

The static HTML provides writing prompts and structural examples.

It does not call an AI model and must not label deterministic text transformations as AI completion.

Any future model integration requires an approved backend, security/privacy controls, clear model-output labeling and human review.

Never invent architecture, parameters, results, inventors, references or public-disclosure facts to make the draft look complete.

Mark missing information as `Needs input` and give a precise follow-up question.

## Optional PatSnap research

The disclosure can be completed from supplied material without MCP.

If the user explicitly requests prior-art research, verified global PatSnap support is:

- `advanced_patent_search`: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing`: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Preserve exact returned global URLs and record search coverage.

Do not claim novelty, inventive step/non-obviousness, validity, infringement or FTO from the search.

## Draft output

The generated draft contains:

1. working invention title;
2. technical field and scope;
3. contributor/applicant context for review;
4. background and known approaches;
5. technical problem and baseline;
6. core inventive concept and mechanism;
7. technical effects and evidence status;
8. detailed solution/architecture/process;
9. parameters, alternatives and variants;
10. embodiments, experiments and drawings;
11. priorities and possible workarounds;
12. disclosure history and planned disclosures;
13. missing-information register;
14. inventor and patent-professional review checklist.

## Confidentiality and privacy

Treat unpublished invention material as potentially confidential.

The standalone asset works locally and intentionally makes no network request.

Users must still assess browser extensions, endpoint management, screen sharing, clipboard history, downloads, backups and approved storage.

Do not enter unnecessary personal data.

Do not store home addresses, protected characteristics or personal identifiers in the disclosure.

## Quality gates

- [ ] The technical problem is specific and measurable.
- [ ] Baseline/known approaches are distinguished from legal prior-art conclusions.
- [ ] Core changed features and relationships are explicit.
- [ ] Mechanism connects the change to the effect.
- [ ] Observed and expected results are separated.
- [ ] Units, conditions, sample sizes and uncertainty are captured where relevant.
- [ ] Architecture/process is internally consistent.
- [ ] Required and optional elements are distinguished.
- [ ] Alternatives and workarounds are documented.
- [ ] At least one embodiment is reproducible/testable at the appropriate stage.
- [ ] Figures are listed and reconciled with text.
- [ ] Failed/negative evidence is not hidden.
- [ ] Contributors, ownership and inventorship are left for qualified review.
- [ ] Public/private disclosures include exact dates and audiences.
- [ ] Missing information remains visibly marked.
- [ ] No claim language or legal conclusion is presented as final.
- [ ] Inventor and patent professional review the draft before use.

## Boundaries

This skill organizes technical material and highlights gaps.

It does not establish inventorship, ownership, confidentiality, filing priority, grace periods, patentability, enablement/support, best mode, claim scope or compliance with any jurisdiction's formal requirements.
