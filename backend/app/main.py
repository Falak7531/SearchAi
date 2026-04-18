"""
main.py - Entry point for the FastAPI application.
Registers routers, configures CORS, and initializes the app.
"""
import time

_t0 = time.perf_counter()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import search, health
from app.core.config import settings

# RAG router — uses lazy imports so this does NOT pull in torch/sentence-transformers.
from app.rag.api import router as rag_router

app = FastAPI(
    title="AI E-Commerce Search API",
    description="Hybrid semantic + keyword search engine for e-commerce products.",
    version="1.0.0",
)

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(rag_router, prefix="/rag", tags=["RAG"])


@app.on_event("startup")
async def startup_event():
    """Run initialization tasks on startup (e.g., load FAISS index)."""
    elapsed = time.perf_counter() - _t0
    print(f"🚀 AI E-Commerce Search API is ready  (cold-start: {elapsed:.1f}s)")
    print(f"   CORS origins: {settings.ALLOWED_ORIGINS}")
    print(f"   PORT: binding via uvicorn CLI")
