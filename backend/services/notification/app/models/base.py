from pydantic import BaseModel, ConfigDict

class ForbidExtraModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

class AllowExtraModel(BaseModel):
    model_config = ConfigDict(
        extra="allow"
    )

class IgnoreExtraModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore"
    )
