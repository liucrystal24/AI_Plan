import sqlite3
from pathlib import Path
from typing import Iterator

from app.core.config import get_settings


def get_conn() -> sqlite3.Connection:
    settings = get_settings()
    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            owner_dept TEXT NOT NULL,
            visibility TEXT NOT NULL,
            hash TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            doc_id TEXT NOT NULL,
            section TEXT,
            idx INTEGER NOT NULL,
            text TEXT NOT NULL,
            chunk_hash TEXT NOT NULL,
            visibility TEXT NOT NULL,
            source_ref TEXT,
            FOREIGN KEY(doc_id) REFERENCES documents(id)
        );

        CREATE TABLE IF NOT EXISTS query_logs (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            dept TEXT NOT NULL,
            role TEXT NOT NULL,
            query TEXT NOT NULL,
            retrieved_chunk_ids TEXT NOT NULL,
            cited_chunk_ids TEXT NOT NULL,
            is_refusal INTEGER NOT NULL,
            refusal_reason TEXT,
            latency_ms INTEGER NOT NULL,
            token_in INTEGER NOT NULL,
            token_out INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id TEXT PRIMARY KEY,
            query_log_id TEXT NOT NULL,
            vote TEXT NOT NULL,
            reason TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(query_log_id) REFERENCES query_logs(id)
        );
        """
    )
    conn.commit()
    conn.close()


def chunk_rows() -> Iterator[sqlite3.Row]:
    conn = get_conn()
    try:
        rows = conn.execute("SELECT * FROM chunks").fetchall()
        for row in rows:
            yield row
    finally:
        conn.close()
