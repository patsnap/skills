#!/usr/bin/env python3
"""Print the localized technology-insight workflow checklist."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Phase:
    number: int
    name: str
    items: tuple[str, ...]


PHASES = (
    Phase(
        0,
        "Scope and preflight",
        (
            "Decision, audience, technical boundary, geographies, languages, report date, and evidence cutoff are explicit.",
            "Confidentiality and authorization for external research are confirmed.",
            "The ten-section s0–s9 report topology is created from the localized skeleton.",
            "The cross-section synchronization register is initialized.",
            "Patent count unit, family normalization, entity normalization, and evidence IDs are defined.",
            "Verified PatSnap connector availability and current callable schemas are checked.",
            "Primary-source plans exist for literature, markets, companies, standards, regulation, and engineering evidence.",
            "Required patent, domain, technical, safety, regulatory, and market reviewers are assigned.",
        ),
    ),
    Phase(
        1,
        "Evidence collection and coverage",
        (
            "Every search has source/tool, exact query, filters, date, language, requested limit, returned/reviewed counts, and truncation.",
            "Patent search uses iterative coverage expansion and does not describe matched_total as fully reviewed records.",
            "Publication, simple-family, paper, standard, case, market, and web counts remain separate.",
            "Patent identities, dates, family/status context, claims reviewed, and stable links are recorded.",
            "Literature methods, results, conditions, editorial status, and limitations are reviewed.",
            "Market values include publisher, report, currency, price year, geography, segment, and scenario status.",
            "Company/current-awareness evidence uses dated primary sources where possible.",
            "Standards and regulation include identifier, version/status, clause, geography, and effective/as-of date.",
            "Rejected, inaccessible, duplicate, and contradictory records remain traceable.",
            "Sparse, failed, omitted, or truncated searches are disclosed.",
        ),
    ),
    Phase(
        2,
        "Analysis and evidence reconciliation",
        (
            "Technology routes, maturity, performance, adoption, and timing are analyzed as separate dimensions.",
            "Value-chain roles and organization inclusion criteria are source-grounded and globally applicable.",
            "Competitor comparisons use shared definitions, dates, and missing-data rules.",
            "Patent landscape metrics identify search universe, denominator, count unit, and coverage limits.",
            "Claim-relevance screening is distinguished from infringement/FTO conclusions.",
            "Candidate gaps say not observed in the reviewed dataset and retain gap-check search IDs.",
            "Standards or regulation gaps distinguish missing evidence, optional provisions, drafts, and actual requirements.",
            "Cross-domain applications include transfer conditions, barriers, and validation requirements.",
            "Every decision finding has supporting and contradicting evidence IDs.",
            "Synchronization-register conflicts are resolved or disclosed.",
        ),
    ),
    Phase(
        3,
        "Static HTML report",
        (
            "Sections s0–s9 exist in order and include explicit not-applicable or evidence-gap states when needed.",
            "The report uses the localized light scientific/editorial design without gradients, scripts, or external runtime.",
            "All charts are self-contained accessible tables, CSS bars, or reviewed inline static SVG with data tables.",
            "Every table has a caption or nearby scope, consistent columns, and responsive overflow.",
            "Version appears consistently in title, metadata, and footer; dates use ISO format.",
            "All links use HTTP(S), mailto, or resolved internal anchors; no local absolute path remains.",
            "All untrusted text is escaped by the population process.",
            "Decision recommendations are written after evidence sections and reference evidence IDs.",
            "Patent specialist and not-legal-advice boundaries appear in header and footer context.",
            "A complete source register and search-method disclosure are present.",
        ),
    ),
    Phase(
        4,
        "Automated and cross-section QA",
        (
            "scripts/quality_check.py passes all structure, version/date, table, link/runtime, cleanliness, legal-language, and metadata checks.",
            "Source register IDs resolve from every factual finding.",
            "Displayed totals reconcile with accepted evidence under labeled units.",
            "Market values and assumptions match everywhere they appear.",
            "Organization, route, maturity, and event statements reconcile across sections.",
            "Claim-screening records link to specialist-review options and no automated infringement conclusion appears.",
            "Candidate gaps retain bounded language, gap-search IDs, and limitations.",
            "Standards/regulatory statements retain jurisdiction, status, clause, and date.",
            "Version, report date, evidence cutoff, and review status match metadata and footer.",
            "CJK, domestic-domain, credential, local-path, gradient, unsafe-DOM, external-runtime, and placeholder scans are clean.",
        ),
    ),
    Phase(
        5,
        "Release review",
        (
            "A reviewer reads the complete report, not only edited sections.",
            "Desktop, narrow-screen, and print layouts are visually reviewed.",
            "Evidence licenses, confidentiality, and permitted quotations are checked.",
            "Patent, legal, safety, regulatory, clinical, financial, and domain-review boundaries are satisfied or withheld.",
            "Every failed/warned quality gate has an owner, resolution, or explicit release exception.",
            "The delivered filename/version, report date, evidence cutoff, and next-review date are correct.",
            "No temporary, cache, credential, local fixture, or source-absent package file is present.",
            "Release decision is recorded as ready for review, approved, withheld, or superseded.",
        ),
    ),
)


def print_phase(phase: Phase) -> None:
    print(f"\nPhase {phase.number} — {phase.name}")
    print("-" * (len(phase.name) + 12))
    for index, item in enumerate(phase.items, start=1):
        print(f"[ ] {index:02d}. {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Print technology-insight workflow QA checklists")
    parser.add_argument(
        "phase",
        nargs="?",
        default="all",
        choices=["all", *(str(phase.number) for phase in PHASES)],
    )
    args = parser.parse_args()
    print("Technology Insight Report — Localized Workflow Checklist")
    selected = PHASES if args.phase == "all" else tuple(
        phase for phase in PHASES if str(phase.number) == args.phase
    )
    for phase in selected:
        print_phase(phase)
    print("\nRun: python scripts/quality_check.py <report.html>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
