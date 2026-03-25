from datetime import datetime, timezone
from typing import Optional

from app.repositories.db import get_conn


def upsert_document(
    doc_id: str,
    title: str,
    source: str,
    owner_dept: str,
    visibility: str,
    content_hash: str,
) -> None:
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO documents (id, title, source, owner_dept, visibility, hash, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            source=excluded.source,
            owner_dept=excluded.owner_dept,
            visibility=excluded.visibility,
            hash=excluded.hash,
            updated_at=excluded.updated_at
        """,
        (
            doc_id,
            title,
            source,
            owner_dept,
            visibility,
            content_hash,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def get_document_hash(doc_id: str) -> Optional[str]:
    conn = get_conn()
    row = conn.execute("SELECT hash FROM documents WHERE id=?", (doc_id,)).fetchone()
    conn.close()
    return row["hash"] if row else None


def get_doc_meta(doc_id: str) -> Optional[dict]:
    conn = get_conn()
    row = conn.execute("SELECT * FROM documents WHERE id=?", (doc_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
