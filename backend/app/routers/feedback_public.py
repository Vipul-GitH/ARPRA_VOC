import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import Campaign, CampaignQuestion, CampaignRecipient, FeedbackAnswer, FeedbackResponse, QuestionFlowRule
from app.services.feedback import compute_scores, create_ticket_if_needed
router = APIRouter(tags=["feedback_public"], include_in_schema=False)
templates = Jinja2Templates(directory="app/templates")


def load_campaign_by_token(db: Session, token: str) -> tuple[Campaign, Optional[CampaignRecipient]]:
    recipient = db.query(CampaignRecipient).filter(CampaignRecipient.personalized_link_token == token).first()
    if recipient:
        campaign = recipient.campaign
        return campaign, recipient
    campaign_query = db.query(Campaign).filter(Campaign.code == token)
    if token.isdigit():
        campaign_query = campaign_query.union(db.query(Campaign).filter(Campaign.id == int(token)))
    campaign = campaign_query.first()
    return campaign, None


def _phlebo_engine():
    settings = get_settings()
    url = make_url(settings.database_url).set(database="phlebo_summary")
    return create_engine(str(url), pool_pre_ping=True)


def _prefill_from_booking(request: Request) -> dict:
    bookingid = request.query_params.get("bookingid")
    mobile_param = request.query_params.get("mobile")
    prefill = {"name": "", "mobile_country": "+91", "mobile_number": "", "lab_id": ""}
    if not bookingid and not mobile_param:
        return prefill
    try:
        engine = _phlebo_engine()
        with engine.connect() as conn:
            row = None
            if bookingid:
                row = conn.execute(
                    text(
                        "SELECT customername, mobile, bookingid FROM tblbooking WHERE bookingid = :bid LIMIT 1"
                    ),
                    {"bid": bookingid},
                ).mappings().first()
            if not row and mobile_param:
                row = conn.execute(
                    text(
                        """
                        SELECT customername, mobile, bookingid
                        FROM tblbooking
                        WHERE mobile = :mob
                        ORDER BY bookingid DESC
                        LIMIT 1
                        """
                    ),
                    {"mob": mobile_param},
                ).mappings().first()
            if row:
                prefill["name"] = row.get("customername") or ""
                digits = "".join(ch for ch in (row.get("mobile") or "") if ch.isdigit())
                if len(digits) > 10 and digits.startswith("91"):
                    digits = digits[-10:]
                prefill["mobile_number"] = digits or (mobile_param or "")
                prefill["lab_id"] = str(row.get("bookingid")) if row.get("bookingid") is not None else ""
    except Exception:
        pass
    return prefill


@router.get("/{token}")
async def view_form(token: str, request: Request, db: Session = Depends(get_db)):
    campaign, recipient = load_campaign_by_token(db, token)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    questions = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign.id)
        .order_by(CampaignQuestion.order_index)
        .all()
    )
    first_question = questions[0] if questions else None
    total_questions = len(questions)
    flow_rules_data = []
    prefill = _prefill_from_booking(request)
    db.commit()
    return templates.TemplateResponse(
        "feedback/form.html",
        {
            "request": request,
            "campaign": campaign,
            "recipient": recipient,
            "questions": questions,
            "total_questions": total_questions,
            "token": token,
            "flow_rules": flow_rules_data,
            "flow_rules_json": json.dumps(flow_rules_data),
            "flow_mapping_json": json.dumps(campaign.exp_flow_map or {}),
            "flow_source_question_id": first_question.id if first_question else None,
            "prefill": prefill,
        },
    )


@router.post("/{token}")
async def submit_form(token: str, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    campaign, recipient = load_campaign_by_token(db, token)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    questions = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign.id)
        .order_by(CampaignQuestion.order_index)
        .all()
    )
    first_question = questions[0] if questions else None
    total_questions = len(questions)
    flow_rules_data = []
    # Collect respondent info
    name = form.get("resp_name", "").strip()
    mobile_country = form.get("resp_mobile_country", "").strip() or "+91"
    mobile_number = form.get("resp_mobile_number", "").strip()
    lab_id = (form.get("resp_lab_id") or "").strip() or None
    visit_date = (form.get("resp_visit_date") or "").strip() or None
    def render_error(msg: str, status: int = 400):
        return templates.TemplateResponse(
            "feedback/form.html",
            {
                "request": request,
                "campaign": campaign,
                "recipient": recipient,
                "questions": questions,
                "total_questions": total_questions,
            "token": token,
            "flow_rules": flow_rules_data,
            "flow_rules_json": json.dumps(flow_rules_data),
            "flow_mapping_json": json.dumps(campaign.exp_flow_map or {}),
            "flow_source_question_id": first_question.id if first_question else None,
            "error": msg,
        },
            status_code=status,
        )

    if not name or not mobile_number:
        return render_error("Name and mobile are required")
    if mobile_country == "+91" and (not mobile_number.isdigit() or len(mobile_number) != 10):
        return render_error("Enter a valid 10-digit mobile number for India")
    pii_data = {
        "name": name,
        "mobile_country": mobile_country,
        "mobile_number": mobile_number,
        "lab_id": lab_id,
        "visit_date": visit_date,
    }

    response = FeedbackResponse(
        campaign_id=campaign.id,
        recipient_id=recipient.id if recipient else None,
        pii_data_json=pii_data,
    )
    db.add(response)
    db.commit()
    db.refresh(response)

    answers = []
    questions = db.query(CampaignQuestion).filter(CampaignQuestion.campaign_id == campaign.id).all()
    for question in questions:
        key = f"q_{question.id}"
        if question.question_type == "mcq_multi":
            value = form.getlist(key)
        else:
            value = form.get(key)
        selected_values = value if isinstance(value, list) else [value] if value else []
        answer_text = value if question.question_type in ["text"] else None
        selected_option_values = selected_values if question.question_type.startswith("mcq") or question.question_type.startswith("rating") else []
        sentiment = None
        score = None
        follow_up_text = None
        if selected_option_values:
            option = (
                db.query(CampaignQuestionOption)
                .filter(
                    CampaignQuestionOption.campaign_question_id == question.id,
                    CampaignQuestionOption.option_value == selected_option_values[0],
                )
                .first()
            )
            if option:
                sentiment = option.sentiment
                score = option.score_value
        # capture follow-up text if any selected option has follow-up
        if question.options:
            for opt in question.options:
                if opt.follow_up_label and opt.option_value in selected_option_values:
                    fu_key = f"followup_{question.id}_{opt.option_value}"
                    fu_val = form.get(fu_key)
                    if fu_val:
                        follow_up_text = fu_val
                        break
        ans = FeedbackAnswer(
            response_id=response.id,
            campaign_question_id=question.id,
            question=question,
            answer_text=answer_text,
            selected_option_values=selected_option_values,
            sentiment=sentiment,
            score_value=score,
            department=None,
            area=None,
            follow_up_text=follow_up_text,
        )
        db.add(ans)
        answers.append(ans)
    db.commit()

    compute_scores(response, answers)
    db.commit()
    create_ticket_if_needed(db, response)

    return templates.TemplateResponse(
        "feedback/thank_you.html",
        {"request": request, "campaign": campaign, "response": response},
    )


from app.models import CampaignQuestionOption  # noqa: E402  keep import local to avoid circular
