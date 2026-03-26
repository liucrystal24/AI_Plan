from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.schemas.chat import UserIdentity
from app.services.permissions import can_access
from app.services.vector_store import query_vectors


@dataclass
class RetrievalResult:
    visible_hits: list[dict]
    has_hidden_relevant_hits: bool
    visible_top_score: float
    hidden_top_score: float


def _visible_filter(user: UserIdentity) -> Optional[dict]:
    if user.role == "admin":
        return None
    allowed = ["employee:all", f"employee:dept:{user.dept}"]
    return {"visibility": {"$in": allowed}}


def retrieve(query: str, user: UserIdentity, top_k: int, min_score: float) -> RetrievalResult:
    visible_hits = query_vectors(query=query, top_k=top_k, where=_visible_filter(user))
    all_hits = query_vectors(query=query, top_k=max(10, top_k * 3), where=None)

    visible_top = max([hit.get("score", 0.0) for hit in visible_hits], default=0.0)
    hidden_scores = [
        hit.get("score", 0.0)
        for hit in all_hits
        if not can_access(hit.get("visibility", ""), user)
    ]
    hidden_top = max(hidden_scores, default=0.0)

    hidden_relevant = any(
        (not can_access(hit.get("visibility", ""), user)) and hit.get("score", 0.0) >= min_score
        for hit in all_hits
    )

    return RetrievalResult(
        visible_hits=visible_hits,
        has_hidden_relevant_hits=hidden_relevant,
        visible_top_score=visible_top,
        hidden_top_score=hidden_top,
    )
