"""FastAPI router exposing RAG ingestion and query endpoints."""

from __future__ import annotations

from functools import lru_cache

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.pipeline import RAGPipeline

router = APIRouter()


class RAGIngestRequest(BaseModel):
    """Request body for ingesting external sources."""

    sources: list[str] = Field(..., min_length=1, description="List of local paths or URLs to ingest.")


class RAGQueryRequest(BaseModel):
    """Request body for querying the RAG pipeline."""

    query: str = Field(..., min_length=1, description="Natural-language user question.")
    top_k: int | None = Field(None, ge=1, le=20, description="Optional override for retrieved chunk count.")


class RAGQueryResponse(BaseModel):
    """Structured response returned by the RAG endpoint."""

    query: str
    answer: str
    reasoning_summary: str
    insufficient_context: bool
    citations: list[dict]
    retrieved_chunks: list[dict]
    telemetry: dict


@lru_cache(maxsize=1)
def get_rag_pipeline() -> RAGPipeline:
    """Create the pipeline lazily so app import does not require eager model boot."""
    return RAGPipeline()


@router.post("/ingest")
async def ingest_documents(request: RAGIngestRequest) -> dict[str, int]:
    """Ingest documents into the RAG knowledge base."""
    try:
        return await get_rag_pipeline().ingest_sources(request.sources)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG ingestion failed: {exc}") from exc


@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest) -> RAGQueryResponse:
    """Answer a question using retrieved document context and grounded generation."""
    try:
        result = await get_rag_pipeline().answer_query(request.query, top_k=request.top_k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG query failed: {exc}") from exc
    return RAGQueryResponse(**result.to_dict())
