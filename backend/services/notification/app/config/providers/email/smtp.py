from typing import Optional
from pydantic import Field
from ....models.base import ForbidExtraModel

class SMTPEmailConfig(ForbidExtraModel):
    enabled: bool = False
    host: str = "localhost"
    port: int = 587
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: bool = True
    timeout: int = 10
    from_address: Optional[str] = Field(default=None, alias="from")