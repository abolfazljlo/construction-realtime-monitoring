from pydantic import EmailStr
from ...base import ForbidExtraModel

class EmailData(ForbidExtraModel):
    to: EmailStr
    subject: str
    body: str
