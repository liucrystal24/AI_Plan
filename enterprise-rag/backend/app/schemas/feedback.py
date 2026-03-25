from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    query_log_id: str
    vote: str
    reason: str | None = None
