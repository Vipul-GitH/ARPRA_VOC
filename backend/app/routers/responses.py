import ast
import csv
import io
import json
import math
from urllib.parse import urlencode

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, text
from sqlalchemy.orm import Session, joinedload, selectinload

from app.database import get_db
from app.models import Campaign, CampaignQuestion, FeedbackAnswer, FeedbackResponse
from app.routers.auth import get_current_user
from app.services.feedback import create_ticket_if_needed
import pytz
from datetime import datetime

router = APIRouter(tags=["responses"])
templates = Jinja2Templates(directory="app/templates")
local_tz = pytz.timezone("Asia/Kolkata")
SPECIAL_CAMPAIGN_CODES = ("code_5", "code_6")


def local_time(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S"):
    if not dt:
        return ""
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(local_tz).strftime(fmt)


templates.env.filters["local_time"] = local_time


def _apply_scope_filter(query, scope: str):
    normalized_scope = scope if scope in {"regular", "special"} else "regular"
    campaign_code = func.lower(Campaign.code)
    query = query.outerjoin(Campaign, Campaign.id == FeedbackResponse.campaign_id)
    if normalized_scope == "special":
        return query.filter(campaign_code.in_(SPECIAL_CAMPAIGN_CODES))
    return query.filter(
        (Campaign.id.is_(None)) | (Campaign.code.is_(None)) | (~campaign_code.in_(SPECIAL_CAMPAIGN_CODES))
    )


def _normalize_ascii(text: str) -> str:
    """Convert smart quotes/dashes to plain ASCII and drop other non-ASCII chars."""
    if not text:
        return ""
    repl = {
        "“": '"',
        "”": '"',
        "„": '"',
        "‟": '"',
        "’": "'",
        "‘": "'",
        "‚": "'",
        "‛": "'",
        "–": "-",
        "—": "-",
        "…": "...",
        "\u00a0": " ",
    }
    out = []
    for ch in text:
        ch = repl.get(ch, ch)
        if ord(ch) < 128:
            out.append(ch)
        else:
            out.append(" ")
    cleaned = "".join(out)
    return " ".join(cleaned.split())


@router.get("/")
async def list_responses(
    request: Request,
    scope: str = Query("regular"),
    campaign_id: str | None = Query(None),
    q: str | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=10, le=200),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    active_scope = scope if scope in {"regular", "special"} else "regular"
    query = _apply_scope_filter(db.query(FeedbackResponse), active_scope)
    campaign_id_val: int | None = None
    if campaign_id and str(campaign_id).strip().isdigit():
        campaign_id_val = int(campaign_id)
        query = query.filter(FeedbackResponse.campaign_id == campaign_id_val)
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(
            (FeedbackResponse.id.like(like))
            | (FeedbackResponse.pii_data_json["name"].as_string().like(like))
            | (FeedbackResponse.pii_data_json["mobile_number"].as_string().like(like))
            | (FeedbackResponse.pii_data_json["lab_id"].as_string().like(like))
        )
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(FeedbackResponse.submission_time >= start_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
            query = query.filter(FeedbackResponse.submission_time < end_dt)
        except ValueError:
            pass
    if status:
        query = query.filter(FeedbackResponse.status == status)
    total = query.count()
    total_pages = max(math.ceil(total / per_page), 1)
    if page > total_pages:
        page = total_pages
    responses = (
        query.options(joinedload(FeedbackResponse.campaign))
        .order_by(FeedbackResponse.submission_time.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    campaigns_query = db.query(Campaign)
    if active_scope == "special":
        campaigns_query = campaigns_query.filter(func.lower(Campaign.code).in_(SPECIAL_CAMPAIGN_CODES))
    else:
        campaigns_query = campaigns_query.filter(
            (Campaign.code.is_(None)) | (~func.lower(Campaign.code).in_(SPECIAL_CAMPAIGN_CODES))
        )
    campaigns = campaigns_query.order_by(Campaign.name).all()
    pagination_params = {
        "scope": active_scope,
        "q": q or "",
        "start_date": start_date or "",
        "end_date": end_date or "",
        "campaign_id": campaign_id or "",
        "status": status or "",
        "per_page": per_page,
    }
    pagination_query = urlencode({k: v for k, v in pagination_params.items() if v != ""})
    return templates.TemplateResponse(
        "responses/list.html",
        {
            "request": request,
            "responses": responses,
            "active_scope": active_scope,
            "campaigns": campaigns,
            "selected_campaign": campaign_id_val,
            "search": q or "",
            "start_date": start_date or "",
            "end_date": end_date or "",
            "status": status or "",
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "pagination_query": pagination_query,
            "user": user,
        },
    )


def _base_response_query(
    db: Session,
    scope: str,
    campaign_id: int | None,
    q: str | None,
    start_date: str | None,
    end_date: str | None,
    status: str | None,
):
    query = _apply_scope_filter(db.query(FeedbackResponse), scope)
    if campaign_id:
        query = query.filter(FeedbackResponse.campaign_id == campaign_id)
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(
            (FeedbackResponse.id.like(like))
            | (FeedbackResponse.pii_data_json["name"].as_string().like(like))
            | (FeedbackResponse.pii_data_json["mobile_number"].as_string().like(like))
            | (FeedbackResponse.pii_data_json["lab_id"].as_string().like(like))
        )
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(FeedbackResponse.submission_time >= start_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
            query = query.filter(FeedbackResponse.submission_time < end_dt)
        except ValueError:
            pass
    if status:
        query = query.filter(FeedbackResponse.status == status)
    return query


@router.get("/export")
@router.get("/export.csv")
async def export_responses(
    request: Request,
    scope: str = Query("regular"),
    campaign_id: str | None = Query(None),
    q: str | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    status: str | None = Query(None),
    ids: str | None = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    active_scope = scope if scope in {"regular", "special"} else "regular"
    campaign_id_val = int(campaign_id) if campaign_id and campaign_id.isdigit() else None

    if ids:
        id_list = [int(x) for x in ids.split(",") if x.strip().isdigit()]
        query = db.query(FeedbackResponse).filter(FeedbackResponse.id.in_(id_list))
    else:
        query = _base_response_query(db, active_scope, campaign_id_val, q, start_date, end_date, status)

    # Preload questions + option labels for friendly export and per-question columns
    response_ids_subq = query.with_entities(FeedbackResponse.id).subquery()
    question_ids = {
        row[0]
        for row in db.query(FeedbackAnswer.campaign_question_id)
        .filter(FeedbackAnswer.response_id.in_(response_ids_subq))
        .distinct()
        .all()
    }
    option_labels: dict[int, dict[str, str]] = {}
    ordered_questions: list[CampaignQuestion] = []
    if question_ids:
        qs = (
            db.query(CampaignQuestion)
            .filter(CampaignQuestion.id.in_(question_ids))
            .all()
        )
        qs_sorted = sorted(
            qs,
            key=lambda q: (
                q.campaign_id or 0,
                q.order_index or 0,
                q.id,
            ),
        )
        ordered_questions = qs_sorted
        for q in qs_sorted:
            opt_map: dict[str, str] = {}
            if q.options:
                for opt in q.options:
                    if opt.option_value is not None:
                        opt_map[str(opt.option_value)] = opt.option_text_en or opt.option_text_hi or str(opt.option_value)
            option_labels[q.id] = opt_map

    question_headers = []
    for q in ordered_questions:
        base = q.question_text_en or q.question_text_hi or ""
        base = base.replace("\n", " ").replace("\r", " ").strip()
        base = _normalize_ascii(base)
        prefix = f"Q{q.order_index or q.id}"
        header = f"{prefix} - {base}" if base else prefix
        question_headers.append(header)

    def csv_rows():
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        def emit(row: list[object]):
            buffer.seek(0)
            buffer.truncate(0)
            writer.writerow(row)
            return buffer.getvalue()

        # Write BOM so Excel opens UTF-8 correctly.
        yield "\ufeff"
        yield emit(
            [
                "id",
                "campaign",
                "name",
                "mobile",
                "lab_id",
                "status",
                "submitted_at",
            ]
            + question_headers
        )

        rows = (
            query.options(
                joinedload(FeedbackResponse.campaign),
                selectinload(FeedbackResponse.answers),
            )
            .order_by(FeedbackResponse.submission_time.desc())
            .yield_per(200)
        )
        for r in rows:
            pii = r.pii_data_json or {}
            mobile = pii.get("contact") or f"{pii.get('mobile_country','')}{pii.get('mobile_number','')}"
            per_q_answers: list[str] = []
            if r.answers:
                ans_map = {a.campaign_question_id: a for a in r.answers}
                for q in ordered_questions:
                    val = ""
                    a = ans_map.get(q.id)
                    if a:
                        val = a.answer_text or ""
                        if not val:
                            raw = a.selected_option_values
                            if isinstance(raw, list):
                                mapped = []
                                for x in raw:
                                    sx = str(x)
                                    mapped.append(option_labels.get(q.id, {}).get(sx, sx))
                                val = ", ".join(mapped)
                            elif raw is not None:
                                sx = str(raw)
                                val = option_labels.get(q.id, {}).get(sx, sx)
                    per_q_answers.append(_normalize_ascii(val) if val else "")
            else:
                per_q_answers = [""] * len(ordered_questions)

            yield emit(
                [
                    r.id,
                    r.campaign.name if r.campaign else "",
                    pii.get("name", ""),
                    mobile,
                    pii.get("lab_id", ""),
                    r.status,
                    local_time(r.submission_time),
                ]
                + per_q_answers
            )

    filename = f"responses_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        csv_rows(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/bookings")
async def bookings_status(
    request: Request,
    q: str | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    base_query = "WHERE 1=1"
    params: dict[str, object] = {}
    if q:
        base_query += (
            " AND (b.bookingid LIKE :q OR b.booking_code LIKE :q "
            "OR b.customername LIKE :q OR b.mobile LIKE :q)"
        )
        params["q"] = f"%{q.strip()}%"
    if start_date:
        base_query += " AND b.enterdate >= :start_date"
        params["start_date"] = start_date
    if end_date:
        base_query += " AND b.enterdate < DATE_ADD(:end_date, INTERVAL 1 DAY)"
        params["end_date"] = end_date
    count = db.execute(text(f"SELECT COUNT(*) AS total FROM bookings b {base_query}"), params).scalar() or 0
    offset = (page - 1) * per_page
    booking_rows = db.execute(
        text(
            f"""
            SELECT
                b.bookingid,
                b.booking_code,
                b.customername,
                b.mobile,
                b.age_years,
                b.preferred_time_slot,
                b.panel_company,
                b.booking_status,
                b.payment_mode,
                b.no_of_pricks,
                b.start_time,
                b.assigned_phlebotomist_id,
                b.assigned_phlebotomist_name,
                b.isCampaingsend,
                b.isResponseSubmitted
            FROM bookings b
            {base_query}
            ORDER BY b.bookingid DESC
            LIMIT :limit OFFSET :offset
            """
        ),
        {**params, "limit": per_page, "offset": offset},
    ).mappings().all()
    rows = [dict(row) for row in booking_rows]
    lab_ids = [str(row["bookingid"]) for row in rows if row.get("bookingid") is not None]
    response_ids_by_lab: dict[str, int] = {}
    if lab_ids:
        lab_params = {f"lab_id_{idx}": lab_id for idx, lab_id in enumerate(lab_ids)}
        placeholders = ", ".join(f":{key}" for key in lab_params)
        response_rows = db.execute(
            text(
                f"""
                SELECT
                    MAX(id) AS id,
                    JSON_UNQUOTE(JSON_EXTRACT(pii_data_json, '$.lab_id')) AS lab_id
                FROM feedback_responses
                WHERE JSON_UNQUOTE(JSON_EXTRACT(pii_data_json, '$.lab_id')) IN ({placeholders})
                GROUP BY lab_id
                """
            ),
            lab_params,
        ).mappings().all()
        response_ids_by_lab = {str(row["lab_id"]): row["id"] for row in response_rows if row["lab_id"] is not None}
    for row in rows:
        row["response_id"] = response_ids_by_lab.get(str(row["bookingid"]))

    totals = db.execute(
        text(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN isCampaingsend = 1 THEN 1 ELSE 0 END) AS sent_count,
                SUM(CASE WHEN isResponseSubmitted = 1 THEN 1 ELSE 0 END) AS responded_count
            FROM bookings
            """
        )
    ).mappings().first()
    return templates.TemplateResponse(
        "responses/bookings.html",
        {
            "request": request,
            "bookings": rows,
            "totals": totals or {},
            "search": q or "",
            "page": page,
            "per_page": per_page,
            "total": count,
            "start_date": start_date or "",
            "end_date": end_date or "",
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
    response = (
        db.query(FeedbackResponse)
        .options(
            joinedload(FeedbackResponse.campaign),
            selectinload(FeedbackResponse.answers)
            .joinedload(FeedbackAnswer.question)
            .selectinload(CampaignQuestion.options),
        )
        .filter(FeedbackResponse.id == response_id)
        .first()
    )
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")

    booking = None
    pii = response.pii_data_json or {}
    lab_id = str(pii.get("lab_id") or "").strip()
    if lab_id.isdigit():
        booking_row = db.execute(
            text(
                """
                SELECT
                    bookingid,
                    booking_code,
                    start_time,
                    age_years,
                    preferred_time_slot,
                    panel_company,
                    booking_status,
                    payment_mode,
                    no_of_pricks,
                    assigned_phlebotomist_id,
                    assigned_phlebotomist_name
                FROM bookings
                WHERE bookingid = :bookingid
                LIMIT 1
                """
            ),
            {"bookingid": int(lab_id)},
        ).mappings().first()
        booking = dict(booking_row) if booking_row else None

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
            label_str = str(label).strip()
            if not label_str or label_str == "[]":
                continue
            if label_str not in seen:
                labels.append(label_str)
                seen.add(label_str)
        if labels:
            answer_labels[answer.id] = labels
    return templates.TemplateResponse(
        "responses/detail.html",
        {
            "request": request,
            "response": response,
            "booking": booking,
            "answer_labels": answer_labels,
            "user": user,
        },
    )


@router.post("/{response_id}/status")
async def update_response_status(
    response_id: int,
    request: Request,
    action: str = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    response = db.query(FeedbackResponse).get(response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    if action == "close":
        response.status = "closed"
        response.needs_manual_review = False
        response.has_updates = True
        db.commit()
    elif action == "create_ticket":
        response.is_complaint = True
        response.status = "ticket_created"
        response.has_updates = True
        db.commit()
        create_ticket_if_needed(db, response)
    return RedirectResponse(url=f"/responses/{response_id}", status_code=302)
