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
    op.add_column("master_questions", sa.Column("placeholder_en", sa.String(length=255), nullable=True))
    op.add_column("campaign_questions", sa.Column("placeholder_en", sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column("campaign_questions", "placeholder_en")
    op.drop_column("master_questions", "placeholder_en")
