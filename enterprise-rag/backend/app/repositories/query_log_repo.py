import json
from datetime import datetime, timezone

from app.repositories.db import get_conn


def insert_query_log(payload: dict) -> None:
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO query_logs (
            id, user_id, dept, role, query, retrieved_chunk_ids, cited_chunk_ids,
            is_refusal, refusal_reason, latency_ms, token_in, token_out, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload["id"],
            payload["user_id"],
            payload["dept"],
            payload["role"],
            payload["query"],
            json.dumps(payload["retrieved_chunk_ids"], ensure_ascii=False),
            json.dumps(payload["cited_chunk_ids"], ensure_ascii=False),
            1 if payload["is_refusal"] else 0,
            payload.get("refusal_reason"),
            payload["latency_ms"],
            payload["token_in"],
            payload["token_out"],
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()
