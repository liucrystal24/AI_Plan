import json

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from app.schemas.chat import AskRequest
from app.services.rag import ask

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask")
def ask_sync(req: AskRequest) -> dict:
    result = ask(
        query=req.query,
        user_id=req.user.user_id,
        role=req.user.role,
        dept=req.user.dept,
        top_k=req.top_k,
    )
    return result.payload.model_dump()


@router.post("/ask/stream")
def ask_stream(req: AskRequest) -> EventSourceResponse:
    result = ask(
        query=req.query,
        user_id=req.user.user_id,
        role=req.user.role,
        dept=req.user.dept,
        top_k=req.top_k,
    )

    async def event_gen():
        text = result.payload.answer
        for idx, segment in enumerate([text[i : i + 40] for i in range(0, len(text), 40)]):
            yield {
                "event": "token",
                "id": str(idx),
                "data": json.dumps({"text": segment}, ensure_ascii=False),
            }

        yield {
            "event": "final",
            "data": json.dumps(result.payload.model_dump(), ensure_ascii=False),
        }

    return EventSourceResponse(event_gen())
