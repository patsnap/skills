# Insight Skills

This repository contains four research-oriented open skills for general-purpose
coding and agent environments. Each skill is packaged as a self-contained
directory with a `SKILL.md`, reusable references, templates, and lightweight
examples.

## Included Skills

| Skill | What it does |
| --- | --- |
| `company-tech-profile` | Single-company technology profiling in a defined topic |
| `competitive-landscape` | Multi-player competitive landscape analysis in one technical arena |
| `rd-initiation-review` | Proposal and R&D initiation review for go/no-go style decisions |
| `tech-route-comparison` | Comparison of two or more technical routes or solution paths |

## Package Structure

Each skill directory follows a small, portable layout:

- `SKILL.md`: the main protocol and execution rules
- `references/`: method notes, quality gates, deliverable guidance, and routing hints
- `templates/`: starter files for request capture, workplan, report structure, and evidence records
- `examples/`: minimal prompt and fallback examples

These skills are designed to be tool-agnostic. They prefer higher-confidence
structured retrieval when available, but they can degrade to general web
research and known-URL reading when needed. The expected artifact model is
file-based and traceable: request, plan, evidence logs, and report stay on disk
throughout the run.

## What Was Intentionally Left Out

This open bundle excludes repository-internal or non-portable material such as:

- regression eval sets
- environment-specific testing docs
- internal maintenance notes
- helper scripts tied to private infrastructure or non-public endpoints

## Usage Notes

Pick the skill whose decision object matches the task:

- one company in one topic: `company-tech-profile`
- multiple players in one arena: `competitive-landscape`
- one concrete proposal or project package: `rd-initiation-review`
- two or more technical routes: `tech-route-comparison`

If you mount these skills into another agent runtime, keep each skill directory
intact so relative links from `SKILL.md` to `references/` and `templates/`
continue to work.
