from abc import ABC, abstractmethod
from datetime import date
from ...models.identity_info import IdentityInfo

class IdentityValidatorInterface(ABC):
    """
    Abstract interface for identity validation service.
    This should be implemented with actual API integration (e.g., Saman, Zarinpal, etc.)
    """

    @abstractmethod
    async def validate_identity(
        self,
        national_code: str,
        birthday: date,
        mobile: str
    ) -> IdentityInfo:
        """
        Validates that:
        1. National code and birthday are correct
        2. Mobile number belongs to the person with this national code
        3. Returns the person's name if validation succeeds

        Args:
            national_code: 10-digit Iranian national code
            birthday: Person's birthday (jalali date; e.g., 1371/1/1)
            mobile: Normalized mobile number (e.g., "9191234567")

        Returns:
            IdentityInfo with first_name, last_name, and is_valid=True if all checks pass

        Raises:
            ValueError: If validation fails (invalid national code, wrong birthday, 
                       mobile doesn't match, etc.)
        """
        pass