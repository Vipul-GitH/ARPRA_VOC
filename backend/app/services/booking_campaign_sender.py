from __future__ import annotations

from typing import Optional
from urllib.parse import quote_plus

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, text

from app.config import get_settings


class BookingCampaignSender:
    """
    Sends WhatsApp template messages for bookings with isCampaingsend=0,
    then marks them as sent.
    """

    def __init__(self, base_db_url: str):
        settings = get_settings()
        self.api_url = settings.whatsapp_api_url
        self.api_token = settings.whatsapp_api_token
        self.template_name = settings.whatsapp_template_name
        self.campaign_link = settings.whatsapp_campaign_link
        self.engine = create_engine(base_db_url, pool_pre_ping=True)
        self.scheduler = BackgroundScheduler(timezone="UTC")

    def _log(self, message: str):
        print(f"[BookingCampaignSender] {message}")

    def _normalize_mobile(self, raw: Optional[str]) -> str:
        if not raw:
            return ""
        digits = "".join(ch for ch in str(raw) if ch.isdigit())
        if not digits:
            return ""
        if len(digits) < 10:
            return ""
        if digits.startswith("91") and len(digits) == 12:
            return digits
        if len(digits) == 10:
            return "91" + digits
        if digits.startswith("0") and len(digits) == 11:
            return "91" + digits[1:]
        return ""

    def start(self):
        self.scheduler.add_job(self.process_pending, "interval", hours=1, max_instances=1, coalesce=True)
        self.scheduler.start()
        self._log("Scheduler started (interval 1h)")
        self.process_pending()

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self._log("Scheduler stopped")

    def _send_whatsapp(
        self,
        mobile: str,
        customername: str,
        bookingid: int | None,
        http: requests.Session | None = None,
    ) -> bool:
        target = self._normalize_mobile(mobile)
        if not target:
            self._log(f"Skip send: invalid mobile '{mobile}'")
            return False
        link = self.campaign_link
        if bookingid is not None:
            link = (
                f"{self.campaign_link}"
                f"?bookingid={quote_plus(str(bookingid))}"
                f"&name={quote_plus(customername or '')}"
                f"&mobile={quote_plus(target)}"
            )
        payload = {
            "message": [
                {
                    "recipient_whatsapp": target,
                    "message_type": "template",
                    "recipient_type": "individual",
                    "type_template": [
                        {
                            "name": self.template_name,
                            "attributes": [
                                customername or "",
                                link,
                            ],
                            "language": {"locale": "en", "policy": "deterministic"},
                        }
                    ],
                }
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        try:
            client = http or requests
            resp = client.post(self.api_url, headers=headers, json=payload, timeout=10)
            ok = 200 <= resp.status_code < 300
            if ok:
                self._log(f"Sent to {target}: HTTP {resp.status_code}")
            else:
                self._log(f"Failed send to {target}: HTTP {resp.status_code}")
            return ok
        except Exception as exc:
            self._log(f"Error sending to {target}: {exc}")
            return False

    def process_pending(self):
        query = text(
            """
            SELECT bookingid, customername, mobile
            FROM bookings
            WHERE isCampaingsend = 0
            ORDER BY bookingid ASC
            LIMIT 200
            """
        )
        update = text(
            """
            UPDATE bookings
            SET isCampaingsend = 1
            WHERE bookingid = :bid
            """
        )
        try:
            with self.engine.connect() as conn:
                rows = conn.execute(query).mappings().all()
            if not rows:
                self._log("No pending bookings")
                return

            self._log(f"Processing {len(rows)} pending bookings")
            sent_booking_ids = []
            with requests.Session() as http:
                for row in rows:
                    sent = self._send_whatsapp(
                        row.get("mobile"),
                        row.get("customername"),
                        row.get("bookingid"),
                        http,
                    )
                    if sent:
                        sent_booking_ids.append({"bid": row.get("bookingid")})

            if sent_booking_ids:
                with self.engine.begin() as conn:
                    conn.execute(update, sent_booking_ids)
        except Exception:
            import traceback
            self._log("Error while sending campaigns (will retry)")
            self._log(traceback.format_exc())
