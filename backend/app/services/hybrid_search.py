"""
services/hybrid_search.py - Merges semantic and keyword search results.
Uses Reciprocal Rank Fusion (RRF) + weighted scoring to combine both
retrieval signals into a single ranked result list.
"""

from typing import List, Optional, Dict
from app.services.semantic_search import semantic_search_service
from app.services.keyword_search import keyword_search_service
from app.services.ranking_service import ranking_service
from app.db.database import db
from app.core.config import settings
from app.models.product import ProductWithScore


class HybridSearchService:
    """
    Orchestrates semantic + keyword search and merges their results.

    Strategy:
        1. Run semantic search (FAISS) and keyword search (Elasticsearch) in parallel.
        2. Normalize scores from each source to [0, 1].
        3. Combine using configurable weights (semantic_weight + keyword_weight).
        4. Apply re-ranking via ranking_service.
        5. Return top_k final results.
    """

    def search(
        self,
        query: str,
        top_k: int = 10,
        category: Optional[str] = None,
    ) -> List[ProductWithScore]:
        # Fetch candidates from both sources (fetch 2x top_k for re-ranking)
        fetch_k = min(top_k * 3, 50)

        semantic_results: Dict[str, float] = {
            r["id"]: r["score"]
            for r in semantic_search_service.search_with_scores_normalized(query, k=fetch_k)
        }
        keyword_results: Dict[str, float] = {
            r[0]: r[1]
            for r in keyword_search_service.search(query, top_k=fetch_k, category=category)
        }

        # Union of all candidate product IDs
        all_ids = set(semantic_results.keys()) | set(keyword_results.keys())

        if not all_ids:
            # Cold start / empty index: fall back to all products
            all_ids = {p["id"] for p in db.get_all()}

        combined_scores: Dict[str, Dict] = {}
        for pid in all_ids:
            s_score = semantic_results.get(pid, 0.0)
            k_score = keyword_results.get(pid, 0.0)
            hybrid = (
                settings.SEMANTIC_WEIGHT * s_score
                + settings.KEYWORD_WEIGHT * k_score
            )
            combined_scores[pid] = {
                "score": hybrid,
                "semantic_score": s_score,
                "keyword_score": k_score,
            }

        # Sort by hybrid score descending
        sorted_ids = sorted(combined_scores, key=lambda x: combined_scores[x]["score"], reverse=True)

        # Fetch product data for top candidates
        candidate_products = db.get_by_ids(sorted_ids[:fetch_k])

        # Apply category filter if semantic search doesn't support it natively
        if category:
            candidate_products = [p for p in candidate_products if p.get("category") == category]

        # Build ProductWithScore objects
        enriched = []
        for product_dict in candidate_products:
            pid = product_dict["id"]
            scores = combined_scores.get(pid, {"score": 0.0, "semantic_score": 0.0, "keyword_score": 0.0})
            enriched.append(
                ProductWithScore(**product_dict, **scores)
            )

        # Apply ranking (boost by rating, popularity, etc.)
        ranked = ranking_service.rank(enriched, query=query)

        return ranked[:top_k]


hybrid_search = HybridSearchService()
