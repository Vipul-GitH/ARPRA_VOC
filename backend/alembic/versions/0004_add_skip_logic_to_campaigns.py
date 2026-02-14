"""add skip_logic to campaigns

Revision ID: 0004_add_skip_logic_to_campaigns
Revises: 0003_add_question_placeholders
Create Date: 2026-02-07 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0004_add_skip_logic_to_campaigns"
down_revision = "0003_add_question_placeholders"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("campaigns", sa.Column("skip_logic", sa.JSON(), nullable=True))


def downgrade():
    op.drop_column("campaigns", "skip_logic")

