"""add booking display fields

Revision ID: 0007_add_booking_display_fields
Revises: 0006_add_hot_path_indexes
Create Date: 2026-09-21 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0007_add_booking_display_fields"
down_revision = "0006_add_hot_path_indexes"
branch_labels = None
depends_on = None


COLUMNS = [
    sa.Column("booking_code", sa.String(length=40), nullable=True),
    sa.Column("age_years", sa.Integer(), nullable=True),
    sa.Column("preferred_time_slot", sa.String(length=30), nullable=True),
    sa.Column("panel_company", sa.String(length=150), nullable=True),
    sa.Column("booking_status", sa.SmallInteger(), nullable=True),
    sa.Column("payment_mode", sa.String(length=120), nullable=True),
    sa.Column("start_time", sa.String(length=20), nullable=True),
    sa.Column("assigned_phlebotomist_id", sa.BigInteger(), nullable=True),
]


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("bookings"):
        return
    existing = {column["name"] for column in inspector.get_columns("bookings")}
    for column in COLUMNS:
        if column.name not in existing:
            op.add_column("bookings", column)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("bookings"):
        return
    existing = {column["name"] for column in inspector.get_columns("bookings")}
    for column in reversed(COLUMNS):
        if column.name in existing:
            op.drop_column("bookings", column.name)
