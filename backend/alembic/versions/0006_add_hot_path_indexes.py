"""add hot path indexes

Revision ID: 0006_add_hot_path_indexes
Revises: 0005_add_has_updates_to_feedback_responses
Create Date: 2026-07-02 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0006_add_hot_path_indexes"
down_revision = "0005_add_has_updates_to_feedback_responses"
branch_labels = None
depends_on = None


INDEXES = [
    ("feedback_responses", "idx_feedback_responses_campaign_time", ["campaign_id", "submission_time"]),
    ("feedback_responses", "idx_feedback_responses_status_time", ["status", "submission_time"]),
    ("feedback_responses", "idx_feedback_responses_complaint_time", ["is_complaint", "submission_time"]),
    ("feedback_responses", "idx_feedback_responses_manual_review_time", ["needs_manual_review", "submission_time"]),
    ("feedback_responses", "idx_feedback_responses_recipient", ["recipient_id"]),
    ("feedback_responses", "idx_feedback_responses_ticket", ["ticket_id"]),
    ("feedback_answers", "idx_feedback_answers_response_question", ["response_id", "campaign_question_id"]),
    ("feedback_tickets", "idx_feedback_tickets_campaign_status", ["campaign_id", "status"]),
    ("feedback_tickets", "idx_feedback_tickets_status_created", ["status", "created_at"]),
    ("feedback_tickets", "idx_feedback_tickets_response", ["response_id"]),
    ("campaign_recipients", "idx_campaign_recipients_campaign_status", ["campaign_id", "status"]),
    ("campaign_recipients", "idx_campaign_recipients_list", ["recipient_list_id"]),
    ("campaign_questions", "idx_campaign_questions_campaign_order", ["campaign_id", "order_index"]),
    ("campaign_question_options", "idx_campaign_question_options_question_order", ["campaign_question_id", "order_index"]),
    ("bookings", "idx_bookings_campaign_send", ["isCampaingsend", "bookingid"]),
    ("bookings", "idx_bookings_response_submitted", ["isResponseSubmitted", "bookingid"]),
    ("bookings", "idx_bookings_enterdate", ["enterdate"]),
]


def _existing_indexes(inspector, table_name: str) -> set[str]:
    return {idx["name"] for idx in inspector.get_indexes(table_name)}


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for table_name, index_name, columns in INDEXES:
        if not inspector.has_table(table_name):
            continue
        if index_name in _existing_indexes(inspector, table_name):
            continue
        existing_cols = {col["name"] for col in inspector.get_columns(table_name)}
        if all(col in existing_cols for col in columns):
            op.create_index(index_name, table_name, columns)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for table_name, index_name, _columns in reversed(INDEXES):
        if not inspector.has_table(table_name):
            continue
        if index_name in _existing_indexes(inspector, table_name):
            op.drop_index(index_name, table_name=table_name)
