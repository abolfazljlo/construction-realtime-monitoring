from ..models.base import ForbidExtraModel

# -------------------------------------------------------------
# Database Config Schema (Pydantic)
# -------------------------------------------------------------
class DatabaseConfig(ForbidExtraModel):
    url: str

