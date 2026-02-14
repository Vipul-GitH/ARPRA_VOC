from app.database import SessionLocal
from app.models.feedback import FeedbackResponse
from app.models import CampaignQuestion


def main():
    session = SessionLocal()
    resp = session.get(FeedbackResponse, 144)
    if not resp:
        print("Response 144 not found")
        return
    qids = [a.campaign_question_id for a in resp.answers]
    questions = {
        q.id: q
        for q in session.query(CampaignQuestion)
        .filter(CampaignQuestion.id.in_(qids))
        .all()
    }
    for ans in resp.answers:
        q = questions.get(ans.campaign_question_id)
        qtext = (q.question_text_en or q.question_text or "") if q else ""
        optmap = {
            str(opt.option_value): (opt.option_text_en or opt.option_text_hi or "")
            for opt in (q.options or [])
        } if q else {}
        if ans.answer_text:
            val = ans.answer_text
        else:
            labels = [
                optmap.get(str(v), str(v)) for v in (ans.selected_option_values or [])
            ]
            val = ", ".join(labels)
        print(f"Q{ans.campaign_question_id}: {qtext}\n  -> {val}")


if __name__ == "__main__":
    main()
