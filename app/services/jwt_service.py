from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone


class JwtService:
    SECRET_KEY = "secret_key"  # TODO: Move to environment variable

    def __init__(self) -> None:
        pass

    def _sign(self, payload: str) -> str:
        digest = hmac.new(self.SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return digest

    def create_jwt_token(self, username: str = "admin") -> str:
        expiration = datetime.now(tz=timezone.utc) + timedelta(hours=3)
        payload = {
            "username": username,
            "exp": int(expiration.timestamp()),
        }
        payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        encoded_payload = base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip("=")
        signature = self._sign(encoded_payload)
        return f"{encoded_payload}.{signature}"

    def decode_jwt_token(self, token: str) -> dict:
        try:
            encoded_payload, signature = token.split(".", 1)
        except ValueError as exc:
            raise Exception("Invalid token") from exc

        expected = self._sign(encoded_payload)
        if not hmac.compare_digest(signature, expected):
            raise Exception("Invalid token")

        try:
            payload_json = base64.urlsafe_b64decode(encoded_payload + "===").decode()
            payload = json.loads(payload_json)
        except Exception as exc:
            raise Exception("Invalid token") from exc

        if int(payload.get("exp", 0)) < int(datetime.now(tz=timezone.utc).timestamp()):
            raise Exception("Token has expired")

        return payload
