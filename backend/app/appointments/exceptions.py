from uuid import UUID

from fastapi import status

from app.exceptions import AppExceptionError

from .constants import ErrorCode


class AppointmentExceptionError(AppExceptionError):
    """Base appointments exception."""


class AppointmentNotFoundExceptionError(AppointmentExceptionError):
    """Exception raised when an appointment is not found."""

    def __init__(self, appointment_id: UUID | None = None) -> None:
        details = {"appointment_id": str(appointment_id)} if appointment_id else {}
        super().__init__(
            error_code=ErrorCode.APPOINTMENT_NOT_FOUND,
            message="Appointment not found",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class AppointmentInvalidTimeExceptionError(AppointmentExceptionError):
    """Exception raised when start time or duration is invalid."""

    def __init__(self, message: str = "Invalid appointment time") -> None:
        super().__init__(
            error_code=ErrorCode.APPOINTMENT_INVALID_TIME,
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class AppointmentAlreadyCancelledExceptionError(AppointmentExceptionError):
    """Exception raised when attempting to cancel a cancelled appointment."""

    def __init__(self, appointment_id: UUID) -> None:
        super().__init__(
            error_code=ErrorCode.APPOINTMENT_ALREADY_CANCELLED,
            message="Appointment is already cancelled",
            status_code=status.HTTP_409_CONFLICT,
            details={"appointment_id": str(appointment_id)},
        )
