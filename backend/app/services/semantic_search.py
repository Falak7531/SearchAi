"""
services/semantic_search.py - Semantic search using sentence embeddings + FAISS.

Flow for every search() call:
    1. Receive plain-text query from the API layer
    2. Convert it to a 384-dim embedding via EmbeddingService
    3. Run nearest-neighbour search against the pre-built FAISSIndex
    4. Return ranked results as a clean list of dicts

This service is stateless — it holds references to shared singletons
(embedding_service, faiss_index) that are loaded once at startup.
"""

from typing import List, Dict

from app.services.embedding_service import embedding_service
from app.vectorstore.faiss_index import faiss_index


class SemanticSearchService:
    """
    Bridges the embedding model and the FAISS vector store.

    Responsibilities:
    - Accept raw query strings from the API
    - Delegate embedding to EmbeddingService
    - Delegate vector search to FAISSIndex
    - Return normalised, API-ready result dicts
    """

    def __init__(self):
        # Reuse the module-level singletons — no extra model loading
        self.embedder = embedding_service
        self.index = faiss_index

    def search(self, query: str, k: int = 10) -> List[Dict]:
        """
        Find the k most semantically similar products for a query.

        Args:
            query: Natural language search string from the user.
                   e.g. "cheap phone with good camera"
            k:     Number of results to return (default 10).

        Returns:
            List of result dicts sorted by ascending L2 distance
            (most similar first):
            [
                { "id": "prod-003", "score": 0.42 },
                { "id": "prod-007", "score": 0.61 },
                ...
            ]

        Returns [] if the FAISS index is empty or not yet built.
        """
        # Guard: nothing to search if the index has no vectors yet
        if self.index.index.ntotal == 0:
            print("⚠️  FAISS index is empty — run build_index.py first.")
            return []

        # Step 1: Encode the query string → shape (1, 384) float32 ndarray
        # encode_query handles normalisation internally
        query_vector = self.embedder.encode_query(query)

        # Step 2: Search the FAISS index for the k nearest product vectors
        # Returns [{ "id": str, "score": float (L2 distance) }, ...]
        results = self.index.search(query_vector, k=k)

        return results

    def search_with_scores_normalized(self, query: str, k: int = 10) -> List[Dict]:
        """
        Same as search() but converts L2 distance to a [0, 1] similarity score.

        similarity = 1 / (1 + l2_distance)
            → 1.0 means identical, approaches 0 as distance grows

        Useful when merging semantic scores with keyword scores in hybrid search.
        """
        raw = self.search(query, k=k)

        # Transform each result's score in-place
        for result in raw:
            result["score"] = round(1 / (1 + result["score"]), 4)

        return raw  # Still sorted best-first (higher similarity = better)


# Singleton — imported and reused by hybrid_search.py and the API layer
semantic_search_service = SemanticSearchService()
