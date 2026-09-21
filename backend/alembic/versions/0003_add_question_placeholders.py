"""add placeholder for text questions

Revision ID: 0003_add_question_placeholders
Revises: 0002_add_campaign_header_title
Create Date: 2025-12-27
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0003_add_question_placeholders"
down_revision = "0002_add_campaign_header_title"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for table_name in ("master_questions", "campaign_questions"):
        existing_cols = (
            {col["name"] for col in inspector.get_columns(table_name)}
            if inspector.has_table(table_name)
            else set()
        )
        if "placeholder_en" not in existing_cols:
            op.add_column(table_name, sa.Column("placeholder_en", sa.String(length=255), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for table_name in ("campaign_questions", "master_questions"):
        existing_cols = (
            {col["name"] for col in inspector.get_columns(table_name)}
            if inspector.has_table(table_name)
            else set()
        )
        if "placeholder_en" in existing_cols:
            op.drop_column(table_name, "placeholder_en")
