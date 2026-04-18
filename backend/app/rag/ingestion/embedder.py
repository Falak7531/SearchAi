"""Embedding model wrapper shared by ingestion and retrieval.

Note: Groq does not provide an embeddings API, so we use local
sentence-transformers models exclusively.
"""

from __future__ import annotations

import asyncio

import numpy as np
from sentence_transformers import SentenceTransformer

from app.rag.config import RAGConfig


class EmbeddingClient:
    """Embed texts using local Sentence Transformers."""

    def __init__(self, config: RAGConfig):
        """Initialize the sentence-transformers embedding provider."""
        self.config = config
        self.provider = config.embeddings.provider.lower()
        self._sentence_model = SentenceTransformer(config.embeddings.sentence_transformer_model)

    async def embed_texts(self, texts: list[str]) -> np.ndarray:
        """Embed a batch of texts into a 2-D float32 matrix."""
        if not texts:
            return np.empty((0, 0), dtype=np.float32)

        vectors = await asyncio.to_thread(
            self._sentence_model.encode,
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return self._normalize(np.asarray(vectors, dtype=np.float32))

    async def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query into a 1-D vector."""
        vectors = await self.embed_texts([query])
        return vectors[0]

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        """Normalize vectors for cosine similarity search."""
        if not self.config.embeddings.normalize or vectors.size == 0:
            return vectors
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.maximum(norms, 1e-12)

