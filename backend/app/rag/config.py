"""YAML-backed configuration for the RAG subsystem."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field


# Load .env from the repo root, no matter where the process is launched from.
# This file lives at: <repo>/backend/app/rag/config.py -> parents[3] == <repo>
_REPO_ROOT = Path(__file__).resolve().parents[3]
for _candidate in (_REPO_ROOT / ".env", _REPO_ROOT / "backend" / ".env"):
    if _candidate.exists():
        load_dotenv(_candidate, override=False)


class AppConfig(BaseModel):
    """Metadata about the RAG application."""

    name: str = "AI E-Commerce Search RAG"


class PathsConfig(BaseModel):
    """Filesystem paths used by the RAG pipeline."""

    data_dir: str
    faiss_index_path: str
    metadata_store_path: str
    embeddings_store_path: str


class ChunkingConfig(BaseModel):
    """Chunking behavior for document ingestion."""

    chunk_size: int = 900
    chunk_overlap: int = 150
    separators: list[str] = Field(default_factory=lambda: ["\n\n", "\n", ". ", " ", ""])


class EmbeddingsConfig(BaseModel):
    """Embedding model configuration."""

    provider: str = "sentence-transformers"
    sentence_transformer_model: str = "all-MiniLM-L6-v2"
    batch_size: int = 32
    normalize: bool = True


class VectorStoreConfig(BaseModel):
    """Vector store configuration for FAISS or Qdrant."""

    provider: str = "faiss"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "rag_chunks"
    distance: str = "cosine"


class RetrievalConfig(BaseModel):
    """Retrieval and fusion knobs."""

    vector_top_k: int = 8
    bm25_top_k: int = 8
    final_top_k: int = 5
    rrf_k: int = 60
    low_confidence_threshold: float = 0.12
    min_source_score: float = 0.05


class GenerationConfig(BaseModel):
    """LLM generation configuration."""

    provider: str = "groq"
    groq_model: str = "llama-3.1-8b-instant"
    ollama_model: str = "llama3.1:8b"
    ollama_base_url: str = "http://localhost:11434"
    temperature: float = 0.1
    max_tokens: int = 700


class EvaluationConfig(BaseModel):
    """Evaluation configuration for RAGAS."""

    enabled: bool = True
    answer_relevancy_model: str = "llama-3.1-8b-instant"


class LoggingConfig(BaseModel):
    """Logging configuration for the pipeline."""

    level: str = "INFO"


class RAGConfig(BaseModel):
    """Root configuration object for the full RAG pipeline."""

    app: AppConfig
    paths: PathsConfig
    chunking: ChunkingConfig
    embeddings: EmbeddingsConfig
    vector_store: VectorStoreConfig
    retrieval: RetrievalConfig
    generation: GenerationConfig
    evaluation: EvaluationConfig
    logging: LoggingConfig

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> "RAGConfig":
        """Load and validate the YAML configuration file."""
        if config_path is None:
            config_path = Path(__file__).with_name("config.yaml")
        else:
            config_path = Path(config_path)

        with config_path.open("r", encoding="utf-8") as handle:
            raw_config = yaml.safe_load(handle)
        config = cls.model_validate(raw_config)
        config.resolve_paths(config_path.parent.parent)
        return config

    def resolve_paths(self, app_root: Path) -> None:
        """Resolve configured paths relative to the backend app root."""
        self.paths.data_dir = str((app_root / self.paths.data_dir).resolve())
        self.paths.faiss_index_path = str((app_root / self.paths.faiss_index_path).resolve())
        self.paths.metadata_store_path = str((app_root / self.paths.metadata_store_path).resolve())
        self.paths.embeddings_store_path = str((app_root / self.paths.embeddings_store_path).resolve())
        os.makedirs(self.paths.data_dir, exist_ok=True)

    def get_env(self, name: str, default: str | None = None) -> str | None:
        """Fetch a secret or runtime override from the environment."""
        return os.getenv(name, default)


@lru_cache(maxsize=1)
def get_rag_config(config_path: str | None = None) -> RAGConfig:
    """Return a cached RAG configuration instance."""
    return RAGConfig.load(config_path)

