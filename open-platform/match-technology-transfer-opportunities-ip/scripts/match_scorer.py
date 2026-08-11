"""Evidence-aware technology-transfer recipient scoring.

The source 40/30/30 model is retained as a configurable baseline. Missing
metrics are not zero and are never silently redistributed. Every scored metric
must carry evidence identifiers and a declared normalization method.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from math import isfinite
from typing import Iterable, Mapping, Sequence


BASELINE_WEIGHTS = {
    "patent": 40.0,
    "public_signal": 30.0,
    "procurement": 30.0,
}

PATENT_WEIGHTS = {
    "classification_overlap": 8.0,
    "technical_similarity": 10.0,
    "recent_relevant_activity": 7.0,
    "citation_context": 5.0,
    "territorial_or_family_fit": 5.0,
    "complementarity_or_relationship": 5.0,
}

PUBLIC_SIGNAL_WEIGHTS = {
    "collaboration_intent": 8.0,
    "facility_or_product_expansion": 6.0,
    "research_investment": 5.0,
    "institutional_collaboration": 5.0,
    "technical_participation": 3.0,
    "certification_or_regulatory_progress": 3.0,
}

PROCUREMENT_WEIGHTS = {
    "requirement_fit": 8.0,
    "budget_or_scale_fit": 6.0,
    "relevant_award_history": 6.0,
    "provider_relationship": 4.0,
    "recency_or_deadline": 4.0,
    "repeat_or_renewal_signal": 2.0,
}

DEFAULT_GRADE_BANDS = (
    (85.0, "Priority 1", "Validate immediately; prepare a tailored engagement case."),
    (70.0, "Priority 2", "Perform focused validation and prepare a recipient-specific case."),
    (55.0, "Priority 3", "Keep in the active longlist and close decisive evidence gaps."),
    (40.0, "Watchlist", "Monitor and validate before allocating engagement resources."),
    (0.0, "Low current priority", "Do not prioritize without new evidence or a changed scope."),
)


class ScoringError(ValueError):
    """Raised when a score would be methodologically invalid."""


@dataclass(frozen=True)
class MetricObservation:
    """One normalized metric with evidence and uncertainty.

    ``value`` and sensitivity bounds use 0..1. ``None`` means not scored.
    """

    value: float | None
    evidence_ids: tuple[str, ...] = ()
    method: str = ""
    as_of: str = ""
    confidence: str = "not_assessed"
    quality: str = "not_assessed"
    lower: float | None = None
    upper: float | None = None
    missing_reason: str = ""
    notes: str = ""

    def validate(self, name: str) -> None:
        if self.value is None:
            if self.evidence_ids:
                raise ScoringError(f"{name}: missing value cannot carry scored evidence")
            if not self.missing_reason:
                raise ScoringError(f"{name}: missing metric requires missing_reason")
            return
        _unit_interval(self.value, f"{name}.value")
        if not self.evidence_ids:
            raise ScoringError(f"{name}: scored metric requires evidence_ids")
        if not self.method.strip():
            raise ScoringError(f"{name}: scored metric requires a normalization method")
        if not self.as_of.strip():
            raise ScoringError(f"{name}: scored metric requires an as_of date")
        if self.lower is not None:
            _unit_interval(self.lower, f"{name}.lower")
        if self.upper is not None:
            _unit_interval(self.upper, f"{name}.upper")
        lower = self.value if self.lower is None else self.lower
        upper = self.value if self.upper is None else self.upper
        if lower > self.value or upper < self.value or lower > upper:
            raise ScoringError(f"{name}: sensitivity bounds must contain value")


@dataclass(frozen=True)
class DimensionInput:
    """Metric observations for one evidence dimension."""

    metrics: Mapping[str, MetricObservation]
    applicable: bool = True
    not_applicable_reason: str = ""


@dataclass(frozen=True)
class DimensionResult:
    name: str
    maximum: float
    raw_score: float | None
    available_weight_score: float | None
    evidence_coverage: float
    sensitivity_low: float | None
    sensitivity_high: float | None
    evidence_ids: tuple[str, ...]
    missing_metrics: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class Eligibility:
    resolved_entity: bool = False
    allowed_recipient: bool = False
    relevant_business_unit: bool = False
    compliance_reviewed: bool = False
    notes: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return all((
            self.resolved_entity,
            self.allowed_recipient,
            self.relevant_business_unit,
            self.compliance_reviewed,
        ))


@dataclass(frozen=True)
class CandidateInput:
    company_name: str
    recipient_type: str
    relevant_business_unit: str
    patent: DimensionInput
    public_signal: DimensionInput
    procurement: DimensionInput
    eligibility: Eligibility
    reasons: tuple[str, ...] = ()
    evidence_gaps: tuple[str, ...] = ()
    next_actions: tuple[str, ...] = ()


@dataclass(frozen=True)
class MatchResult:
    company_name: str
    recipient_type: str
    relevant_business_unit: str
    dimensions: Mapping[str, DimensionResult]
    raw_total: float | None
    evidence_coverage: float
    sensitivity_low: float | None
    sensitivity_high: float | None
    grade_label: str
    action: str
    eligible: bool
    rankable: bool
    model_version: str
    reasons: tuple[str, ...] = ()
    evidence_gaps: tuple[str, ...] = ()
    next_actions: tuple[str, ...] = ()


def _unit_interval(value: float, label: str) -> float:
    if not isinstance(value, (int, float)) or not isfinite(float(value)):
        raise ScoringError(f"{label} must be a finite number")
    numeric = float(value)
    if not 0.0 <= numeric <= 1.0:
        raise ScoringError(f"{label} must be between 0 and 1")
    return numeric


def _validate_weight_map(weights: Mapping[str, float], expected_total: float, name: str) -> None:
    if not weights:
        raise ScoringError(f"{name}: weight map cannot be empty")
    for metric, weight in weights.items():
        if not isinstance(weight, (int, float)) or not isfinite(float(weight)) or weight < 0:
            raise ScoringError(f"{name}.{metric}: weight must be finite and nonnegative")
    if abs(sum(weights.values()) - expected_total) > 1e-7:
        raise ScoringError(f"{name}: weights must total {expected_total}")


def score_dimension(
    name: str,
    data: DimensionInput,
    metric_weights: Mapping[str, float],
    maximum: float,
) -> DimensionResult:
    """Score a dimension without converting missing observations to zero."""
    _validate_weight_map(metric_weights, maximum, name)
    unknown = set(data.metrics) - set(metric_weights)
    if unknown:
        raise ScoringError(f"{name}: unknown metrics: {sorted(unknown)}")
    if not data.applicable:
        if not data.not_applicable_reason:
            raise ScoringError(f"{name}: non-applicable dimension requires a reason")
        return DimensionResult(
            name=name,
            maximum=maximum,
            raw_score=None,
            available_weight_score=None,
            evidence_coverage=0.0,
            sensitivity_low=None,
            sensitivity_high=None,
            evidence_ids=(),
            missing_metrics=tuple(metric_weights),
            status="not_applicable",
        )

    raw = 0.0
    low = 0.0
    high = 0.0
    available_weight = 0.0
    evidence: set[str] = set()
    missing: list[str] = []
    for metric, weight in metric_weights.items():
        observation = data.metrics.get(metric)
        if observation is None:
            missing.append(metric)
            continue
        observation.validate(f"{name}.{metric}")
        if observation.value is None:
            missing.append(metric)
            continue
        available_weight += weight
        raw += observation.value * weight
        low += (observation.lower if observation.lower is not None else observation.value) * weight
        high += (observation.upper if observation.upper is not None else observation.value) * weight
        evidence.update(observation.evidence_ids)

    coverage = 0.0 if maximum == 0 else available_weight / maximum
    available_score = None if available_weight == 0 else raw / available_weight * maximum
    status = "scored" if available_weight else "not_scored"
    return DimensionResult(
        name=name,
        maximum=maximum,
        raw_score=round(raw, 2) if available_weight else None,
        available_weight_score=round(available_score, 2) if available_score is not None else None,
        evidence_coverage=round(coverage, 4),
        sensitivity_low=round(low, 2) if available_weight else None,
        sensitivity_high=round(high, 2) if available_weight else None,
        evidence_ids=tuple(sorted(evidence)),
        missing_metrics=tuple(missing),
        status=status,
    )


def grade(total: float | None, bands: Sequence[tuple[float, str, str]] = DEFAULT_GRADE_BANDS) -> tuple[str, str]:
    if total is None:
        return "Not scored", "Close evidence gaps before prioritization."
    for threshold, label, action in sorted(bands, reverse=True):
        if total >= threshold:
            return label, action
    return "Not scored", "Review the scoring configuration."


def score_candidate(
    candidate: CandidateInput,
    *,
    minimum_coverage: float = 0.70,
    model_version: str = "global-transfer-match-1.0",
    top_weights: Mapping[str, float] = BASELINE_WEIGHTS,
) -> MatchResult:
    """Score one candidate and apply eligibility/evidence gates."""
    _unit_interval(minimum_coverage, "minimum_coverage")
    _validate_weight_map(top_weights, 100.0, "top_weights")
    dimensions = {
        "patent": score_dimension("patent", candidate.patent, PATENT_WEIGHTS, 40.0),
        "public_signal": score_dimension("public_signal", candidate.public_signal, PUBLIC_SIGNAL_WEIGHTS, 30.0),
        "procurement": score_dimension("procurement", candidate.procurement, PROCUREMENT_WEIGHTS, 30.0),
    }

    # Top-level weights may change, so convert each dimension to a 0..1 raw
    # contribution based on all configured metrics. Missing remains uncovered.
    total = 0.0
    low = 0.0
    high = 0.0
    covered = 0.0
    applicable_weight = 0.0
    for name, top_weight in top_weights.items():
        result = dimensions[name]
        if result.status == "not_applicable":
            continue
        applicable_weight += top_weight
        covered += top_weight * result.evidence_coverage
        if result.raw_score is not None:
            total += top_weight * (result.raw_score / result.maximum)
            low += top_weight * ((result.sensitivity_low or 0.0) / result.maximum)
            high += top_weight * ((result.sensitivity_high or 0.0) / result.maximum)

    evidence_coverage = 0.0 if applicable_weight == 0 else covered / applicable_weight
    has_score = any(result.raw_score is not None for result in dimensions.values())
    raw_total = round(total, 2) if has_score else None
    label, action = grade(raw_total)
    weighted_not_applicable = tuple(
        name
        for name, weight in top_weights.items()
        if weight > 0 and dimensions[name].status == "not_applicable"
    )
    rankable = (
        candidate.eligibility.passed
        and evidence_coverage >= minimum_coverage
        and has_score
        and not weighted_not_applicable
    )
    if weighted_not_applicable:
        label = "Scoring model redesign required"
        action = (
            "Approve a new 100-point weight model that excludes the non-applicable "
            f"dimension(s): {', '.join(weighted_not_applicable)}."
        )
    elif not candidate.eligibility.passed:
        label = "Eligibility review required"
        action = "Resolve entity, business-unit and compliance gates before ranking."
    elif evidence_coverage < minimum_coverage:
        label = "Insufficient evidence coverage"
        action = "Close material evidence gaps before ranking."

    return MatchResult(
        company_name=candidate.company_name,
        recipient_type=candidate.recipient_type,
        relevant_business_unit=candidate.relevant_business_unit,
        dimensions=dimensions,
        raw_total=raw_total,
        evidence_coverage=round(evidence_coverage, 4),
        sensitivity_low=round(low, 2) if has_score else None,
        sensitivity_high=round(high, 2) if has_score else None,
        grade_label=label,
        action=action,
        eligible=candidate.eligibility.passed,
        rankable=rankable,
        model_version=model_version,
        reasons=candidate.reasons,
        evidence_gaps=candidate.evidence_gaps,
        next_actions=candidate.next_actions,
    )


def rank_candidates(results: Iterable[MatchResult], top_n: int = 10) -> list[MatchResult]:
    """Rank comparable candidates; retain unrankable items after them."""
    if top_n < 1:
        raise ScoringError("top_n must be at least 1")
    values = list(results)
    eligible = sorted(
        (item for item in values if item.rankable),
        key=lambda item: (-(item.raw_total or 0.0), -item.evidence_coverage, item.company_name.casefold()),
    )[:top_n]
    unrankable = sorted(
        (item for item in values if not item.rankable),
        key=lambda item: item.company_name.casefold(),
    )
    return eligible + unrankable


def rescore_with_weights(
    candidate: CandidateInput,
    scenarios: Mapping[str, Mapping[str, float]],
    *,
    minimum_coverage: float = 0.70,
) -> dict[str, MatchResult]:
    """Run disclosed weight scenarios for rank-sensitivity analysis."""
    output = {}
    for name, weights in scenarios.items():
        output[name] = score_candidate(
            candidate,
            minimum_coverage=minimum_coverage,
            model_version=f"global-transfer-match-1.0:{name}",
            top_weights=weights,
        )
    return output


def markdown(result: MatchResult, rank: int | None = None) -> str:
    heading = f"### {rank}. {result.company_name}" if rank is not None else f"### {result.company_name}"
    rows = []
    for name, dimension in result.dimensions.items():
        score = "Not scored" if dimension.raw_score is None else f"{dimension.raw_score:.2f}/{dimension.maximum:.0f}"
        rows.append(f"| {name.replace('_', ' ').title()} | {score} | {dimension.evidence_coverage:.0%} | {dimension.status} |")
    total = "Not scored" if result.raw_total is None else f"{result.raw_total:.2f}/100"
    reasons = "\n".join(f"- {item}" for item in result.reasons) or "- No supported reason supplied."
    gaps = "\n".join(f"- {item}" for item in result.evidence_gaps) or "- None recorded."
    actions = "\n".join(f"- {item}" for item in result.next_actions) or f"- {result.action}"
    return f"""{heading}

| Dimension | Raw score | Evidence coverage | Status |
|---|---:|---:|---|
{chr(10).join(rows)}

**Total:** {total}  
**Overall evidence coverage:** {result.evidence_coverage:.0%}  
**Sensitivity interval:** {result.sensitivity_low}–{result.sensitivity_high}  
**Priority label:** {result.grade_label}  
**Eligible/rankable:** {result.eligible}/{result.rankable}  
**Model:** `{result.model_version}`

**Supported reasons**

{reasons}

**Evidence gaps**

{gaps}

**Next validation actions**

{actions}
"""


def _fixture_observation(value: float, evidence_id: str) -> MetricObservation:
    return MetricObservation(
        value=value,
        evidence_ids=(evidence_id,),
        method="Synthetic fixture; linear 0..1 anchor",
        as_of="2026-08-07",
        confidence="synthetic",
        quality="synthetic",
        lower=max(0.0, value - 0.1),
        upper=min(1.0, value + 0.1),
    )


def synthetic_fixture() -> CandidateInput:
    """Return non-factual data for local deterministic tests."""
    patent = DimensionInput({name: _fixture_observation(0.7, f"P-{i}") for i, name in enumerate(PATENT_WEIGHTS, 1)})
    public = DimensionInput({name: _fixture_observation(0.6, f"N-{i}") for i, name in enumerate(PUBLIC_SIGNAL_WEIGHTS, 1)})
    procurement_metrics = {
        name: MetricObservation(value=None, missing_reason="Synthetic procurement evidence unavailable")
        for name in PROCUREMENT_WEIGHTS
    }
    return CandidateInput(
        company_name="Example Recipient, Inc.",
        recipient_type="Joint-development candidate",
        relevant_business_unit="Example R&D unit",
        patent=patent,
        public_signal=public,
        procurement=DimensionInput(procurement_metrics, applicable=False, not_applicable_reason="Not relevant to fixture"),
        eligibility=Eligibility(True, True, True, True),
        reasons=("Synthetic technical fit.", "Synthetic public R&D signal."),
        evidence_gaps=("No real evidence; fixture only.",),
        next_actions=("Replace every fixture value with sourced evidence.",),
    )


if __name__ == "__main__":
    fixture = synthetic_fixture()
    result = score_candidate(fixture, minimum_coverage=0.65)
    print(markdown(result, rank=1))
