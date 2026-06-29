from datetime import datetime
from typing import List

import io
import csv
import re
from io import BytesIO, StringIO
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

# Optional PDF export dependency
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:  # pragma: no cover - fallback if reportlab not installed
    A4 = None
    mm = None
    canvas = None
    pdfmetrics = None
    TTFont = None

router = APIRouter(tags=["campaigns"])
templates = Jinja2Templates(directory="app/templates")
PUBLIC_HOST = "https://labmate.bhasinpathlabs.com:4668"
WHATSAPP_SEND_API = "http://10.1.1.44:3004/api/messages/send"
WHATSAPP_ACCOUNT_ID = 1
WHATSAPP_MEDIA_URL = "https://labmate.bhasinpathlabs.com:4668/static/img/santa.gif"


@router.get("/")
async def list_campaigns(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    campaigns = db.query(Campaign).all()
    return templates.TemplateResponse(
        "campaigns/list.html", {"request": request, "campaigns": campaigns, "user": user}
    )


@router.get("/flow_pdf/{campaign_id}")
async def export_campaign_flow_pdf(
    campaign_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if canvas is None:
        raise HTTPException(
            status_code=501,
            detail="PDF export requires reportlab in the app environment.",
        )
    campaign = db.query(Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    questions = (
        db.query(CampaignQuestion)
        .filter(CampaignQuestion.campaign_id == campaign.id)
        .order_by(CampaignQuestion.order_index, CampaignQuestion.id)
        .all()
    )
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 20 * mm

    # Force ASCII to drop Hindi characters (per request); use Helvetica
    force_ascii = True
    font_name = "Helvetica"

    max_width = width - 40 * mm

    def wrap_text(text: str, size: int) -> list[str]:
        """ASCII-only, clean punctuation, wrap to page width."""
        if not text:
            return [""]
        replacements = {
            "–": "-",
            "—": "-",
            "−": "-",
            "•": "-",
            ",": " ",
            "/": " ",
            "?": " ",
            "(": " ",
            ")": " ",
            ".": " ",
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        # keep only A-Z a-z 0-9 dash and space
        cleaned = []
        for ch in text:
            if ch.isascii() and (ch.isalnum() or ch in {"-", " "}):
                cleaned.append(ch)
            else:
                cleaned.append(" ")
        text = "".join(cleaned)
        words = text.split()
        if not words:
            return [""]
        max_chars = int(max_width / (size * 0.55))
        lines = []
        line = []
        count = 0
        for w in words:
            if count + len(w) + (1 if line else 0) > max_chars:
                lines.append(" ".join(line))
                line = [w]
                count = len(w)
            else:
                line.append(w)
                count += len(w) + (1 if line[:-1] else 0)
        if line:
            lines.append(" ".join(line))
        return lines or [""]

    def add_line(text: str, font=font_name, size=11, leading=14, color=colors.black):
        nonlocal y
        if y < 20 * mm:
            pdf.showPage()
            y = height - 20 * mm
        pdf.setFont(font, size)
        for ln in wrap_text(text, size):
            if y < 20 * mm:
                pdf.showPage()
                y = height - 20 * mm
                pdf.setFont(font, size)
            pdf.setFillColor(color)
            pdf.drawString(20 * mm, y, ln)
            pdf.setFillColor(colors.black)
            y -= leading

    sentiment_colors = {
        "positive": colors.HexColor("#22c55e"),
        "neutral": colors.HexColor("#facc15"),
        "negative": colors.HexColor("#ef4444"),
    }
    add_line(f"Campaign: {campaign.name}", size=14, leading=18)
    add_line(f"Code: {campaign.code or ''}", size=12, leading=16)
    add_line(f"Total Questions: {len(questions)}", size=10, leading=14)
    # Legend directly under heading
    legend_items = [("positive", "Positive"), ("neutral", "Neutral"), ("negative", "Negative")]
    if y < 25 * mm:
        pdf.showPage()
        y = height - 20 * mm
    pdf.setFont(font_name, 9)
    for idx, (key, label) in enumerate(legend_items):
        r = 3.5
        x = 20 * mm + idx * 45
        pdf.setFillColor(sentiment_colors[key])
        pdf.circle(x, y, r, fill=1, stroke=0)
        pdf.setFillColor(colors.black)
        pdf.drawString(x + 7, y + r - 1, label)
    y -= 14
    add_line("")

    # Section: Questions
    add_line("Questions", size=13, leading=17)
    add_line("----------------------------------------", size=9, leading=12)
    for q in questions:
        q_title = q.question_text_en or q.question_text or ""
        add_line(f"Q{q.order_index or q.id}: {q_title}", size=11, leading=15)
        if q.options:
            for opt in sorted(q.options, key=lambda o: (o.order_index or 0, o.id)):
                opt_text = opt.option_text_en or opt.option_text_hi or str(opt.option_value)
                sentiment = (opt.sentiment or "").lower()
                # draw badge + text manually (sentiment optional)
                sentiment = (opt.sentiment or "").lower()
                color = sentiment_colors.get(sentiment, colors.lightgrey)
                text_font_size = 10
                leading = 13
                opt_lines = wrap_text(opt_text, text_font_size)
                if y < 20 * mm:
                    pdf.showPage()
                    y = height - 20 * mm
                for idx, ln in enumerate(opt_lines):
                    pdf.setFillColor(color)
                    pdf.circle(22 * mm, y + 2, 3, fill=1, stroke=0)
                    pdf.setFillColor(colors.black)
                    pdf.setFont(font_name, text_font_size)
                    pdf.drawString(28 * mm, y, ln)
                    y -= leading
        add_line("")

    # Flow mapping (exp_flow_map uses Q1 options -> follow-up question IDs)
    flow_map = campaign.exp_flow_map or {}
    first_question = questions[0] if questions else None
    if flow_map and first_question and first_question.options:
        q_lookup = {q.id: q for q in questions}
        opt_lookup = {}
        for opt in first_question.options:
            if opt.option_value is not None:
                opt_lookup[opt.option_value] = opt
                opt_lookup[str(opt.option_value)] = opt
            if opt.option_text_en:
                opt_lookup[opt.option_text_en] = opt
            if opt.option_text_hi:
                opt_lookup[opt.option_text_hi] = opt

        add_line("Flow mapping (driven by Q1)", size=12, leading=16)
        add_line("----------------------------------------", size=9, leading=12)
        add_line(f"Q1: {first_question.question_text_en or first_question.question_text or ''}", size=10, leading=14)
        for key, targets in flow_map.items():
            opt = opt_lookup.get(key)
            label = opt.option_text_en or opt.option_text_hi or str(opt.option_value) if opt else str(key)
            target_lines = []
            for qid in targets or []:
                q_obj = q_lookup.get(qid)
                if q_obj:
                    target_lines.append(f"Q{q_obj.order_index or q_obj.id}: {q_obj.question_text_en or q_obj.question_text or ''}")
            add_line(f"If Q1 = {label} ->", size=11, leading=15)
            if target_lines:
                for tl in target_lines:
                    add_line(f"    • {tl}", size=9, leading=12)
            else:
                add_line("    (no follow-up mapped)", size=9, leading=12)
        add_line("")

    # Skip logic summary (if present)
    if campaign.skip_logic:
        sl = campaign.skip_logic
        add_line("Skip logic", size=12, leading=16)
        add_line("----------------------------------------", size=9, leading=12)
        add_line(f"Check question order: {sl.get('question_order')}", size=10, leading=13)
        add_line(f"Mode: {sl.get('mode', 'allow')} (allow=show only when value matches; block=hide when matches)", size=9, leading=12)
        add_line(f"Match values: {', '.join([str(v) for v in sl.get('values', [])])}", size=9, leading=12)
        add_line("")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    filename = f"campaign_{campaign_id}_flow.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename=\"{filename}\"'},
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
    request: Request,
    campaign_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    campaigns = db.query(Campaign).order_by(Campaign.name).all()
    return templates.TemplateResponse(
        "campaigns/send.html",
        {
            "request": request,
            "user": user,
            "campaigns": campaigns,
            "selected_campaign_id": campaign_id,
            "summary": None,
            "error": None,
        },
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

        recipient_rows: List[dict] = []
        for entry in contacts:
            recipient = CampaignRecipient(
                recipient_list_id=recipient_list.id,
                campaign_id=campaign_id,
                pii_data_json={"name": entry["name"], "contact": entry["contact"]},
                personalized_link_token=uuid4().hex,
                status="pending",
            )
            db.add(recipient)
            recipient_rows.append({"entry": entry, "recipient": recipient})
        db.commit()

        # Send WhatsApp messages
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
        details: List[dict] = []
        for row in recipient_rows:
            entry = row["entry"]
            recipient = row["recipient"]
            target = _normalize_contact(entry["contact"])
            if not target:
                recipient.status = "failed"
                failed.append({"target": entry["contact"], "error": "invalid contact"})
                details.append({"target": entry["contact"], "name": entry["name"], "status": "failed", "error": "invalid contact"})
                continue
            mobile_param = quote(target[-10:]) if len(target) >= 10 else quote(target)
            name_param = quote(entry["name"])
            token = recipient.personalized_link_token or str(campaign.code if campaign.code else campaign.id)
            link = f"{PUBLIC_HOST}/feedback/{token}?name={name_param}&mobile={mobile_param}&country=91"
            # Custom message for campaign code_5
            if (campaign.code or "").lower() == "code_5":
                nm = entry["name"]
                msg = (
                    f"Hello {nm},\n"
                    "At Dr Bhasin’s Lab, accuracy and patient safety depend on people, not machines alone.\n"
                    "This feedback is not for fault-finding. It is to understand your experience, improve systems, and support you better.\n"
                    "Your honest responses will help us work better together and serve patients better.\n"
                    f"Share Your Experience here: {link}\n\n"
                    f"प्रिय {nm} ,\n"
                    "डॉ. भसीन लैब में सटीकता और मरीजों की सुरक्षा केवल मशीनों से नहीं, बल्कि लोगों से सुनिश्चित होती है।\n"
                    "यह फीडबैक किसी की गलती निकालने के लिए नहीं है। इसका उद्देश्य आपके अनुभव को समझना, कार्यप्रणाली सुधारना और आपको बेहतर सहयोग देना है।\n"
                    "आपकी ईमानदार राय हमें बेहतर काम करने और मरीजों को बेहतर सेवा देने में मदद करेगी।\n"
                    f"अपना अनुभव यहां साझा करें: {link}\n\n"
                    "With Care,\nDr Vishu Bhasin & Dr Vipul Bhasin\nDr Bhasin's Lab"
                )
            elif (campaign.code or "").lower() == "code_6":
                msg = (
                    "Tomorrow is our Director Dr. Vipul Bhasin’s birthday. "
                    "We have shared a small feedback form where you can wish Sir. "
                    "Please fill out the form and send your good wishes to Sir. Thank you.\n\n"
                    "कल हमारे निदेशक डॉ. विपुल भसीन का जन्मदिन है। "
                    "इसके लिए हमने एक छोटा फीडबैक फॉर्म साझा किया है, जिसमें आप सर को शुभकामनाएं दे सकते हैं। "
                    "कृपया फॉर्म भरें और सर को अपनी शुभकामनाएं दें। धन्यवाद।\n\n"
                    f"{link}"
                )
            else:
                msg = f"Hi {entry['name']}, please share your feedback: {link}"

            payload = {
                "accountId": WHATSAPP_ACCOUNT_ID,
                "target": target,
                "message": msg,
            }
            if media_url:
                payload["mediaUrl"] = media_url
            if media_data:
                payload.setdefault("attachments", []).append(media_data)
            try:
                resp = requests.post(WHATSAPP_SEND_API, json=payload, timeout=8)
                if 200 <= resp.status_code < 300:
                    recipient.status = "complete"
                    success_count += 1
                    details.append({"target": entry["contact"], "name": entry["name"], "status": "success"})
                else:
                    recipient.status = "failed"
                    failed.append({"target": entry["contact"], "error": f"HTTP {resp.status_code}"})
                    details.append({"target": entry["contact"], "name": entry["name"], "status": "failed", "error": f"HTTP {resp.status_code}", "body": resp.text[:200] if resp.text else ""})
            except Exception as exc:
                recipient.status = "failed"
                failed.append({"target": entry["contact"], "error": str(exc)})
                details.append({"target": entry["contact"], "name": entry["name"], "status": "failed", "error": str(exc)})

        db.commit()

        summary = {
            "count": len(contacts),
            "campaign": campaign.name,
            "list_name": list_name,
            "send_success": success_count,
            "send_failed": failed,
        }
        # Log send summary to file
        try:
            logs_dir = Path("logs")
            logs_dir.mkdir(parents=True, exist_ok=True)
            log_path = logs_dir / "campaign_send.log"
            ts = datetime.utcnow().isoformat()
            with log_path.open("a", encoding="utf-8") as fh:
                fh.write(
                    f"{ts} | campaign={campaign.code or campaign.id} | name={campaign.name} | total={len(contacts)} | "
                    f"success={success_count} | failed={len(failed)} | list={list_name}\n"
                )
                for item in details:
                    status = item.get("status")
                    tgt = item.get("target")
                    nm = item.get("name")
                    err = item.get("error", "")
                    fh.write(f"  - status={status} target={tgt} name={nm}")
                    if err:
                        fh.write(f" error={err}")
                    fh.write("\n")
        except Exception as e:
            print(f"[CampaignSend] log write failed: {e}")
        return templates.TemplateResponse(
            "campaigns/send.html",
            {
                "request": request,
                "user": user,
                "campaigns": campaigns,
                "selected_campaign_id": campaign_id,
                "summary": summary,
                "error": None,
            },
        )
    except HTTPException as exc:
        return templates.TemplateResponse(
            "campaigns/send.html",
            {
                "request": request,
                "user": user,
                "campaigns": campaigns,
                "selected_campaign_id": campaign_id,
                "summary": None,
                "error": exc.detail,
            },
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
    db.refresh(campaign)
    return RedirectResponse(url=f"/questionnaire/{campaign.id}", status_code=302)


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
