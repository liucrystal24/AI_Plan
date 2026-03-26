from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    query_log_id: str
    vote: str
    reason: Optional[str] = None
