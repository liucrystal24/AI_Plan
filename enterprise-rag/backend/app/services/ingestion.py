from __future__ import annotations

import hashlib
import uuid
from pathlib import Path

from app.repositories.chunk_repo import replace_chunks_for_doc
from app.repositories.document_repo import get_document_hash, upsert_document
from app.services.chunking import split_markdown
from app.services.vector_store import VectorRecord, upsert_doc_vectors


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def ingest_markdown(path: str, owner_dept: str, visibility: str) -> dict:
    p = Path(path)
    if not p.exists() or p.suffix.lower() != ".md":
        raise ValueError("仅支持存在的 .md 文件")

    content = p.read_text(encoding="utf-8")
    content_hash = _sha256(content)
    doc_id = _sha256(str(p.resolve()))[:16]

    old_hash = get_document_hash(doc_id)
    if old_hash == content_hash:
        return {"doc_id": doc_id, "status": "skipped", "chunks": 0}

    upsert_document(
        doc_id=doc_id,
        title=p.stem,
        source=str(p.resolve()),
        owner_dept=owner_dept,
        visibility=visibility,
        content_hash=content_hash,
    )

    rows = []
    vector_rows: list[VectorRecord] = []
    for idx, (section, text) in enumerate(split_markdown(content)):
        chunk_id = str(uuid.uuid4())
        chunk_hash = _sha256(f"{doc_id}:{idx}:{text}")
        source_ref = f"{p.resolve()}#chunk-{idx}"
        rows.append(
            {
                "id": chunk_id,
                "doc_id": doc_id,
                "section": section,
                "idx": idx,
                "text": text,
                "chunk_hash": chunk_hash,
                "visibility": visibility,
                "source_ref": source_ref,
            }
        )
        vector_rows.append(
            VectorRecord(
                chunk_id=chunk_id,
                doc_id=doc_id,
                title=p.stem,
                section=section,
                visibility=visibility,
                source_ref=source_ref,
                text=text,
            )
        )

    chunk_count = replace_chunks_for_doc(doc_id, rows)
    upsert_doc_vectors(doc_id, vector_rows)
    return {"doc_id": doc_id, "status": "indexed", "chunks": chunk_count}
