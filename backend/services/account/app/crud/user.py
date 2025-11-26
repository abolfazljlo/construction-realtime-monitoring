from datetime import date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.db.user import User


class UserCRUD:

    # ---------------------------------------------------------
    # Get user by ID
    # ---------------------------------------------------------
    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # ---------------------------------------------------------
    # Get user by mobile
    # ---------------------------------------------------------
    @staticmethod
    async def get_by_mobile(session: AsyncSession, mobile: str) -> User | None:
        stmt = select(User).where(User.mobile == mobile)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    # ---------------------------------------------------------
    # Get user by national code
    # ---------------------------------------------------------
    @staticmethod
    async def get_by_national_code(session: AsyncSession, national_code: str) -> User | None:
        stmt = select(User).where(User.national_code == national_code)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # ---------------------------------------------------------
    # Exist user by national code
    # ---------------------------------------------------------
    @staticmethod
    async def exists_by_national_code(session: AsyncSession, national_code: str) -> bool:
        stmt = select(func.count()).select_from(User).where(User.national_code == national_code)
        result = await session.execute(stmt)
        return result.scalar_one() > 0
    
    # ---------------------------------------------------------
    # Exist user by mobile
    # ---------------------------------------------------------
    @staticmethod
    async def exists_by_mobile(session: AsyncSession, mobile: str) -> bool:
        stmt = select(func.count()).select_from(User).where(User.mobile == mobile)
        result = await session.execute(stmt)
        return result.scalar_one() > 0
    
    # ---------------------------------------------------------
    # Create a user
    # ---------------------------------------------------------
    @staticmethod
    async def create(
        session: AsyncSession,
        *,
        mobile: str,
        national_code: str,
        birthday_date: date,
        password_hash: str,
        first_name: str,
        last_name: str
    ) -> User:
        user = User(
            mobile=mobile,
            national_code=national_code,
            birthday_date=birthday_date,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    # ---------------------------------------------------------
    # Update user password
    # ---------------------------------------------------------
    @staticmethod
    async def update_password(session: AsyncSession, user: User, new_hash: str) -> None:
        user.password_hash = new_hash
        await session.commit()

    # ---------------------------------------------------------
    # Activate/deactivate user
    # ---------------------------------------------------------
    @staticmethod
    async def set_active_status(session: AsyncSession, user: User, is_active: bool) -> None:
        user.is_active = is_active
        await session.commit()
