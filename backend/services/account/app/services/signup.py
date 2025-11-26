import json
import time
import uuid
from datetime import date

from .base import SingletonClass
from .identity_validator.base import IdentityValidatorInterface

from ..utils.normalizer import normalize_mobile
from ..utils.date_converter import jalali_to_gregorian
from ..utils.hashing import hash_password
from ..utils.otp import generate_otp

from ..crud.user import UserCRUD

from ..resources.database import DatabaseResource
from ..resources.redis import RedisResource
from ..resources.jwt import JWTResource


class SignupService(SingletonClass):

    SIGNUP_PREFIX = "signup:"
    SIGNUP_TTL = 15 * 60  # 15 minutes

    def __init__(
        self, 
        db: DatabaseResource, 
        redis: RedisResource, 
        jwt: JWTResource,
        identity_validator: IdentityValidatorInterface
    ):
        self.db = db
        self.redis = redis.client
        self.jwt = jwt
        self.identity_validator = identity_validator

    # ---------------------------------------------------------
    # 1️⃣ REQUEST SIGNUP OTP
    # ---------------------------------------------------------
    async def signup_request(
        self,
        mobile: str,
        password: str,
        national_code: str,
        birthday_jalali: str,
    ) -> str:

        normalized_mobile = normalize_mobile(mobile)

        # Convert Jalali → Gregorian birthday date
        birthday_date: date = jalali_to_gregorian(birthday_jalali)

        # DB checks
        async with self.db.get_session() as session:
            # Constraint 1: Check if national code is already registered
            if await UserCRUD.exists_by_national_code(session, national_code):
                raise ValueError("This national code is already registered")
            
            # Check if mobile is already registered
            if await UserCRUD.exists_by_mobile(session, normalized_mobile):
                raise ValueError("This mobile number is already registered")

        # Constraints 2 & 3: Validate identity (national_code, birthday, mobile relationship)
        # This will also retrieve the person's name
        identity_info = await self.identity_validator.validate_identity(
            national_code=national_code,
            birthday=birthday_date,
            mobile=normalized_mobile
        )

        # Hash password to store in the database
        password_hash = hash_password(password)

        # Generate OTP to send to the user
        otp = generate_otp()

        # Temporary signup session to store in the Redis
        data = {
            "mobile": normalized_mobile,
            "password_hash": password_hash,
            "national_code": national_code,
            "birthday_date": birthday_date.isoformat(),
            "first_name": identity_info.first_name,
            "last_name": identity_info.last_name,
            "otp": otp,
            "otp_expiry": int(time.time()) + 120,
        }

        # Unique key to identify the signup session
        unique_key = uuid.uuid4().hex
        redis_key = f"{self.SIGNUP_PREFIX}{unique_key}"

        # Store the signup session in the Redis
        await self.redis.setex(redis_key, self.SIGNUP_TTL, json.dumps(data))

        # TODO: send OTP through notification service
        print(f"OTP ({otp}) sent to {normalized_mobile}")
        return unique_key

    # ---------------------------------------------------------
    # 2️⃣ VERIFY OTP AND CREATE USER
    # ---------------------------------------------------------
    async def verify_otp(self, key: str, otp_input: str):

        # Get the signup session from the Redis
        redis_key = f"{self.SIGNUP_PREFIX}{key}"
        data_str = await self.redis.get(redis_key)

        if not data_str:
            raise ValueError("Signup session expired or invalid")

        data = json.loads(data_str)

        # OTP expired?
        if int(time.time()) > data["otp_expiry"]:
            raise ValueError("OTP expired")

        # Wrong OTP?
        if otp_input != data["otp"]:
            raise ValueError("Invalid OTP")

        birthday_date = date.fromisoformat(data["birthday_date"])

        # CREATE USER
        async with self.db.get_session() as session:
            user = await UserCRUD.create(
                session,
                mobile=data["mobile"],
                national_code=data["national_code"],
                birthday_date=birthday_date,
                password_hash=data["password_hash"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )

        # Remove session
        await self.redis.delete(redis_key)

        # JWT
        access = self.jwt.create_access_token({"user_id": user.id})
        refresh = self.jwt.create_refresh_token({"user_id": user.id})

        return {
            "user": user,
            "access_token": access,
            "refresh_token": refresh,
        }
