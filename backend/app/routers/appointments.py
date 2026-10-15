"""REST endpoints for clinic appointments."""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Appointment, AppointmentStatus
from ..schemas import AppointmentCreate, AppointmentOut, AppointmentStats, AppointmentUpdate

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("", response_model=list[AppointmentOut])
def list_appointments(
    status: AppointmentStatus | None = None,
    department: str | None = None,
    doctor: str | None = None,
    search: str | None = None,
    limit: int = Query(200, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """List appointments with optional status/department/doctor/search filters."""
    stmt = select(Appointment)
    if status is not None:
        stmt = stmt.where(Appointment.status == status.value)
    if department:
        stmt = stmt.where(Appointment.department == department)
    if doctor:
        stmt = stmt.where(Appointment.doctor_name == doctor)
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                Appointment.patient_name.ilike(pattern),
                Appointment.doctor_name.ilike(pattern),
                Appointment.reason.ilike(pattern),
            )
        )
    stmt = stmt.order_by(Appointment.scheduled_at.asc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


@router.get("/stats", response_model=AppointmentStats)
def appointment_stats(db: Session = Depends(get_db)):
    """Aggregate KPIs for the dashboard header cards."""
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today_start + timedelta(days=1)
    next_week = today_start + timedelta(days=7)

    def count(*conditions) -> int:
        stmt = select(func.count(Appointment.id)).where(*conditions)
        return db.execute(stmt).scalar_one()

    by_department = {
        dept: n
        for dept, n in db.execute(
            select(Appointment.department, func.count(Appointment.id)).group_by(
                Appointment.department
            )
        ).all()
    }

    doctors = db.execute(
        select(func.count(func.distinct(Appointment.doctor_name)))
    ).scalar_one()

    return AppointmentStats(
        total=count(),
        scheduled=count(Appointment.status == AppointmentStatus.scheduled.value),
        completed=count(Appointment.status == AppointmentStatus.completed.value),
        cancelled=count(Appointment.status == AppointmentStatus.cancelled.value),
        today=count(
            Appointment.scheduled_at >= today_start,
            Appointment.scheduled_at < tomorrow,
        ),
        upcoming_week=count(
            Appointment.scheduled_at >= tomorrow,
            Appointment.scheduled_at < next_week,
            Appointment.status == AppointmentStatus.scheduled.value,
        ),
        doctors=doctors,
        by_department=by_department,
    )


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.get(Appointment, appointment_id)
    if appt is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "appointment not found")
    return appt


@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    appt = Appointment(**payload.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: int, payload: AppointmentUpdate, db: Session = Depends(get_db)
):
    appt = db.get(Appointment, appointment_id)
    if appt is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "appointment not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(appt, field, value)
    db.commit()
    db.refresh(appt)
    return appt


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.get(Appointment, appointment_id)
    if appt is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "appointment not found")
    db.delete(appt)
    db.commit()
