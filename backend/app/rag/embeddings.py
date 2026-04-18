"""Embeddings facade — re-exports the canonical :class:`EmbeddingClient`.

The implementation lives in :mod:`app.rag.ingestion.embedder` because it is
shared by both ingestion and query-time retrieval. This module provides a
flat, top-level import path so callers can write::

    from app.rag.embeddings import EmbeddingClient
"""

from __future__ import annotations

from app.rag.ingestion.embedder import EmbeddingClient

__all__ = ["EmbeddingClient"]
