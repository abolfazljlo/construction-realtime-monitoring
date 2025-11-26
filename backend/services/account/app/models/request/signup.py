from ..base import ForbidExtraModel

class SignupRequest(ForbidExtraModel):
    mobile: str
    password: str
    national_code: str
    birthday: str

class SignupVerifyOTP(ForbidExtraModel):
    key: str
    code: str