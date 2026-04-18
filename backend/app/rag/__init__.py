"""Lazy public API — heavy imports only happen when symbols are first used."""
from __future__ import annotations

import importlib
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover – only for type checkers / IDEs
    from app.rag.embeddings import EmbeddingClient as EmbeddingClient
    from app.rag.pipeline import RAGPipeline as RAGPipeline
    from app.rag.ranker import Ranker as Ranker
    from app.rag.retriever import Retriever as Retriever
    from app.rag.types import (
        Citation as Citation,
        EvaluationSample as EvaluationSample,
        PipelineTelemetry as PipelineTelemetry,
        RAGQueryResult as RAGQueryResult,
        RetrievedChunk as RetrievedChunk,
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

# ── Lazy attribute access ─────────────────────────────────────
_LAZY_MAP: dict[str, tuple[str, str]] = {
    "RAGPipeline":       ("app.rag.pipeline",    "RAGPipeline"),
    "EmbeddingClient":   ("app.rag.embeddings",  "EmbeddingClient"),
    "Retriever":         ("app.rag.retriever",   "Retriever"),
    "Ranker":            ("app.rag.ranker",      "Ranker"),
    "RetrievedChunk":    ("app.rag.types",       "RetrievedChunk"),
    "RAGQueryResult":    ("app.rag.types",       "RAGQueryResult"),
    "Citation":          ("app.rag.types",       "Citation"),
    "EvaluationSample":  ("app.rag.types",       "EvaluationSample"),
    "PipelineTelemetry": ("app.rag.types",       "PipelineTelemetry"),
}


def __getattr__(name: str):
    if name in _LAZY_MAP:
        mod_path, attr = _LAZY_MAP[name]
        mod = importlib.import_module(mod_path)
        val = getattr(mod, attr)
        globals()[name] = val  # cache so __getattr__ is called only once
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


@lru_cache(maxsize=1)
def get_pipeline():
    """Return a cached singleton RAGPipeline instance (lazy)."""
    from app.rag.pipeline import RAGPipeline  # noqa: F811
    return RAGPipeline()


async def search(query: str, top_k: int | None = None):
    """High-level entry: query -> RAGQueryResult. Heavy imports only on first call."""
    return await get_pipeline().answer_query(query, top_k=top_k)

