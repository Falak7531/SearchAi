"""Re-ranking facade for retrieved chunks.

The :class:`HybridRetriever` already produces a fused score via Reciprocal Rank
Fusion. The :class:`Ranker` here applies an additional business-rule pass:

    final_score = relevance_weight * fused_score
                + freshness_weight * freshness_signal
                + length_penalty   * length_signal

This is intentionally separate from
:class:`app.services.ranking_service.RankingService`, which re-ranks
:class:`ProductWithScore` objects for the lexical/semantic *product* search
endpoint. This module re-ranks :class:`RetrievedChunk` objects for RAG.
"""

from __future__ import annotations

from app.rag.types import RetrievedChunk

__all__ = ["Ranker"]


class Ranker:
    """Apply business-rule re-ranking on top of fused retrieval scores."""

    RELEVANCE_WEIGHT = 0.85
    LENGTH_PENALTY_WEIGHT = 0.15

    def rerank(self, chunks: list[RetrievedChunk], query: str = "") -> list[RetrievedChunk]:
        """Re-score and sort retrieved chunks by composite relevance.

        Args:
            chunks: Chunks already fused by hybrid retrieval.
            query: Original query (reserved for query-aware boosts).

        Returns:
            Chunks sorted by ``fused_score`` descending. Mutates ``fused_score``
            in place to incorporate the length penalty.
        """
        if not chunks:
            return chunks

        max_len = max(len(c.content) for c in chunks) or 1
        for chunk in chunks:
            length_signal = 1.0 - (len(chunk.content) / max_len)
            chunk.fused_score = (
                self.RELEVANCE_WEIGHT * chunk.fused_score
                + self.LENGTH_PENALTY_WEIGHT * length_signal
            )

        return sorted(chunks, key=lambda c: c.fused_score, reverse=True)
