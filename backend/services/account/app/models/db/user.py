from datetime import datetime, date
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, Boolean, Date, DateTime, func
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # -----------------------------------------
    # Phone (normalized: "919XXXXXXX")
    # -----------------------------------------
    mobile: Mapped[str] = mapped_column(String(15), nullable=False, unique=True, index=True)

    # -----------------------------------------
    # Identity info
    # -----------------------------------------
    national_code: Mapped[str] = mapped_column(String(10), nullable=False)
    birthday_date: Mapped[date] = mapped_column(Date, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # -----------------------------------------
    # Auth
    # -----------------------------------------
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    # -----------------------------------------
    # System fields
    # -----------------------------------------
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
