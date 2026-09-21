from __future__ import annotations

import os
import socket
import uuid
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.database import engine


IST = ZoneInfo("Asia/Kolkata")
daily_summary_scheduler: BackgroundScheduler | None = None
SCHEDULER_LOCK_NAME = "daily_summary_scheduler"
SCHEDULER_LOCK_TTL_SECONDS = 180
RUN_LOCK_TTL_MINUTES = 30
_scheduler_owner_token = f"{socket.gethostname()}:{os.getpid()}:{uuid.uuid4()}"


def _utc_day_bounds(report_date: date) -> tuple[datetime, datetime]:
    start_ist = datetime.combine(report_date, time.min, tzinfo=IST)
    end_ist = start_ist + timedelta(days=1)
    return (
        start_ist.astimezone(timezone.utc).replace(tzinfo=None),
        end_ist.astimezone(timezone.utc).replace(tzinfo=None),
    )


def collect_daily_summary(report_date: date | None = None) -> dict[str, int | float | date]:
    report_date = report_date or datetime.now(IST).date()
    start_utc, end_utc = _utc_day_bounds(report_date)
    next_date = report_date + timedelta(days=1)

    with engine.connect() as conn:
        campaign_sent = conn.execute(
            text(
                """
                SELECT COUNT(*)
                FROM bookings
                WHERE isCampaingsend = 1
                  AND enterdate >= :report_date
                  AND enterdate < :next_date
                """
            ),
            {"report_date": report_date, "next_date": next_date},
        ).scalar() or 0
        responses = conn.execute(
            text(
                """
                SELECT
                    COUNT(*) AS received,
                    SUM(CASE WHEN needs_manual_review = 1 THEN 1 ELSE 0 END) AS manual_review,
                    SUM(CASE WHEN LOWER(COALESCE(overall_sentiment, '')) = 'neutral' THEN 1 ELSE 0 END) AS neutral
                FROM feedback_responses
                WHERE submission_time >= :start_utc AND submission_time < :end_utc
                """
            ),
            {"start_utc": start_utc, "end_utc": end_utc},
        ).mappings().one()
        tickets = conn.execute(
            text(
                """
                SELECT
                    SUM(CASE WHEN created_at >= :start_utc AND created_at < :end_utc THEN 1 ELSE 0 END) AS created_today,
                    SUM(CASE WHEN closed_at >= :start_utc AND closed_at < :end_utc THEN 1 ELSE 0 END) AS closed_today,
                    SUM(CASE WHEN status IN ('open', 'in_progress') THEN 1 ELSE 0 END) AS open_overall
                FROM feedback_tickets
                """
            ),
            {"start_utc": start_utc, "end_utc": end_utc},
        ).mappings().one()

    received = int(responses["received"] or 0)
    sent = int(campaign_sent)
    return {
        "report_date": report_date,
        "campaign_sent": sent,
        "responses_received": received,
        "manual_review": int(responses["manual_review"] or 0),
        "neutral_responses": int(responses["neutral"] or 0),
        "tickets_created": int(tickets["created_today"] or 0),
        "tickets_closed": int(tickets["closed_today"] or 0),
        "open_tickets": int(tickets["open_overall"] or 0),
        "response_rate": round((received / sent * 100), 1) if sent else 0.0,
    }


def format_daily_summary(summary: dict[str, int | float | date]) -> str:
    report_date = summary["report_date"]
    return (
        "ARPRA VoC - Daily Summary\n"
        f"Date: {report_date.strftime('%d %b %Y')}\n\n"
        "Today's Activity\n"
        f"Campaign Messages Sent: {summary['campaign_sent']}\n"
        f"Responses Received: {summary['responses_received']}\n"
        f"Manual Review Required: {summary['manual_review']}\n"
        f"Neutral Responses: {summary['neutral_responses']}\n\n"
        "Ticket Activity\n"
        f"Tickets Created Today: {summary['tickets_created']}\n"
        f"Tickets Closed Today: {summary['tickets_closed']}\n"
        f"Open Tickets Overall: {summary['open_tickets']}\n\n"
        f"Response Rate: {summary['response_rate']:.1f}%\n\n"
        f"Report generated at: {datetime.now(IST).strftime('%I:%M %p')}"
    )


def _normalize_target(raw: str) -> str:
    digits = "".join(character for character in raw if character.isdigit())
    if len(digits) == 10:
        return f"91{digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return digits
    return ""


def _claim_scheduler_lock() -> bool:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO scheduler_locks (lock_name, owner_token, expires_at, updated_at)
                VALUES (:lock_name, :owner_token, DATE_ADD(UTC_TIMESTAMP(), INTERVAL :ttl SECOND), UTC_TIMESTAMP())
                ON DUPLICATE KEY UPDATE
                    owner_token = IF(expires_at < UTC_TIMESTAMP() OR owner_token = VALUES(owner_token), VALUES(owner_token), owner_token),
                    expires_at = IF(expires_at < UTC_TIMESTAMP() OR owner_token = VALUES(owner_token), VALUES(expires_at), expires_at),
                    updated_at = IF(expires_at < UTC_TIMESTAMP() OR owner_token = VALUES(owner_token), UTC_TIMESTAMP(), updated_at)
                """
            ),
            {
                "lock_name": SCHEDULER_LOCK_NAME,
                "owner_token": _scheduler_owner_token,
                "ttl": SCHEDULER_LOCK_TTL_SECONDS,
            },
        )
        owner = conn.execute(
            text("SELECT owner_token FROM scheduler_locks WHERE lock_name = :lock_name"),
            {"lock_name": SCHEDULER_LOCK_NAME},
        ).scalar()
    return owner == _scheduler_owner_token


def _refresh_scheduler_lock() -> None:
    with engine.begin() as conn:
        updated = conn.execute(
            text(
                """
                UPDATE scheduler_locks
                SET expires_at = DATE_ADD(UTC_TIMESTAMP(), INTERVAL :ttl SECOND),
                    updated_at = UTC_TIMESTAMP()
                WHERE lock_name = :lock_name AND owner_token = :owner_token
                """
            ),
            {
                "lock_name": SCHEDULER_LOCK_NAME,
                "owner_token": _scheduler_owner_token,
                "ttl": SCHEDULER_LOCK_TTL_SECONDS,
            },
        ).rowcount
    if not updated:
        raise RuntimeError("Daily summary scheduler lock was lost")


def _release_scheduler_lock() -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                DELETE FROM scheduler_locks
                WHERE lock_name = :lock_name AND owner_token = :owner_token
                """
            ),
            {"lock_name": SCHEDULER_LOCK_NAME, "owner_token": _scheduler_owner_token},
        )


def _claim_report_run(report_date: date) -> bool:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO daily_summary_runs (report_date, status, owner_token, locked_until, created_at, updated_at)
                VALUES (:report_date, 'running', :owner_token, DATE_ADD(UTC_TIMESTAMP(), INTERVAL :ttl MINUTE), UTC_TIMESTAMP(), UTC_TIMESTAMP())
                ON DUPLICATE KEY UPDATE
                    owner_token = IF(status <> 'sent' AND locked_until < UTC_TIMESTAMP(), VALUES(owner_token), owner_token),
                    locked_until = IF(status <> 'sent' AND locked_until < UTC_TIMESTAMP(), VALUES(locked_until), locked_until),
                    status = IF(status <> 'sent' AND locked_until < UTC_TIMESTAMP(), 'running', status),
                    error_message = IF(status <> 'sent' AND locked_until < UTC_TIMESTAMP(), NULL, error_message),
                    updated_at = IF(status <> 'sent' AND locked_until < UTC_TIMESTAMP(), UTC_TIMESTAMP(), updated_at)
                """
            ),
            {
                "report_date": report_date,
                "owner_token": _scheduler_owner_token,
                "ttl": RUN_LOCK_TTL_MINUTES,
            },
        )
        owner = conn.execute(
            text(
                """
                SELECT owner_token
                FROM daily_summary_runs
                WHERE report_date = :report_date AND status = 'running'
                """
            ),
            {"report_date": report_date},
        ).scalar()
    return owner == _scheduler_owner_token


def _finish_report_run(report_date: date, message: str) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                UPDATE daily_summary_runs
                SET status = 'sent',
                    sent_at = UTC_TIMESTAMP(),
                    message_snapshot = :message,
                    locked_until = NULL,
                    error_message = NULL,
                    updated_at = UTC_TIMESTAMP()
                WHERE report_date = :report_date AND owner_token = :owner_token
                """
            ),
            {
                "report_date": report_date,
                "owner_token": _scheduler_owner_token,
                "message": message,
            },
        )


def _fail_report_run(report_date: date, error_message: str) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                UPDATE daily_summary_runs
                SET status = 'failed',
                    locked_until = NULL,
                    error_message = :error_message,
                    updated_at = UTC_TIMESTAMP()
                WHERE report_date = :report_date AND owner_token = :owner_token
                """
            ),
            {
                "report_date": report_date,
                "owner_token": _scheduler_owner_token,
                "error_message": error_message[:1000],
            },
        )


def send_daily_summary(report_date: date | None = None) -> dict[str, object]:
    settings = get_settings()
    report_date = report_date or datetime.now(IST).date()
    if not _claim_report_run(report_date):
        print(f"[DailySummary] report for {report_date} already claimed or sent; skipping")
        return {"skipped": True, "report_date": report_date}
    try:
        summary = collect_daily_summary(report_date)
        message = format_daily_summary(summary)
        recipients = [
            target
            for raw in settings.daily_summary_recipients.split(",")
            if (target := _normalize_target(raw.strip()))
        ]
        if not recipients:
            raise RuntimeError("No valid DAILY_SUMMARY_RECIPIENTS configured")

        results = []
        with requests.Session() as http:
            for target in recipients:
                response = http.post(
                    settings.daily_summary_api_url,
                    json={
                        "accountId": settings.daily_summary_account_id,
                        "target": target,
                        "message": message,
                    },
                    timeout=15,
                )
                results.append({"target": target, "status_code": response.status_code})
                response.raise_for_status()
        _finish_report_run(report_date, message)
        print(f"[DailySummary] sent report for {summary['report_date']} to {len(results)} recipient(s)")
        return {"summary": summary, "message": message, "results": results}
    except Exception as exc:
        _fail_report_run(report_date, str(exc))
        raise


def start_daily_summary_scheduler():
    global daily_summary_scheduler
    if daily_summary_scheduler and daily_summary_scheduler.running:
        return
    try:
        if not _claim_scheduler_lock():
            print("[DailySummary] scheduler lock is held by another process; skipping local scheduler")
            return
    except SQLAlchemyError as exc:
        print(f"[DailySummary] scheduler lock could not be acquired: {exc}")
        raise
    daily_summary_scheduler = BackgroundScheduler(timezone=IST)
    daily_summary_scheduler.add_job(
        _refresh_scheduler_lock,
        "interval",
        seconds=60,
        id="daily_voc_summary_lock_heartbeat",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    daily_summary_scheduler.add_job(
        send_daily_summary,
        "cron",
        hour=23,
        minute=59,
        id="daily_voc_summary",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=3600,
    )
    daily_summary_scheduler.start()
    print("[DailySummary] scheduler started for 11:59 PM Asia/Kolkata")


def stop_daily_summary_scheduler():
    global daily_summary_scheduler
    if daily_summary_scheduler and daily_summary_scheduler.running:
        daily_summary_scheduler.shutdown(wait=False)
    _release_scheduler_lock()
    daily_summary_scheduler = None
