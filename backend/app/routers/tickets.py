from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FeedbackTicket, TicketUpdate
from app.routers.auth import get_current_user, require_role
import pytz
from datetime import datetime

router = APIRouter(tags=["tickets"])
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
async def list_tickets(
    request: Request,
    q: str | None = None,
    status: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    tickets = db.query(FeedbackTicket)
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
    tickets = tickets.order_by(FeedbackTicket.created_at.desc()).all()
    return templates.TemplateResponse(
        "tickets/list.html",
        {
            "request": request,
            "tickets": tickets,
            "user": user,
            "search": q or "",
            "status": status or "",
            "start_date": start_date or "",
            "end_date": end_date or "",
        },
    )


@router.get("/{ticket_id}")
async def view_ticket(ticket_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ticket = db.query(FeedbackTicket).get(ticket_id)
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
    if closure_mood:
        ticket.closure_mood = closure_mood
    update = TicketUpdate(ticket_id=ticket_id, update_text=update_text, updated_by_user_id=user.id)
    db.add(update)
    db.commit()
    return RedirectResponse(url=f"/tickets/{ticket_id}", status_code=302)
