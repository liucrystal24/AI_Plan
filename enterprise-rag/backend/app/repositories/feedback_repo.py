from datetime import datetime, timezone
import uuid

from app.repositories.db import get_conn


def add_feedback(query_log_id: str, vote: str, reason: str | None = None) -> str:
    feedback_id = str(uuid.uuid4())
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO feedback (id, query_log_id, vote, reason, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            feedback_id,
            query_log_id,
            vote,
            reason,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()
    return feedback_id
