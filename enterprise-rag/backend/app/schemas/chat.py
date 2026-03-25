from typing import List, Optional
from pydantic import BaseModel, Field


class UserIdentity(BaseModel):
    user_id: str = Field(..., description="用户唯一标识")
    role: str = Field(default="employee")
    dept: str = Field(default="public")


class AskRequest(BaseModel):
    query: str
    user: UserIdentity
    top_k: Optional[int] = None


class Citation(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    section: str
    source_ref: str
    snippet: str
    score: float


class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]
    is_refusal: bool
    refusal_reason: Optional[str] = None
    request_id: str
