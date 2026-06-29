from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import FeedbackAnswer, FeedbackResponse, FeedbackTicket


def compute_scores(
    response: FeedbackResponse,
    answers: List[FeedbackAnswer],
    campaign_code: str | None = None,
):
    # Scoring disabled; use only sentiment.
    response.overall_score = None
    response.overall_rating_value = None
    normalized_campaign_code = (campaign_code or "").strip().lower()

    has_negative = any(a.sentiment == "negative" for a in answers)
    has_neutral = any(a.sentiment == "neutral" for a in answers)

    if has_negative:
        response.overall_sentiment = "negative"
        response.is_complaint = True
        response.status = "ticket_created"
    elif has_neutral:
        response.overall_sentiment = "neutral"
        response.needs_manual_review = True
        response.status = "manual_review"
    else:
        response.overall_sentiment = "positive"
        if normalized_campaign_code == "code_3":
            response.needs_manual_review = True
            response.status = "manual_review"
        else:
            response.status = "auto_processed"


def create_ticket_if_needed(db: Session, response: FeedbackResponse) -> Optional[FeedbackTicket]:
    if not response.is_complaint:
        return None
    ticket = FeedbackTicket(
        ticket_number=f"TKT-{response.id}",
        response_id=response.id,
        campaign_id=response.campaign_id,
        severity="high" if response.overall_sentiment == "negative" else "medium",
        summary="Complaint triggered by low rating",
        details="System generated ticket for complaint",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    response.ticket_id = ticket.id
    db.commit()
    return ticket
