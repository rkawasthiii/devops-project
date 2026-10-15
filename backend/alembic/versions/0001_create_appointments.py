"""create appointments table

Revision ID: 0001_create_appointments
Revises:
Create Date: 2026-10-10 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "0001_create_appointments"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_name", sa.String(length=120), nullable=False),
        sa.Column("patient_phone", sa.String(length=32), nullable=True),
        sa.Column("doctor_name", sa.String(length=120), nullable=False),
        sa.Column("department", sa.String(length=80), nullable=False),
        sa.Column("visit_type", sa.String(length=40), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_appointments_status", "appointments", ["status"])
    op.create_index("ix_appointments_scheduled_at", "appointments", ["scheduled_at"])


def downgrade() -> None:
    op.drop_index("ix_appointments_scheduled_at", table_name="appointments")
    op.drop_index("ix_appointments_status", table_name="appointments")
    op.drop_table("appointments")
