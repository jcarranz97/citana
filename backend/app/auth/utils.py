from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.config import settings

from .exceptions import InvalidTokenExceptionError

pwd_context = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Create JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "iat": datetime.now(UTC), "type": "access"})

    return jwt.encode(
        to_encode, settings.AUTH.SECRET_KEY, algorithm=settings.AUTH.ALGORITHM
    )


def verify_token(token: str) -> dict[str, Any]:
    """Verify and decode JWT token."""
    try:
        return jwt.decode(
            token, settings.AUTH.SECRET_KEY, algorithms=[settings.AUTH.ALGORITHM]
        )
    except InvalidTokenError as e:
        raise InvalidTokenExceptionError from e


def extract_username_from_token(token: str) -> str:
    """Extract username from JWT token."""
    payload = verify_token(token)
    username = payload.get("sub")

    if not username or not isinstance(username, str):
        raise InvalidTokenExceptionError

    return username
