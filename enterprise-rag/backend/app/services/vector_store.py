from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.config import Settings as ChromaSettings
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

from app.core.config import get_settings


@dataclass
class VectorRecord:
    chunk_id: str
    doc_id: str
    title: str
    section: str
    visibility: str
    source_ref: str
    text: str


def _get_collection() -> Collection:
    settings = get_settings()
    Path(settings.chroma_path).mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=settings.chroma_path,
        settings=ChromaSettings(anonymized_telemetry=False),
    )
    embedding = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])
    return client.get_or_create_collection(
        name=settings.chroma_collection,
        metadata={"hnsw:space": "cosine"},
        embedding_function=embedding,
    )


def upsert_doc_vectors(doc_id: str, records: list[VectorRecord]) -> None:
    collection = _get_collection()
    collection.delete(where={"doc_id": doc_id})

    if not records:
        return

    collection.upsert(
        ids=[r.chunk_id for r in records],
        documents=[r.text for r in records],
        metadatas=[
            {
                "doc_id": r.doc_id,
                "title": r.title,
                "section": r.section,
                "visibility": r.visibility,
                "source_ref": r.source_ref,
            }
            for r in records
        ],
    )


def query_vectors(query: str, top_k: int, where: Optional[dict] = None) -> list[dict]:
    collection = _get_collection()
    raw = collection.query(query_texts=[query], n_results=top_k, where=where)

    ids = raw.get("ids", [[]])[0]
    metadatas = raw.get("metadatas", [[]])[0]
    docs = raw.get("documents", [[]])[0]
    distances = raw.get("distances", [[]])[0]

    rows: list[dict] = []
    for idx, chunk_id in enumerate(ids):
        distance = float(distances[idx]) if idx < len(distances) else 1.0
        score = max(0.0, min(1.0, 1 - distance))
        md = metadatas[idx] if idx < len(metadatas) else {}
        text = docs[idx] if idx < len(docs) else ""
        rows.append(
            {
                "id": chunk_id,
                "doc_id": md.get("doc_id", ""),
                "title": md.get("title", ""),
                "section": md.get("section", "未命名章节"),
                "visibility": md.get("visibility", ""),
                "source_ref": md.get("source_ref", ""),
                "text": text,
                "distance": distance,
                "score": score,
            }
        )
    return rows
