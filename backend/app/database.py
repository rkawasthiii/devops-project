"""Database engine and session configuration.

The connection string is taken from the DATABASE_URL environment variable so
that the same code runs against docker-compose, Kubernetes and a developer's
local PostgreSQL instance without modification.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://medidesk:medidesk@localhost:5432/medidesk",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a scoped database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
