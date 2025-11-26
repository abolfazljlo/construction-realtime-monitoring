from sqlalchemy.ext.asyncio import AsyncSession
from ..crud.user import UserCRUD
from ..models.db.user import User


class UserService:

    # ---------------------------------------------------------
    # Get user by ID
    # ---------------------------------------------------------
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
        return await UserCRUD.get_by_id(db, user_id)

    # ---------------------------------------------------------
    # Get user by mobile
    # ---------------------------------------------------------
    @staticmethod
    async def get_user_by_mobile(db: AsyncSession, mobile: str) -> User | None:
        return await UserCRUD.get_by_mobile(db, mobile)

    # ---------------------------------------------------------
    # Get user by national code
    # ---------------------------------------------------------
    @staticmethod
    async def get_user_by_national_code(db: AsyncSession, national_code: str) -> User | None:
        return await UserCRUD.get_by_national_code(db, national_code)

    # ---------------------------------------------------------
    # Exist user by national code
    # ---------------------------------------------------------
    @staticmethod
    async def exists_by_national_code(db: AsyncSession, national_code: str) -> bool:
        return await UserCRUD.exists_by_national_code(db, national_code)

    # ---------------------------------------------------------
    # Deactivate user
    # ---------------------------------------------------------
    @staticmethod
    async def deactivate_user(session: AsyncSession, user: User) -> None:
        await UserCRUD.set_active_status(session, user, False)

    # ---------------------------------------------------------
    # Activate user
    # ---------------------------------------------------------
    @staticmethod
    async def activate_user(session: AsyncSession, user: User) -> None:
        await UserCRUD.set_active_status(session, user, True)
