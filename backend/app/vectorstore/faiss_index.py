"""
vectorstore/faiss_index.py - FAISS index for semantic similarity search.

Uses IndexFlatL2 (exact L2 / Euclidean distance search) to find the
nearest product vectors to a given query vector.

Lower L2 distance  →  more similar product.

Flow:
    1. Build: encode all products → add_vectors(vectors, ids)
    2. Query: encode user query  → search(query_vector, k=10)
    3. Results: list of { id, score } dicts sorted by distance (asc)
"""

import os
import json
import numpy as np
from typing import List, Dict

import faiss

# Paths for persisting the index and ID mapping between runs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "faiss.index")
ID_MAP_PATH = os.path.join(BASE_DIR, "id_map.json")


class FAISSIndex:
    """
    Wraps a FAISS IndexFlatL2 index and maps its integer row positions
    to human-readable product ID strings.

    Why IndexFlatL2?
    - Exact (no approximation) — correct for small-to-medium catalogs
    - Simple to reason about: distance = Euclidean distance in embedding space
    - Swap to IndexIVFFlat or IndexHNSWFlat for million-scale datasets
    """

    def __init__(self, dim: int = 384):
        """
        Args:
            dim: Dimensionality of the embedding vectors.
                 Must match the output of the embedding model (384 for all-MiniLM-L6-v2).
        """
        self.dim = dim

        # IndexFlatL2 computes exact L2 distances — no training required
        self.index = faiss.IndexFlatL2(dim)

        # Parallel list: position i holds the product_id for FAISS row i
        # FAISS only understands integer row indices, so we maintain this map ourselves
        self.id_map: List[str] = []

        # Attempt to restore a previously saved index from disk
        self._load()

    # ── Persistence ───────────────────────────────────────────────────────

    def _load(self):
        """Reload index and ID map from disk if both files exist."""
        if os.path.exists(INDEX_PATH) and os.path.exists(ID_MAP_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(ID_MAP_PATH, "r") as f:
                self.id_map = json.load(f)
            print(f"✅ FAISS index loaded: {self.index.ntotal} vectors (dim={self.dim})")
        else:
            print("ℹ️  No FAISS index on disk — call add_vectors() to build one.")

    def save(self):
        """Persist the FAISS index and ID map to disk for reuse across restarts."""
        faiss.write_index(self.index, INDEX_PATH)
        with open(ID_MAP_PATH, "w") as f:
            json.dump(self.id_map, f)
        print(f"✅ FAISS index saved ({self.index.ntotal} vectors).")

    # ── Indexing ──────────────────────────────────────────────────────────

    def add_vectors(self, vectors: np.ndarray, ids: List[str]):
        """
        Add product embedding vectors to the FAISS index.

        Args:
            vectors: numpy array of shape (n, dim) and dtype float32.
                     Each row is one product's embedding vector.
            ids:     List of product ID strings matching the row order of vectors.

        Example:
            embeddings = embedding_service.encode_products(texts)  # (10, 384)
            faiss_index.add_vectors(embeddings, ["prod-001", ..., "prod-010"])
        """
        if len(ids) != vectors.shape[0]:
            raise ValueError(
                f"Length mismatch: {len(ids)} ids vs {vectors.shape[0]} vectors."
            )

        # FAISS requires contiguous float32 arrays
        vectors_f32 = np.array(vectors, dtype=np.float32)

        # Reset index so we don't accumulate duplicates on rebuild
        self.index = faiss.IndexFlatL2(self.dim)
        self.id_map = []

        self.index.add(vectors_f32)   # Add all rows in one efficient call
        self.id_map.extend(ids)       # Keep our id_map in sync

        self.save()
        print(f"✅ Indexed {len(ids)} product vectors into FAISS.")

    # ── Search ────────────────────────────────────────────────────────────

    def search(self, query_vector: np.ndarray, k: int = 10) -> List[Dict]:
        """
        Find the k most similar products to the query vector.

        Args:
            query_vector: numpy array of shape (1, dim) or (dim,) — the encoded query.
            k:            Number of nearest neighbours to return.

        Returns:
            List of dicts, sorted by ascending L2 distance (closest first):
            [
                { "id": "prod-003", "score": 0.142 },
                { "id": "prod-007", "score": 0.289 },
                ...
            ]

        Note on score interpretation:
            score = L2 distance → lower is better (0.0 = identical vector).
        """
        if self.index.ntotal == 0:
            print("⚠️  FAISS index is empty. Run add_vectors() first.")
            return []

        # Ensure shape is (1, dim) — FAISS expects a 2-D query matrix
        query = np.array(query_vector, dtype=np.float32).reshape(1, -1)

        # Clamp k to the number of indexed vectors
        k = min(k, self.index.ntotal)

        # distances: (1, k) — L2 distances to each neighbour
        # indices:   (1, k) — row positions in the FAISS index
        distances, indices = self.index.search(query, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            # idx == -1 means FAISS could not find enough neighbours (shouldn't happen with FlatL2)
            if idx == -1 or idx >= len(self.id_map):
                continue
            results.append({
                "id": self.id_map[idx],      # Map integer row → product ID string
                "score": float(dist),         # L2 distance (lower = more similar)
            })

        return results  # Already sorted ascending by FAISS


# Singleton — one shared index for the entire application lifetime
faiss_index = FAISSIndex()

# Legacy alias so existing code using `faiss_store` continues to work
faiss_store = faiss_index
