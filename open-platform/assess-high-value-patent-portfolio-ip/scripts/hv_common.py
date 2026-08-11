#!/usr/bin/env python3
"""Shared secure helpers for the high-value patent screening pipeline.

The source filename and stage topology are retained. This localized module uses
the global PatSnap Connect host and Bearer authentication. It never persists a
credential, follows a redirect, or treats a failed request as factual zero.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import pathlib
import random
import time
import uuid
from dataclasses import dataclass
from typing import Any, Iterable, Iterator
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]


BASE = "https://connect.patsnap.com"
SCHEMA_VERSION = "2.0"
RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}
DEFAULT_CONNECT_TIMEOUT = 10.0
DEFAULT_READ_TIMEOUT = 90.0
_CREDENTIAL: str | None = None


class PatSnapRequestError(RuntimeError):
    """A safe request failure containing no credential or response body."""

    def __init__(self, path: str, message: str, *, status: int | None = None):
        self.path = path
        self.status = status
        super().__init__(f"PatSnap request failed at {path}: {message}" + (f" (HTTP {status})" if status else ""))


@dataclass(frozen=True)
class RequestEvidence:
    path: str
    method: str
    retrieved_at: str
    status: int
    attempt_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "method": self.method,
            "retrieved_at": self.retrieved_at,
            "http_status": self.status,
            "attempt_count": self.attempt_count,
        }


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def key() -> str:
    """Resolve a private API key without accepting a default working-dir file."""
    global _CREDENTIAL
    if _CREDENTIAL is not None:
        return _CREDENTIAL
    value = (os.environ.get("PATSNAP_API_KEY") or "").strip()
    key_file = (os.environ.get("PATSNAP_API_KEY_FILE") or "").strip()
    if not value and key_file:
        path = pathlib.Path(key_file).expanduser()
        if not path.is_file():
            raise RuntimeError("PATSNAP_API_KEY_FILE does not identify a readable file.")
        value = path.read_text(encoding="utf-8-sig").strip()
    if not value or value.lower().startswith(("replace", "example", "your_")):
        raise RuntimeError("Set PATSNAP_API_KEY or PATSNAP_API_KEY_FILE before REST retrieval.")
    _CREDENTIAL = value
    return value


def load_query() -> str:
    """Load one reviewed PatSnap query from an environment variable or explicit file."""
    query = (os.environ.get("HVP_QUERY") or "").strip()
    query_file = (os.environ.get("HVP_QUERY_FILE") or "").strip()
    if not query and query_file:
        path = pathlib.Path(query_file).expanduser()
        if not path.is_file():
            raise RuntimeError("HVP_QUERY_FILE does not identify a readable file.")
        query = path.read_text(encoding="utf-8-sig").strip()
    if not query:
        raise RuntimeError("Set HVP_QUERY or HVP_QUERY_FILE to a human-reviewed PatSnap query.")
    return query


def query_hash(query: str) -> str:
    return hashlib.sha256(query.encode("utf-8")).hexdigest()


def hjson() -> dict[str, str]:
    return {
        "Authorization": "Bearer " + key(),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "patsnap-high-value-screening/2.0",
    }


def hget() -> dict[str, str]:
    return {
        "Authorization": "Bearer " + key(),
        "Accept": "application/json",
        "User-Agent": "patsnap-high-value-screening/2.0",
    }


def _validate_base(base_url: str) -> str:
    parsed = urlparse(base_url)
    if parsed.scheme.lower() != "https" or not parsed.netloc:
        raise ValueError("PatSnap base URL must be an absolute HTTPS URL.")
    return f"{parsed.scheme}://{parsed.netloc}".rstrip("/")


def _validate_path(path: str) -> str:
    cleaned = "/" + str(path or "").lstrip("/")
    if "?" in cleaned or "#" in cleaned or ".." in cleaned:
        raise ValueError("API path must be a plain absolute service path.")
    return cleaned


def _extract_data(envelope: Any, path: str) -> Any:
    if not isinstance(envelope, dict):
        raise PatSnapRequestError(path, "response is not a JSON object")
    success = envelope.get("status")
    if success is False or success in (0, "0", "false", "False"):
        code = envelope.get("error_code") or envelope.get("code") or "unknown"
        message = envelope.get("error_message") or envelope.get("message") or "service returned failure"
        raise PatSnapRequestError(path, f"service error {code}: {message}")
    if "data" not in envelope:
        raise PatSnapRequestError(path, "response has no data field")
    return envelope["data"]


def _retry_delay(attempt: int, response: Any | None) -> float:
    if response is not None:
        header = response.headers.get("Retry-After")
        if header and str(header).isdigit():
            return min(30.0, float(header))
    return min(16.0, (2 ** max(0, attempt - 1)) + random.uniform(0.0, 0.35))


def api_request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    payload: dict[str, Any] | None = None,
    tries: int = 4,
    base_url: str = BASE,
    session: Any | None = None,
) -> tuple[Any, dict[str, Any]]:
    if requests is None:
        raise RuntimeError("REST retrieval requires the 'requests' package.")
    root = _validate_base(base_url)
    safe_path = _validate_path(path)
    url = root + safe_path
    client = session or requests.Session()
    last_message = "request did not run"
    last_status: int | None = None
    maximum = max(1, int(tries))
    for attempt in range(1, maximum + 1):
        response = None
        try:
            response = client.request(
                method.upper(),
                url,
                headers=hjson() if method.upper() != "GET" else hget(),
                params=params,
                json=payload,
                timeout=(DEFAULT_CONNECT_TIMEOUT, DEFAULT_READ_TIMEOUT),
                allow_redirects=False,
            )
            last_status = int(response.status_code)
            if 300 <= response.status_code < 400:
                raise PatSnapRequestError(safe_path, "redirect rejected to protect Authorization", status=last_status)
            if response.status_code in RETRYABLE_STATUS and attempt < maximum:
                time.sleep(_retry_delay(attempt, response))
                continue
            if response.status_code < 200 or response.status_code >= 300:
                raise PatSnapRequestError(safe_path, "non-success response", status=last_status)
            try:
                envelope = response.json()
            except ValueError as exc:
                raise PatSnapRequestError(safe_path, "response is not valid JSON", status=last_status) from exc
            evidence = RequestEvidence(safe_path, method.upper(), utc_now(), last_status, attempt)
            return _extract_data(envelope, safe_path), evidence.as_dict()
        except PatSnapRequestError:
            raise
        except requests.RequestException as exc:
            last_message = exc.__class__.__name__
            if attempt < maximum:
                time.sleep(_retry_delay(attempt, response))
                continue
    raise PatSnapRequestError(safe_path, last_message, status=last_status)


def api_get(path: str, params: dict[str, Any], tries: int = 4) -> Any:
    """Source-compatible getter that now raises on failure rather than returning None."""
    data, _ = api_request("GET", path, params=params, tries=tries)
    return data


def api_get_with_evidence(path: str, params: dict[str, Any], tries: int = 4) -> tuple[Any, dict[str, Any]]:
    return api_request("GET", path, params=params, tries=tries)


def api_post_with_evidence(path: str, payload: dict[str, Any], tries: int = 4) -> tuple[Any, dict[str, Any]]:
    return api_request("POST", path, payload=payload, tries=tries)


def chunks(values: list[Any], size: int) -> Iterator[list[Any]]:
    if size <= 0:
        raise ValueError("Chunk size must be positive.")
    for index in range(0, len(values), size):
        yield values[index:index + size]


def jload(filename: str | pathlib.Path) -> Any:
    return json.loads(pathlib.Path(filename).read_text(encoding="utf-8-sig"))


def jdump(value: Any, filename: str | pathlib.Path) -> None:
    path = pathlib.Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def require_checkpoint(value: Any, *, keys: Iterable[str], filename: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{filename} must contain a JSON object.")
    if value.get("schema_version") not in (None, SCHEMA_VERSION):
        raise ValueError(f"{filename} uses an incompatible schema version.")
    missing = [field for field in keys if field not in value]
    if missing:
        raise ValueError(f"{filename} is missing required fields: {', '.join(missing)}")
    return value


def new_run_id() -> str:
    return str(uuid.uuid4())


def checkpoint_meta(
    *,
    stage: str,
    run_id: str,
    source_mode: str = "rest",
    query: str | None = None,
    upstream_sha256: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "stage": stage,
        "run_id": run_id,
        "generated_at": utc_now(),
        "source_mode": source_mode,
        "query_sha256": query_hash(query) if query else None,
        "upstream_sha256": upstream_sha256,
    }


def file_sha256(path: str | pathlib.Path) -> str:
    digest = hashlib.sha256()
    with pathlib.Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
