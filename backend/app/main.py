"""
main.py - Entry point for the FastAPI application.
Registers routers, configures CORS, and initializes the app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import search, health
from app.core.config import settings
from app.rag import api as rag_api

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
app.include_router(rag_api.router, prefix="/rag", tags=["RAG"])


@app.on_event("startup")
async def startup_event():
    """Run initialization tasks on startup (e.g., load FAISS index)."""
    print("🚀 AI E-Commerce Search API is starting up...")
