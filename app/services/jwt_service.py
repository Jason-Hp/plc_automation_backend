from __future__ import annotations

from datetime import datetime, timedelta, timezone


class JwtService:
    SECRET_KEY = "secret_key"  # TODO: Move to environment variable

    def __init__(self) -> None:
        pass

    @staticmethod
    def _jwt_module():
        try:
            import jwt  # type: ignore
            return jwt
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("PyJWT is required for admin token operations") from exc

    def create_jwt_token(self, username: str = "admin") -> str:
        jwt = self._jwt_module()
        expiration = datetime.now(tz=timezone.utc) + timedelta(hours=3)
        payload = {
            "username": username,
            "exp": expiration,
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

    def decode_jwt_token(self, token: str) -> dict:
        jwt = self._jwt_module()
        try:
            return jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as exc:
            raise Exception("Token has expired") from exc
        except jwt.InvalidTokenError as exc:
            raise Exception("Invalid token") from exc
