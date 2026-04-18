"""
api/search.py - Search API endpoint.

Exposes POST /search for semantic product search and returns full product
records enriched with relevance scores so the frontend can render cards.
"""

import re
from fastapi import APIRouter, HTTPException

from app.db.database import db
from app.models.search import SearchRequest, SearchResponse
from app.services.semantic_search import semantic_search_service

router = APIRouter()


def _to_product_result(raw_product: dict, score: float) -> dict:
    """Normalize raw JSON product data into the frontend's expected shape."""
    return {
        "id": str(raw_product["id"]),
        "name": raw_product.get("name") or raw_product.get("title", "Untitled Product"),
        "description": raw_product.get("description", ""),
        "category": raw_product.get("category", "uncategorized"),
        "price": float(raw_product.get("price", 0)),
        "brand": raw_product.get("brand"),
        "tags": raw_product.get("tags", []),
        "image_url": raw_product.get("image_url"),
        "rating": raw_product.get("rating"),
        "stock": raw_product.get("stock"),
        "score": score,
        "semantic_score": score,
        "keyword_score": None,
    }


@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Run semantic search and return product details with scores."""
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be blank.")

    max_price = None
    min_price = None

    match_max = re.search(r'(?:under|less than|below|max|<|<=)\s*\$?\s*(\d+(?:\.\d{1,2})?)', query, re.IGNORECASE)
    if match_max:
        max_price = float(match_max.group(1))

    match_min = re.search(r'(?:over|more than|above|min|>|>=)\s*\$?\s*(\d+(?:\.\d{1,2})?)', query, re.IGNORECASE)
    if match_min:
        min_price = float(match_min.group(1))

    try:
        # Fetch more candidates to account for filtering
        scored_results = semantic_search_service.search_with_scores_normalized(
            query=query,
            k=max(request.top_k * 5, 50),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(exc)}")

    products_by_id = {str(product["id"]): product for product in db.get_all()}
    results = []

    for item in scored_results:
        product = products_by_id.get(str(item["id"]))
        if not product:
            continue

        if request.category and product.get("category") != request.category:
            continue

        price = float(product.get("price", 0))
        if max_price is not None and price >= max_price:
            continue
        if min_price is not None and price <= min_price:
            continue

        results.append(_to_product_result(product, item["score"]))

        if len(results) >= request.top_k:
            break

    return SearchResponse(
        query=query,
        total=len(results),
        results=results,
    )
