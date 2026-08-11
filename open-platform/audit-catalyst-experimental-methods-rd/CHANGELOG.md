# Changelog

## v0.5.0 — Global English localization

### Changed

- Localized the complete skill package, deterministic rule set, schemas, prompts, HTML, Word output, and validation messages into international scientific English.
- Renamed the package to `audit-catalyst-experimental-methods-rd` while preserving the source file topology.
- Replaced domestic configuration text with a local-first execution contract and optional verified global PatSnap MCP references.
- Reworked report terminology for global research, R&D, and technical-review practice.
- Updated the report to a restrained, accessible scientific/editorial visual system.
- Distinguished `not specified` from evidence that a method or control was not performed.

### Added

- Explicit EHS, hazardous-gas, pressure-equipment, containment, waste, and stop-work review boundaries.
- Measurement-chain review covering calibration, detection limits, balances, replication, uncertainty, and exclusions.
- Claim-to-evidence matrix and alternative-explanation discipline for mechanistic claims.
- Output-file safety and symlink validation guidance.

### Removed

- Generated Python bytecode found in the frozen source; it is a runtime cache, not maintainable package material.

## v0.4.1 — Runtime cleanup and extraction hardening

### Fixed

- Removed runtime dependency on `python-docx`; DOCX generation and validation use the Python standard library.
- Prevented runtime package-install prompts.
- Reset the selected output directory before report generation to prevent stale report contamination.
- Kept generated reports and `report_context.json` under the selected output directory.
- Filtered gas atmospheres, solvents, equipment, and solution labels from catalyst sample candidates.
- Improved preparation-operation classification.
- Strengthened output validation without third-party dependencies.

### Changed

- Reduced chat completion output to a concise status message; full findings remain in HTML and Word artifacts.

## v0.4.0 — Catalyst preparation and evaluation method audit

### Added

- Repositioned the skill from proposal pre-audit to preparation and evaluation method audit.
- Added material classification for procedures, screenshots, proposals, patent examples, paper methods, and draft concepts.
- Added the deterministic execution entry point `scripts/run_audit.py`.
- Added fixed report-context schema and deterministic issue rules.
- Added preparation executability, sample/control, evaluation-condition, and claim-validation audits.
- Added a canonical issue catalog to reduce run-to-run drift.
- Added exactly one HTML report and one Word report plus a machine-readable context.
- Added validation for empty reports, raw object leakage, inconsistent counts, and missing sections.

### Removed

- Removed embedded test cases, proposal-only assumptions, optional scale-up analysis, and patent-barrier analysis from the original scope.
