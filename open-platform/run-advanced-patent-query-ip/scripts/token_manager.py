"""OAuth client-credentials token management."""

import time

import requests


class TokenManager:
    """Cache a short-lived access token without persisting credentials."""

    def __init__(self, token_url, client_id, client_secret, timeout=15):
        self._url = token_url
        self._id = client_id
        self._secret = client_secret
        self._timeout = timeout
        self._token = None
        self._expires_at = 0.0

    def get_token(self):
        """Return a cached token or request a new one."""
        if self._token and time.time() < self._expires_at:
            return self._token
        response = requests.post(
            self._url,
            data={
                "grant_type": "client_credentials",
                "client_id": self._id,
                "client_secret": self._secret,
            },
            timeout=self._timeout,
        )
        response.raise_for_status()
        body = response.json()
        inner = body.get("data") if isinstance(body.get("data"), dict) else body
        token = inner.get("access_token") or inner.get("token")
        if not token:
            raise RuntimeError("The token response did not contain an access token.")
        try:
            expires_in = max(1, int(inner.get("expires_in", 3600)))
        except (TypeError, ValueError) as exc:
            raise RuntimeError("The token response contains an invalid expires_in value.") from exc
        self._token = token
        self._expires_at = time.time() + expires_in * 0.5
        return self._token
