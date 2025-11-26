from typing import Optional
from ....models.base import ForbidExtraModel

class TwilioSMSConfig(ForbidExtraModel):
    enabled: bool = False
    account_sid: Optional[str] = None
    auth_token: Optional[str] = None
    from_number: Optional[str] = None