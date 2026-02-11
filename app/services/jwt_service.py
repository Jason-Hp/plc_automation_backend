from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


class JwtTokenError(Exception):
    """Raised when a JWT token is invalid or expired."""


class JwtService:
    def __init__(self) -> None:
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.expiration_hours = settings.jwt_expiration_hours

    def create_jwt_token(self, username: str = "admin") -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": username,
            "username": username,
            "iat": now,
            "exp": now + timedelta(hours=self.expiration_hours),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_jwt_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"require": ["exp", "iat", "sub"]},
            )
        except jwt.ExpiredSignatureError as exc:
            raise JwtTokenError("Token has expired") from exc
        except jwt.InvalidTokenError as exc:
            raise JwtTokenError("Invalid token") from exc
