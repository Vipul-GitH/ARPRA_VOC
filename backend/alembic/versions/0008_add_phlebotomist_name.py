"""add assigned phlebotomist name to bookings

Revision ID: 0008_add_phlebotomist_name
Revises: 0007_add_booking_display_fields
Create Date: 2026-09-21 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0008_add_phlebotomist_name"
down_revision = "0007_add_booking_display_fields"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("bookings"):
        return
    existing = {column["name"] for column in inspector.get_columns("bookings")}
    if "assigned_phlebotomist_name" not in existing:
        op.add_column(
            "bookings",
            sa.Column("assigned_phlebotomist_name", sa.String(length=255), nullable=True),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("bookings"):
        return
    existing = {column["name"] for column in inspector.get_columns("bookings")}
    if "assigned_phlebotomist_name" in existing:
        op.drop_column("bookings", "assigned_phlebotomist_name")
