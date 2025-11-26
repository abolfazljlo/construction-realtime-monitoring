from typing import Optional
from ....models.base import ForbidExtraModel

class GhasedakSMSConfig(ForbidExtraModel):
    enabled: bool = False
    api_key: Optional[str] = None
    line_number: Optional[str] = None