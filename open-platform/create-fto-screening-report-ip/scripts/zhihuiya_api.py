"""Global PatSnap Open Platform REST client for the FTO screening package.

The source filename is retained for exact topology. All runtime names,
endpoints, authentication, messages, and documentation in this localized file
refer to the global PatSnap service.

Supported source capabilities:

* P070 Keyword Assistant
* P002 query-based patent search
* P018 claim data
* AI07 supporting analysis
* P025 technical-summary fallback (never a claim substitute)

Security properties:

* API keys are sent only as a Bearer Authorization header;
* HTTPS is mandatory;
* no key is included in repr, logs, exceptions, URLs, or returned provenance;
* redirects are rejected so Authorization cannot cross hosts;
* transient requests use bounded retry and backoff;
* dry-run/network authorization is controlled by the runner.

This client retrieves data. It does not determine claim construction,
infringement, validity, enforceability, or freedom to operate.
"""

from __future__ import annotations

import html
import json
import logging
import random
import re
import time
from dataclasses import dataclass
from typing import Any, Iterable
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:  # Offline rendering remains available in minimal document runtimes.
    requests = None  # type: ignore[assignment]


logger = logging.getLogger(__name__)

BASE_URL = "https://connect.patsnap.com"
P002_PATH = "/search/patent/query-search-patent/v2"
P070_PATH = "/search/patent/keyword-suggest"
P018_PATH = "/basic-patent-data/claim-data"
AI07_PATH = "/chat/cc-gpt-stream"
P025_PATH = "/high-value-data/tech-problem-and-benefit-summary"

TRANSIENT_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}
SENSITIVE_KEY_NAMES = {
    "authorization",
    "apikey",
    "api_key",
    "patsnap_api_key",
    "token",
    "access_token",
    "client_secret",
}


def _strip_claim_html(text: str) -> str:
    """Convert a claim HTML fragment to readable text without joining words."""

    if not text:
        return ""
    value = re.sub(r"(?i)<br\s*/?>", "\n", str(text))
    value = re.sub(r"(?i)</(?:div|p|li|tr)\s*>", "\n", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value).replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", item).strip() for item in value.splitlines()]
    return "\n".join(item for item in lines if item)


def _redacted(value: Any) -> Any:
    """Return a recursively sanitized object suitable for diagnostics."""

    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if str(key).lower() in SENSITIVE_KEY_NAMES else _redacted(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redacted(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_redacted(item) for item in value)
    return value


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None


def _extract_data(envelope: Any, endpoint: str) -> Any:
    """Validate a PatSnap response envelope and return its data member."""

    if not isinstance(envelope, dict):
        raise PatSnapApiError(endpoint, "invalid_response", "Response JSON is not an object.")
    status = _as_bool(envelope.get("status"))
    error_code = envelope.get("error_code", envelope.get("code", 0))
    error_message = str(envelope.get("error_msg") or envelope.get("message") or "")
    if status is False or error_code not in {None, 0, "0", ""}:
        raise PatSnapApiError(endpoint, error_code, error_message or "PatSnap returned an error.")
    if "data" not in envelope:
        raise PatSnapApiError(endpoint, "invalid_response", "Response is missing the data field.")
    return envelope.get("data")


@dataclass(frozen=True)
class RequestEvidence:
    """Sanitized metadata for a completed request."""

    method: str
    endpoint: str
    attempt_count: int
    http_status: int
    elapsed_seconds: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": "PatSnap Open Platform",
            "mode": "rest",
            "method": self.method,
            "endpoint": self.endpoint,
            "attempt_count": self.attempt_count,
            "http_status": self.http_status,
            "elapsed_seconds": round(self.elapsed_seconds, 3),
        }


class PatSnapApiError(RuntimeError):
    """Sanitized PatSnap business, protocol, or transport error."""

    def __init__(self, endpoint: str, error_code: Any, error_message: str):
        self.endpoint = endpoint
        self.error_code = error_code
        self.error_message = str(error_message or "Unknown API error")
        super().__init__(f"PatSnap request failed at {endpoint}: {self.error_message} (code={error_code})")


class PatSnapClient:
    """Bounded global PatSnap REST client using Bearer API-key authentication."""

    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        connect_timeout: float = 10,
        read_timeout: float = 60,
        max_retries: int = 2,
        retry_backoff: float = 1.0,
        session: requests.Session | None = None,
    ):
        if requests is None:
            raise RuntimeError("REST mode requires the 'requests' package; offline and dry-run modes do not.")
        key = str(api_key or "").strip()
        if not key or key == "PUT_YOUR_PATSNAP_API_KEY_HERE":
            raise ValueError("A private PatSnap API key is required; replace the placeholder locally.")
        parsed = urlparse(str(base_url or ""))
        if parsed.scheme.lower() != "https" or not parsed.netloc:
            raise ValueError("PatSnap base URL must be an absolute HTTPS URL.")
        self._api_key = key
        self.base_url = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
        self.connect_timeout = max(0.1, float(connect_timeout))
        self.read_timeout = max(0.1, float(read_timeout))
        self.max_retries = max(0, int(max_retries))
        self.retry_backoff = max(0.0, float(retry_backoff))
        self.session = session or requests.Session()
        self.last_request_evidence: RequestEvidence | None = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(base_url={self.base_url!r}, "
            f"connect_timeout={self.connect_timeout!r}, read_timeout={self.read_timeout!r}, "
            f"max_retries={self.max_retries!r}, credential='[redacted]')"
        )

    def _headers(self, *, accept: str = "application/json") -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": accept,
            "Content-Type": "application/json",
            "User-Agent": "PatSnap-FTO-Screening-Skill/2.0",
        }

    def _url(self, path: str) -> str:
        if not str(path).startswith("/"):
            raise ValueError("API path must begin with '/'.")
        url = urljoin(self.base_url + "/", str(path).lstrip("/"))
        parsed = urlparse(url)
        base = urlparse(self.base_url)
        if parsed.scheme != "https" or parsed.netloc != base.netloc:
            raise ValueError("API path resolved outside the approved PatSnap host.")
        return url

    def _sleep_before_retry(self, attempt: int, response: requests.Response | None) -> None:
        retry_after: float | None = None
        if response is not None:
            raw = response.headers.get("Retry-After", "").strip()
            try:
                retry_after = max(0.0, float(raw)) if raw else None
            except ValueError:
                retry_after = None
        delay = retry_after if retry_after is not None else self.retry_backoff * (2 ** max(0, attempt - 1))
        if delay:
            delay += random.uniform(0, min(0.25, delay * 0.1))
            time.sleep(delay)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        stream: bool = False,
    ) -> requests.Response:
        url = self._url(path)
        started = time.monotonic()
        last_error: Exception | None = None
        response: requests.Response | None = None
        for attempt in range(1, self.max_retries + 2):
            try:
                response = self.session.request(
                    method.upper(),
                    url,
                    params=params or None,
                    json=payload if payload is not None else None,
                    headers=self._headers(accept="text/event-stream, application/json" if stream else "application/json"),
                    timeout=(self.connect_timeout, self.read_timeout),
                    stream=stream,
                    allow_redirects=False,
                )
                if 300 <= response.status_code < 400:
                    raise PatSnapApiError(path, response.status_code, "Redirect rejected to protect credentials.")
                if response.status_code in TRANSIENT_HTTP_STATUS and attempt <= self.max_retries:
                    self._sleep_before_retry(attempt, response)
                    continue
                response.raise_for_status()
                self.last_request_evidence = RequestEvidence(
                    method=method.upper(),
                    endpoint=path,
                    attempt_count=attempt,
                    http_status=response.status_code,
                    elapsed_seconds=time.monotonic() - started,
                )
                return response
            except PatSnapApiError:
                raise
            except requests.RequestException as exc:
                last_error = exc
                status = getattr(response, "status_code", "transport_error")
                if attempt <= self.max_retries and (response is None or status in TRANSIENT_HTTP_STATUS):
                    self._sleep_before_retry(attempt, response)
                    continue
                message = type(exc).__name__
                if response is not None:
                    message = f"HTTP {response.status_code}"
                raise PatSnapApiError(path, status, message) from exc
        raise PatSnapApiError(path, "transport_error", type(last_error).__name__ if last_error else "Unknown error")

    def _json(self, response: requests.Response, path: str) -> dict[str, Any]:
        content_type = response.headers.get("Content-Type", "").lower()
        if "json" not in content_type and response.content:
            raise PatSnapApiError(path, "invalid_content_type", f"Expected JSON; received {content_type or 'unknown'}.")
        try:
            value = response.json()
        except (ValueError, json.JSONDecodeError) as exc:
            raise PatSnapApiError(path, "invalid_json", "Response body is not valid JSON.") from exc
        if not isinstance(value, dict):
            raise PatSnapApiError(path, "invalid_response", "Response JSON is not an object.")
        return value

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self._request("POST", path, payload=payload)
        return self._json(response, path)

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._request("GET", path, params=params)
        return self._json(response, path)

    def expand_keywords(
        self,
        keyword: str | Iterable[str],
        *,
        languages: Iterable[str] = ("en",),
        relation_types: Iterable[str] = ("synonym", "related"),
        max_words: int | None = None,
    ) -> list[str]:
        """Return reviewed-candidate terms from P070, including input terms."""

        inputs = [str(item).strip() for item in ([keyword] if isinstance(keyword, str) else keyword) if str(item).strip()]
        if not inputs:
            return []
        envelope = self._post(
            P070_PATH,
            {
                "keyword": inputs,
                "lang": [str(item).lower() for item in languages],
                "type": [str(item).lower() for item in relation_types],
            },
        )
        data = _extract_data(envelope, P070_PATH)
        items = data.get("items", []) if isinstance(data, dict) else []
        ordered: list[str] = []
        seen: set[str] = set()

        def retain(value: Any) -> None:
            text = str(value or "").strip()
            key = text.casefold()
            if text and key not in seen:
                seen.add(key)
                ordered.append(text)

        for value in inputs:
            retain(value)
        for item in items if isinstance(items, list) else []:
            if not isinstance(item, dict):
                continue
            retain(item.get("input"))
            values = item.get("keyword_list") or []
            for candidate in values if isinstance(values, list) else []:
                retain(candidate.get("keyword") if isinstance(candidate, dict) else candidate)
        return ordered[: max(0, int(max_words))] if max_words is not None else ordered

    def search_patents(
        self,
        query: str,
        *,
        limit: int = 100,
        offset: int = 0,
        stemming: int = 0,
        sort: list[dict[str, str]] | None = None,
        collapse_by: str = "PBD",
        collapse_type: str = "ALL",
        collapse_order: str = "LATEST",
        collapse_order_authority: list[str] | None = None,
    ) -> dict[str, Any]:
        """Run one P002 page and return normalized envelope data."""

        text = str(query or "").strip()
        if not text:
            raise ValueError("P002 query must not be empty.")
        if limit <= 0 or offset < 0:
            raise ValueError("P002 limit must be positive and offset must be non-negative.")
        payload: dict[str, Any] = {
            "query_text": text,
            "limit": int(limit),
            "offset": int(offset),
            "sort": sort or [{"field": "SCORE", "order": "DESC"}],
            "stemming": int(stemming),
            "collapse_by": collapse_by,
            "collapse_type": collapse_type,
            "collapse_order": collapse_order,
            "collapse_order_authority": collapse_order_authority or ["US", "EP", "JP", "KR", "CN"],
        }
        envelope = self._post(P002_PATH, payload)
        data = _extract_data(envelope, P002_PATH)
        if not isinstance(data, dict):
            raise PatSnapApiError(P002_PATH, "invalid_response", "P002 data is not an object.")
        results = data.get("results") or []
        if not isinstance(results, list):
            raise PatSnapApiError(P002_PATH, "invalid_response", "P002 data.results is not an array.")
        return {
            "results": results,
            "total": data.get("total", data.get("total_count")),
            "limit": int(limit),
            "offset": int(offset),
            "request_evidence": self.last_request_evidence.as_dict() if self.last_request_evidence else {},
        }

    def search_all_patents(
        self,
        query: str,
        *,
        max_total: int = 500,
        page_size: int = 100,
        stemming: int = 0,
        collapse_order_authority: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Collect bounded P002 pages while detecting repeated results."""

        maximum = max(0, int(max_total))
        size = max(1, min(int(page_size), maximum or int(page_size)))
        collected: list[dict[str, Any]] = []
        seen_page_signatures: set[tuple[str, ...]] = set()
        offset = 0
        while len(collected) < maximum:
            page = self.search_patents(
                query,
                limit=min(size, maximum - len(collected)),
                offset=offset,
                stemming=stemming,
                collapse_order_authority=collapse_order_authority,
            )
            records = page["results"]
            signature = tuple(
                str(item.get("patent_id") or item.get("pn") or item.get("publication_number") or index)
                for index, item in enumerate(records)
                if isinstance(item, dict)
            )
            if signature in seen_page_signatures and signature:
                raise PatSnapApiError(P002_PATH, "repeated_page", f"P002 repeated a prior page at offset {offset}.")
            seen_page_signatures.add(signature)
            collected.extend(item for item in records if isinstance(item, dict))
            if len(records) < page["limit"]:
                break
            total = page.get("total")
            if isinstance(total, int) and len(collected) >= total:
                break
            offset += page["limit"]
        return collected[:maximum]

    def get_claim_records(
        self,
        *,
        patent_number: str = "",
        patent_id: str = "",
        replace_by_related: bool = False,
    ) -> list[dict[str, Any]]:
        """Retrieve raw P018 claim records with explicit replacement policy."""

        number = str(patent_number or "").strip()
        identifier = str(patent_id or "").strip()
        if not number and not identifier:
            raise ValueError("P018 requires patent_number or patent_id.")
        params: dict[str, Any] = {"replace_by_related": "1" if replace_by_related else "0"}
        if identifier:
            params["patent_id"] = identifier
        else:
            params["patent_number"] = number
        envelope = self._get(P018_PATH, params)
        data = _extract_data(envelope, P018_PATH)
        if not isinstance(data, list):
            raise PatSnapApiError(P018_PATH, "invalid_response", "P018 data is not an array.")
        return [item for item in data if isinstance(item, dict)]

    def get_claims(
        self,
        patent_number: str,
        *,
        language: str = "EN",
        replace_by_related: bool = False,
    ) -> list[str]:
        """Return readable claim-text records for one patent number."""

        records = self.get_claim_records(
            patent_number=patent_number,
            replace_by_related=replace_by_related,
        )
        preferred = str(language or "EN").upper()
        claims: list[str] = []
        fallback: list[str] = []
        for record in records:
            containers = record.get("claims") or []
            if isinstance(containers, dict):
                containers = [containers]
            for item in containers if isinstance(containers, list) else []:
                if not isinstance(item, dict):
                    continue
                raw = item.get("claim_text") or item.get("text") or ""
                text = _strip_claim_html(str(raw))
                if not text:
                    continue
                fallback.append(text)
                if str(item.get("lang") or "").upper() == preferred:
                    claims.append(text)
        return claims or fallback

    def get_claims_batch(
        self,
        patent_numbers: list[str],
        *,
        language: str = "EN",
        replace_by_related: bool = False,
        batch_size: int = 100,
    ) -> dict[str, list[str]]:
        """Retrieve claims in documented batches while retaining missing entries."""

        numbers = list(dict.fromkeys(str(item).strip() for item in patent_numbers if str(item).strip()))
        output: dict[str, list[str]] = {number: [] for number in numbers}
        size = max(1, min(100, int(batch_size)))
        for start in range(0, len(numbers), size):
            batch = numbers[start : start + size]
            records = self.get_claim_records(
                patent_number=",".join(batch),
                replace_by_related=replace_by_related,
            )
            for record in records:
                number = str(record.get("pn") or record.get("patent_number") or "").strip()
                if not number:
                    continue
                containers = record.get("claims") or []
                if isinstance(containers, dict):
                    containers = [containers]
                preferred_text: list[str] = []
                fallback_text: list[str] = []
                for item in containers if isinstance(containers, list) else []:
                    if not isinstance(item, dict):
                        continue
                    text = _strip_claim_html(str(item.get("claim_text") or item.get("text") or ""))
                    if text:
                        fallback_text.append(text)
                        if str(item.get("lang") or "").upper() == language.upper():
                            preferred_text.append(text)
                output[number] = preferred_text or fallback_text
        return output

    def call_ai07(self, prompt: str, *, stream: bool = True) -> dict[str, Any]:
        """Call AI07 and return raw/assembled supporting output."""

        text = str(prompt or "").strip()
        if not text:
            raise ValueError("AI07 prompt must not be empty.")
        response = self._request("POST", AI07_PATH, payload={"prompt": text, "stream": bool(stream)}, stream=bool(stream))
        if not stream:
            envelope = self._json(response, AI07_PATH)
            return {
                "raw": envelope,
                "text": str(envelope.get("text") or envelope.get("content") or ""),
                "request_evidence": self.last_request_evidence.as_dict() if self.last_request_evidence else {},
            }
        events: list[Any] = []
        text_parts: list[str] = []
        for raw_line in response.iter_lines(decode_unicode=True):
            line = str(raw_line or "").strip()
            if not line or line.startswith(":"):
                continue
            if line.startswith("data:"):
                line = line[5:].strip()
            if line in {"[DONE]", "DONE"}:
                break
            try:
                event: Any = json.loads(line)
            except json.JSONDecodeError:
                event = line
            events.append(event)
            if isinstance(event, str):
                text_parts.append(event)
            elif isinstance(event, dict):
                candidate = event.get("text") or event.get("content") or event.get("answer") or event.get("delta")
                if isinstance(candidate, str):
                    text_parts.append(candidate)
                elif isinstance(candidate, dict) and isinstance(candidate.get("content"), str):
                    text_parts.append(candidate["content"])
        return {
            "raw_events": events,
            "text": "".join(text_parts),
            "request_evidence": self.last_request_evidence.as_dict() if self.last_request_evidence else {},
            "boundary": "AI07 output is supporting evidence and requires structured and human review.",
        }

    def get_tech_summary(self, patent_number: str, *, language: str = "en") -> dict[str, Any]:
        """Retrieve P025 technical summary; never present it as claim text."""

        number = str(patent_number or "").strip()
        if not number:
            raise ValueError("P025 requires a patent number.")
        envelope = self._get(P025_PATH, {"patent_number": number, "lang": language})
        data = _extract_data(envelope, P025_PATH)
        return {
            "data": data if isinstance(data, dict) else {"value": data},
            "request_evidence": self.last_request_evidence.as_dict() if self.last_request_evidence else {},
            "boundary": "Technical summary evidence is not claim text and cannot replace P018.",
        }


# Backward-compatible source names so the source runner/import pattern remains valid.
ZhihuiyaApiError = PatSnapApiError
ZhihuiyaClient = PatSnapClient


__all__ = [
    "AI07_PATH",
    "BASE_URL",
    "P002_PATH",
    "P018_PATH",
    "P025_PATH",
    "P070_PATH",
    "PatSnapApiError",
    "PatSnapClient",
    "RequestEvidence",
    "ZhihuiyaApiError",
    "ZhihuiyaClient",
    "_strip_claim_html",
]
