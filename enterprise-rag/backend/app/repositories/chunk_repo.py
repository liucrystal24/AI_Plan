from typing import Iterable

from app.repositories.db import get_conn


def replace_chunks_for_doc(doc_id: str, rows: Iterable[dict]) -> int:
    conn = get_conn()
    conn.execute("DELETE FROM chunks WHERE doc_id=?", (doc_id,))
    count = 0
    for row in rows:
        conn.execute(
            """
            INSERT INTO chunks (id, doc_id, section, idx, text, chunk_hash, visibility, source_ref)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["doc_id"],
                row["section"],
                row["idx"],
                row["text"],
                row["chunk_hash"],
                row["visibility"],
                row["source_ref"],
            ),
        )
        count += 1
    conn.commit()
    conn.close()
    return count


def list_all_chunks() -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT c.*, d.title
        FROM chunks c
        JOIN documents d ON c.doc_id = d.id
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
