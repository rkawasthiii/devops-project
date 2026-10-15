"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .models import AppointmentStatus, VisitType


class AppointmentBase(BaseModel):
    patient_name: str = Field(..., min_length=1, max_length=120)
    patient_phone: str | None = Field(None, max_length=32)
    doctor_name: str = Field(..., min_length=1, max_length=120)
    department: str = Field(..., min_length=1, max_length=80)
    visit_type: VisitType = VisitType.consultation
    scheduled_at: datetime
    duration_minutes: int = Field(30, ge=5, le=240)
    status: AppointmentStatus = AppointmentStatus.scheduled
    reason: str | None = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    """Partial update — every field optional."""

    patient_name: str | None = Field(None, min_length=1, max_length=120)
    patient_phone: str | None = Field(None, max_length=32)
    doctor_name: str | None = Field(None, min_length=1, max_length=120)
    department: str | None = Field(None, min_length=1, max_length=80)
    visit_type: VisitType | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = Field(None, ge=5, le=240)
    status: AppointmentStatus | None = None
    reason: str | None = None


class AppointmentOut(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class AppointmentStats(BaseModel):
    total: int
    scheduled: int
    completed: int
    cancelled: int
    today: int
    upcoming_week: int
    doctors: int
    by_department: dict[str, int]
