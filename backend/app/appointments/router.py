from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies import CurrentActiveUser, get_db

from . import schemas, service
from .constants import AppointmentStatus

router = APIRouter(prefix="/appointments", tags=["appointments"])

DatabaseDep = Annotated[Session, Depends(get_db)]


@router.get("/health")
async def appointments_health_check() -> dict[str, str]:
    """Appointments domain health check."""
    return {"status": "healthy", "domain": "appointments"}


@router.get("/", response_model=list[schemas.AppointmentResponse])
async def list_appointments(
    _user: CurrentActiveUser,
    db: DatabaseDep,
    status_filter: Annotated[AppointmentStatus | None, Query(alias="status")] = None,
) -> list[schemas.AppointmentResponse]:
    """List appointments (admin)."""
    appts = service.appointment_service.list_appointments(db, status_filter)
    return [schemas.AppointmentResponse.model_validate(a) for a in appts]


@router.post(
    "/",
    response_model=schemas.AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    payload: schemas.AppointmentCreate,
    _user: CurrentActiveUser,
    db: DatabaseDep,
) -> schemas.AppointmentResponse:
    """Create a new appointment (admin)."""
    appt = service.appointment_service.create_appointment(db, payload)
    return schemas.AppointmentResponse.model_validate(appt)


@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
async def get_appointment(
    appointment_id: UUID,
    _user: CurrentActiveUser,
    db: DatabaseDep,
) -> schemas.AppointmentResponse:
    """Fetch an appointment by id."""
    appt = service.appointment_service.get_appointment_by_id(db, appointment_id)
    return schemas.AppointmentResponse.model_validate(appt)


@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
async def update_appointment(
    appointment_id: UUID,
    payload: schemas.AppointmentUpdate,
    _user: CurrentActiveUser,
    db: DatabaseDep,
) -> schemas.AppointmentResponse:
    """Apply partial updates to an appointment."""
    appt = service.appointment_service.get_appointment_by_id(db, appointment_id)
    updated = service.appointment_service.update_appointment(db, appt, payload)
    return schemas.AppointmentResponse.model_validate(updated)


@router.delete(
    "/{appointment_id}",
    response_model=schemas.AppointmentResponse,
)
async def cancel_appointment(
    appointment_id: UUID,
    _user: CurrentActiveUser,
    db: DatabaseDep,
) -> schemas.AppointmentResponse:
    """Soft-cancel an appointment (sets status to cancelled)."""
    appt = service.appointment_service.get_appointment_by_id(db, appointment_id)
    cancelled = service.appointment_service.cancel_appointment(db, appt)
    return schemas.AppointmentResponse.model_validate(cancelled)
