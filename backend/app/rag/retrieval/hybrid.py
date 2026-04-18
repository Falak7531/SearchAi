"""Hybrid retrieval using reciprocal rank fusion over vector and BM25 results."""

from __future__ import annotations

from app.rag.config import RAGConfig
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.vector_store import VectorStore
from app.rag.types import RetrievedChunk


class HybridRetriever:
    """Fuse semantic and keyword retrieval into a single ranked list."""

    def __init__(self, config: RAGConfig, vector_store: VectorStore, bm25_retriever: BM25Retriever):
        """Initialize the hybrid retriever with its component retrievers."""
        self.config = config
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever

    def search(self, query: str, query_vector, top_k: int | None = None) -> list[RetrievedChunk]:
        """Retrieve the most relevant chunks via reciprocal rank fusion."""
        vector_results = self.vector_store.search(query_vector, self.config.retrieval.vector_top_k)
        keyword_results = self.bm25_retriever.search(query, self.config.retrieval.bm25_top_k)

        combined: dict[str, RetrievedChunk] = {}
        rrf_constant = self.config.retrieval.rrf_k

        for rank, chunk in enumerate(vector_results, start=1):
            combined.setdefault(chunk.chunk_id, chunk).fused_score += 1.0 / (rrf_constant + rank)

        for rank, chunk in enumerate(keyword_results, start=1):
            if chunk.chunk_id not in combined:
                combined[chunk.chunk_id] = chunk
            else:
                combined[chunk.chunk_id].keyword_score = chunk.keyword_score
            combined[chunk.chunk_id].fused_score += 1.0 / (rrf_constant + rank)

        ranked = sorted(combined.values(), key=lambda item: item.fused_score, reverse=True)
        final_k = top_k or self.config.retrieval.final_top_k
        return ranked[:final_k]

