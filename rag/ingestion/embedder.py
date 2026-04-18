"""Embedding model abstraction (local sentence-transformers only).

Note: Groq does not provide an embeddings API, so we use local models.
"""
from __future__ import annotations

from typing import Any

import numpy as np

from rag.utils import logger


class Embedder:
    """Unified embedding interface with batched inference."""

    def __init__(self, cfg: dict[str, Any]) -> None:
        self.cfg = cfg["embedding"]
        self.batch_size = self.cfg["batch_size"]
        self._model: Any = None
        self._init_backend()

    def _init_backend(self) -> None:
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(self.cfg["model_name"])
        logger.info("Loaded local embedder: %s", self.cfg["model_name"])

    @property
    def dimension(self) -> int:
        return int(self.cfg["dimension"])

    def embed(self, texts: list[str]) -> np.ndarray:
        """Embed a list of strings → (N, dim) float32 array."""
        if not texts:
            return np.zeros((0, self.dimension), dtype=np.float32)

        vecs = self._model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return vecs.astype(np.float32)

    def embed_query(self, text: str) -> np.ndarray:
        """Embed a single query string → (dim,) array."""
        return self.embed([text])[0]
