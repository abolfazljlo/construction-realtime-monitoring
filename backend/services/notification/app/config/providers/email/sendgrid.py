from typing import Optional
from ....models.base import ForbidExtraModel

class SendGridEmailConfig(ForbidExtraModel):
    enabled: bool = False
    api_key: Optional[str] = None