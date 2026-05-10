import logging
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from . import models, schemas
from .constants import AppointmentStatus
from .exceptions import (
    AppointmentAlreadyCancelledExceptionError,
    AppointmentInvalidTimeExceptionError,
    AppointmentNotFoundExceptionError,
)

logger = logging.getLogger(__name__)


class AppointmentService:
    """Appointment business logic service — Phase 1 stub."""

    @staticmethod
    def list_appointments(
        db: Session,
        status_filter: AppointmentStatus | None = None,
    ) -> list[models.Appointment]:
        """List all appointments, optionally filtered by status."""
        query = db.query(models.Appointment).filter(models.Appointment.active.is_(True))
        if status_filter is not None:
            query = query.filter(models.Appointment.status == status_filter.value)
        return query.order_by(models.Appointment.start_time.asc()).all()

    @staticmethod
    def get_appointment_by_id(db: Session, appointment_id: UUID) -> models.Appointment:
        """Fetch an appointment by id; raise if missing."""
        appt = (
            db.query(models.Appointment)
            .filter(
                models.Appointment.id == appointment_id,
                models.Appointment.active.is_(True),
            )
            .first()
        )
        if appt is None:
            raise AppointmentNotFoundExceptionError(appointment_id)
        return appt

    @staticmethod
    def create_appointment(
        db: Session,
        payload: schemas.AppointmentCreate,
    ) -> models.Appointment:
        """Create a new appointment.

        Phase 1: rejects start times in the past. No conflict detection
        yet (that lands in Phase 2 with the resources/services model).
        """
        AppointmentService._validate_start_time(payload.start_time)

        appt = models.Appointment(
            customer_name=payload.customer_name,
            customer_phone=payload.customer_phone,
            start_time=payload.start_time,
            duration_minutes=payload.duration_minutes,
            notes=payload.notes,
            status=AppointmentStatus.PENDING.value,
        )

        db.add(appt)
        db.commit()
        db.refresh(appt)
        logger.info(
            "Appointment created",
            extra={
                "appointment_id": str(appt.id),
                "customer_phone_last4": payload.customer_phone[-4:],
            },
        )
        return appt

    @staticmethod
    def update_appointment(
        db: Session,
        appt: models.Appointment,
        payload: schemas.AppointmentUpdate,
    ) -> models.Appointment:
        """Apply partial updates to an appointment."""
        update_data = payload.model_dump(exclude_unset=True)

        if "start_time" in update_data:
            AppointmentService._validate_start_time(update_data["start_time"])

        for field, value in update_data.items():
            if field == "status" and isinstance(value, AppointmentStatus):
                setattr(appt, field, value.value)
            else:
                setattr(appt, field, value)

        db.commit()
        db.refresh(appt)
        return appt

    @staticmethod
    def cancel_appointment(
        db: Session,
        appt: models.Appointment,
    ) -> models.Appointment:
        """Soft-cancel an appointment."""
        if appt.status == AppointmentStatus.CANCELLED.value:
            raise AppointmentAlreadyCancelledExceptionError(appt.id)
        appt.status = AppointmentStatus.CANCELLED.value
        db.commit()
        db.refresh(appt)
        return appt

    @staticmethod
    def _validate_start_time(start_time: datetime) -> None:
        now = datetime.now(UTC)
        compare_to = start_time
        if start_time.tzinfo is None:
            compare_to = start_time.replace(tzinfo=UTC)
        if compare_to < now:
            raise AppointmentInvalidTimeExceptionError(
                "start_time must be in the future"
            )


appointment_service = AppointmentService()
