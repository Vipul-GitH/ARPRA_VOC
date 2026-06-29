"""add has_updates to feedback_responses

Revision ID: 0005_add_has_updates_to_feedback_responses
Revises: 0004_add_skip_logic_to_campaigns
Create Date: 2026-04-02 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_add_has_updates_to_feedback_responses"
down_revision = "0004_add_skip_logic_to_campaigns"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_cols = (
        {col["name"] for col in inspector.get_columns("feedback_responses")}
        if inspector.has_table("feedback_responses")
        else set()
    )
    if "has_updates" not in existing_cols:
        op.add_column(
            "feedback_responses",
            sa.Column("has_updates", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_cols = (
        {col["name"] for col in inspector.get_columns("feedback_responses")}
        if inspector.has_table("feedback_responses")
        else set()
    )
    if "has_updates" in existing_cols:
        op.drop_column("feedback_responses", "has_updates")
