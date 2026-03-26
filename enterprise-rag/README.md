# Enterprise Knowledge RAG QA (V1 Scaffold)

基于需求文档搭建的项目起始版本，目标是先跑通：
- 文档导入与增量索引（Markdown）
- 权限过滤检索
- 问答输出 + 引用列表 + 拒答
- SSE 流式输出
- 反馈采集与审计日志
- 离线评测脚本

## 1. 目录结构

```text
enterprise-rag/
  backend/        # FastAPI + RAG pipeline
  frontend/       # Vue3 + Vite 问答页
  data/
    raw_docs/     # 原始知识文档
    eval/         # 回归评测数据
  deploy/         # Docker Compose
```

## 2. 后端启动

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
DB_PATH=$(pwd)/rag.db CHROMA_PATH=$(pwd)/chroma_db uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

健康检查：`GET http://localhost:8000/health`

## 3. 导入文档

```bash
cd backend
PYTHONPATH=. .venv/bin/python scripts/import_docs.py --path ../data/raw_docs --owner-dept finance --visibility employee:all

# 示例：导入部门私有文档，用于权限拒答测试
PYTHONPATH=. .venv/bin/python scripts/import_docs.py --path ../data/raw_docs/B部门私密手册.md --owner-dept dept-b --visibility employee:dept:dept-b
```

## 4. 前端启动

```bash
cd frontend
corepack enable
pnpm install
pnpm run dev -- --host
```

访问：`http://localhost:5173`

## 5. 跑评测

```bash
cd backend
PYTHONPATH=. .venv/bin/python eval/run.py --dataset ../data/eval/eval_cases.jsonl --output ./eval/report.json
```

门禁默认阈值：
- 引用率 >= 0.95
- 拒答准确率 >= 0.90
- 越权率 <= 0.0

## 6. 当前实现与需求映射

- 已实现：真实 Embedding + Chroma 向量检索、权限预过滤检索、权限拒答精判、引用返回、拒答输出、SSE、反馈、日志、离线评测门禁。
- 待迭代：混合检索/BM25、重排模型、可观测性面板与指标落盘、缓存与限流。

## 7. API 概览

- `POST /admin/ingest` 导入单个 markdown
- `POST /chat/ask` 同步问答
- `POST /chat/ask/stream` 流式问答
- `POST /feedback` 反馈提交
- `GET /health` 健康检查
