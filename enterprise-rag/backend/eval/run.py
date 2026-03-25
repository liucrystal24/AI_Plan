import argparse
import json
from pathlib import Path

from app.services.rag import ask


def main() -> None:
    parser = argparse.ArgumentParser(description="Run offline eval")
    parser.add_argument("--dataset", default="../../data/eval/eval_cases.jsonl")
    parser.add_argument("--output", default="./report.json")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    total = 0
    refusal_ok = 0
    citation_ok = 0
    permission_violation = 0
    failures = []

    for line in dataset_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        total += 1
        result = ask(
            query=case["question"],
            user_id=case.get("user_id", "eval-user"),
            role=case.get("role", "employee"),
            dept=case.get("dept", "public"),
        ).payload

        expected = case["expected_behavior"]
        if expected == "refusal" and result.is_refusal:
            refusal_ok += 1
        if expected == "answer" and (not result.is_refusal) and len(result.citations) >= 2:
            citation_ok += 1
        if expected == "permission_refusal" and (result.refusal_reason == "permission_denied"):
            refusal_ok += 1
        if expected == "permission_refusal" and not result.is_refusal:
            permission_violation += 1

        if expected == "answer" and (result.is_refusal or len(result.citations) < 2):
            failures.append({"case": case, "got": result.model_dump()})

    summary = {
        "total": total,
        "citation_rate": round(citation_ok / total, 4) if total else 0,
        "refusal_accuracy_proxy": round(refusal_ok / total, 4) if total else 0,
        "permission_violation_rate": round(permission_violation / total, 4) if total else 0,
        "failures": failures,
    }

    Path(args.output).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
