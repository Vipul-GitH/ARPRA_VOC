"""add campaign header_title

Revision ID: 0002_add_campaign_header_title
Revises: 0001_create_infra_tables
Create Date: 2025-12-26
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002_add_campaign_header_title"
down_revision = "0001_create_infra_tables"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_cols = {col["name"] for col in inspector.get_columns("campaigns")} if inspector.has_table("campaigns") else set()
    if "header_title" not in existing_cols:
        op.add_column("campaigns", sa.Column("header_title", sa.String(length=255), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_cols = {col["name"] for col in inspector.get_columns("campaigns")} if inspector.has_table("campaigns") else set()
    if "header_title" in existing_cols:
        op.drop_column("campaigns", "header_title")
