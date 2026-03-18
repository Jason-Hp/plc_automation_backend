from typing import Optional

import jwt
from jwt import PyJWKClient

from app.config import settings


class JwtTokenError(Exception):
    """Custom exception for JWT validation errors."""

class JwtService:
    """
    JWT validation service backed by Supabase's public JWKS.

    Tokens are expected to be issued by Supabase and signed with ES256/RS256.
    
    """

    def __init__(self) -> None:
        if not settings.supabase_url:
            raise RuntimeError("SUPABASE_URL is not configured")

        jwks_url = f"{settings.supabase_url.rstrip('/')}/auth/v1/keys"
        self._jwks_client = PyJWKClient(jwks_url)
        self._audience: Optional[str] = settings.supabase_jwt_audience or None

    def decode_jwt_token(self, token: str) -> dict:
        """
        Validate a Supabase-issued JWT and return its payload.
        """
        try:
            signing_key = self._jwks_client.get_signing_key_from_jwt(token)

            decode_kwargs: dict = {
                "algorithms": ["ES256", "RS256"],
                "options": {"require": ["exp", "iat", "sub"]},
            }

            if self._audience:
                decode_kwargs["audience"] = self._audience

            return jwt.decode(
                token,
                signing_key.key,
                **decode_kwargs,
            )
        except jwt.ExpiredSignatureError as exc:
            raise JwtTokenError("Token has expired") from exc
        except jwt.InvalidTokenError as exc:
            raise JwtTokenError("Invalid token") from exc
