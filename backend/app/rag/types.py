"""Shared typed models used across the RAG pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class RawDocument:
    """A source document before chunking."""

    document_id: str
    document_name: str
    source_uri: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the document into a JSON-safe dictionary."""
        return asdict(self)


@dataclass(slots=True)
class ChunkRecord:
    """A chunked document fragment stored in the retrieval system."""

    chunk_id: str
    document_id: str
    document_name: str
    source_uri: str
    content: str
    chunk_index: int
    token_count: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the chunk into a JSON-safe dictionary."""
        return asdict(self)


@dataclass(slots=True)
class RetrievedChunk:
    """A chunk returned by retrieval, enriched with ranking signals."""

    chunk_id: str
    document_id: str
    document_name: str
    source_uri: str
    content: str
    chunk_index: int
    metadata: dict[str, Any]
    vector_score: float | None = None
    keyword_score: float | None = None
    fused_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize the retrieved chunk into a JSON-safe dictionary."""
        return asdict(self)


@dataclass(slots=True)
class Citation:
    """A source citation exposed in the final answer."""

    chunk_id: str
    document_name: str
    source_uri: str
    relevance_score: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize the citation into a JSON-safe dictionary."""
        return asdict(self)


@dataclass(slots=True)
class GeneratedAnswer:
    """Structured LLM output after parsing the model response."""

    answer: str
    reasoning_summary: str
    insufficient_context: bool
    cited_chunk_ids: list[str] = field(default_factory=list)
    raw_response: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the generated answer into a JSON-safe dictionary."""
        return asdict(self)


@dataclass(slots=True)
class PipelineTelemetry:
    """Latency and retrieval diagnostics for a single RAG request."""

    retrieval_latency_ms: float
    llm_latency_ms: float
    total_latency_ms: float
    retrieval_scores: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the telemetry into a JSON-safe dictionary."""
        return asdict(self)


@dataclass(slots=True)
class RAGQueryResult:
    """The final structured response returned by the RAG pipeline."""

    query: str
    answer: str
    reasoning_summary: str
    insufficient_context: bool
    citations: list[Citation]
    retrieved_chunks: list[RetrievedChunk]
    telemetry: PipelineTelemetry

    def to_dict(self) -> dict[str, Any]:
        """Serialize the query result into a JSON-safe dictionary."""
        return {
            "query": self.query,
            "answer": self.answer,
            "reasoning_summary": self.reasoning_summary,
            "insufficient_context": self.insufficient_context,
            "citations": [citation.to_dict() for citation in self.citations],
            "retrieved_chunks": [chunk.to_dict() for chunk in self.retrieved_chunks],
            "telemetry": self.telemetry.to_dict(),
        }


@dataclass(slots=True)
class EvaluationSample:
    """A query/ground-truth example used for RAG evaluation."""

    question: str
    ground_truth: str


@dataclass(slots=True)
class EvaluationRecord:
    """A model answer paired with retrieval context for RAGAS evaluation."""

    question: str
    answer: str
    contexts: list[str]
    ground_truth: str

