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
from app.services.booking_notifier import BookingNotifier
import pytz
from datetime import datetime

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
notifier: BookingNotifier | None = None

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
    print("[BookingNotifier] startup hook entered")
    global notifier
    try:
        notifier = BookingNotifier(
            base_db_url=settings.database_url,
            campaign_link="https://labmate.bhasinpathlabs.com:4667/feedback/CODE_2",
            whatsapp_api=campaigns.WHATSAPP_SEND_API,
            account_id=campaigns.WHATSAPP_ACCOUNT_ID,
        )
        notifier.start()
        print("[BookingNotifier] registered from startup")
    except Exception as exc:
        notifier = None
        print(f"[BookingNotifier] failed to start: {exc}")


@app.on_event("shutdown")
async def _stop_notifier():
    print("[BookingNotifier] shutdown hook entered")
    global notifier
    if notifier:
        try:
            notifier.stop()
        finally:
            notifier = None
