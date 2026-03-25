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
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

健康检查：`GET http://localhost:8000/health`

## 3. 导入文档

```bash
cd backend
PYTHONPATH=. python scripts/import_docs.py --path ../data/raw_docs --owner-dept finance --visibility employee:all
```

## 4. 前端启动

```bash
cd frontend
npm install
npm run dev -- --host
```

访问：`http://localhost:5173`

## 5. 跑评测

```bash
cd backend
PYTHONPATH=. python eval/run.py --dataset ../data/eval/eval_cases.jsonl --output ./eval/report.json
```

## 6. 当前实现与需求映射

- 已实现：RAG 基本闭环、引用返回、拒答输出、SSE、反馈、日志、离线评测入口。
- 待迭代：真实 Embedding + 向量库（Chroma）、混合检索/BM25、重排模型、权限拒答更精细判定、监控面板与指标落盘。

## 7. API 概览

- `POST /admin/ingest` 导入单个 markdown
- `POST /chat/ask` 同步问答
- `POST /chat/ask/stream` 流式问答
- `POST /feedback` 反馈提交
- `GET /health` 健康检查
