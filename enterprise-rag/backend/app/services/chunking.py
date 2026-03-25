from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChunkConfig:
    chunk_size: int = 500
    overlap: int = 80


def split_markdown(text: str, config: ChunkConfig | None = None) -> list[tuple[str, str]]:
    cfg = config or ChunkConfig()
    lines = text.splitlines()

    sections: list[tuple[str, str]] = []
    current_title = "根章节"
    buf: list[str] = []

    for line in lines:
        if line.startswith("#"):
            if buf:
                sections.append((current_title, "\n".join(buf).strip()))
                buf = []
            current_title = line.lstrip("#").strip() or "未命名章节"
        else:
            buf.append(line)

    if buf:
        sections.append((current_title, "\n".join(buf).strip()))

    chunks: list[tuple[str, str]] = []
    for title, content in sections:
        if not content:
            continue
        start = 0
        while start < len(content):
            end = min(len(content), start + cfg.chunk_size)
            chunk_text = content[start:end].strip()
            if chunk_text:
                chunks.append((title, chunk_text))
            if end == len(content):
                break
            start = max(0, end - cfg.overlap)

    return chunks
