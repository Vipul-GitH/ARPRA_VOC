from __future__ import annotations

from pathlib import Path
from urllib.parse import quote_plus
from zoneinfo import ZoneInfo

import json
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, text

from app.config import get_settings


class BookingSync:
    """
    Pulls home collection patient rows from an external read-only database
    and upserts them into arpra_voc.bookings.
    """

    def __init__(self, base_db_url: str):
        settings = get_settings()
        source_url = self._build_source_url(
            settings.mysql_host,
            settings.mysql_port,
            settings.mysql_user,
            settings.mysql_password,
            settings.mysql_db,
        )
        self.source_engine = create_engine(source_url, pool_pre_ping=True)
        self.target_engine = create_engine(base_db_url, pool_pre_ping=True)
        self.scheduler = BackgroundScheduler(timezone=ZoneInfo("Asia/Kolkata"))
        self.state_path = Path(__file__).with_name("booking_sync_state.json")
        self.last_bookingid: int = self._load_checkpoint()

    @staticmethod
    def _build_source_url(
        host: str,
        port: int,
        user: str,
        password: str,
        db_name: str,
    ) -> str:
        if not all([host, port, user, db_name]):
            raise ValueError("Missing MYSQL_* settings for source booking sync")
        safe_password = quote_plus(password or "")
        return f"mysql+pymysql://{user}:{safe_password}@{host}:{port}/{db_name}"

    def _log(self, message: str):
        print(f"[BookingSync] {message}")

    def _load_checkpoint(self) -> int:
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
        self._ensure_target_table()
        self._log(
            f"Source DB: {self.source_engine.url.host}:{self.source_engine.url.port}/{self.source_engine.url.database}"
        )
        self._log(
            f"Target DB: {self.target_engine.url.host}:{self.target_engine.url.port}/{self.target_engine.url.database}"
        )
        # 6:00 AM to 2:45 PM every 15 minutes (local time)
        self.scheduler.add_job(
            self.process_pending_bookings,
            "cron",
            hour="6-14",
            minute="0,15,30,45",
            max_instances=1,
            coalesce=True,
        )
        # 3:00 PM to 5:00 AM every 2 hours (local time)
        self.scheduler.add_job(
            self.process_pending_bookings,
            "cron",
            hour="15,17,19,21,23,1,3,5",
            minute=0,
            max_instances=1,
            coalesce=True,
        )
        self.scheduler.start()
        self._log("Scheduler started (15m/2h windows) for current-date scans")
        # Fetch current data once on startup.
        self.process_pending_bookings()

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self._log("Scheduler stopped")
        self._persist_checkpoint()

    def _ensure_target_table(self):
        ddl = text(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                bookingid BIGINT PRIMARY KEY,
                customername VARCHAR(255),
                dob DATE NULL,
                slot VARCHAR(100),
                mobile VARCHAR(50),
                isCampaingsend TINYINT(1) NOT NULL DEFAULT 0,
                isResponseSubmitted TINYINT(1) NOT NULL DEFAULT 0,
                enterdate DATETIME NULL
            )
            """
        )
        try:
            with self.target_engine.begin() as conn:
                conn.execute(ddl)
                try:
                    conn.execute(
                        text(
                            "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS isCampaingsend TINYINT(1) NOT NULL DEFAULT 0"
                        )
                    )
                except Exception as exc:
                    self._log(f"Column ensure skipped: {exc}")
                try:
                    conn.execute(
                        text(
                            "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS isResponseSubmitted TINYINT(1) NOT NULL DEFAULT 0"
                        )
                    )
                except Exception as exc:
                    self._log(f"Column ensure skipped: {exc}")
                try:
                    conn.execute(
                        text(
                            "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS enterdate DATETIME NULL"
                        )
                    )
                except Exception as exc:
                    self._log(f"Column ensure skipped: {exc}")
            self._log("Ensured target table bookings")
        except Exception as exc:
            self._log(f"Target table ensure failed: {exc}")

    def _sync_checkpoint_from_target(self):
        try:
            with self.target_engine.connect() as conn:
                result = conn.execute(text("SELECT COALESCE(MAX(bookingid), 0) AS max_id FROM bookings"))
                max_id = result.scalar() or 0
            if max_id > self.last_bookingid:
                self.last_bookingid = int(max_id)
                self._persist_checkpoint()
            self._log(f"Checkpoint synced from target: {self.last_bookingid}")
        except Exception as exc:
            self._log(f"Checkpoint sync failed: {exc}")

    def process_pending_bookings(self):
        query = text(
            """
            SELECT
                bp.id AS bookingid,
                pm.full_name AS customername,
                pm.date_of_birth AS dob,
                b.preferred_time_slot AS slot,
                pm.contact_mobile AS mobile,
                CAST(b.preferred_visit_date AS DATETIME) AS enterdate
            FROM hhome_collection_booking_patient bp
            JOIN hhome_collection_booking b
                ON b.id = bp.booking_id
            JOIN hpatient_master pm
                ON pm.id = bp.patient_id
            WHERE bp.booking_patient_status = 3
              AND b.preferred_visit_date = CURDATE()
            ORDER BY bp.id ASC
            LIMIT 500
            """
        )
        insert_stmt = text(
            """
            INSERT IGNORE INTO bookings (bookingid, customername, dob, slot, mobile, enterdate)
            VALUES (:bookingid, :customername, :dob, :slot, :mobile, :enterdate)
            """
        )
        try:
            with self.source_engine.connect() as source_conn:
                source_conn.execute(text("SELECT 1"))
                self._log("Source DB connection OK")
                rows = source_conn.execute(query).mappings().all()
            if not rows:
                self._log("No pending bookings")
                return
            self._log(f"Syncing {len(rows)} booking rows")
            with self.target_engine.begin() as target_conn:
                target_conn.execute(text("SELECT 1"))
                self._log("Target DB connection OK")
                payload = [dict(row) for row in rows]
                result = target_conn.execute(insert_stmt, payload)
                try:
                    self._log(f"Upserted rows: {result.rowcount}")
                except Exception:
                    self._log("Upsert completed")
        except Exception:
            import traceback
            self._log("Error while syncing bookings (will retry)")
            self._log(traceback.format_exc())
            return
