from datetime import datetime
from typing import List

import io
import csv
import re
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import qrcode
import requests
from urllib.parse import quote
import base64
from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, File
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import (
    Campaign,
    CampaignQuestion,
    CampaignQuestionOption,
    CampaignChannel,
    CampaignPiiField,
    CampaignRecipient,
    CampaignRecipientList,
    CampaignSendSchedule,
    CollectionChannel,
    FeedbackAnswer,
    FeedbackFile,
    FeedbackResponse,
    FeedbackTicket,
    MasterQuestion,
    QuestionFlowRule,
    ResponseReward,
    TicketUpdate,
)
from app.routers.auth import get_current_user, require_role
from app.routers.questionnaire import ensure_campaign_has_exp_lab_question, ensure_exp_lab_master_question

router = APIRouter(tags=["campaigns"])
templates = Jinja2Templates(directory="app/templates")
PUBLIC_HOST = "https://labmate.bhasinpathlabs.com:4667"
WHATSAPP_SEND_API = "http://192.168.0.71:3004/api/messages/send"
WHATSAPP_ACCOUNT_ID = 1
WHATSAPP_MEDIA_URL = "https://labmate.bhasinpathlabs.com:4667/static/img/santa.gif"


@router.get("/")
async def list_campaigns(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    campaigns = db.query(Campaign).all()
    return templates.TemplateResponse(
        "campaigns/list.html", {"request": request, "campaigns": campaigns, "user": user}
    )


def _parse_contacts_from_upload(file: UploadFile) -> List[dict]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Please upload a file with contacts.")
    name = file.filename.lower()
    content = file.file.read()
    contacts = []

    def normalize(col: str) -> str:
        return re.sub(r"[^a-z0-9]", "", col.lower())

    if name.endswith(".csv"):
        text = content.decode("utf-8", errors="ignore")
        rows = list(csv.reader(text.splitlines()))
        if not rows:
            raise HTTPException(status_code=400, detail="The uploaded CSV is empty.")
        header = [normalize(h) for h in rows[0]]
        data_rows = rows[1:] if len(rows) > 1 else []
        if not data_rows:
            data_rows = rows  # treat first line as data if no header
        try:
            name_idx = header.index("name")
        except ValueError:
            name_idx = 0
        contact_idx = None
        for key in ("contact", "mobile", "phone"):
            if key in header:
                contact_idx = header.index(key)
                break
        if contact_idx is None:
            contact_idx = 1 if len(header) > 1 else 0
        for row in data_rows:
            if contact_idx >= len(row):
                continue
            contact = (row[contact_idx] or "").strip()
            if not contact:
                continue
            nm = (row[name_idx] if name_idx < len(row) else "").strip()
            contacts.append({"name": nm or "Friend", "contact": contact})
    elif name.endswith(".xlsx"):
        try:
            from openpyxl import load_workbook
        except ImportError:
            raise HTTPException(status_code=400, detail="openpyxl is required to read .xlsx files")
        wb = load_workbook(BytesIO(content), read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            raise HTTPException(status_code=400, detail="The uploaded sheet is empty.")
        header = [normalize(str(h or "")) for h in rows[0]]
        data_rows = rows[1:] if len(rows) > 1 else rows
        try:
            name_idx = header.index("name")
        except ValueError:
            name_idx = 0
        contact_idx = None
        for key in ("contact", "mobile", "phone"):
            if key in header:
                contact_idx = header.index(key)
                break
        if contact_idx is None:
            contact_idx = 1 if len(header) > 1 else 0
        for row in data_rows:
            row = list(row)
            if contact_idx >= len(row):
                continue
            contact = str(row[contact_idx] or "").strip()
            if not contact:
                continue
            nm = str(row[name_idx] or "").strip() if name_idx < len(row) else ""
            contacts.append({"name": nm or "Friend", "contact": contact})
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload .csv or .xlsx.")

    if not contacts:
        raise HTTPException(status_code=400, detail="No contacts found in the file.")
    return contacts


def _normalize_contact(raw: str) -> str:
    if not raw:
        return ""
    raw = str(raw).strip()
    if "@" in raw:
        return raw  # group or jid style; leave as is
    if raw.startswith("+"):
        raw = raw[1:]
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return ""
    # Ensure country code 91 prefix
    if len(digits) == 10:
        digits = "91" + digits
    elif len(digits) == 12 and not digits.startswith("91"):
        digits = "91" + digits[-10:]
    return digits


def _encode_image_b64(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    ext = path.suffix.lower().replace(".", "") or "png"
    mime = f"image/{'jpeg' if ext in ['jpg', 'jpeg'] else ext}"
    return mime, b64


@router.get("/send")
async def send_campaign(
    request: Request, db: Session = Depends(get_db), user=Depends(require_role("admin"))
):
    campaigns = db.query(Campaign).order_by(Campaign.name).all()
    return templates.TemplateResponse(
        "campaigns/send.html",
        {"request": request, "user": user, "campaigns": campaigns, "summary": None, "error": None},
    )


@router.post("/send")
async def upload_recipients(
    request: Request,
    campaign_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaigns = db.query(Campaign).order_by(Campaign.name).all()
    try:
        contacts = _parse_contacts_from_upload(file)
        # Store recipients for future sending (no external send here)
        list_name = f"Upload {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
        recipient_list = CampaignRecipientList(
            campaign_id=campaign_id,
            source_type="upload_excel",
            name=list_name,
            description=f"Uploaded {len(contacts)} contacts via send page",
        )
        db.add(recipient_list)
        db.flush()

        for entry in contacts:
            db.add(
                CampaignRecipient(
                    recipient_list_id=recipient_list.id,
                    campaign_id=campaign_id,
                    pii_data_json={"name": entry["name"], "contact": entry["contact"]},
                    status="pending",
                )
            )
        db.commit()

        # Send WhatsApp messages
        base_link = f"{PUBLIC_HOST}/feedback/{campaign.code if campaign.code else campaign.id}"
        media_url = WHATSAPP_MEDIA_URL
        media_data = None
        try:
            default_path = Path("app/static/img/santa.gif")
            if default_path.exists():
                mime, b64 = _encode_image_b64(default_path)
                media_data = {"type": "image", "mime": mime, "data": b64, "filename": "santa.gif"}
        except Exception:
            media_data = None

        success_count = 0
        failed = []
        for entry in contacts:
            target = _normalize_contact(entry["contact"])
            if not target:
                failed.append({"target": entry["contact"], "error": "invalid contact"})
                continue
            mobile_param = quote(target[-10:]) if len(target) >= 10 else quote(target)
            name_param = quote(entry["name"])
            link = f"{base_link}?name={name_param}&mobile={mobile_param}&country=91"
            payload = {
                "accountId": WHATSAPP_ACCOUNT_ID,
                "target": target,
                "message": f"Hi {entry['name']}, please share your feedback: {link}",
            }
            if media_url:
                payload["mediaUrl"] = media_url
            if media_data:
                payload.setdefault("attachments", []).append(media_data)
            try:
                resp = requests.post(WHATSAPP_SEND_API, json=payload, timeout=8)
                if 200 <= resp.status_code < 300:
                    success_count += 1
                else:
                    failed.append({"target": entry["contact"], "error": f"HTTP {resp.status_code}"})
            except Exception as exc:
                failed.append({"target": entry["contact"], "error": str(exc)})

        summary = {
            "count": len(contacts),
            "campaign": campaign.name,
            "list_name": list_name,
            "send_success": success_count,
            "send_failed": failed,
        }
        return templates.TemplateResponse(
            "campaigns/send.html",
            {"request": request, "user": user, "campaigns": campaigns, "summary": summary, "error": None},
        )
    except HTTPException as exc:
        return templates.TemplateResponse(
            "campaigns/send.html",
            {"request": request, "user": user, "campaigns": campaigns, "summary": None, "error": exc.detail},
            status_code=exc.status_code,
        )

@router.get("/new")
async def new_campaign(request: Request, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    master_questions = db.query(MasterQuestion).filter(MasterQuestion.is_active.is_(True)).order_by(MasterQuestion.code).all()
    return templates.TemplateResponse(
        "campaigns/edit.html",
        {
            "request": request,
            "campaign": None,
            "action": "/campaigns/new",
            "user": user,
            "channels": [],
            "questions": [],
            "flow_rules": [],
            "master_questions": master_questions,
        },
    )


@router.post("/new")
async def create_campaign(
    request: Request,
    name: str = Form(...),
    code: str = Form(...),
    header_title: str = Form(""),
    campaign_type: str = Form("walk_in"),
    layout_type: str = Form("one_page"),
    primary_language: str = Form("en"),
    estimated_fill_time_seconds: int = Form(60),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = Campaign(
        name=name,
        code=code,
        header_title=header_title or None,
        campaign_type=campaign_type,
        layout_type=layout_type,
        primary_language=primary_language,
        estimated_fill_time_seconds=estimated_fill_time_seconds,
        status="draft",
        created_by=user.id,
    )
    db.add(campaign)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        master_questions = (
            db.query(MasterQuestion)
            .filter(MasterQuestion.is_active.is_(True))
            .order_by(MasterQuestion.code)
            .all()
        )
        return templates.TemplateResponse(
            "campaigns/edit.html",
            {
                "request": request,
                "campaign": None,
                "action": "/campaigns/new",
                "user": user,
                "channels": [],
                "questions": [],
                "flow_rules": [],
                "master_questions": master_questions,
                "error": "Campaign code already exists. Please choose a unique code.",
            },
            status_code=400,
        )
    return RedirectResponse(url="/campaigns/", status_code=302)


@router.get("/{campaign_id}/edit")
async def edit_campaign(
    campaign_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    exp_master = ensure_exp_lab_master_question(db)
    channels = db.query(CollectionChannel).all()
    questions = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .order_by(CampaignQuestion.order_index)
        .all()
    )
    first_question = questions[0] if questions else None
    campaign_master_question = ensure_campaign_has_exp_lab_question(db, campaign)
    flow_rules = []
    master_questions = (
        db.query(MasterQuestion)
        .filter(MasterQuestion.is_active.is_(True))
        .order_by(MasterQuestion.code)
        .all()
    )
    return templates.TemplateResponse(
        "campaigns/edit.html",
        {
            "request": request,
            "campaign": campaign,
            "action": f"/campaigns/{campaign_id}/edit",
            "user": user,
            "channels": channels,
            "questions": questions,
            "flow_rules": flow_rules,
            "flow_map": campaign.exp_flow_map or {},
            "exp_lab_master": exp_master,
            "campaign_master_question": campaign_master_question,
            "master_questions": master_questions,
            "first_question": first_question,
        },
    )


@router.get("/{campaign_id}/qr")
async def campaign_qr(campaign_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    link = request.url_for("view_form", token=campaign.code)
    img = qrcode.make(link)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    headers = {"Content-Disposition": f'attachment; filename="campaign-{campaign.code}-qr.png"'}
    return StreamingResponse(buf, media_type="image/png", headers=headers)


@router.post("/{campaign_id}/copy")
async def copy_campaign(
    campaign_id: int,
    request: Request,
    new_name: str = Form(None),
    new_code: str = Form(None),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    src = db.query(Campaign).get(campaign_id)
    if not src:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # generate unique code
    def unique_code(base: str) -> str:
        candidate = base
        suffix = 2
        while db.query(Campaign).filter(Campaign.code == candidate).first():
            candidate = f"{base}-{suffix}"
            suffix += 1
        return candidate

    base_code = (new_code or f"{src.code}-copy").lower()
    code = unique_code(base_code)
    name = new_name or f"{src.name} (Copy)"

    new_campaign = Campaign(
        name=name,
        code=code,
        description=src.description,
        header_title=src.header_title,
        campaign_type=src.campaign_type,
        status="draft",
        primary_language=src.primary_language,
        available_languages=src.available_languages,
        layout_type=src.layout_type,
        estimated_fill_time_seconds=src.estimated_fill_time_seconds,
        max_score=src.max_score,
        scoring_method=src.scoring_method,
        created_by=user.id if getattr(user, "id", None) else src.created_by,
        thank_you_title=getattr(src, "thank_you_title", None),
        thank_you_message=getattr(src, "thank_you_message", None),
        thank_you_image_url=getattr(src, "thank_you_image_url", None),
    )
    db.add(new_campaign)
    db.flush()

    # copy questions and options
    questions = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign_id)
        .order_by(CampaignQuestion.order_index, CampaignQuestion.id)
        .all()
    )
    id_map = {}
    for q in questions:
        new_q = CampaignQuestion(
            campaign_id=new_campaign.id,
            master_question_id=q.master_question_id,
            question_text_en=q.question_text_en,
            question_text_hi=q.question_text_hi,
            question_type=q.question_type,
            is_required=q.is_required,
            order_index=q.order_index,
            page_number=q.page_number,
            is_master=q.is_master,
            is_overall_rating=q.is_overall_rating,
        )
        db.add(new_q)
        db.flush()
        id_map[q.id] = new_q.id

        options = (
            db.query(CampaignQuestionOption)
            .filter(CampaignQuestionOption.campaign_question_id == q.id)
            .order_by(CampaignQuestionOption.order_index, CampaignQuestionOption.id)
            .all()
        )
        for opt in options:
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
                    order_index=opt.order_index,
                )
            )

    # copy flow map if present
    if getattr(src, "exp_flow_map", None):
        new_map = {}
        for key, ids in src.exp_flow_map.items():
            mapped_ids = [id_map[i] for i in ids if i in id_map]
            new_map[key] = mapped_ids
        new_campaign.exp_flow_map = new_map

    db.commit()
    return RedirectResponse(url=f"/campaigns/{new_campaign.id}/edit", status_code=302)


@router.post("/{campaign_id}/edit")
async def update_campaign(
    campaign_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    header_title: str = Form(""),
    campaign_type: str = Form("walk_in"),
    status: str = Form("draft"),
    layout_type: str = Form("one_page"),
    primary_language: str = Form("en"),
    estimated_fill_time_seconds: int = Form(60),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.name = name
    campaign.description = description
    campaign.header_title = header_title or None
    campaign.campaign_type = campaign_type
    campaign.status = status
    campaign.layout_type = layout_type
    campaign.primary_language = primary_language
    campaign.estimated_fill_time_seconds = estimated_fill_time_seconds
    campaign.updated_at = datetime.utcnow()
    db.commit()
    return RedirectResponse(url="/campaigns/", status_code=302)


@router.post("/{campaign_id}/delete")
async def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Clean up related data to avoid FK conflicts
    ticket_ids_subq = db.query(FeedbackTicket.id).filter(FeedbackTicket.campaign_id == campaign_id).subquery()
    response_ids_subq = db.query(FeedbackResponse.id).filter(FeedbackResponse.campaign_id == campaign_id).subquery()
    question_ids_subq = db.query(CampaignQuestion.id).filter(CampaignQuestion.campaign_id == campaign_id).subquery()

    # Remove ticket updates
    db.query(TicketUpdate).filter(TicketUpdate.ticket_id.in_(ticket_ids_subq)).delete(synchronize_session=False)
    # Clear cross-links
    db.query(FeedbackResponse).filter(FeedbackResponse.campaign_id == campaign_id).update({FeedbackResponse.ticket_id: None}, synchronize_session=False)
    db.query(FeedbackTicket).filter(FeedbackTicket.campaign_id == campaign_id).update({FeedbackTicket.response_id: None}, synchronize_session=False)
    # Delete tickets
    db.query(FeedbackTicket).filter(FeedbackTicket.campaign_id == campaign_id).delete(synchronize_session=False)

    # Delete response attachments, rewards, answers, then responses
    db.query(ResponseReward).filter(ResponseReward.response_id.in_(response_ids_subq)).delete(synchronize_session=False)
    db.query(FeedbackFile).filter(FeedbackFile.response_id.in_(response_ids_subq)).delete(synchronize_session=False)
    db.query(FeedbackAnswer).filter(FeedbackAnswer.response_id.in_(response_ids_subq)).delete(synchronize_session=False)
    db.query(FeedbackResponse).filter(FeedbackResponse.campaign_id == campaign_id).delete(synchronize_session=False)

    # Delete question options, flow rules, questions
    db.query(CampaignQuestionOption).filter(CampaignQuestionOption.campaign_question_id.in_(question_ids_subq)).delete(synchronize_session=False)
    db.query(QuestionFlowRule).filter(QuestionFlowRule.campaign_id == campaign_id).delete(synchronize_session=False)
    db.query(CampaignQuestion).filter(CampaignQuestion.campaign_id == campaign_id).delete(synchronize_session=False)

    db.query(CampaignChannel).filter(CampaignChannel.campaign_id == campaign_id).delete(synchronize_session=False)
    db.query(CampaignPiiField).filter(CampaignPiiField.campaign_id == campaign_id).delete(synchronize_session=False)
    db.query(CampaignSendSchedule).filter(CampaignSendSchedule.campaign_id == campaign_id).delete(synchronize_session=False)
    db.query(CampaignRecipient).filter(CampaignRecipient.campaign_id == campaign_id).delete(synchronize_session=False)
    db.query(CampaignRecipientList).filter(CampaignRecipientList.campaign_id == campaign_id).delete(synchronize_session=False)

    db.delete(campaign)
    db.commit()
    return RedirectResponse(url="/campaigns/", status_code=302)
