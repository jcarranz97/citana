from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class Appointment(BaseModel):
    """Appointment booking — Phase 1 stub.

    Phase 2 will normalize `customer_*` into a separate `customers` table
    and add `service_id` / `resource_id` foreign keys plus conflict
    detection. For now this model carries the minimum needed to verify
    the scaffolding end-to-end.
    """

    __tablename__ = "appointments"

    customer_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    customer_phone: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        ENUM(
            "pending",
            "confirmed",
            "cancelled",
            "completed",
            name="appointment_status",
        ),
        nullable=False,
        default="pending",
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        """String representation of Appointment."""
        return (
            f"<Appointment(id={self.id}, customer='{self.customer_phone}', "
            f"start='{self.start_time}', status='{self.status}')>"
        )
