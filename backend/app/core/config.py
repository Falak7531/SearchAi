"""
config.py - Centralized configuration using environment variables.
All app-wide settings live here for easy management.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI E-Commerce Search"
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX: str = "products"

    # Sentence Transformer model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # FAISS
    FAISS_INDEX_PATH: str = "vectorstore/faiss.index"
    FAISS_ID_MAP_PATH: str = "vectorstore/id_map.json"

    # Hybrid Search weights (must sum to 1.0)
    SEMANTIC_WEIGHT: float = 0.6
    KEYWORD_WEIGHT: float = 0.4

    # Data
    PRODUCTS_PATH: str = "../data/products.json"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
