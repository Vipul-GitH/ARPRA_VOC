from __future__ import annotations

import json
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

from app.config import get_settings
from app.database import SessionLocal
from app.models import FeedbackAnswer, FeedbackResponse
from app.services.feedback import compute_scores, create_ticket_if_needed


def _parse_selected_values(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(v) for v in raw]
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
            return [str(parsed)]
        except Exception:
            if "," in raw:
                return [v.strip() for v in raw.split(",") if v.strip()]
            return [raw]
    return [str(raw)]


def main():
    settings = get_settings()
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    SessionLocal.configure(bind=engine)
    db: Session = SessionLocal()
    try:
        responses = (
            db.query(FeedbackResponse)
            .options(
                joinedload(FeedbackResponse.answers).joinedload(FeedbackAnswer.question).joinedload("options")
            )
            .all()
        )
        for response in responses:
            for ans in response.answers:
                values = _parse_selected_values(ans.selected_option_values)
                if not values or not ans.question or not ans.question.options:
                    continue
                # pick first matched option (or leave as is if not found)
                for opt in ans.question.options:
                    if str(opt.option_value) in values:
                        ans.sentiment = opt.sentiment
                        break
            compute_scores(response, response.answers)
            # if ticket should exist, ensure it
            create_ticket_if_needed(db, response)
        db.commit()
        print(f"Recomputed sentiments for {len(responses)} responses")
    finally:
        db.close()


if __name__ == "__main__":
    main()
