from ..models.base import ForbidExtraModel
from pydantic import Field

# -------------------------------------------------------------
# API.IR Config Schema (Pydantic)
# -------------------------------------------------------------
class ApiIrConfig(ForbidExtraModel):
    base_url: str = Field(default="https://s.api.ir")
    api_key: str
    timeout_seconds: int = Field(default=30)

