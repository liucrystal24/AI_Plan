from fastapi import APIRouter, HTTPException

from app.repositories.feedback_repo import add_feedback
from app.schemas.feedback import FeedbackRequest

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("")
def submit_feedback(req: FeedbackRequest) -> dict:
    if req.vote not in {"useful", "not_useful"}:
        raise HTTPException(status_code=400, detail="vote must be useful or not_useful")
    feedback_id = add_feedback(req.query_log_id, req.vote, req.reason)
    return {"feedback_id": feedback_id}
