"""
services/embedding_service.py - Generates dense vector embeddings.
Uses Sentence Transformers to encode text queries and product descriptions
into high-dimensional vectors for semantic similarity search.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# Model name — all-MiniLM-L6-v2 is fast, lightweight, and accurate
# enough for production semantic search (384-dim output)
MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:
    """
    Wraps a Sentence Transformer model to generate dense vector embeddings.
    Vectors are L2-normalized so cosine similarity equals dot product —
    making them directly compatible with FAISS IndexFlatIP.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        # Load the model once at startup; reused for all requests
        print(f"🔄 Loading embedding model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as exc:
            print(f"⚠️ Online model load failed, retrying from local cache: {exc}")
            self.model = SentenceTransformer(model_name, local_files_only=True)
        print("✅ Embedding model ready.")

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        """L2-normalize each row so dot product == cosine similarity."""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.maximum(norms, 1e-10)

    def embed_text(self, text: str) -> np.ndarray:
        """
        Embed a single string into a dense vector.

        Args:
            text: Any plain-text string (query, product name, description, etc.)

        Returns:
            1-D numpy array of shape (384,) — normalized embedding vector.
        """
        # encode() expects a list; [0] unwraps the single result
        vector = self.model.encode([text], convert_to_numpy=True, show_progress_bar=False)
        return self._normalize(vector)[0]

    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Embed a list of strings in a single efficient batch pass.

        Args:
            texts: List of strings to encode (e.g. all product descriptions).

        Returns:
            List of 1-D numpy arrays, each of shape (384,).
            Order matches the input list.
        """
        # Batch encoding is significantly faster than calling embed_text in a loop
        vectors = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        normalized = self._normalize(vectors)
        # Return as a plain Python list of 1-D arrays for easy iteration
        return [normalized[i] for i in range(len(normalized))]

    # ── Convenience aliases used internally by other services ────────────
    def encode_query(self, query: str) -> np.ndarray:
        """Returns shape (1, 384) for direct FAISS index.search() input."""
        return self.embed_text(query).reshape(1, -1)

    def encode_products(self, texts: List[str]) -> np.ndarray:
        """Returns shape (n, 384) for FAISS index.add() input."""
        vectors = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return self._normalize(vectors)


# Singleton — loaded once when the module is first imported
embedding_service = EmbeddingService()
