from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import MasterQuestion, MasterQuestionOption, CampaignQuestion
from app.routers.auth import require_role

router = APIRouter(tags=["master_questions"])
templates = Jinja2Templates(directory="app/templates")


def wants_json(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "application/json" in accept.lower()


@router.get("/")
async def list_master_questions(request: Request, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    masters = db.query(MasterQuestion).order_by(MasterQuestion.code).all()
    return templates.TemplateResponse(
        "master_questions/list.html",
        {"request": request, "user": user, "masters": masters},
    )


@router.post("/new")
async def create_master_question(
    request: Request,
    code: str = Form(...),
    question_text_en: str = Form(...),
    question_type: str = Form(...),
    placeholder_en: str = Form(""),
    option_text_en: List[str] = Form([]),
    sentiment: List[str] = Form([]),
    score_value: List[str] = Form([]),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    existing = db.query(MasterQuestion).filter(MasterQuestion.code == code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Code already exists")
    needs_options = question_type in ["mcq_single", "mcq_multi", "rating_1_5"]
    has_options = any(text.strip() for text in option_text_en)
    if needs_options and not has_options:
        raise HTTPException(status_code=400, detail="At least one option is required for this question type")
    master = MasterQuestion(
        code=code,
        default_text_en=question_text_en,
        question_type=question_type,
        placeholder_en=placeholder_en.strip() if question_type == "text" and placeholder_en else None,
        is_active=True,
    )
    db.add(master)
    db.flush()
    # Create options if provided
    created_options = []
    if question_type in ["mcq_single", "mcq_multi", "rating_1_5"]:
        for idx, text in enumerate(option_text_en):
            if not text or not text.strip():
                continue
            val = str(idx + 1)
            sent = sentiment[idx] if idx < len(sentiment) and sentiment[idx] else "neutral"
            try:
                score = int(score_value[idx]) if idx < len(score_value) and score_value[idx] not in (None, "") else 0
            except (ValueError, TypeError):
                score = 0
            opt = MasterQuestionOption(
                master_question_id=master.id,
                option_text_en=text.strip(),
                option_value=val.strip(),
                sentiment=sent,
                score_value=score,
            )
            db.add(opt)
            db.flush()
            created_options.append(
                {
                    "id": opt.id,
                    "option_text_en": opt.option_text_en,
                    "option_value": opt.option_value,
                    "sentiment": opt.sentiment,
                    "score_value": opt.score_value,
                }
            )
    db.commit()
    if wants_json(request):
        return JSONResponse(
            {
                "status": "ok",
                "master": {
                    "id": master.id,
                    "code": master.code,
                    "question_text_en": master.default_text_en,
                    "question_type": master.question_type,
                    "placeholder_en": master.placeholder_en,
                    "is_active": master.is_active,
                },
                "options": created_options,
            }
        )
    return RedirectResponse(url="/master_questions/", status_code=302)


@router.post("/{master_id}/update")
async def update_master_question(
    request: Request,
    master_id: int,
    question_text_en: str = Form(...),
    question_type: str = Form(...),
    placeholder_en: str = Form(""),
    is_active: bool = Form(False),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    master = db.query(MasterQuestion).get(master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master question not found")
    master.default_text_en = question_text_en
    master.question_type = question_type
    master.placeholder_en = placeholder_en.strip() if question_type == "text" and placeholder_en else None
    master.is_active = is_active
    db.commit()
    if wants_json(request):
        return JSONResponse(
            {
                "status": "ok",
                "master": {
                    "id": master.id,
                    "question_text_en": master.default_text_en,
                    "question_type": master.question_type,
                    "placeholder_en": master.placeholder_en,
                    "is_active": master.is_active,
                },
            }
        )
    return RedirectResponse(url="/master_questions/", status_code=302)


@router.post("/{master_id}/delete")
async def delete_master_question(
    master_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    master = db.query(MasterQuestion).get(master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master question not found")
    # Prevent deletion if linked to campaign questions
    linked_count = db.query(CampaignQuestion).filter(CampaignQuestion.master_question_id == master_id).count()
    if linked_count:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete: this master question is linked to campaign questions. Unlink or delete those first.",
        )
    # Remove options first to avoid FK issues
    db.query(MasterQuestionOption).filter(MasterQuestionOption.master_question_id == master_id).delete()
    db.delete(master)
    db.commit()
    return RedirectResponse(url="/master_questions/", status_code=302)


@router.post("/{master_id}/options/add")
async def add_master_option(
    request: Request,
    master_id: int,
    option_text_en: List[str] = Form([]),
    sentiment: List[str] = Form([]),
    score_value: List[str] = Form([]),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    master = db.query(MasterQuestion).get(master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master question not found")
    existing_count = (
        db.query(MasterQuestionOption)
        .filter(MasterQuestionOption.master_question_id == master_id)
        .count()
    )
    created = []
    for idx, text in enumerate(option_text_en):
        if not text or not text.strip():
            continue
        val = str(existing_count + idx + 1)
        sent = sentiment[idx] if idx < len(sentiment) and sentiment[idx] else "neutral"
        try:
            score = int(score_value[idx]) if idx < len(score_value) and score_value[idx] not in (None, "") else 0
        except (ValueError, TypeError):
            score = 0
        opt = MasterQuestionOption(
            master_question_id=master_id,
            option_text_en=text.strip(),
            option_value=val.strip(),
            sentiment=sent,
            score_value=score,
        )
        db.add(opt)
        db.flush()
        created.append(
            {
                "id": opt.id,
                "option_text_en": opt.option_text_en,
                "option_value": opt.option_value,
                "sentiment": opt.sentiment,
                "score_value": opt.score_value,
            }
        )
    db.commit()
    if wants_json(request):
        return JSONResponse({"status": "ok", "created": created})
    return RedirectResponse(url="/master_questions/", status_code=302)


@router.post("/{master_id}/options/{option_id}/update")
async def update_master_option(
    request: Request,
    master_id: int,
    option_id: int,
    option_text_en: str = Form(...),
    sentiment: str = Form("neutral"),
    score_value: str = Form("0"),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    opt = db.query(MasterQuestionOption).get(option_id)
    if not opt or opt.master_question_id != master_id:
        raise HTTPException(status_code=404, detail="Option not found")
    opt.option_text_en = option_text_en
    opt.sentiment = sentiment
    try:
        opt.score_value = int(score_value) if score_value not in (None, "") else 0
    except (ValueError, TypeError):
        opt.score_value = 0
    db.commit()
    if wants_json(request):
        return JSONResponse(
            {
                "status": "ok",
                "option": {
                    "id": opt.id,
                    "option_text_en": opt.option_text_en,
                    "option_value": opt.option_value,
                    "sentiment": opt.sentiment,
                    "score_value": opt.score_value,
                },
            }
        )
    return RedirectResponse(url="/master_questions/", status_code=302)


@router.post("/{master_id}/options/{option_id}/delete")
async def delete_master_option(
    request: Request,
    master_id: int,
    option_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    opt = db.query(MasterQuestionOption).get(option_id)
    if not opt or opt.master_question_id != master_id:
        raise HTTPException(status_code=404, detail="Option not found")
    db.delete(opt)
    db.commit()
    if wants_json(request):
        return JSONResponse({"status": "ok", "deleted": option_id})
    return RedirectResponse(url="/master_questions/", status_code=302)
