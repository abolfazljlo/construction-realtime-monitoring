from fastapi import APIRouter, Request, Depends
from ...services.signup import SignupService
from ...models.request.signup import SignupRequest, SignupVerifyOTP

def get_signup_service(request: Request):
    return SignupService(
        request.app.state.db,
        request.app.state.redis,
        request.app.state.jwt,
        request.app.state.identity_validator if hasattr(request.app.state, 'identity_validator') else None
    )

signup_router = APIRouter()

@signup_router.post(
    path="/"
)
async def signup_request(body: SignupRequest, singup_service: SignupService = Depends(get_signup_service)):
    return await singup_service.signup_request(
        body.mobile,
        body.password,
        body.national_code,
        body.birthday,
    )

@signup_router.post(
    path="/verify"
)
async def signup_verify_otp(body: SignupVerifyOTP, singup_service: SignupService = Depends(get_signup_service)):
    return await singup_service.verify_otp(
        body.key,
        body.code
    )