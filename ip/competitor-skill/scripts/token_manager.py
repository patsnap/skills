import time
import requests


class TokenManager:
    def __init__(self, token_url, client_id, client_secret):
        self._url = token_url
        self._id = client_id
        self._secret = client_secret
        self._token = None
        self._expires_at = 0

    def get_token(self):
        if self._token and time.time() < self._expires_at:
            return self._token
        resp = requests.post(
            self._url,
            data={"grant_type": "client_credentials", "client_id": self._id, "client_secret": self._secret},
            timeout=15,
        )
        resp.raise_for_status()
        body = resp.json()
        # 支持两种响应格式：顶层 access_token/token，或嵌套在 data 字段中
        inner = body.get("data") if isinstance(body.get("data"), dict) else body
        self._token = inner.get("access_token") or inner.get("token")
        expires_in = int(inner.get("expires_in", 3600))
        self._expires_at = time.time() + expires_in * 0.5
        return self._token
