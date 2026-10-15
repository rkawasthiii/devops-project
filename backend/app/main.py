"""MediDesk API — clinic appointment management backend.

FastAPI application exposing appointment CRUD, dashboard statistics,
operational health endpoints and Prometheus metrics.
"""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import get_db
from .routers import appointments

app = FastAPI(
    title="MediDesk API",
    version="1.0.0",
    description="Clinic appointment management platform — DevOps Capstone project.",
)

# Same-origin routing is handled by Nginx/Ingress; CORS stays permissive so the
# API can also be called directly during local development and demos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, include_in_schema=False)

app.include_router(appointments.router, prefix="/api")


@app.get("/", tags=["ops"])
def root():
    return {
        "service": "medidesk-api",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["ops"])
def health():
    """Liveness probe — cheap check that the process is up."""
    return {"status": "ok"}


@app.get("/ready", tags=["ops"])
def ready(db: Session = Depends(get_db)):
    """Readiness probe — verifies the database is reachable before traffic."""
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse({"status": "not ready"}, status_code=503)
    return {"status": "ready"}
