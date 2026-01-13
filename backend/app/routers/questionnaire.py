from typing import Dict, List
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Campaign,
    CampaignQuestion,
    CampaignQuestionOption,
    FeedbackAnswer,
    MasterQuestion,
    MasterQuestionOption,
    QuestionFlowRule,
)
from app.routers.auth import get_current_user, require_role

router = APIRouter(tags=["questionnaire"])
templates = Jinja2Templates(directory="app/templates")

EXP_LAB_CODE = "Exp_Lab"
EXP_LAB_TEXT = "Overall, how would you rate your experience with Dr Bhasin’s Lab?"
EXP_LAB_OPTIONS = [
    ("5", "Excellent – Felt truly cared for"),
    ("4", "Good – Everything went smoothly"),
    ("3", "Average – It was okay"),
    ("2", "Poor – Needs improvement"),
    ("1", "Very Poor – Unacceptable experience"),
]


def ensure_exp_lab_master_question(db: Session) -> MasterQuestion:
    """Ensure the master question exists globally with options."""
    master = db.query(MasterQuestion).filter(MasterQuestion.code == EXP_LAB_CODE).first()
    if not master:
        master = MasterQuestion(
            code=EXP_LAB_CODE,
            default_text_en=EXP_LAB_TEXT,
            question_type="rating_1_5",
            is_active=True,
        )
        db.add(master)
        db.flush()
    existing_opts = {opt.option_value: opt for opt in master.options}
    for value, text in EXP_LAB_OPTIONS:
        if value not in existing_opts:
            db.add(
                MasterQuestionOption(
                    master_question_id=master.id,
                    option_value=value,
                    option_text_en=text,
                    score_value=int(value),
                    sentiment="positive" if value in {"4", "5"} else "negative" if value in {"1", "2"} else "neutral",
                )
            )
    return master


def ensure_campaign_has_exp_lab_question(db: Session, campaign: Campaign) -> CampaignQuestion:
    """Return the campaign's Exp_Lab question if present; do not auto-create."""
    master = ensure_exp_lab_master_question(db)
    campaign_master = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign.id, CampaignQuestion.master_question_id == master.id)
        .first()
    )
    if campaign_master:
        campaign_master.is_overall_rating = True
        # Keep admin edits to the master question; only fill defaults when missing.
        if not campaign_master.question_text_en:
            campaign_master.question_text_en = master.default_text_en
        if not campaign_master.question_type:
            campaign_master.question_type = master.question_type
    return campaign_master


def reindex_campaign_questions(db: Session, campaign_id: int):
    questions = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .order_by(CampaignQuestion.order_index, CampaignQuestion.id)
        .all()
    )
    masters = [q for q in questions if q.master_question_id]
    others = [q for q in questions if not q.master_question_id]
    ordered = masters + others if masters else questions
    idx = 1
    for q in ordered:
        q.order_index = idx
        idx += 1
    db.flush()


def reindex_question_options(db: Session, question_id: int):
    options = (
        db.query(CampaignQuestionOption)
        .filter(CampaignQuestionOption.campaign_question_id == question_id)
        .order_by(CampaignQuestionOption.order_index, CampaignQuestionOption.id)
        .all()
    )
    idx = 1
    for opt in options:
        opt.order_index = idx
        idx += 1
    db.flush()


def clone_master_to_campaign_question(db: Session, master: MasterQuestion, campaign_id: int, is_required: bool = False, order_index: int = 0) -> CampaignQuestion:
    question = CampaignQuestion(
        campaign_id=campaign_id,
        master_question_id=master.id,
        question_text_en=master.default_text_en,
        question_type=master.question_type,
        placeholder_en=master.placeholder_en if master.question_type == "text" else None,
        is_required=is_required,
        order_index=order_index,
        is_master=True,
    )
    db.add(question)
    db.flush()
    db.query(CampaignQuestionOption).filter(CampaignQuestionOption.campaign_question_id == question.id).delete()
    for idx, opt in enumerate(master.options, start=1):
        db.add(
            CampaignQuestionOption(
                campaign_question_id=question.id,
                option_value=opt.option_value,
                option_text_en=opt.option_text_en,
                sentiment=opt.sentiment,
                score_value=opt.score_value,
                order_index=idx,
            )
        )
    return question


@router.get("/{campaign_id}")
async def view_questionnaire(
    campaign_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    questions = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .order_by(CampaignQuestion.order_index)
        .all()
    )
    exp_master = ensure_exp_lab_master_question(db)
    campaign_master_question = ensure_campaign_has_exp_lab_question(db, campaign)
    first_question = questions[0] if questions else None
    flow_rules = []
    flow_map = campaign.exp_flow_map or {}
    master_questions = db.query(MasterQuestion).filter(MasterQuestion.is_active.is_(True)).order_by(MasterQuestion.code).all()
    db.commit()
    return templates.TemplateResponse(
        "campaigns/edit.html",
        {
            "request": request,
            "campaign": campaign,
            "questions": questions,
            "action": f"/campaigns/{campaign_id}/edit",
            "user": user,
            "channels": [],
            "flow_rules": flow_rules,
            "flow_map": flow_map,
            "exp_lab_master": exp_master,
            "campaign_master_question": campaign_master_question,
            "master_questions": master_questions,
            "first_question": first_question,
        },
    )


@router.post("/{campaign_id}/add_question")
async def add_question(
    campaign_id: int,
    request: Request,
    question_text_en: str = Form(...),
    question_type: str = Form(...),
    placeholder_en: str = Form(""),
    is_required: bool = Form(False),
    option_text_en: List[str] = Form([]),
    option_value: List[str] = Form([]),
    sentiment: List[str] = Form([]),
    score_value: List[str] = Form([]),
    follow_up_label: List[str] = Form([]),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    order_index = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .count()
    )
    needs_options = question_type in ["mcq_single", "mcq_multi", "rating_1_5"]
    has_options = any(text.strip() for text in option_text_en)
    if needs_options and not has_options:
        raise HTTPException(status_code=400, detail="At least one option is required for this question type")

    question = CampaignQuestion(
        campaign_id=campaign_id,
        question_text_en=question_text_en,
        question_type=question_type,
        placeholder_en=placeholder_en.strip() if question_type == "text" and placeholder_en else None,
        is_required=is_required,
        order_index=order_index + 1,
    )
    db.add(question)
    db.flush()

    if question_type in ["mcq_single", "mcq_multi", "rating_1_5"]:
        for idx, text in enumerate(option_text_en):
            if not text or not text.strip():
                continue
            val = option_value[idx] if idx < len(option_value) and option_value[idx].strip() else str(idx + 1)
            sent = sentiment[idx] if idx < len(sentiment) and sentiment[idx] else "neutral"
            try:
                score = int(score_value[idx]) if idx < len(score_value) and score_value[idx] not in (None, "") else 0
            except (ValueError, TypeError):
                score = 0
            fu = follow_up_label[idx].strip() if idx < len(follow_up_label) and follow_up_label[idx] else None
            db.add(
                CampaignQuestionOption(
                    campaign_question_id=question.id,
                    option_text_en=text.strip(),
                    option_value=val.strip(),
                    sentiment=sent,
                    score_value=score,
                    order_index=idx + 1,
                    follow_up_label=fu,
                )
            )

    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/add_master_question")
async def add_master_question(
    campaign_id: int,
    master_question_id: int = Form(...),
    is_required: bool = Form(False),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    master = db.query(MasterQuestion).get(master_question_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master question not found")
    order_index = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .count()
    ) + 1
    clone_master_to_campaign_question(db, master, campaign_id, is_required=is_required, order_index=order_index)
    reindex_campaign_questions(db, campaign_id)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/questions/{question_id}/add_option")
async def add_option(
    campaign_id: int,
    question_id: int,
    option_text_en: str = Form(...),
    option_value: str = Form(...),
    sentiment: str = Form("neutral"),
    score_value: str = Form("0"),
    follow_up_label: str = Form(""),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    question = db.query(CampaignQuestion).get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    current_count = (
        db.query(CampaignQuestionOption)
        .filter(CampaignQuestionOption.campaign_question_id == question_id)
        .count()
    )
    try:
        score_val = int(score_value) if score_value not in (None, "") else 0
    except (ValueError, TypeError):
        score_val = 0

    option = CampaignQuestionOption(
        campaign_question_id=question_id,
        option_text_en=option_text_en,
        option_value=option_value,
        sentiment=sentiment,
        score_value=score_val,
        order_index=current_count + 1,
        follow_up_label=follow_up_label or None,
    )
    db.add(option)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/questions/{question_id}/update")
async def update_question(
    campaign_id: int,
    question_id: int,
    question_text_en: str = Form(...),
    question_type: str = Form(...),
    placeholder_en: str = Form(""),
    is_required: bool = Form(False),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    question = db.query(CampaignQuestion).get(question_id)
    if not question or question.campaign_id != campaign_id:
        raise HTTPException(status_code=404, detail="Question not found")
    question.question_text_en = question_text_en
    question.question_type = question_type
    question.placeholder_en = placeholder_en.strip() if question_type == "text" and placeholder_en else None
    question.is_required = is_required
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/questions/{question_id}/move")
async def move_question(
    campaign_id: int,
    question_id: int,
    direction: str = Form(...),  # "up" or "down"
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    question = db.query(CampaignQuestion).get(question_id)
    if not question or question.campaign_id != campaign_id:
        raise HTTPException(status_code=404, detail="Question not found")

    questions = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .order_by(CampaignQuestion.order_index, CampaignQuestion.id)
        .all()
    )
    idx_map = {q.id: i for i, q in enumerate(questions)}
    if question_id not in idx_map:
        raise HTTPException(status_code=404, detail="Question not found in campaign")
    i = idx_map[question_id]
    if direction == "up" and i > 1:
        # prevent moving ahead of the first question (Exp_Lab)
        if i == 1:
            pass
        else:
            questions[i].order_index, questions[i - 1].order_index = questions[i - 1].order_index, questions[i].order_index
    elif direction == "down" and i < len(questions) - 1:
        questions[i].order_index, questions[i + 1].order_index = questions[i + 1].order_index, questions[i].order_index
    db.flush()
    reindex_campaign_questions(db, campaign_id)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/questions/{question_id}/copy")
async def copy_question(
    campaign_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    src = db.query(CampaignQuestion).get(question_id)
    if not src or src.campaign_id != campaign_id:
        raise HTTPException(status_code=404, detail="Question not found")
    order_index = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .count()
    ) + 1
    new_q = CampaignQuestion(
        campaign_id=campaign_id,
        master_question_id=src.master_question_id,
        question_text_en=src.question_text_en,
        question_type=src.question_type,
        placeholder_en=src.placeholder_en if src.question_type == "text" else None,
        is_required=src.is_required,
        order_index=order_index,
        is_master=src.is_master,
        is_overall_rating=False,
    )
    db.add(new_q)
    db.flush()
    opts = (
        db.query(CampaignQuestionOption)
        .filter(CampaignQuestionOption.campaign_question_id == question_id)
        .order_by(CampaignQuestionOption.order_index, CampaignQuestionOption.id)
        .all()
    )
    for idx, opt in enumerate(opts, start=1):
        db.add(
            CampaignQuestionOption(
                campaign_question_id=new_q.id,
                option_value=opt.option_value,
                option_text_en=opt.option_text_en,
                option_text_hi=opt.option_text_hi,
                sentiment=opt.sentiment,
                department=opt.department,
                area=opt.area,
                score_value=opt.score_value,
                order_index=idx,
            )
        )
    reindex_campaign_questions(db, campaign_id)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/questions/{question_id}/sync_master")
async def sync_question_from_master(
    campaign_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    question = db.query(CampaignQuestion).get(question_id)
    if not question or question.campaign_id != campaign_id or not question.master_question_id:
        raise HTTPException(status_code=404, detail="Linked master not found for this question")
    master = db.query(MasterQuestion).get(question.master_question_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master question not found")

    question.question_text_en = master.default_text_en
    question.question_type = master.question_type
    question.placeholder_en = master.placeholder_en if master.question_type == "text" else None
    # Keep required flag as is
    db.query(CampaignQuestionOption).filter(CampaignQuestionOption.campaign_question_id == question.id).delete()
    for idx, opt in enumerate(master.options, start=1):
        db.add(
            CampaignQuestionOption(
                campaign_question_id=question.id,
                option_value=opt.option_value,
                option_text_en=opt.option_text_en,
                sentiment=opt.sentiment,
                score_value=opt.score_value,
                order_index=idx,
            )
        )
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/questions/{question_id}/delete")
async def delete_question(
    campaign_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    question = db.query(CampaignQuestion).get(question_id)
    if not question or question.campaign_id != campaign_id:
        raise HTTPException(status_code=404, detail="Question not found")
    # Clean up dependent data to avoid FK conflicts
    db.query(FeedbackAnswer).filter(FeedbackAnswer.campaign_question_id == question_id).delete()
    db.query(CampaignQuestionOption).filter(CampaignQuestionOption.campaign_question_id == question_id).delete()
    db.query(QuestionFlowRule).filter(
        (QuestionFlowRule.source_question_id == question_id)
        | (QuestionFlowRule.target_question_id == question_id)
    ).delete()
    campaign = db.query(Campaign).get(campaign_id)
    if campaign and campaign.exp_flow_map:
        new_map: Dict[str, List[int]] = {}
        for key, ids in campaign.exp_flow_map.items():
            filtered = [qid for qid in ids if qid != question_id]
            new_map[key] = filtered
        campaign.exp_flow_map = new_map
    db.delete(question)
    db.commit()
    reindex_campaign_questions(db, campaign_id)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/options/{option_id}/update")
async def update_option(
    campaign_id: int,
    option_id: int,
    option_text_en: str = Form(...),
    option_value: str = Form(...),
    sentiment: str = Form("neutral"),
    score_value: str = Form("0"),
    follow_up_label: str = Form(""),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    option = db.query(CampaignQuestionOption).get(option_id)
    if not option or option.question.campaign_id != campaign_id:
        raise HTTPException(status_code=404, detail="Option not found")
    option.option_text_en = option_text_en
    option.option_value = option_value
    option.sentiment = sentiment
    try:
        option.score_value = int(score_value) if score_value not in (None, "") else 0
    except (ValueError, TypeError):
        option.score_value = 0
    option.follow_up_label = follow_up_label or None
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/options/{option_id}/move")
async def move_option(
    campaign_id: int,
    option_id: int,
    direction: str = Form(...),  # "up" or "down"
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    option = db.query(CampaignQuestionOption).get(option_id)
    if not option or option.question.campaign_id != campaign_id:
        raise HTTPException(status_code=404, detail="Option not found")
    question_id = option.campaign_question_id
    options = (
        db.query(CampaignQuestionOption)
        .filter(CampaignQuestionOption.campaign_question_id == question_id)
        .order_by(CampaignQuestionOption.order_index, CampaignQuestionOption.id)
        .all()
    )
    idx_map = {o.id: i for i, o in enumerate(options)}
    if option_id not in idx_map:
        raise HTTPException(status_code=404, detail="Option not in list")
    i = idx_map[option_id]
    if direction == "up" and i > 0:
        options[i].order_index, options[i - 1].order_index = options[i - 1].order_index, options[i].order_index
    elif direction == "down" and i < len(options) - 1:
        options[i].order_index, options[i + 1].order_index = options[i + 1].order_index, options[i].order_index
    db.flush()
    reindex_question_options(db, question_id)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/options/{option_id}/delete")
async def delete_option(
    campaign_id: int,
    option_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    option = db.query(CampaignQuestionOption).get(option_id)
    if not option or option.question.campaign_id != campaign_id:
        raise HTTPException(status_code=404, detail="Option not found")
    question_id = option.campaign_question_id
    db.delete(option)
    db.commit()
    reindex_question_options(db, question_id)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/flow_rules/add")
async def add_flow_rule(
    campaign_id: int,
    source_question_id: int = Form(...),
    target_question_id: int = Form(...),
    source_option_value: str = Form(...),
    condition_type: str = Form("equals"),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    rule = QuestionFlowRule(
        campaign_id=campaign_id,
        source_question_id=source_question_id,
        target_question_id=target_question_id,
        source_option_value=source_option_value,
        condition_type=condition_type,
    )
    db.add(rule)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/flow_rules/{rule_id}/delete")
async def delete_flow_rule(
    campaign_id: int,
    rule_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    rule = db.query(QuestionFlowRule).get(rule_id)
    if not rule or rule.campaign_id != campaign_id:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)


@router.post("/{campaign_id}/flow_mapping")
async def update_flow_mapping(
    campaign_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    form = await request.form()
    flow_map: Dict[str, List[int]] = {}
    first_question = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .order_by(CampaignQuestion.order_index, CampaignQuestion.id)
        .first()
    )
    if first_question and first_question.options:
        for opt in first_question.options:
            selected_ids: List[int] = []
            for v in form.getlist(f"mapping_{opt.option_value}"):
                try:
                    selected_ids.append(int(v))
                except (TypeError, ValueError):
                    continue
            flow_map[str(opt.option_value)] = selected_ids
    else:
        flow_map = {}
    campaign.exp_flow_map = flow_map
    campaign.thank_you_title = form.get("thank_you_title") or None
    campaign.thank_you_message = form.get("thank_you_message") or None
    upload_dir = Path("app/static/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    thank_you_image = form.get("thank_you_image")
    if thank_you_image and getattr(thank_you_image, "filename", ""):
        filename = f"thankyou_{uuid4().hex}{Path(thank_you_image.filename).suffix}"
        dest = upload_dir / filename
        content = thank_you_image.file.read()
        dest.write_bytes(content)
        campaign.thank_you_image_url = f"/static/uploads/{filename}"
    else:
        campaign.thank_you_image_url = form.get("thank_you_image_url") or None
    db.commit()
    return RedirectResponse(url=f"/questionnaire/{campaign_id}", status_code=302)
