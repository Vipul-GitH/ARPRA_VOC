import ast
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Campaign, FeedbackResponse
from app.routers.auth import get_current_user
import pytz
from datetime import datetime

router = APIRouter(tags=["responses"])
templates = Jinja2Templates(directory="app/templates")
local_tz = pytz.timezone("Asia/Kolkata")


def local_time(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S"):
    if not dt:
        return ""
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(local_tz).strftime(fmt)


templates.env.filters["local_time"] = local_time


@router.get("/")
async def list_responses(
    request: Request,
    campaign_id: int | None = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(FeedbackResponse)
    if campaign_id:
        query = query.filter(FeedbackResponse.campaign_id == campaign_id)
    responses = query.order_by(FeedbackResponse.submission_time.desc()).all()
    campaigns = db.query(Campaign).all()
    return templates.TemplateResponse(
        "responses/list.html",
        {
            "request": request,
            "responses": responses,
            "campaigns": campaigns,
            "selected_campaign": campaign_id,
            "user": user,
        },
    )


@router.get("/{response_id}")
async def response_detail(
    response_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    response = db.query(FeedbackResponse).get(response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    answer_labels: dict[int, list[str]] = {}
    for answer in response.answers:
        raw = answer.selected_option_values
        values: list[str] = []
        if isinstance(raw, list):
            values = [str(v) for v in raw]
        elif isinstance(raw, str):
            raw = raw.strip()
            if raw:
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        values = [str(v) for v in parsed]
                    else:
                        values = [str(parsed)]
                except Exception:
                    try:
                        parsed = ast.literal_eval(raw)
                        if isinstance(parsed, (list, tuple)):
                            values = [str(v) for v in parsed]
                        else:
                            values = [str(parsed)]
                    except Exception:
                        if "," in raw:
                            values = [part.strip() for part in raw.split(",") if part.strip()]
                        else:
                            values = [raw]
        if values:
            cleaned: list[str] = []
            for value in values:
                value = value.strip().strip("[]").strip()
                if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
                    value = value[1:-1]
                cleaned.append(value)
            values = cleaned
        elif raw is not None:
            values = [str(raw)]
        labels: list[str] = []
        seen: set[str] = set()
        for value in values:
            opt = next(
                (opt for opt in (answer.question.options or []) if str(opt.option_value) == value),
                None,
            )
            label = opt.option_text_en if opt and opt.option_text_en else value
            if label not in seen:
                labels.append(label)
                seen.add(label)
        if labels:
            answer_labels[answer.id] = labels
    return templates.TemplateResponse(
        "responses/detail.html",
        {"request": request, "response": response, "answer_labels": answer_labels, "user": user},
    )
