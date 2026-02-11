import jwt
from datetime import datetime, timedelta

class JwtService:
    SECRET_KEY = "secret_key"  # TODO: Move to environment variable

    def __init__(self) -> None:
        pass

    def create_jwt_token(self, username: str = "admin") -> str:
        expiration = datetime.utcnow() + timedelta(hours=3)
        payload = {
            "username": username,
            "exp": expiration
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
        return token

    def decode_jwt_token(self, token: str) -> dict:
        try:
            decoded_payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")