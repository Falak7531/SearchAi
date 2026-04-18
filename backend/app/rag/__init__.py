"""
RAG (Retrieval-Augmented Generation) package.

Single source of truth for all RAG logic. Provides a clean public API:

    from app.rag import (
        RAGPipeline,        # Full async pipeline (ingest, retrieve, generate)
        EmbeddingClient,    # Sentence-transformer embeddings
        Retriever,          # Hybrid (vector + BM25) retrieval
        Ranker,             # Re-ranking with business signals
        get_pipeline,       # Cached singleton accessor
        search,             # High-level async entry point: query -> answer
    )

Package layout:

    rag/
    ├── __init__.py        # Public API (this file)
    ├── embeddings.py      # Facade: EmbeddingClient
    ├── retriever.py       # Facade: Retriever (HybridRetriever + components)
    ├── ranker.py          # Facade: Ranker (re-ranking helpers)
    ├── utils.py           # Shared helpers (timing, formatting)
    ├── pipeline.py        # RAGPipeline orchestrator
    ├── api.py             # FastAPI router (mounted at /rag)
    ├── config.py          # YAML-backed settings
    ├── config.yaml        # Pipeline configuration
    ├── evaluation.py      # RAGAS evaluation
    ├── types.py           # Dataclasses
    ├── ingestion/         # loader, chunker, embedder
    ├── retrieval/         # vector_store, bm25_retriever, hybrid
    └── generation/        # llm_client, prompt_builder
"""

from __future__ import annotations

from functools import lru_cache

from app.rag.embeddings import EmbeddingClient
from app.rag.pipeline import RAGPipeline
from app.rag.ranker import Ranker
from app.rag.retriever import Retriever
from app.rag.types import (
    Citation,
    EvaluationSample,
    PipelineTelemetry,
    RAGQueryResult,
    RetrievedChunk,
)

__all__ = [
    "RAGPipeline",
    "EmbeddingClient",
    "Retriever",
    "Ranker",
    "RetrievedChunk",
    "RAGQueryResult",
    "Citation",
    "EvaluationSample",
    "PipelineTelemetry",
    "get_pipeline",
    "search",
]


@lru_cache(maxsize=1)
def get_pipeline() -> RAGPipeline:
    """Return a cached singleton :class:`RAGPipeline` instance."""
    return RAGPipeline()


async def search(query: str, top_k: int | None = None) -> RAGQueryResult:
    """High-level entry point: run the RAG pipeline for a natural-language query.

    Args:
        query: The user's natural-language question.
        top_k: Optional override for retrieved chunk count.

    Returns:
        A :class:`RAGQueryResult` with answer, citations, and telemetry.
    """
    return await get_pipeline().answer_query(query, top_k=top_k)

