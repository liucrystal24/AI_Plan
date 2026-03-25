from __future__ import annotations

from collections import Counter
from math import sqrt

from app.repositories.chunk_repo import list_all_chunks
from app.schemas.chat import UserIdentity
from app.services.permissions import can_access


def _tokenize(text: str) -> list[str]:
    return [t for t in text.lower().replace("\n", " ").split(" ") if t]


def _cosine_similarity(a: Counter, b: Counter) -> float:
    common = set(a.keys()) & set(b.keys())
    dot = sum(a[k] * b[k] for k in common)
    na = sqrt(sum(v * v for v in a.values()))
    nb = sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def retrieve(query: str, user: UserIdentity, top_k: int) -> list[dict]:
    query_vec = Counter(_tokenize(query))
    candidates = []

    for row in list_all_chunks():
        if not can_access(row["visibility"], user):
            continue
        score = _cosine_similarity(query_vec, Counter(_tokenize(row["text"])))
        if score > 0:
            row = dict(row)
            row["score"] = score
            candidates.append(row)

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:top_k]
