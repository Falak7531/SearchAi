"""
services/keyword_search.py - Elasticsearch-based keyword (BM25) search.
Provides exact and fuzzy keyword matching as the second leg of hybrid search.
Falls back gracefully if Elasticsearch is unavailable.
"""

from typing import List, Tuple, Optional
from app.core.config import settings

try:
    from elasticsearch import Elasticsearch
    ES_AVAILABLE = True
except ImportError:
    ES_AVAILABLE = False


class KeywordSearchService:
    """
    Wraps Elasticsearch for BM25 keyword search.
    Returns a list of (product_id, bm25_score) tuples.
    """

    def __init__(self):
        self.client: Optional[object] = None
        self.index = settings.ELASTICSEARCH_INDEX
        if ES_AVAILABLE:
            try:
                self.client = Elasticsearch(settings.ELASTICSEARCH_URL)
                if self.client.ping():
                    print("✅ Connected to Elasticsearch.")
                else:
                    print("⚠️  Elasticsearch ping failed. Keyword search will be skipped.")
                    self.client = None
            except Exception as e:
                print(f"⚠️  Elasticsearch not available: {e}")
                self.client = None

    def search(self, query: str, top_k: int = 20, category: Optional[str] = None) -> List[Tuple[str, float]]:
        """
        Search products using BM25 full-text search.

        Args:
            query: The search query string.
            top_k: Number of results to fetch.
            category: Optional category filter.

        Returns:
            List of (product_id, normalized_score) tuples.
        """
        if self.client is None:
            # Gracefully degrade: return empty results
            return []

        must_clauses = [
            {
                "multi_match": {
                    "query": query,
                    "fields": ["name^3", "description^2", "tags^2", "brand", "category"],
                    "fuzziness": "AUTO",
                    "type": "best_fields",
                }
            }
        ]

        filter_clauses = []
        if category:
            filter_clauses.append({"term": {"category.keyword": category}})

        es_query = {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "filter": filter_clauses,
                }
            },
            "size": top_k,
        }

        response = self.client.search(index=self.index, body=es_query)
        hits = response["hits"]["hits"]

        if not hits:
            return []

        max_score = hits[0]["_score"] or 1.0
        return [(hit["_id"], hit["_score"] / max_score) for hit in hits]

    def index_products(self, products: List[dict]):
        """Index all products into Elasticsearch (run once during setup)."""
        if self.client is None:
            print("⚠️  Elasticsearch not available. Skipping indexing.")
            return

        for product in products:
            self.client.index(
                index=self.index,
                id=product["id"],
                body=product,
            )
        print(f"✅ Indexed {len(products)} products into Elasticsearch.")


keyword_search_service = KeywordSearchService()
