# AI E-Commerce Search

Production-ready hybrid AI search engine combining **semantic search** (FAISS + sentence-transformers) with **keyword search** (Elasticsearch BM25) and a **RAG pipeline** (Groq LLM) for natural language product queries.

## Architecture

```
├── frontend/          React + Vite SPA
│   ├── src/
│   │   ├── components/   SearchBar, ProductCard, Filters
│   │   ├── pages/        Home, Results
│   │   ├── hooks/        useSearch
│   │   └── services/     api.js (centralized API client)
│   └── vite.config.js
│
├── backend/           FastAPI API server
│   ├── app/
│   │   ├── api/          health, search endpoints
│   │   ├── services/     embedding, semantic, keyword, hybrid, ranking
│   │   ├── models/       Pydantic schemas (Product, Search)
│   │   ├── db/           JSON product database
│   │   ├── vectorstore/  FAISS index management
│   │   ├── rag/          Retrieval-Augmented Generation pipeline
│   │   │   ├── ingestion/   loader, chunker, embedder
│   │   │   ├── retrieval/   vector_store, bm25, hybrid
│   │   │   └── generation/  llm_client (Groq), prompt_builder
│   │   ├── core/         app config
│   │   └── utils/        preprocessing, scoring
│   ├── Procfile          deployment entry (Heroku/Render)
│   ├── runtime.txt       Python version pin
│   └── requirements.txt
│
├── data/              Product catalog (JSON)
├── scripts/           Data loading & embedding generation
├── render.yaml        Render Blueprint (backend + static frontend)
└── experiments/       Jupyter notebooks (not production)
```

## Quick Start (Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- (Optional) Groq API key for RAG features

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend proxies `/search` and `/health` to the backend at `http://127.0.0.1:8000`.

### Environment Variables
Copy `.env.example` to `.env` and set your keys:
```
GROQ_API_KEY=gsk_...      # Required for RAG features
BACKEND_PORT=8000
VITE_API_BASE_URL=http://localhost:8000
```

## Production Deployment

This project deploys as a **two-service Render Blueprint** (or any Python host: Railway, Fly.io, Heroku). No Docker required.

### Render (one-click via [render.yaml](render.yaml))
1. Push the repo to GitHub.
2. In Render → **New → Blueprint** → select the repo.
3. Set `GROQ_API_KEY` in the backend service's environment dashboard.
4. Update `ALLOWED_ORIGINS` (backend) and `VITE_API_URL` (frontend) to match your final domains.

### Manual / other platforms
**Backend** start command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
- Working directory: `backend/`
- Build: `pip install -r backend/requirements.txt`
- Health check path: `/health`
- Required env: `GROQ_API_KEY`, `ALLOWED_ORIGINS`

**Frontend** (static):
```bash
npm ci && npm run build       # produces frontend/dist
```
- Set `VITE_API_URL` at build time to your backend's public URL.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health/` | Service health check |
| POST | `/search/` | Hybrid semantic + keyword search |
| POST | `/rag/query` | RAG-powered Q&A over documents |
| POST | `/rag/ingest` | Ingest documents into RAG knowledge base |

## Tech Stack

- **Frontend**: React 18, Vite 8, React Router, Axios
- **Backend**: FastAPI, Pydantic, uvicorn
- **Search**: FAISS (semantic), Elasticsearch (keyword), sentence-transformers
- **RAG**: Groq (LLM), BM25 + FAISS hybrid retrieval, LangChain text splitters
- **Deployment**: Render / Railway / Fly.io (no Docker required)
