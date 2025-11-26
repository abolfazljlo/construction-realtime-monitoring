from .base import AllowExtraModel
from ..enum.gender import Gender

class IdentityInfo(AllowExtraModel):
    first_name: str
    last_name: str
    gender: Gender