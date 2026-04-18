"""
services/ranking_service.py - Post-retrieval re-ranking logic.
Applies business rules (ratings, stock, relevance boosts) on top of
the raw hybrid score to produce a final production-quality ranking.
"""

from typing import List
from app.models.product import ProductWithScore


class RankingService:
    """
    Re-ranks hybrid search results using a composite scoring formula:
    
        final_score = hybrid_score * relevance_weight
                    + rating_boost * rating_weight
                    + stock_boost * stock_weight
    """

    RELEVANCE_WEIGHT = 0.75
    RATING_WEIGHT = 0.20
    STOCK_WEIGHT = 0.05

    def rank(self, products: List[ProductWithScore], query: str = "") -> List[ProductWithScore]:
        """
        Re-rank products by combining hybrid score with business signals.

        Args:
            products: List of products with hybrid scores.
            query: Original query (can be used for future query-specific boosts).

        Returns:
            Products sorted by final composite score (descending).
        """
        for product in products:
            rating_boost = (product.rating or 3.0) / 5.0
            stock_boost = min((product.stock or 0) / 500.0, 1.0)

            final_score = (
                self.RELEVANCE_WEIGHT * product.score
                + self.RATING_WEIGHT * rating_boost
                + self.STOCK_WEIGHT * stock_boost
            )
            product.score = round(final_score, 4)

        return sorted(products, key=lambda p: p.score, reverse=True)


ranking_service = RankingService()
