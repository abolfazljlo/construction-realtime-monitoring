from ..models.base import ForbidExtraModel
from pydantic import Field

# -------------------------------------------------------------
# JWT Config Schema (Pydantic)
# -------------------------------------------------------------
class JWTConfig(ForbidExtraModel):
    
    secret: str
    access_expires_minutes: int = Field(default=15)
    refresh_expires_days: int = Field(default=30)

    @property
    def algorithm(self):
        return "HS256"