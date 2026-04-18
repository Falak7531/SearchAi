"""Vector store abstraction supporting FAISS and Qdrant."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import faiss
import numpy as np

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qdrant_models
except ImportError:  # pragma: no cover - optional dependency during local dev
    QdrantClient = None
    qdrant_models = None

from app.rag.config import RAGConfig
from app.rag.types import ChunkRecord, RetrievedChunk


class VectorStore:
    """Persist and query chunk embeddings in FAISS or Qdrant."""

    def __init__(self, config: RAGConfig):
        """Initialize the configured vector store provider."""
        self.config = config
        self.provider = config.vector_store.provider.lower()
        self.metadata_path = Path(config.paths.metadata_store_path)
        self.embeddings_path = Path(config.paths.embeddings_store_path)
        self.index_path = Path(config.paths.faiss_index_path)
        self._chunks: dict[str, ChunkRecord] = {}
        self._vectors: dict[str, np.ndarray] = {}
        self._faiss_index: faiss.IndexIDMap2 | None = None
        self._qdrant_client: QdrantClient | None = None
        self._dim: int | None = None

        if self.provider == "qdrant":
            if QdrantClient is None or qdrant_models is None:
                raise ValueError("qdrant-client must be installed to use vector_store.provider=qdrant.")
            self._qdrant_client = QdrantClient(url=config.vector_store.qdrant_url)

        self._load()

    def upsert(self, chunks: list[ChunkRecord], embeddings: np.ndarray) -> None:
        """Upsert chunks and their embeddings into the configured store."""
        if len(chunks) != len(embeddings):
            raise ValueError("Chunk count must match embedding count during upsert.")
        if not chunks:
            return

        self._dim = int(embeddings.shape[1])
        for chunk, vector in zip(chunks, embeddings):
            self._chunks[chunk.chunk_id] = chunk
            self._vectors[chunk.chunk_id] = np.asarray(vector, dtype=np.float32)

        if self.provider == "faiss":
            self._persist_faiss_state()
        else:
            self._persist_qdrant_state(chunks, embeddings)

    def search(self, query_vector: np.ndarray, top_k: int) -> list[RetrievedChunk]:
        """Run vector similarity search and return retrieved chunks."""
        if self.provider == "faiss":
            return self._search_faiss(query_vector, top_k)
        return self._search_qdrant(query_vector, top_k)

    def list_chunks(self) -> list[ChunkRecord]:
        """Return all known chunks for BM25 indexing and diagnostics."""
        return list(self._chunks.values())

    def _load(self) -> None:
        """Load persisted metadata and vectors when available."""
        if self.metadata_path.exists():
            with self.metadata_path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    payload = json.loads(line)
                    chunk = ChunkRecord(**payload)
                    self._chunks[chunk.chunk_id] = chunk

        if self.provider == "faiss" and self.embeddings_path.exists():
            embeddings = np.load(self.embeddings_path)
            ordered_chunks = list(self._chunks.values())
            for chunk, vector in zip(ordered_chunks, embeddings):
                self._vectors[chunk.chunk_id] = vector.astype(np.float32)
            if ordered_chunks:
                self._dim = int(embeddings.shape[1])
                self._rebuild_faiss_index()

    def _persist_faiss_state(self) -> None:
        """Persist metadata, vectors, and a rebuilt FAISS index.

        Rebuilding from persisted vectors is slower than in-place mutation but
        much safer for consistency in a small-to-medium document corpus.
        """
        ordered_chunk_ids = list(self._chunks.keys())
        ordered_chunks = [self._chunks[chunk_id] for chunk_id in ordered_chunk_ids]
        ordered_vectors = np.asarray([self._vectors[chunk_id] for chunk_id in ordered_chunk_ids], dtype=np.float32)

        with self.metadata_path.open("w", encoding="utf-8") as handle:
            for chunk in ordered_chunks:
                handle.write(json.dumps(chunk.to_dict()) + "\n")
        np.save(self.embeddings_path, ordered_vectors)
        self._rebuild_faiss_index()

    def _persist_qdrant_state(self, chunks: list[ChunkRecord], embeddings: np.ndarray) -> None:
        """Upsert data into Qdrant and persist metadata for BM25 fallback."""
        assert self._qdrant_client is not None
        distance = qdrant_models.Distance.COSINE
        if not self._qdrant_client.collection_exists(self.config.vector_store.qdrant_collection):
            self._qdrant_client.create_collection(
                collection_name=self.config.vector_store.qdrant_collection,
                vectors_config=qdrant_models.VectorParams(
                    size=int(embeddings.shape[1]),
                    distance=distance,
                ),
            )

        points = []
        for chunk, vector in zip(chunks, embeddings):
            points.append(
                qdrant_models.PointStruct(
                    id=self._numeric_id(chunk.chunk_id),
                    vector=vector.tolist(),
                    payload=chunk.to_dict(),
                )
            )
        self._qdrant_client.upsert(
            collection_name=self.config.vector_store.qdrant_collection,
            points=points,
        )

        with self.metadata_path.open("w", encoding="utf-8") as handle:
            for chunk in self._chunks.values():
                handle.write(json.dumps(chunk.to_dict()) + "\n")

    def _rebuild_faiss_index(self) -> None:
        """Rebuild the FAISS index from persisted in-memory vectors."""
        if not self._vectors:
            self._faiss_index = None
            return

        assert self._dim is not None
        index = faiss.IndexIDMap2(faiss.IndexFlatIP(self._dim))
        ordered_chunk_ids = list(self._chunks.keys())
        vectors = np.asarray([self._vectors[chunk_id] for chunk_id in ordered_chunk_ids], dtype=np.float32)
        ids = np.asarray([self._numeric_id(chunk_id) for chunk_id in ordered_chunk_ids], dtype=np.int64)
        index.add_with_ids(vectors, ids)
        faiss.write_index(index, str(self.index_path))
        self._faiss_index = index

    def _search_faiss(self, query_vector: np.ndarray, top_k: int) -> list[RetrievedChunk]:
        """Search a FAISS cosine-similarity index."""
        if self._faiss_index is None:
            return []
        query = np.asarray(query_vector, dtype=np.float32).reshape(1, -1)
        scores, ids = self._faiss_index.search(query, top_k)

        results: list[RetrievedChunk] = []
        for score, numeric_id in zip(scores[0], ids[0]):
            if numeric_id == -1:
                continue
            chunk = self._chunk_from_numeric_id(int(numeric_id))
            if chunk is None:
                continue
            results.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    document_name=chunk.document_name,
                    source_uri=chunk.source_uri,
                    content=chunk.content,
                    chunk_index=chunk.chunk_index,
                    metadata=chunk.metadata,
                    vector_score=float(score),
                    fused_score=float(score),
                )
            )
        return results

    def _search_qdrant(self, query_vector: np.ndarray, top_k: int) -> list[RetrievedChunk]:
        """Search a Qdrant collection."""
        assert self._qdrant_client is not None
        response = self._qdrant_client.search(
            collection_name=self.config.vector_store.qdrant_collection,
            query_vector=query_vector.tolist(),
            limit=top_k,
            with_payload=True,
        )
        results: list[RetrievedChunk] = []
        for point in response:
            payload: dict[str, Any] = point.payload or {}
            chunk = ChunkRecord(**payload)
            results.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    document_name=chunk.document_name,
                    source_uri=chunk.source_uri,
                    content=chunk.content,
                    chunk_index=chunk.chunk_index,
                    metadata=chunk.metadata,
                    vector_score=float(point.score),
                    fused_score=float(point.score),
                )
            )
        return results

    def _chunk_from_numeric_id(self, numeric_id: int) -> ChunkRecord | None:
        """Map a FAISS numeric ID back to the stored chunk."""
        for chunk_id in self._chunks:
            if self._numeric_id(chunk_id) == numeric_id:
                return self._chunks[chunk_id]
        return None

    @staticmethod
    def _numeric_id(chunk_id: str) -> int:
        """Convert a hex chunk ID into a stable signed 63-bit integer."""
        return int(chunk_id[:15], 16)

