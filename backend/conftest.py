"""Pytest fixtures — isolated in-memory SQLite database.

The real DATABASE_URL (PostgreSQL) is never touched: `get_db` is overridden
with a session bound to a StaticPool SQLite engine, and tables are recreated
from ORM metadata. Every test also gets a clean table state.
"""

import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_tables():
    yield
    with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_appointment():
    return {
        "patient_name": "Test Patient",
        "patient_phone": "+91-90000 00000",
        "doctor_name": "Dr. Test",
        "department": "General Medicine",
        "visit_type": "consultation",
        "scheduled_at": "2030-01-15T10:30:00",
        "duration_minutes": 30,
        "reason": "Routine visit",
    }
