import re
import uuid
from datetime import datetime

from pydantic import ConfigDict, Field, field_validator

from app.schemas import AppBaseModel

from .constants import (
    MAX_DURATION_MINUTES,
    MIN_DURATION_MINUTES,
    AppointmentStatus,
)

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{6,14}$")


class AppointmentBase(AppBaseModel):
    """Base appointment fields shared between create/update/response."""

    customer_name: str | None = Field(default=None, max_length=200)
    customer_phone: str = Field(..., min_length=7, max_length=32)
    start_time: datetime
    duration_minutes: int = Field(..., ge=MIN_DURATION_MINUTES, le=MAX_DURATION_MINUTES)
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("customer_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone is roughly E.164-ish.

        Accepts an optional leading "+" followed by 7-15 digits. Strips
        spaces. Strict E.164 validation (country-code-aware) is intentionally
        out of scope for v1.
        """
        cleaned = v.strip().replace(" ", "")
        if not PHONE_REGEX.fullmatch(cleaned):
            raise ValueError(
                "customer_phone must be 7-15 digits, optionally prefixed with '+'"
            )
        return cleaned

    @field_validator("customer_name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        """Trim whitespace; empty becomes None."""
        if v is None:
            return None
        cleaned = v.strip()
        return cleaned or None


class AppointmentCreate(AppointmentBase):
    """Schema for creating an appointment."""


class AppointmentUpdate(AppBaseModel):
    """Schema for updating an appointment."""

    customer_name: str | None = Field(default=None, max_length=200)
    start_time: datetime | None = None
    duration_minutes: int | None = Field(
        default=None, ge=MIN_DURATION_MINUTES, le=MAX_DURATION_MINUTES
    )
    status: AppointmentStatus | None = None
    notes: str | None = Field(default=None, max_length=2000)


class AppointmentResponse(AppointmentBase):
    """Appointment response schema."""

    id: uuid.UUID
    status: AppointmentStatus
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
