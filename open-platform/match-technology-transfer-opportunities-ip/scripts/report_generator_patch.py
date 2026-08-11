"""Safe output helpers for technology-transfer reports.

The source forced writes to Desktop and an implicit home/session backup. This
localized module writes only to exact user-approved paths and never overwrites
an existing file unless the caller explicitly allows it.
"""

from __future__ import annotations

import os
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


class OutputError(ValueError):
    """Raised when output handling would violate the approved contract."""


@dataclass(frozen=True)
class SaveResult:
    primary_path: str
    backup_path: str
    success: bool
    message: str


def safe_filename(topic: str, report_date: str | None = None) -> str:
    """Create a portable English filename from untrusted topic text."""
    day = report_date or date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise OutputError("report_date must use YYYY-MM-DD")
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", str(topic).strip()).strip("-._")
    cleaned = cleaned[:60] or "technology-transfer"
    return f"{cleaned}-transfer-match-{day}.html"


def _validated_destination(path: str | os.PathLike[str], label: str) -> Path:
    if not str(path).strip():
        raise OutputError(f"{label} path is required")
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        raise OutputError(f"{label} must be an exact absolute path approved by the user")
    if candidate.name in {"", ".", ".."}:
        raise OutputError(f"{label} must identify a file")
    if candidate.suffix.lower() not in {".html", ".htm"}:
        raise OutputError(f"{label} must end in .html or .htm")
    return candidate.resolve(strict=False)


def _write_one(content: str, destination: Path, *, overwrite: bool) -> None:
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {destination}")
    if destination.exists() and not destination.is_file():
        raise OutputError(f"Destination is not a file: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp")
    if temporary.exists():
        raise FileExistsError(f"Temporary path already exists: {temporary}")
    try:
        temporary.write_text(content, encoding="utf-8", newline="\n")
        if destination.exists() and overwrite:
            destination.unlink()
        temporary.replace(destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def save_report(
    html_content: str,
    primary_path: str | os.PathLike[str],
    *,
    backup_path: str | os.PathLike[str] | None = None,
    overwrite: bool = False,
) -> SaveResult:
    """Save a report to approved destinations.

    ``backup_path`` is optional and must be separately approved. This function
    never assumes Desktop, home, session, temporary, or network locations.
    """
    if not isinstance(html_content, str) or not html_content.strip():
        raise OutputError("html_content must be a non-empty string")
    if "<html" not in html_content.lower() or "</html>" not in html_content.lower():
        raise OutputError("html_content does not appear to be a complete HTML document")

    primary = _validated_destination(primary_path, "primary_path")
    backup = _validated_destination(backup_path, "backup_path") if backup_path is not None else None
    if backup == primary:
        raise OutputError("backup_path must differ from primary_path")

    _write_one(html_content, primary, overwrite=overwrite)
    backup_text = ""
    try:
        if backup is not None:
            _write_one(html_content, backup, overwrite=overwrite)
            backup_text = os.fspath(backup)
    except Exception:
        # The completed primary file is not deleted. The caller receives the
        # backup exception and can report the primary path accurately.
        raise

    return SaveResult(
        primary_path=os.fspath(primary),
        backup_path=backup_text,
        success=True,
        message="Report saved to the approved path(s).",
    )


def save_and_announce(
    html_content: str,
    topic: str,
    *,
    output_directory: str | os.PathLike[str],
    backup_directory: str | os.PathLike[str] | None = None,
    report_date: str | None = None,
    overwrite: bool = False,
) -> dict[str, object]:
    """Compatibility wrapper using explicitly approved directories."""
    filename = safe_filename(topic, report_date)
    output_dir = Path(output_directory).expanduser()
    if not output_dir.is_absolute():
        raise OutputError("output_directory must be an approved absolute path")
    primary = output_dir / filename
    backup = None
    if backup_directory is not None:
        backup_dir = Path(backup_directory).expanduser()
        if not backup_dir.is_absolute():
            raise OutputError("backup_directory must be an approved absolute path")
        backup = backup_dir / filename
    result = save_report(html_content, primary, backup_path=backup, overwrite=overwrite)
    return asdict(result)


if __name__ == "__main__":
    raise SystemExit(
        "This module is a library. Supply validated HTML and explicit approved paths from the calling workflow."
    )
