.PHONY: backend-install backend-run frontend-install frontend-run ingest eval

backend-install:
	cd backend && pip install -r requirements.txt

backend-run:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend-install:
	cd frontend && npm install

frontend-run:
	cd frontend && npm run dev -- --host

ingest:
	cd backend && PYTHONPATH=. python scripts/import_docs.py --path ../data/raw_docs --owner-dept finance --visibility employee:all

eval:
	cd backend && PYTHONPATH=. python eval/run.py --dataset ../data/eval/eval_cases.jsonl --output ./eval/report.json
