from datetime import datetime, timedelta, timezone
import jwt
from .base import ResourceInterface
from ..config.jwt import JWTConfig
from ..utils.log import Log

class JWTResource(ResourceInterface[JWTConfig]):

    async def initialize(self):
        """
        no async init needed, but kept for symmetry
        """
        Log.info(f"[JWTResource] initialized successfully.")

    async def close(self):
        """
        no async close needed, but kept for symmetry
        """
        Log.info(f"[JWTResource] closed successfully.")

    def create_access_token(self, payload: dict):
        data = payload.copy()
        data["exp"] = datetime.now(timezone.utc) + timedelta(
            minutes=self.settings.access_expires_minutes
        )
        return jwt.encode(
            data,
            self.settings.secret,
            self.settings.algorithm
        )

    def create_refresh_token(self, payload: dict):
        data = payload.copy()
        data["exp"] = datetime.now(timezone.utc) + timedelta(
            days=self.settings.refresh_expires_days
        )
        return jwt.encode(
            data, 
            self.settings.secret, 
            self.settings.algorithm
        )

    # -------------------------------------------------------------
    # Decode Token
    # -------------------------------------------------------------
    def decode_token(self, token: str) -> dict:
        return jwt.decode(
            jwt=token,
            key=self.settings.secret,
            algorithms=["HS256"]
        )
