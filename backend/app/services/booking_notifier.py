from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url


class BookingNotifier:
    """
    Polls phlebo_summary.tblbooking for startappbooking=1 rows,
    sends WhatsApp links, and marks feedback_sent to avoid repeats.
    """

    def __init__(self, base_db_url: str, campaign_link: str, whatsapp_api: str, account_id: int):
        self.campaign_link = campaign_link
        self.whatsapp_api = whatsapp_api
        self.account_id = account_id
        booking_url = self._with_db(base_db_url, "phlebo_summary")
        self.engine = create_engine(booking_url, pool_pre_ping=True)
        self.scheduler = BackgroundScheduler(timezone="UTC")
        self.state_path = Path(__file__).with_name("booking_notifier_state.json")
        self.last_bookingid: int = self._load_checkpoint()

    @staticmethod
    def _with_db(db_url: str, db_name: str) -> str:
        url = make_url(db_url)
        url = url.set(database=db_name)
        return str(url)

    def _log(self, message: str):
        print(f"[BookingNotifier] {message}")

    def _load_checkpoint(self) -> int:
        """
        Resume from the last processed booking id so we don't rescan a huge table on restart.
        """
        try:
            if self.state_path.exists():
                data = json.loads(self.state_path.read_text())
                return int(data.get("last_bookingid", 0))
        except Exception:
            self._log("Checkpoint load failed; starting from 0")
        return 0

    def _persist_checkpoint(self):
        try:
            self.state_path.write_text(json.dumps({"last_bookingid": self.last_bookingid}))
        except Exception as exc:
            self._log(f"Checkpoint persist failed: {exc}")

    def start(self):
        self._ensure_feedback_column()
        # Run every hour; max_instances=1 prevents overlap.
        self.scheduler.add_job(self.process_pending_bookings, "interval", hours=1, max_instances=1, coalesce=True)
        self.scheduler.start()
        self._log(f"Scheduler started (interval 1h) from bookingid>{self.last_bookingid}")

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self._log("Scheduler stopped")
        # Persist last processed id on clean shutdown
        self._persist_checkpoint()

    def _ensure_feedback_column(self):
        # Add feedback_sent and feedback_sent_at if missing; safe no-op if MySQL supports IF NOT EXISTS.
        ddls = [
            "ALTER TABLE tblbooking ADD COLUMN IF NOT EXISTS feedback_sent TINYINT(1) DEFAULT 0",
            "ALTER TABLE tblbooking ADD COLUMN IF NOT EXISTS feedback_sent_at DATETIME NULL",
        ]
        with self.engine.begin() as conn:
            for ddl in ddls:
                try:
                    conn.execute(text(ddl))
                except Exception as exc:
                    # Older MySQL may not support IF NOT EXISTS; ignore if column already exists.
                    self._log(f"Column ensure skipped: {exc}")
        self._log("Ensured feedback_sent and feedback_sent_at columns")

    def _normalize_contact(self, raw: Optional[str]) -> str:
        if not raw:
            return ""
        raw = str(raw).strip()
        if "@" in raw:
            return raw  # group id
        digits = "".join(ch for ch in raw if ch.isdigit())
        if not digits:
            return ""
        if digits.startswith("91") and len(digits) == 12:
            return digits
        if len(digits) == 10:
            return "91" + digits
        return digits

    def _send_whatsapp(
        self,
        mobile: str,
        bookingid: Optional[str] = None,
        http: requests.Session | None = None,
    ) -> bool:
        target = self._normalize_contact(mobile)
        if not target:
            self._log(f"Skip send: invalid mobile '{mobile}'")
            return False
        link = self.campaign_link
        params = []
        if bookingid:
            params.append(f"bookingid={quote_plus(str(bookingid))}")
        if mobile:
            params.append(f"mobile={quote_plus(str(mobile))}")
        if params:
            link = f"{link}?{'&'.join(params)}"
        self._log(f"Sending WhatsApp to {target} (bookingid={bookingid})")
        payload = {
            "accountId": self.account_id,
            "target": target,
            "message": f"HOME SAMPLE COLLECTION PATIENT FEEDBACK: {link}",
        }
        try:
            client = http or requests
            resp = client.post(self.whatsapp_api, json=payload, timeout=8)
            ok = 200 <= resp.status_code < 300
            if ok:
                self._log(f"Sent to {target}: HTTP {resp.status_code}")
            else:
                self._log(f"Failed send to {target}: HTTP {resp.status_code}")
            return ok
        except Exception as exc:
            self._log(f"Error sending to {target}: {exc}")
            return False

    def process_pending_bookings(self):
        query = text(
            """
            SELECT bookingid, mobile
            FROM tblbooking
            WHERE startappbooking = 1
              AND (feedback_sent IS NULL OR feedback_sent = 0)
              AND bookingid > :last_id
            ORDER BY bookingid ASC
            LIMIT 200
            """
        )
        update = text(
            """
            UPDATE tblbooking
            SET feedback_sent = :sent,
                feedback_sent_at = :ts
            WHERE bookingid = :bid
            """
        )
        now = datetime.utcnow()
        try:
            with self.engine.connect() as conn:
                rows = conn.execute(query, {"last_id": self.last_bookingid}).fetchall()
            if not rows:
                self._log("No pending bookings")
                return

            self._log(f"Processing {len(rows)} pending bookings")
            updates = []
            max_id = self.last_bookingid
            with requests.Session() as http:
                for row in rows:
                    sent = self._send_whatsapp(row.mobile, getattr(row, "bookingid", None), http)
                    updates.append(
                        {
                            "sent": 1 if sent else 0,
                            "ts": now,
                            "bid": row.bookingid,
                        }
                    )
                    self._log(f"Marked booking {row.bookingid} feedback_sent={1 if sent else 0}")
                    if row.bookingid and row.bookingid > max_id:
                        max_id = row.bookingid

            if updates:
                with self.engine.begin() as conn:
                    conn.execute(update, updates)
            self.last_bookingid = max_id
            # Persist checkpoint so restart does not rescan billions of old rows
            self._persist_checkpoint()
        except Exception:
            # Silent fail; next tick will retry unsent rows.
            import traceback
            self._log("Error while processing bookings (will retry)")
            self._log(traceback.format_exc())
            return
