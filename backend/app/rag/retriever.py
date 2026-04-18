"""Retriever facade — exposes a single :class:`Retriever` entry point.

Wraps the underlying :class:`HybridRetriever` (vector + BM25 with RRF fusion)
behind a clean, query-string-friendly API. Callers should not need to import
from :mod:`app.rag.retrieval` directly.

Usage::

    from app.rag import Retriever
    retriever = Retriever()
    chunks = await retriever.search("wireless headphones", top_k=10)
"""

from __future__ import annotations

from app.rag.config import RAGConfig, get_rag_config
from app.rag.embeddings import EmbeddingClient
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.hybrid import HybridRetriever
from app.rag.retrieval.vector_store import VectorStore
from app.rag.types import RetrievedChunk

__all__ = ["Retriever", "HybridRetriever", "VectorStore", "BM25Retriever"]


class Retriever:
    """High-level hybrid retriever combining semantic + keyword search."""

    def __init__(self, config: RAGConfig | None = None):
        """Build the retriever with the shared YAML config (or a custom one)."""
        self.config = config or get_rag_config()
        self.embedder = EmbeddingClient(self.config)
        self.vector_store = VectorStore(self.config)
        self.bm25 = BM25Retriever()
        self.bm25.rebuild(self.vector_store.list_chunks())
        self.hybrid = HybridRetriever(self.config, self.vector_store, self.bm25)

    async def search(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        """Embed the query and return the top-k fused chunks."""
        query_vector = await self.embedder.embed_query(query)
        return self.hybrid.search(query, query_vector, top_k=top_k)
