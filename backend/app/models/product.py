"""
models/product.py - Pydantic model for a Product entity.
Defines the data shape for products stored and returned from the system.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class Product(BaseModel):
    id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Detailed product description")
    category: str = Field(..., description="Product category (e.g., Electronics)")
    price: float = Field(..., ge=0, description="Price in USD")
    brand: Optional[str] = Field(None, description="Brand or manufacturer")
    tags: List[str] = Field(default_factory=list, description="Searchable tags")
    image_url: Optional[str] = Field(None, description="URL to product image")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating")
    stock: Optional[int] = Field(None, ge=0, description="Available stock count")


class ProductWithScore(Product):
    """Product enriched with a hybrid search relevance score."""
    score: float = Field(..., description="Hybrid relevance score (0.0 - 1.0)")
    semantic_score: Optional[float] = Field(None, description="FAISS cosine similarity score")
    keyword_score: Optional[float] = Field(None, description="Elasticsearch BM25 score")
