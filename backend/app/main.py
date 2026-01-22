from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates

from app import models
from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, campaigns, dashboard, feedback_public, master_questions, questionnaire, responses, tickets
# from app.services.booking_notifier import BookingNotifier
from app.services.booking_sync import BookingSync
from app.services.booking_campaign_sender import BookingCampaignSender
import pytz
from datetime import datetime

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
# notifier: BookingNotifier | None = None
booking_sync: BookingSync | None = None
campaign_sender: BookingCampaignSender | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
local_tz = pytz.timezone("Asia/Kolkata")


def local_time(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S"):
    if not dt:
        return ""
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(local_tz).strftime(fmt)


templates.env.filters["local_time"] = local_time


@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)
    return RedirectResponse(url="/dashboard", status_code=302)


app.include_router(auth.router, prefix="/auth")
app.include_router(campaigns.router, prefix="/campaigns")
app.include_router(questionnaire.router, prefix="/questionnaire")
app.include_router(feedback_public.router, prefix="/feedback")
app.include_router(responses.router, prefix="/responses")
app.include_router(tickets.router, prefix="/tickets")
app.include_router(dashboard.router, prefix="")
app.include_router(master_questions.router, prefix="/master_questions")

@app.on_event("startup")
async def _start_notifier():
    # BookingNotifier disabled for now.
    print("[BookingSync] startup hook entered")
    global booking_sync
    try:
        booking_sync = BookingSync(base_db_url=settings.database_url)
        booking_sync.start()
        print("[BookingSync] registered from startup")
    except Exception as exc:
        booking_sync = None
        print(f"[BookingSync] failed to start: {exc}")
    print("[BookingCampaignSender] startup hook entered")
    global campaign_sender
    try:
        campaign_sender = BookingCampaignSender(base_db_url=settings.database_url)
        campaign_sender.start()
        print("[BookingCampaignSender] registered from startup")
    except Exception as exc:
        campaign_sender = None
        print(f"[BookingCampaignSender] failed to start: {exc}")


@app.on_event("shutdown")
async def _stop_notifier():
    # BookingNotifier disabled for now.
    print("[BookingSync] shutdown hook entered")
    global booking_sync
    if booking_sync:
        try:
            booking_sync.stop()
        finally:
            booking_sync = None
    print("[BookingCampaignSender] shutdown hook entered")
    global campaign_sender
    if campaign_sender:
        try:
            campaign_sender.stop()
        finally:
            campaign_sender = None
