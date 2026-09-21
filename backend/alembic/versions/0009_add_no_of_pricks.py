"""add number of pricks to bookings

Revision ID: 0009_add_no_of_pricks
Revises: 0008_add_phlebotomist_name
Create Date: 2026-09-21 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0009_add_no_of_pricks"
down_revision = "0008_add_phlebotomist_name"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("bookings"):
        return
    existing = {column["name"] for column in inspector.get_columns("bookings")}
    if "no_of_pricks" not in existing:
        op.add_column(
            "bookings",
            sa.Column("no_of_pricks", sa.String(length=20), nullable=True),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("bookings"):
        return
    existing = {column["name"] for column in inspector.get_columns("bookings")}
    if "no_of_pricks" in existing:
        op.drop_column("bookings", "no_of_pricks")
