from datetime import date
from .base import IdentityValidatorInterface
from ...models.identity_info import IdentityInfo
from ...resources.api_ir import ApiIrResource
from ...enum.gender import Gender
from ...utils.log import Log
from ...utils.date_converter import gregorian_to_jalali


class ApiIrIdentityValidator(IdentityValidatorInterface):
    """
    Identity validator implementation using s.api.ir service.
    """

    def __init__(self, api_resource: ApiIrResource):
        self.api = api_resource

    def __gregorian_to_jalali(self, gregorian_date: date) -> str:
        return gregorian_to_jalali(gregorian_date)

    def __format_mobile(self, mobile: str) -> str:
        """Format mobile number for API (e.g., 09191234567)"""
        # If mobile starts with 9, add 0 prefix
        if mobile.startswith("9") and len(mobile) == 10:
            return f"0{mobile}"
        return mobile

    async def validate_identity(
        self,
        national_code: str,
        birthday: date,
        mobile: str
    ) -> IdentityInfo:
        """
        Validates identity using s.api.ir service.
        
        This implementation:
        1. Checks if mobile number belongs to the person
        2. Validates national code and birthday, and retrieves personal information
        
        Args:
            national_code: 10-digit Iranian national code
            birthday: Person's birthday (Gregorian date)
            mobile: Normalized mobile number (e.g., "9191234567")
            
        Returns:
            IdentityInfo with first_name, last_name, and gender
            
        Raises:
            ValueError: If validation fails
        """
        try:
            # Convert birthday to Jalali format for API
            birthday_jalali = self.__gregorian_to_jalali(birthday)
            formatted_mobile = self.__format_mobile(mobile)

            # NOTE: Endpoint paths and request/response formats may need adjustment
            # based on the actual s.api.ir API documentation at https://s.api.ir/swagger/index.html

            # Step 1: Check if mobile number belongs to this person
            mobile_check_response = await self.api.post(
                "/api/sw1/ShahkarLite",
                json={
                    "nationalCode": national_code,
                    "mobile": formatted_mobile,
                }
            )

            if not mobile_check_response.get("success", False):
                raise ValueError(
                    mobile_check_response.get("message", "Mobile number does not belong to this person")
                )

            # Step 2: Validate national code and birthday
            identity_response = await self.api.post(
                "/api/sw1/PersonInfo",
                json={
                    "nationalCode": national_code,
                    "birthDate": birthday_jalali,
                }
            )

            if not identity_response.get("success", False):
                error_msg = identity_response.get("message", "Identity validation failed")
                raise ValueError(f"Identity validation failed: {error_msg}")

            # Extract name and gender from response
            personal_data = identity_response.get("data")
            if not isinstance(personal_data, dict):
                raise ValueError("Could not retrieve personal data from API")

            if not personal_data.get("alive"):
                raise ValueError("Identity validation failed: Person is not alive")

            first_name = personal_data.get("firstName")
            last_name = personal_data.get("lastName")
           
            # Map gender from API response
            gender_int = personal_data.get("gender", 1)
            if gender_int == 1:
                gender = Gender.MALE
            else:
                gender = Gender.FEMALE

            if not first_name or not last_name:
                raise ValueError("Could not retrieve personal information from API")

            Log.info(f"[ApiIrIdentityValidator] Successfully validated identity for national_code: {national_code}")

            return IdentityInfo(
                first_name=first_name,
                last_name=last_name,
                gender=gender
            )

        except Exception as e:
            if isinstance(e, ValueError):
                raise
            Log.error(f"[ApiIrIdentityValidator] Error validating identity: {e}")
            raise ValueError(f"Identity validation failed: {str(e)}")

