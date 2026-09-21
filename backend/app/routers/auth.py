import hmac
import re
import secrets
from functools import lru_cache
from typing import Optional
from urllib.parse import quote_plus

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import User, UserRole
from app.utils import hash_password, verify_password

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@lru_cache(maxsize=1)
def _external_user_engine():
    settings = get_settings()
    if not all([settings.mysql_host, settings.mysql_user, settings.mysql_db]):
        raise RuntimeError("External user database is not configured")
    password = quote_plus(settings.mysql_password or "")
    url = (
        f"mysql+pymysql://{settings.mysql_user}:{password}"
        f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_db}"
    )
    return create_engine(url, pool_pre_ping=True, pool_recycle=1800)


def _dob_password(dob: object) -> str:
    return re.sub(r"\D", "", str(dob or ""))


def _app_role_from_designation(designation: object) -> str:
    if str(designation or "").strip().casefold() == "admin":
        return UserRole.admin.value
    return UserRole.l1.value


@router.get("/external-users")
async def external_users(q: str = ""):
    search = q.strip()
    if len(search) < 2:
        return JSONResponse([])
    try:
        with _external_user_engine().connect() as conn:
            rows = conn.execute(
                text(
                    """
                    SELECT id, name, designation
                    FROM users
                    WHERE status = 'Active'
                      AND name LIKE :search
                    ORDER BY name
                    LIMIT 10
                    """
                ),
                {"search": f"%{search}%"},
            ).mappings().all()
    except Exception:
        return JSONResponse([], status_code=503)
    return JSONResponse(
        [
            {
                "id": row["id"],
                "name": row["name"],
                "designation": row["designation"] or "",
            }
            for row in rows
        ]
    )


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "error": None})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    external_user_id: str = Form(""),
    db: Session = Depends(get_db),
):
    external_user = None
    try:
        with _external_user_engine().connect() as conn:
            if external_user_id.isdigit():
                external_user = conn.execute(
                    text(
                        """
                        SELECT id, name, contact, departments, designation, dob
                        FROM users
                        WHERE id = :user_id AND status = 'Active'
                        LIMIT 1
                        """
                    ),
                    {"user_id": int(external_user_id)},
                ).mappings().first()
                if external_user and external_user["name"].strip().casefold() != username.strip().casefold():
                    external_user = None
            else:
                candidates = conn.execute(
                    text(
                        """
                        SELECT id, name, contact, departments, designation, dob
                        FROM users
                        WHERE status = 'Active' AND LOWER(name) = LOWER(:name)
                        LIMIT 10
                        """
                    ),
                    {"name": username.strip()},
                ).mappings().all()
                external_user = next(
                    (
                        candidate
                        for candidate in candidates
                        if hmac.compare_digest(_dob_password(candidate["dob"]), password.strip())
                    ),
                    None,
                )
    except Exception:
        external_user = None

    if external_user and hmac.compare_digest(
        _dob_password(external_user["dob"]), password.strip()
    ):
        local_username = f"external:{external_user['id']}"
        app_role = _app_role_from_designation(external_user["designation"])
        user = db.query(User).filter(User.username == local_username).first()
        if not user:
            user = User(
                username=local_username,
                name=external_user["name"],
                mobile=external_user["contact"],
                department=external_user["departments"],
                role=app_role,
                password_hash=hash_password(secrets.token_urlsafe(32)),
            )
            db.add(user)
        else:
            user.name = external_user["name"]
            user.mobile = external_user["contact"]
            user.department = external_user["departments"]
            user.role = app_role
        db.commit()
        db.refresh(user)
        request.session["user"] = {"id": user.id, "name": user.name, "role": user.role}
        return RedirectResponse(url="/dashboard", status_code=302)

    # Preserve local admin access for maintenance and external DB outages.
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "auth/login.html", {"request": request, "error": "Invalid credentials"}
        )
    request.session["user"] = {"id": user.id, "name": user.name, "role": user.role}
    return RedirectResponse(url="/dashboard", status_code=302)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/auth/login", status_code=302)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_data = request.session.get("user")
    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = db.query(User).get(user_data["id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(role: Optional[str] = None):
    def _role_dependency(user: User = Depends(get_current_user)):
        if role and user.role != role and user.role != UserRole.admin.value:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return _role_dependency
