from typing import Optional
from ....models.base import ForbidExtraModel

class KavenegarSMSConfig(ForbidExtraModel):
    enabled: bool = False
    api_key: Optional[str] = None
    sender: Optional[str] = None
    timeout: int = 10