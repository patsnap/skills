"""Runtime configuration for the advanced-query reporting scripts.

Credentials must be supplied by the execution environment. This module does
not search personal folders or write a skill-local .env file.
"""

import os


PATSNAP_API_KEY = os.getenv("PATSNAP_API_KEY", "").strip()
PATSNAP_BASE_URL = os.getenv("PATSNAP_BASE_URL", "").strip()
LITERATURE_API_KEY = os.getenv("PATSNAP_LITERATURE_API_KEY", "").strip()
LITERATURE_BASE_URL = os.getenv("PATSNAP_LITERATURE_BASE_URL", "").strip()


def require_setting(name: str, value: str) -> str:
    """Return a configured value or fail closed with a useful message."""
    if value:
        return value
    raise RuntimeError(
        f"{name} is not configured. Use the verified PatSnap MCP workflow, "
        "or set an endpoint documented for your PatSnap Open account."
    )


def patent_api_settings() -> tuple[str, str]:
    """Return explicitly configured patent REST settings."""
    return (
        require_setting("PATSNAP_BASE_URL", PATSNAP_BASE_URL),
        require_setting("PATSNAP_API_KEY", PATSNAP_API_KEY),
    )


def literature_api_settings() -> tuple[str, str]:
    """Return explicitly configured literature REST settings."""
    return (
        require_setting("PATSNAP_LITERATURE_BASE_URL", LITERATURE_BASE_URL),
        require_setting("PATSNAP_LITERATURE_API_KEY", LITERATURE_API_KEY),
    )
