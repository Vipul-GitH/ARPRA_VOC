import math
import re
from datetime import datetime, timedelta
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import pymysql
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload

from app.config import get_settings
from app.database import get_db
from app.models import Campaign, FeedbackTicket, TicketUpdate
from app.routers.auth import get_current_user, require_role
import pytz
from datetime import datetime

router = APIRouter(tags=["tickets"])
templates = Jinja2Templates(directory="app/templates")
local_tz = pytz.timezone("Asia/Kolkata")
SPECIAL_CAMPAIGN_CODES = ("code_5", "code_6")


class OdtTicketCreateRequest(BaseModel):
    username: str = "api_user"
    ticket_origin: str = "ODT"
    source: str = "patient"
    country_code: str = "+91"
    mobile_number: str | None = None
    patient_name: str | None = None
    patient_labmate_id: str | None = ""
    panel_name: str | None = ""
    client_name: str | None = ""
    whatsapp_opt_in: str | None = "1"
    ticket_category: str | None = "Report courier"
    commitment_predefined: str | None = ""
    tags_json: str | None = "[]"
    additional_info: str | None = ""


def _commitment_minutes(value: str | None) -> int:
    if not value:
        return 30
    match = re.search(r"\d+", value)
    if not match:
        return 30
    minutes = int(match.group())
    if "hour" in value.lower() or "hr" in value.lower():
        minutes *= 60
    return max(minutes, 1)


def _nullable(value: str | None):
    value = (value or "").strip()
    return value or None


def _value_or_na(value: str | None) -> str:
    value = (value or "").strip()
    return value or "N/A"


def _odt_db_connect():
    settings = get_settings()
    return pymysql.connect(
        host=settings.odt_mysql_host,
        port=settings.odt_mysql_port,
        user=settings.odt_mysql_user,
        password=settings.odt_mysql_password,
        database=settings.odt_mysql_db,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        connect_timeout=5,
    )


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
    query = query.outerjoin(Campaign, Campaign.id == FeedbackTicket.campaign_id)
    if normalized_scope == "special":
        return query.filter(campaign_code.in_(SPECIAL_CAMPAIGN_CODES))
    return query.filter(
        (Campaign.id.is_(None)) | (Campaign.code.is_(None)) | (~campaign_code.in_(SPECIAL_CAMPAIGN_CODES))
    )


@router.post("/create")
async def create_odt_ticket(payload: OdtTicketCreateRequest):
    if payload.username != "api_user":
        raise HTTPException(status_code=401, detail="Invalid API user")

    settings = get_settings()
    if not re.fullmatch(r"[A-Za-z0-9_]+", settings.odt_tickets_table):
        raise HTTPException(status_code=500, detail="Invalid ODT tickets table name")

    commitment_minutes = _commitment_minutes(payload.commitment_predefined)
    sql = f"""
        INSERT INTO `{settings.odt_tickets_table}` (
          source,
          country_code,
          mobile_number,
          patient_name,
          patient_labmate_id,
          client_name,
          panel_name,
          whatsapp_opt_in,
          ticket_category,
          commitment_at,
          tags_json,
          additional_info,
          status,
          created_by,
          designation,
          ticket_origin
        ) VALUES (
          %s, %s, %s, %s, %s, %s, %s, %s, %s,
          DATE_ADD(NOW(), INTERVAL %s MINUTE),
          %s, %s, %s, %s, %s, %s
        )
    """
    values = (
        payload.source,
        payload.country_code,
        _value_or_na(payload.mobile_number),
        _value_or_na(payload.patient_name),
        payload.patient_labmate_id or "",
        _nullable(payload.client_name),
        _nullable(payload.panel_name),
        1 if str(payload.whatsapp_opt_in or "1").strip() in {"1", "true", "yes", "Y"} else 0,
        payload.ticket_category or "Report courier",
        commitment_minutes,
        payload.tags_json or "[]",
        _value_or_na(payload.additional_info),
        "Open",
        "API_USER",
        "ODT",
        payload.ticket_origin or "ODT",
    )

    try:
        conn = _odt_db_connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                ticket_id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=502, detail=f"ODT DB insert failed: {exc}") from exc

    return {"ok": True, "ticket_id": ticket_id, "status": "Open"}


@router.get("/")
async def list_tickets(
    request: Request,
    scope: str = Query("regular"),
    q: str | None = None,
    status: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=10, le=200),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    active_scope = scope if scope in {"regular", "special"} else "regular"
    tickets = _apply_scope_filter(db.query(FeedbackTicket), active_scope)
    if status:
        tickets = tickets.filter(FeedbackTicket.status == status)
    if q:
        like = f"%{q.strip()}%"
        tickets = tickets.filter(
            (FeedbackTicket.ticket_number.like(like))
            | (FeedbackTicket.summary.like(like))
            | (FeedbackTicket.details.like(like))
        )
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            tickets = tickets.filter(FeedbackTicket.created_at >= start_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
            tickets = tickets.filter(FeedbackTicket.created_at < end_dt)
        except ValueError:
            pass
    total = tickets.count()
    total_pages = max(math.ceil(total / per_page), 1)
    if page > total_pages:
        page = total_pages
    tickets = (
        tickets.options(joinedload(FeedbackTicket.campaign))
        .order_by(FeedbackTicket.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    pagination_params = {
        "scope": active_scope,
        "q": q or "",
        "status": status or "",
        "start_date": start_date or "",
        "end_date": end_date or "",
        "per_page": per_page,
    }
    pagination_query = urlencode({k: v for k, v in pagination_params.items() if v != ""})
    return templates.TemplateResponse(
        "tickets/list.html",
        {
            "request": request,
            "tickets": tickets,
            "active_scope": active_scope,
            "user": user,
            "search": q or "",
            "status": status or "",
            "start_date": start_date or "",
            "end_date": end_date or "",
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "pagination_query": pagination_query,
        },
    )


@router.get("/{ticket_id}")
async def view_ticket(ticket_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ticket = (
        db.query(FeedbackTicket)
        .options(
            joinedload(FeedbackTicket.response),
            joinedload(FeedbackTicket.campaign),
            selectinload(FeedbackTicket.updates).joinedload(TicketUpdate.updated_by_user),
        )
        .filter(FeedbackTicket.id == ticket_id)
        .first()
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return templates.TemplateResponse(
        "tickets/detail.html", {"request": request, "ticket": ticket, "user": user}
    )


@router.post("/{ticket_id}/update")
async def add_update(
    ticket_id: int,
    request: Request,
    update_text: str = Form(...),
    status: str = Form("open"),
    closure_mood: str | None = Form(None),
    db: Session = Depends(get_db),
    user=Depends(require_role("l2")),
):
    ticket = db.query(FeedbackTicket).get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.status == "closed":
        return RedirectResponse(url=f"/tickets/{ticket_id}", status_code=302)
    ticket.status = status
    if status == "closed":
        ticket.closed_at = datetime.utcnow()
    if closure_mood:
        ticket.closure_mood = closure_mood
    if ticket.response and ticket.response.status in {"manual_review", "ticket_created"}:
        ticket.response.has_updates = True
    update = TicketUpdate(ticket_id=ticket_id, update_text=update_text, updated_by_user_id=user.id)
    db.add(update)
    db.commit()
    return RedirectResponse(url=f"/tickets/{ticket_id}", status_code=302)
