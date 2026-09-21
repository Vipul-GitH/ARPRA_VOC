"""add daily summary scheduler guards

Revision ID: 0011_add_daily_summary_guards
Revises: 0010_add_ticket_closed_at
Create Date: 2026-09-21 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0011_add_daily_summary_guards"
down_revision = "0010_add_ticket_closed_at"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("scheduler_locks"):
        op.create_table(
            "scheduler_locks",
            sa.Column("lock_name", sa.String(length=100), primary_key=True),
            sa.Column("owner_token", sa.String(length=255), nullable=False),
            sa.Column("expires_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
        )

    if not inspector.has_table("daily_summary_runs"):
        op.create_table(
            "daily_summary_runs",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("report_date", sa.Date(), nullable=False),
            sa.Column("status", sa.String(length=30), nullable=False),
            sa.Column("owner_token", sa.String(length=255), nullable=True),
            sa.Column("locked_until", sa.DateTime(), nullable=True),
            sa.Column("sent_at", sa.DateTime(), nullable=True),
            sa.Column("message_snapshot", sa.Text(), nullable=True),
            sa.Column("error_message", sa.String(length=1000), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.UniqueConstraint("report_date", name="uq_daily_summary_runs_report_date"),
        )
        op.create_index(
            "ix_daily_summary_runs_status_locked_until",
            "daily_summary_runs",
            ["status", "locked_until"],
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("daily_summary_runs"):
        op.drop_index("ix_daily_summary_runs_status_locked_until", table_name="daily_summary_runs")
        op.drop_table("daily_summary_runs")
    if inspector.has_table("scheduler_locks"):
        op.drop_table("scheduler_locks")
