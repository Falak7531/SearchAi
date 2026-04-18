"""
config.py - Centralized configuration using environment variables.
All app-wide settings live here for easy management.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union

# Resolve repo-root .env regardless of where the process is launched from.
# This file lives at: <repo>/backend/app/core/config.py  -> parents[3] == <repo>
_REPO_ROOT = Path(__file__).resolve().parents[3]
_ENV_FILES = (
    _REPO_ROOT / ".env",                      # shared root env (preferred)
    _REPO_ROOT / "backend" / ".env",          # optional backend-specific override
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=tuple(str(p) for p in _ENV_FILES if p.exists()) or None,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # Application
    APP_NAME: str = "AI E-Commerce Search"
    DEBUG: bool = True

    # CORS — accepts a comma-separated string in .env, e.g.
    #   ALLOWED_ORIGINS=http://localhost:5173,https://app.example.com
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://search-ai-ebon.vercel.app",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def _split_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

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

    # Optional secrets (forwarded to RAG layer)
    GROQ_API_KEY: str = ""


settings = Settings()
