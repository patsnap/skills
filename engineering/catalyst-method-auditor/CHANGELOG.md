# Changelog

## v0.4.1 - Runtime cleanup and extraction hardening

### Fixed
- Removed runtime dependency on `python-docx`; DOCX report generation and DOCX validation now use Python standard library only.
- Prevented runtime `pip install` prompts during audit execution.
- Forced every run to reset the selected `outputs/` directory before report generation, preventing stale or intermediate report contamination.
- Enforced that all generated reports and `report_context.json` are written only under `outputs/`.
- Added stable filtering so gas atmospheres, solvents, equipment names and solution labels such as `H2/Ar` are not identified as catalyst samples.
- Improved preparation-step operation classification with formal process categories such as hydrothermal treatment, calcination, impregnation, reduction, washing/separation and drying.
- Strengthened output validation without third-party dependencies.

### Changed
- Completion output is now a concise status message; full report content remains only in HTML and Word files.


## v0.4.0 - Catalyst preparation and evaluation executability audit

### Added
- Repositioned the skill from "catalyst proposal pre-audit" to "catalyst preparation and evaluation scheme audit".
- Added material-type diagnosis for preparation-step screenshots, preparation method sections, experimental proposals, patent examples, paper methods, and draft ideas.
- Added a single deterministic execution entry: `scripts/run_audit.py`.
- Added fixed report context schema and deterministic issue generation rules.
- Added preparation-step executability audit, sample/control design audit, evaluation-condition audit, and claim-validation linkage audit.
- Added canonical issue catalogue to reduce run-to-run drift in core conclusions.
- Added strict output policy: exactly one HTML report and one Word report.
- Added stronger output validation to detect empty Word reports, dict-like raw objects, inconsistent issue counts, and missing sections.

### Changed
- Report title changed to `催化剂制备与评价方案审核报告`.
- User-facing terms changed to formal Chinese technical-review style.
- Internal English enum labels are not displayed in reports except in appendices when necessary.

### Removed
- Removed embedded test cases from the skill package.
- Removed proposal-only assumption.
- Removed optional engineering scale-up and patent-barrier analysis scope.
