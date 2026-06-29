from datetime import datetime, timedelta
from typing import Dict, Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Campaign,
    CampaignRecipient,
    FeedbackResponse,
    FeedbackTicket,
    ResponseReward,
)
from app.routers.auth import get_current_user

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")
SPECIAL_CAMPAIGN_CODES = ("code_5", "code_6")


def _regular_campaign_filter(query, campaign_id_col):
    campaign_code = func.lower(Campaign.code)
    return (
        query.outerjoin(Campaign, Campaign.id == campaign_id_col)
        .filter(
            _regular_campaign_condition()
        )
    )


def _regular_campaign_condition():
    campaign_code = func.lower(Campaign.code)
    return (
        (Campaign.id.is_(None))
        | (Campaign.code.is_(None))
        | (~campaign_code.in_(SPECIAL_CAMPAIGN_CODES))
    )


@router.get("/dashboard")
async def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    range: str = Query("30d", alias="range"),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
):
    """Dashboard with richer stats and time windowing."""

    def parse_window(range_param: str, start_param: Optional[str], end_param: Optional[str]):
        now = datetime.utcnow()
        # Priority: explicit start/end overrides the preset ranges.
        if start_param:
            try:
                window_start = datetime.fromisoformat(start_param)
            except ValueError:
                window_start = now - timedelta(days=30)
        else:
            days = 30
            if range_param in {"7d", "30d", "90d"}:
                days = int(range_param.replace("d", ""))
            window_start = now - timedelta(days=days)

        if end_param:
            try:
                window_end = datetime.fromisoformat(end_param)
            except ValueError:
                window_end = now
        else:
            window_end = now

        if window_start > window_end:
            window_start, window_end = window_end - timedelta(days=30), window_end

        label = f"{window_start.date()} \u2192 {window_end.date()}"
        return window_start, window_end, label

    window_start, window_end, window_label = parse_window(range, start, end)
    window_span = window_end - window_start
    prior_start = window_start - window_span
    prior_end = window_start

    # Windowed aggregates
    window_feedback = (
        _regular_campaign_filter(db.query(func.count(FeedbackResponse.id)), FeedbackResponse.campaign_id)
        .filter(FeedbackResponse.submission_time.between(window_start, window_end))
        .scalar()
        or 0
    )
    window_complaints = (
        _regular_campaign_filter(db.query(func.count(FeedbackResponse.id)), FeedbackResponse.campaign_id)
        .filter(FeedbackResponse.is_complaint.is_(True))
        .filter(FeedbackResponse.submission_time.between(window_start, window_end))
        .scalar()
        or 0
    )
    complaint_rate = round((window_complaints / window_feedback) * 100, 1) if window_feedback else 0

    prior_feedback = (
        _regular_campaign_filter(db.query(func.count(FeedbackResponse.id)), FeedbackResponse.campaign_id)
        .filter(FeedbackResponse.submission_time.between(prior_start, prior_end))
        .scalar()
        or 0
    )
    feedback_delta = window_feedback - prior_feedback

    # Lifetime basics
    total_feedback = (
        _regular_campaign_filter(db.query(func.count(FeedbackResponse.id)), FeedbackResponse.campaign_id).scalar() or 0
    )
    open_statuses = ["open", "in_progress"]
    open_tickets = (
        _regular_campaign_filter(db.query(FeedbackTicket), FeedbackTicket.campaign_id)
        .filter(FeedbackTicket.status.in_(open_statuses))
        .count()
    )

    # Ticket breakdowns
    tickets_by_status_rows = (
        _regular_campaign_filter(
            db.query(FeedbackTicket.status, func.count(FeedbackTicket.id)),
            FeedbackTicket.campaign_id,
        )
        .group_by(FeedbackTicket.status)
        .all()
    )
    tickets_by_status = {row[0] or "unknown": row[1] for row in tickets_by_status_rows} if tickets_by_status_rows else {}

    tickets_by_severity_rows = (
        _regular_campaign_filter(
            db.query(FeedbackTicket.severity, func.count(FeedbackTicket.id)),
            FeedbackTicket.campaign_id,
        )
        .group_by(FeedbackTicket.severity)
        .all()
    )
    tickets_by_severity = {row[0] or "unknown": row[1] for row in tickets_by_severity_rows} if tickets_by_severity_rows else {}

    open_ticket_dates = (
        _regular_campaign_filter(db.query(FeedbackTicket.created_at), FeedbackTicket.campaign_id)
        .filter(FeedbackTicket.status.in_(open_statuses))
        .all()
    )
    now = datetime.utcnow()
    open_ticket_age_days = [
        max((now - row[0]).days, 0)
        for row in open_ticket_dates
        if row[0]
    ]
    avg_ticket_age_days = round(sum(open_ticket_age_days) / len(open_ticket_age_days), 1) if open_ticket_age_days else 0

    # Campaign response rates & top movers
    response_stats = (
        _regular_campaign_filter(
            db.query(
            FeedbackResponse.campaign_id.label("cid"),
            func.count(FeedbackResponse.id).label("responses"),
            func.sum(
                case(
                    (FeedbackResponse.is_complaint.is_(True), 1),
                    else_=0,
                )
            ).label("complaints"),
            ),
            FeedbackResponse.campaign_id,
        )
        .group_by(FeedbackResponse.campaign_id)
        .subquery()
    )
    recipient_stats = (
        _regular_campaign_filter(
            db.query(
            CampaignRecipient.campaign_id.label("cid"),
            func.count(CampaignRecipient.id).label("recipients"),
            ),
            CampaignRecipient.campaign_id,
        )
        .group_by(CampaignRecipient.campaign_id)
        .subquery()
    )
    campaign_response_rates = (
        db.query(
            Campaign.name,
            func.coalesce(response_stats.c.responses, 0),
            func.coalesce(recipient_stats.c.recipients, 0),
            func.coalesce(response_stats.c.complaints, 0),
        )
        .outerjoin(response_stats, response_stats.c.cid == Campaign.id)
        .outerjoin(recipient_stats, recipient_stats.c.cid == Campaign.id)
        .filter(_regular_campaign_condition())
        .order_by(func.coalesce(response_stats.c.responses, 0).desc(), Campaign.name)
        .limit(5)
        .all()
    )

    # Manual review queue & rewards
    manual_review_count = (
        _regular_campaign_filter(db.query(func.count(FeedbackResponse.id)), FeedbackResponse.campaign_id)
        .filter(FeedbackResponse.needs_manual_review.is_(True))
        .scalar()
        or 0
    )
    manual_review_items = (
        db.query(
            FeedbackResponse.submission_time,
            FeedbackResponse.overall_score,
            FeedbackResponse.overall_sentiment,
            Campaign.name,
        )
        .join(Campaign, Campaign.id == FeedbackResponse.campaign_id)
        .filter(_regular_campaign_condition())
        .filter(FeedbackResponse.needs_manual_review.is_(True))
        .order_by(FeedbackResponse.submission_time.desc())
        .limit(5)
        .all()
    )

    pending_rewards = (
        _regular_campaign_filter(
            db.query(func.count(ResponseReward.id)).join(
                FeedbackResponse, FeedbackResponse.id == ResponseReward.response_id
            ),
            FeedbackResponse.campaign_id,
        )
        .filter(ResponseReward.status == "pending")
        .scalar()
        or 0
    )

    # Sentiment mix by language (windowed)
    sentiment_rows = (
        _regular_campaign_filter(
            db.query(
            FeedbackResponse.language,
            FeedbackResponse.overall_sentiment,
            func.count(FeedbackResponse.id),
            ),
            FeedbackResponse.campaign_id,
        )
        .filter(FeedbackResponse.submission_time.between(window_start, window_end))
        .group_by(FeedbackResponse.language, FeedbackResponse.overall_sentiment)
        .all()
    )
    sentiment_by_language: Dict[str, Dict[str, int]] = {}
    for lang, sentiment, count in sentiment_rows:
        lang_key = lang or "unknown"
        sentiment_key = sentiment or "neutral"
        sentiment_by_language.setdefault(lang_key, {})[sentiment_key] = count

    # Campaigns and responses over time
    campaign_breakdown = (
        db.query(Campaign.name, func.count(FeedbackResponse.id))
        .join(FeedbackResponse, FeedbackResponse.campaign_id == Campaign.id)
        .filter(_regular_campaign_condition())
        .filter(FeedbackResponse.submission_time.between(window_start, window_end))
        .group_by(Campaign.name)
        .order_by(func.count(FeedbackResponse.id).desc())
        .limit(5)
        .all()
    )

    daily_trend = (
        _regular_campaign_filter(
            db.query(func.date(FeedbackResponse.submission_time).label("date"), func.count(FeedbackResponse.id)),
            FeedbackResponse.campaign_id,
        )
        .filter(FeedbackResponse.submission_time.between(window_start, window_end))
        .group_by(func.date(FeedbackResponse.submission_time))
        .order_by(func.date(FeedbackResponse.submission_time))
        .all()
    )
    daily_trend_max = max([row[1] for row in daily_trend]) if daily_trend else 0

    recent_responses = (
        db.query(
            FeedbackResponse.submission_time,
            FeedbackResponse.overall_sentiment,
            Campaign.name,
        )
        .join(Campaign, Campaign.id == FeedbackResponse.campaign_id)
        .filter(_regular_campaign_condition())
        .order_by(FeedbackResponse.submission_time.desc())
        .limit(10)
        .all()
    )

    campaign_statuses = (
        db.query(Campaign)
        .filter(_regular_campaign_condition())
        .order_by(func.coalesce(Campaign.updated_at, Campaign.created_at).desc(), Campaign.created_at.desc())
        .limit(6)
        .all()
    )

    return templates.TemplateResponse(
        "dashboard/index.html",
        {
            "request": request,
            "user": user,
            "stats": {
                "window_start": window_start,
                "window_end": window_end,
                "window_label": window_label,
                "window_feedback": window_feedback,
                "feedback_delta": feedback_delta,
                "window_complaints": window_complaints,
                "complaint_rate": complaint_rate,
                "total_feedback": total_feedback,
                "open_tickets": open_tickets,
                "avg_ticket_age_days": avg_ticket_age_days,
                "tickets_by_status": tickets_by_status,
                "tickets_by_severity": tickets_by_severity,
                "campaign_breakdown": campaign_breakdown,
                "daily_trend": daily_trend,
                "daily_trend_max": daily_trend_max,
                "sentiment_by_language": sentiment_by_language,
                "campaign_response_rates": campaign_response_rates,
                "recent_responses": recent_responses,
                "manual_review_count": manual_review_count,
                "manual_review_items": manual_review_items,
                "pending_rewards": pending_rewards,
                "campaign_statuses": campaign_statuses,
            },
        },
    )
