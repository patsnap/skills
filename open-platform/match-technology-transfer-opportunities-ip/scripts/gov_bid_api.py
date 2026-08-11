"""Provider-neutral procurement evidence adapter.

The filename preserves the source package topology. The localized module does
not call gov-bid.com or any other network service, contains no credential, and
does not assume Chinese province/industry codes. It validates and normalizes
records already retrieved from an authorized, documented regional provider.

Integration pattern
-------------------
1. Obtain user authorization for a specific procurement source.
2. Verify that provider's current endpoint, terms, authentication and schema.
3. Retrieve outside this module using an approved connector/client.
4. map provider fields with ``ProviderMapping``;
5. normalize through ``normalize_records``; and
6. retain the returned provenance and validation issues.

Never put an API key in this file, a query URL, a report, or a fixture.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlparse


class ProcurementDataError(ValueError):
    """Raised when provider data cannot be normalized safely."""


ALLOWED_ROLES = {
    "buyer",
    "supplier",
    "awardee",
    "contracting_authority",
    "agency",
    "unknown",
}

ALLOWED_STAGES = {
    "planned",
    "open",
    "closed",
    "awarded",
    "contracted",
    "cancelled",
    "unknown",
}

ISO_CURRENCY = re.compile(r"^[A-Z]{3}$")
ISO_COUNTRY = re.compile(r"^[A-Z]{2}$")


@dataclass(frozen=True)
class ProviderMapping:
    """Map a verified provider schema into the normalized contract."""

    provider_name: str
    provider_record_id: str
    title: str
    publication_date: str
    url: str
    country: str
    stage: str = ""
    deadline: str = ""
    description: str = ""
    buyer_name: str = ""
    supplier_names: str = ""
    agency_name: str = ""
    amount: str = ""
    currency: str = ""
    region: str = ""
    classification: str = ""
    source_document_url: str = ""
    retrieved_at: str = ""

    def required_fields(self) -> tuple[str, ...]:
        return (
            self.provider_record_id,
            self.title,
            self.publication_date,
            self.url,
            self.country,
        )


@dataclass(frozen=True)
class Party:
    name: str
    role: str
    identifier: str = ""
    country: str = ""
    evidence_locator: str = ""


@dataclass(frozen=True)
class Money:
    amount: str
    currency: str
    amount_type: str = "reported"
    converted_amount: str = ""
    converted_currency: str = ""
    conversion_date: str = ""
    conversion_source: str = ""


@dataclass(frozen=True)
class ProcurementRecord:
    record_id: str
    provider: str
    provider_record_id: str
    title: str
    description: str
    publication_date: str
    deadline: str
    stage: str
    country: str
    region: str
    classifications: tuple[str, ...]
    parties: tuple[Party, ...]
    money: Money | None
    url: str
    source_document_url: str
    retrieved_at: str
    relevance_terms: tuple[str, ...] = ()
    relevance_notes: str = ""
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationIssue:
    record_number: int
    severity: str
    field: str
    message: str


@dataclass(frozen=True)
class NormalizationResult:
    records: tuple[ProcurementRecord, ...]
    issues: tuple[ValidationIssue, ...]
    provider: str
    input_count: int
    output_count: int
    generated_at: str


def get_path(record: Mapping[str, Any], path: str, default: Any = None) -> Any:
    """Resolve a dot-separated mapping path without executing expressions."""
    if not path:
        return default
    value: Any = record
    for part in path.split("."):
        if not isinstance(value, Mapping) or part not in value:
            return default
        value = value[part]
    return value


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return "; ".join(clean_text(item) for item in value if clean_text(item))
    return " ".join(str(value).split())


def safe_url(value: Any) -> str:
    candidate = clean_text(value)
    parsed = urlparse(candidate)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    return candidate


def iso_date(value: Any, field_name: str, *, required: bool = False) -> str:
    candidate = clean_text(value)
    if not candidate:
        if required:
            raise ProcurementDataError(f"{field_name} is required")
        return ""
    if "T" in candidate:
        candidate = candidate.split("T", 1)[0]
    try:
        return date.fromisoformat(candidate).isoformat()
    except ValueError as exc:
        raise ProcurementDataError(f"{field_name} must use ISO YYYY-MM-DD: {candidate!r}") from exc


def iso_country(value: Any) -> str:
    candidate = clean_text(value).upper()
    if not ISO_COUNTRY.fullmatch(candidate):
        raise ProcurementDataError(f"country must be ISO 3166-1 alpha-2: {candidate!r}")
    return candidate


def currency_code(value: Any) -> str:
    candidate = clean_text(value).upper()
    if not ISO_CURRENCY.fullmatch(candidate):
        raise ProcurementDataError(f"currency must be a three-letter ISO 4217 code: {candidate!r}")
    return candidate


def decimal_amount(value: Any) -> str:
    candidate = clean_text(value).replace(",", "")
    if not candidate:
        return ""
    try:
        number = Decimal(candidate)
    except InvalidOperation as exc:
        raise ProcurementDataError(f"amount must be numeric: {candidate!r}") from exc
    if not number.is_finite() or number < 0:
        raise ProcurementDataError("amount must be finite and nonnegative")
    return format(number, "f")


def normalized_stage(value: Any) -> str:
    candidate = clean_text(value).lower().replace(" ", "_").replace("-", "_") or "unknown"
    if candidate not in ALLOWED_STAGES:
        return "unknown"
    return candidate


def split_values(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (list, tuple, set)):
        values = [clean_text(item) for item in value]
    else:
        values = [clean_text(item) for item in re.split(r"[;|]", clean_text(value))]
    return tuple(dict.fromkeys(item for item in values if item))


def build_parties(raw: Mapping[str, Any], mapping: ProviderMapping, country: str) -> tuple[Party, ...]:
    parties: list[Party] = []
    buyer = clean_text(get_path(raw, mapping.buyer_name))
    if buyer:
        parties.append(Party(name=buyer, role="buyer", country=country))
    for supplier in split_values(get_path(raw, mapping.supplier_names)):
        parties.append(Party(name=supplier, role="supplier", country=""))
    agency = clean_text(get_path(raw, mapping.agency_name))
    if agency:
        parties.append(Party(name=agency, role="agency", country=country))
    return tuple(parties)


def build_money(raw: Mapping[str, Any], mapping: ProviderMapping) -> Money | None:
    raw_amount = get_path(raw, mapping.amount)
    raw_currency = get_path(raw, mapping.currency)
    amount = decimal_amount(raw_amount)
    currency = clean_text(raw_currency)
    if not amount and not currency:
        return None
    if not amount or not currency:
        raise ProcurementDataError("amount and currency must be supplied together")
    return Money(amount=amount, currency=currency_code(currency))


def normalize_record(
    raw: Mapping[str, Any],
    mapping: ProviderMapping,
    number: int,
    *,
    default_retrieved_at: str,
) -> ProcurementRecord:
    if not isinstance(raw, Mapping):
        raise ProcurementDataError("record must be an object")
    provider_id = clean_text(get_path(raw, mapping.provider_record_id))
    title = clean_text(get_path(raw, mapping.title))
    publication_date = iso_date(get_path(raw, mapping.publication_date), "publication_date", required=True)
    url = safe_url(get_path(raw, mapping.url))
    country = iso_country(get_path(raw, mapping.country))
    if not provider_id:
        raise ProcurementDataError("provider_record_id is required")
    if not title:
        raise ProcurementDataError("title is required")
    if not url:
        raise ProcurementDataError("url must be a safe absolute HTTP(S) URL")

    retrieved = iso_date(get_path(raw, mapping.retrieved_at), "retrieved_at") or default_retrieved_at
    record_id = f"PROC-{mapping.provider_name}-{provider_id}"
    record_id = re.sub(r"[^A-Za-z0-9._:-]+", "-", record_id)
    source_document = safe_url(get_path(raw, mapping.source_document_url))
    limitations: list[str] = []
    if mapping.source_document_url and not source_document:
        limitations.append("Provider source-document URL was absent or unsafe.")
    stage_raw = get_path(raw, mapping.stage)
    stage = normalized_stage(stage_raw)
    if clean_text(stage_raw) and stage == "unknown":
        limitations.append(f"Unmapped provider stage: {clean_text(stage_raw)}")

    return ProcurementRecord(
        record_id=record_id,
        provider=mapping.provider_name,
        provider_record_id=provider_id,
        title=title,
        description=clean_text(get_path(raw, mapping.description)),
        publication_date=publication_date,
        deadline=iso_date(get_path(raw, mapping.deadline), "deadline"),
        stage=stage,
        country=country,
        region=clean_text(get_path(raw, mapping.region)),
        classifications=split_values(get_path(raw, mapping.classification)),
        parties=build_parties(raw, mapping, country),
        money=build_money(raw, mapping),
        url=url,
        source_document_url=source_document,
        retrieved_at=retrieved,
        limitations=tuple(limitations),
    )


def validate_mapping(mapping: ProviderMapping) -> None:
    if not mapping.provider_name.strip():
        raise ProcurementDataError("provider_name is required")
    if any(not path.strip() for path in mapping.required_fields()):
        raise ProcurementDataError("mapping requires ID, title, publication date, URL and country paths")


def normalize_records(
    payload: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    mapping: ProviderMapping,
    *,
    items_path: str = "",
    strict: bool = False,
    retrieved_at: str | None = None,
) -> NormalizationResult:
    """Normalize provider data without sending a network request."""
    validate_mapping(mapping)
    default_retrieved = iso_date(retrieved_at or date.today().isoformat(), "retrieved_at", required=True)
    raw_items: Any = get_path(payload, items_path) if items_path else payload
    if not isinstance(raw_items, Sequence) or isinstance(raw_items, (str, bytes, bytearray)):
        raise ProcurementDataError("payload/items_path must resolve to an array")

    records: list[ProcurementRecord] = []
    issues: list[ValidationIssue] = []
    seen: set[tuple[str, str]] = set()
    for number, raw in enumerate(raw_items, 1):
        try:
            normalized = normalize_record(raw, mapping, number, default_retrieved_at=default_retrieved)
            duplicate_key = (normalized.provider, normalized.provider_record_id)
            if duplicate_key in seen:
                issues.append(ValidationIssue(number, "warning", "provider_record_id", "Duplicate record omitted"))
                continue
            seen.add(duplicate_key)
            records.append(normalized)
        except (ProcurementDataError, TypeError) as exc:
            issues.append(ValidationIssue(number, "error", "record", str(exc)))
            if strict:
                raise ProcurementDataError(f"record {number}: {exc}") from exc

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return NormalizationResult(
        records=tuple(records),
        issues=tuple(issues),
        provider=mapping.provider_name,
        input_count=len(raw_items),
        output_count=len(records),
        generated_at=generated,
    )


def record_to_dict(record: ProcurementRecord) -> dict[str, Any]:
    return asdict(record)


def result_to_dict(result: NormalizationResult) -> dict[str, Any]:
    return {
        "provider": result.provider,
        "input_count": result.input_count,
        "output_count": result.output_count,
        "generated_at": result.generated_at,
        "records": [record_to_dict(item) for item in result.records],
        "issues": [asdict(item) for item in result.issues],
    }


def relevance_terms(record: ProcurementRecord, terms: Iterable[str]) -> tuple[str, ...]:
    """Return literal case-insensitive matches for auditable pre-screening."""
    haystack = f"{record.title} {record.description}".casefold()
    output = []
    for term in terms:
        normalized = clean_text(term)
        if normalized and normalized.casefold() in haystack:
            output.append(normalized)
    return tuple(dict.fromkeys(output))


def within_date_window(record: ProcurementRecord, start_date: str, end_date: str) -> bool:
    start = date.fromisoformat(iso_date(start_date, "start_date", required=True))
    end = date.fromisoformat(iso_date(end_date, "end_date", required=True))
    if start > end:
        raise ProcurementDataError("start_date must not exceed end_date")
    published = date.fromisoformat(record.publication_date)
    return start <= published <= end


def filter_records(
    records: Iterable[ProcurementRecord],
    *,
    start_date: str,
    end_date: str,
    countries: Iterable[str] = (),
    stages: Iterable[str] = (),
    terms: Iterable[str] = (),
) -> list[ProcurementRecord]:
    country_set = {iso_country(item) for item in countries}
    stage_set = {normalized_stage(item) for item in stages}
    term_list = tuple(terms)
    output = []
    for record in records:
        if not within_date_window(record, start_date, end_date):
            continue
        if country_set and record.country not in country_set:
            continue
        if stage_set and record.stage not in stage_set:
            continue
        if term_list and not relevance_terms(record, term_list):
            continue
        output.append(record)
    return output


def buyer_candidates(records: Iterable[ProcurementRecord]) -> dict[str, list[str]]:
    """Map buyer names to supporting procurement record IDs."""
    output: dict[str, list[str]] = {}
    for record in records:
        for party in record.parties:
            if party.role not in {"buyer", "contracting_authority"}:
                continue
            output.setdefault(party.name, []).append(record.record_id)
    return output


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_mapping(path: Path) -> ProviderMapping:
    raw = load_json(path)
    if not isinstance(raw, Mapping):
        raise ProcurementDataError("mapping file must contain an object")
    allowed = set(ProviderMapping.__dataclass_fields__)
    unknown = set(raw) - allowed
    if unknown:
        raise ProcurementDataError(f"unknown mapping fields: {sorted(unknown)}")
    return ProviderMapping(**raw)


def cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize authorized procurement JSON; this tool performs no network request."
    )
    parser.add_argument("input", type=Path, help="UTF-8 provider JSON")
    parser.add_argument("mapping", type=Path, help="UTF-8 ProviderMapping JSON")
    parser.add_argument("--items-path", default="", help="Optional dot path to the record array")
    parser.add_argument("--output", type=Path, help="Optional normalized JSON output")
    parser.add_argument("--strict", action="store_true", help="Fail on the first invalid record")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = cli_parser().parse_args(argv)
    try:
        result = normalize_records(
            load_json(args.input),
            load_mapping(args.mapping),
            items_path=args.items_path,
            strict=args.strict,
        )
        rendered = json.dumps(result_to_dict(result), ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, json.JSONDecodeError, ProcurementDataError, TypeError) as exc:
        print(f"procurement normalization failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
