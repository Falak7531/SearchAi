"""BM25 retrieval over chunk text for hybrid search."""

from __future__ import annotations

import re

from rank_bm25 import BM25Okapi

from app.rag.types import ChunkRecord, RetrievedChunk


class BM25Retriever:
    """Keyword retrieval over ingested document chunks."""

    def __init__(self) -> None:
        """Initialize an empty BM25 index."""
        self._bm25: BM25Okapi | None = None
        self._chunks: list[ChunkRecord] = []
        self._tokenized_corpus: list[list[str]] = []

    def rebuild(self, chunks: list[ChunkRecord]) -> None:
        """Rebuild the BM25 index from the current chunk corpus."""
        self._chunks = chunks
        self._tokenized_corpus = [self._tokenize(chunk.content) for chunk in chunks]
        self._bm25 = BM25Okapi(self._tokenized_corpus) if self._tokenized_corpus else None

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        """Run BM25 search against chunk content."""
        if self._bm25 is None:
            return []

        tokenized_query = self._tokenize(query)
        scores = self._bm25.get_scores(tokenized_query)
        ranked_indices = sorted(range(len(scores)), key=lambda idx: scores[idx], reverse=True)[:top_k]
        max_score = max((scores[idx] for idx in ranked_indices), default=1.0) or 1.0

        results: list[RetrievedChunk] = []
        for idx in ranked_indices:
            raw_score = float(scores[idx])
            if raw_score <= 0:
                continue
            chunk = self._chunks[idx]
            results.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    document_name=chunk.document_name,
                    source_uri=chunk.source_uri,
                    content=chunk.content,
                    chunk_index=chunk.chunk_index,
                    metadata=chunk.metadata,
                    keyword_score=raw_score / max_score,
                    fused_score=raw_score / max_score,
                )
            )
        return results

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Tokenize text with a lightweight regex-based tokenizer."""
        return re.findall(r"\w+", text.lower())

