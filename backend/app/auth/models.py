from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class User(BaseModel):
    """User model representing application users (admins)."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(
        ENUM("admin", "user", name="user_role"), nullable=False, default="user"
    )

    def __repr__(self) -> str:
        """String representation of the User model."""
        return f"<User(username='{self.username}')>"
