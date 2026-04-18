"""
models/search.py - Pydantic models for Search request and response.
Ensures consistent API contracts for all search operations.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.product import ProductWithScore


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User search query")
    top_k: int = Field(10, ge=1, le=50, description="Max results to return")
    category: Optional[str] = Field(None, description="Filter by product category")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "wireless noise cancelling headphones",
                "top_k": 10,
                "category": "Electronics",
            }
        }


class SearchResponse(BaseModel):
    query: str = Field(..., description="Original user query")
    total: int = Field(..., description="Number of results returned")
    results: List[ProductWithScore] = Field(..., description="Ranked list of products")
