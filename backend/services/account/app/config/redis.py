from ..models.base import ForbidExtraModel
from pydantic import Field

# -------------------------------------------------------------
# Redis Config Schema (Pydantic)
# -------------------------------------------------------------
class RedisConfig(ForbidExtraModel):
    url: str
    db: int = Field(default=0)

