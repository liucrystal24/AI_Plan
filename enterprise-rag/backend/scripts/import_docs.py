import argparse
from pathlib import Path

from app.repositories.db import init_db
from app.services.ingestion import ingest_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Import markdown docs into RAG index")
    parser.add_argument("--path", required=True, help="Markdown file or directory path")
    parser.add_argument("--owner-dept", default="public")
    parser.add_argument("--visibility", default="employee:all")
    args = parser.parse_args()

    init_db()

    p = Path(args.path)
    targets = [p] if p.is_file() else list(p.rglob("*.md"))
    if not targets:
        print("No markdown files found")
        return

    for file_path in targets:
        result = ingest_markdown(str(file_path), args.owner_dept, args.visibility)
        print(f"{file_path}: {result}")


if __name__ == "__main__":
    main()
