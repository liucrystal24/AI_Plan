from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Optional
import uuid

from app.core.config import get_settings
from app.core.security import is_prompt_injection_risk
from app.repositories.query_log_repo import insert_query_log
from app.schemas.chat import AskResponse, Citation, UserIdentity
from app.services.retrieval import retrieve


@dataclass
class RagResult:
    payload: AskResponse
    retrieved_ids: list[str]


def _build_refusal(reason: str, request_id: str) -> AskResponse:
    suggestions = {
        "evidence_insufficient": "建议补充关键词、时间范围或系统名；如仍无结果可提交工单补充文档。",
        "permission_denied": "当前账号权限不足，请联系管理员申请可见范围。",
        "prompt_injection_risk": "问题包含高风险指令，请改为业务问题并聚焦文档内容。",
    }
    return AskResponse(
        answer=f"无法基于当前知识库回答：{reason}。{suggestions.get(reason, '')}",
        citations=[],
        is_refusal=True,
        refusal_reason=reason,
        request_id=request_id,
    )


def ask(query: str, user_id: str, role: str, dept: str, top_k: Optional[int] = None) -> RagResult:
    started = perf_counter()
    settings = get_settings()
    request_id = str(uuid.uuid4())
    k = top_k or settings.default_top_k

    if is_prompt_injection_risk(query):
        response = _build_refusal("prompt_injection_risk", request_id)
        _write_log(response, query, user_id, role, dept, [], started)
        return RagResult(payload=response, retrieved_ids=[])

    user = UserIdentity(user_id=user_id, role=role, dept=dept)
    retrieval = retrieve(query=query, user=user, top_k=k, min_score=settings.min_evidence_score)
    results = retrieval.visible_hits

    hidden_is_dominant = (
        retrieval.hidden_top_score >= settings.min_evidence_score
        and retrieval.hidden_top_score > (retrieval.visible_top_score + 0.05)
    )
    if hidden_is_dominant:
        response = _build_refusal("permission_denied", request_id)
        _write_log(response, query, user_id, role, dept, [r["id"] for r in results], started)
        return RagResult(payload=response, retrieved_ids=[r["id"] for r in results])

    if len(results) < 2 or (results and results[0]["score"] < settings.min_evidence_score):
        reason = "permission_denied" if retrieval.has_hidden_relevant_hits else "evidence_insufficient"
        response = _build_refusal(reason, request_id)
        _write_log(response, query, user_id, role, dept, [r["id"] for r in results], started)
        return RagResult(payload=response, retrieved_ids=[r["id"] for r in results])

    citations = [
        Citation(
            chunk_id=r["id"],
            doc_id=r["doc_id"],
            title=r["title"],
            section=r["section"] or "未命名章节",
            source_ref=r["source_ref"] or "",
            snippet=r["text"][:220],
            score=round(r["score"], 4),
        )
        for r in results[: max(2, min(len(results), settings.max_context_chunks))]
    ]

    answer = _render_answer(query, citations)
    response = AskResponse(
        answer=answer,
        citations=citations,
        is_refusal=False,
        refusal_reason=None,
        request_id=request_id,
    )
    _write_log(response, query, user_id, role, dept, [r["id"] for r in results], started)
    return RagResult(payload=response, retrieved_ids=[r["id"] for r in results])


def _render_answer(query: str, citations: list[Citation]) -> str:
    key_points = "\n".join([f"- {c.title} / {c.section}: {c.snippet[:80]}..." for c in citations[:3]])
    return (
        f"结论：基于检索到的文档，问题“{query}”可由以下证据支撑。\n"
        f"关键依据：\n{key_points}\n"
        "如需精确条款，请打开引用来源查看完整原文。"
    )


def _write_log(
    response: AskResponse,
    query: str,
    user_id: str,
    role: str,
    dept: str,
    retrieved_ids: list[str],
    started: float,
) -> None:
    latency_ms = int((perf_counter() - started) * 1000)
    insert_query_log(
        {
            "id": response.request_id,
            "user_id": user_id,
            "dept": dept,
            "role": role,
            "query": query,
            "retrieved_chunk_ids": retrieved_ids,
            "cited_chunk_ids": [c.chunk_id for c in response.citations],
            "is_refusal": response.is_refusal,
            "refusal_reason": response.refusal_reason,
            "latency_ms": latency_ms,
            "token_in": max(1, len(query) // 4),
            "token_out": max(1, len(response.answer) // 4),
        }
    )
