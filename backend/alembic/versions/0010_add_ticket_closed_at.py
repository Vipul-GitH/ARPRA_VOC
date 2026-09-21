"""add ticket closed timestamp

Revision ID: 0010_add_ticket_closed_at
Revises: 0009_add_no_of_pricks
Create Date: 2026-09-21 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0010_add_ticket_closed_at"
down_revision = "0009_add_no_of_pricks"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("feedback_tickets"):
        return
    existing = {column["name"] for column in inspector.get_columns("feedback_tickets")}
    if "closed_at" not in existing:
        op.add_column("feedback_tickets", sa.Column("closed_at", sa.DateTime(), nullable=True))
    op.execute(
        """
        UPDATE feedback_tickets ticket
        SET closed_at = COALESCE(
            (SELECT MAX(ticket_updates.updated_at)
             FROM ticket_updates
             WHERE ticket_updates.ticket_id = ticket.id),
            ticket.created_at
        )
        WHERE ticket.status = 'closed' AND ticket.closed_at IS NULL
        """
    )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("feedback_tickets"):
        return
    existing = {column["name"] for column in inspector.get_columns("feedback_tickets")}
    if "closed_at" in existing:
        op.drop_column("feedback_tickets", "closed_at")
