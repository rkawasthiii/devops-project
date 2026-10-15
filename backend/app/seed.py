"""Demo data seeder.

Runs as `python -m app.seed` from the container entrypoint after migrations.
Inserts a realistic schedule only when the appointments table is empty, so
restarts never create duplicates and a fresh deployment always demos well.
"""

import logging
from datetime import datetime, timedelta

from sqlalchemy import func, select

from .database import SessionLocal
from .models import Appointment, AppointmentStatus, VisitType

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("seed")


def _at(days: int, hour: int, minute: int = 0) -> datetime:
    base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return base + timedelta(days=days, hours=hour, minutes=minute)


DEMO_APPOINTMENTS = [
    # --- history (completed) ---
    dict(patient_name="Aarav Mehta", patient_phone="+91-98110 22415",
         doctor_name="Dr. Asha Verma", department="Cardiology",
         visit_type=VisitType.follow_up, scheduled_at=_at(-3, 10),
         duration_minutes=20, status=AppointmentStatus.completed,
         reason="Post-angioplasty review"),
    dict(patient_name="Sana Qureshi", patient_phone="+91-99870 55102",
         doctor_name="Dr. Imran Sheikh", department="Dermatology",
         visit_type=VisitType.consultation, scheduled_at=_at(-2, 12, 30),
         status=AppointmentStatus.completed, reason="Eczema flare-up"),
    dict(patient_name="Rohan Iyer", patient_phone="+91-98220 41788",
         doctor_name="Dr. Vikram Rao", department="Orthopedics",
         visit_type=VisitType.follow_up, scheduled_at=_at(-1, 9, 30),
         duration_minutes=25, status=AppointmentStatus.completed,
         reason="ACL rehab progress check"),
    dict(patient_name="Meera Krishnan", patient_phone="+91-97405 66120",
         doctor_name="Dr. Priya Nair", department="General Medicine",
         visit_type=VisitType.checkup, scheduled_at=_at(-1, 16),
         status=AppointmentStatus.completed, reason="Annual physical"),
    dict(patient_name="Dev Patel", patient_phone="+91-98600 30917",
         doctor_name="Dr. Naina Kapoor", department="Pediatrics",
         visit_type=VisitType.consultation, scheduled_at=_at(-1, 11),
         status=AppointmentStatus.cancelled, reason="Fever — guardian cancelled"),
    # --- today ---
    dict(patient_name="Ishita Banerjee", patient_phone="+91-98300 72441",
         doctor_name="Dr. Asha Verma", department="Cardiology",
         visit_type=VisitType.emergency, scheduled_at=_at(0, 9),
         duration_minutes=45, status=AppointmentStatus.completed,
         reason="Chest pain evaluation"),
    dict(patient_name="Kabir Malhotra", patient_phone="+91-99530 18276",
         doctor_name="Dr. Vikram Rao", department="Orthopedics",
         visit_type=VisitType.consultation, scheduled_at=_at(0, 10, 30),
         status=AppointmentStatus.completed, reason="Lower back pain"),
    dict(patient_name="Anaya Reddy", patient_phone="+91-96010 44852",
         doctor_name="Dr. Naina Kapoor", department="Pediatrics",
         visit_type=VisitType.checkup, scheduled_at=_at(0, 12),
         status=AppointmentStatus.scheduled, reason="Vaccination — MMR booster"),
    dict(patient_name="Farhan Ali", patient_phone="+91-97020 83519",
         doctor_name="Dr. Imran Sheikh", department="Dermatology",
         visit_type=VisitType.follow_up, scheduled_at=_at(0, 14, 30),
         duration_minutes=15, status=AppointmentStatus.scheduled,
         reason="Psoriasis treatment review"),
    dict(patient_name="Lakshmi Menon", patient_phone="+91-98450 29038",
         doctor_name="Dr. Priya Nair", department="General Medicine",
         visit_type=VisitType.consultation, scheduled_at=_at(0, 16),
         status=AppointmentStatus.scheduled, reason="Persistent fatigue"),
    # --- upcoming ---
    dict(patient_name="Vihaan Sharma", patient_phone="+91-98710 60433",
         doctor_name="Dr. Naina Kapoor", department="Pediatrics",
         visit_type=VisitType.consultation, scheduled_at=_at(1, 10),
         status=AppointmentStatus.scheduled, reason="Recurrent ear infection"),
    dict(patient_name="Nandini Pillai", patient_phone="+91-99460 35271",
         doctor_name="Dr. Asha Verma", department="Cardiology",
         visit_type=VisitType.checkup, scheduled_at=_at(1, 11, 30),
         duration_minutes=40, status=AppointmentStatus.scheduled,
         reason="Hypertension monitoring"),
    dict(patient_name="Arjun Deshmukh", patient_phone="+91-98900 51746",
         doctor_name="Dr. Vikram Rao", department="Orthopedics",
         visit_type=VisitType.emergency, scheduled_at=_at(2, 9, 30),
         duration_minutes=60, status=AppointmentStatus.scheduled,
         reason="Suspected wrist fracture"),
    dict(patient_name="Priyanka Joshi", patient_phone="+91-97690 24508",
         doctor_name="Dr. Imran Sheikh", department="Dermatology",
         visit_type=VisitType.consultation, scheduled_at=_at(3, 13),
         status=AppointmentStatus.scheduled, reason="Acne treatment plan"),
    dict(patient_name="Suresh Kulkarni", patient_phone="+91-98500 73192",
         doctor_name="Dr. Priya Nair", department="General Medicine",
         visit_type=VisitType.follow_up, scheduled_at=_at(4, 15, 30),
         status=AppointmentStatus.scheduled, reason="Diabetes review — HbA1c"),
    dict(patient_name="Tanvi Bhat", patient_phone="+91-99200 46815",
         doctor_name="Dr. Asha Verma", department="Cardiology",
         visit_type=VisitType.consultation, scheduled_at=_at(5, 10, 30),
         status=AppointmentStatus.cancelled, reason="Travel — rebook requested"),
    dict(patient_name="Reyansh Gupta", patient_phone="+91-98100 93527",
         doctor_name="Dr. Naina Kapoor", department="Pediatrics",
         visit_type=VisitType.checkup, scheduled_at=_at(6, 11),
         status=AppointmentStatus.scheduled, reason="Growth assessment"),
]


def seed() -> None:
    db = SessionLocal()
    try:
        existing = db.execute(select(func.count(Appointment.id))).scalar_one()
        if existing:
            log.info("appointments table already populated (%s rows) — skipping", existing)
            return
        db.add_all(Appointment(**row) for row in DEMO_APPOINTMENTS)
        db.commit()
        log.info("seeded %s demo appointments", len(DEMO_APPOINTMENTS))
    finally:
        db.close()


if __name__ == "__main__":
    seed()
