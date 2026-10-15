"""SQLAlchemy models for the MediDesk clinic platform."""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class VisitType(str, enum.Enum):
    consultation = "consultation"
    follow_up = "follow_up"
    emergency = "emergency"
    checkup = "checkup"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_name: Mapped[str] = mapped_column(String(120), nullable=False)
    patient_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    doctor_name: Mapped[str] = mapped_column(String(120), nullable=False)
    department: Mapped[str] = mapped_column(String(80), nullable=False)
    visit_type: Mapped[str] = mapped_column(
        String(40), nullable=False, default=VisitType.consultation.value
    )
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=AppointmentStatus.scheduled.value
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("ix_appointments_status", "status"),
        Index("ix_appointments_scheduled_at", "scheduled_at"),
    )
