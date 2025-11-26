from ...base import ForbidExtraModel

class SMSData(ForbidExtraModel):
    phone: str
    message: str
