from fastapi import APIRouter, HTTPException

from app.schemas.ingest import IngestRequest
from app.services.ingestion import ingest_markdown

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/ingest")
def ingest(req: IngestRequest) -> dict:
    try:
        return ingest_markdown(req.path, req.owner_dept, req.visibility)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
