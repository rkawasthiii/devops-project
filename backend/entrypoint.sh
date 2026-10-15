#!/bin/sh
set -e

# Wait for PostgreSQL to accept connections (covers container and K8s starts).
python - <<'PY'
import os, sys, time
from sqlalchemy import create_engine, text

url = os.environ["DATABASE_URL"]
last_err = None
for attempt in range(1, 31):
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("database is reachable")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        last_err = exc
        print(f"waiting for database ({attempt}/30): {exc}")
        time.sleep(2)
sys.exit(f"database never became reachable: {last_err}")
PY

echo "running database migrations"
alembic upgrade head

echo "seeding demo data (skipped automatically if already seeded)"
python -m app.seed

echo "starting uvicorn"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
