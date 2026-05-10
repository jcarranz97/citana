from enum import StrEnum


class AppointmentStatus(StrEnum):
    """Appointment lifecycle states."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ErrorCode:
    """Appointment error codes."""

    APPOINTMENT_NOT_FOUND = "APPOINTMENT_NOT_FOUND"
    APPOINTMENT_INVALID_TIME = "APPOINTMENT_INVALID_TIME"
    APPOINTMENT_ALREADY_CANCELLED = "APPOINTMENT_ALREADY_CANCELLED"


MIN_DURATION_MINUTES = 5
MAX_DURATION_MINUTES = 24 * 60
