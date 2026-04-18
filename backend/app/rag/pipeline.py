"""End-to-end orchestrator for ingestion, retrieval, generation, and evaluation."""

from __future__ import annotations

import logging
import time
from pathlib import Path

from app.rag.config import RAGConfig, get_rag_config
from app.rag.evaluation import RAGEvaluator
from app.rag.generation.llm_client import LLMClient
from app.rag.generation.prompt_builder import PromptBuilder
from app.rag.ingestion.chunker import DocumentChunker
from app.rag.ingestion.embedder import EmbeddingClient
from app.rag.ingestion.loader import DocumentLoader
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.hybrid import HybridRetriever
from app.rag.retrieval.vector_store import VectorStore
from app.rag.types import (
    Citation,
    EvaluationRecord,
    EvaluationSample,
    PipelineTelemetry,
    RAGQueryResult,
    RetrievedChunk,
)


class RAGPipeline:
    """Coordinates document ingestion, retrieval, answer generation, and evaluation."""

    def __init__(self, config_path: str | Path | None = None):
        """Build the full pipeline from the shared YAML config."""
        self.config: RAGConfig = get_rag_config(str(config_path) if config_path else None)
        logging.basicConfig(level=getattr(logging, self.config.logging.level.upper(), logging.INFO))
        self.logger = logging.getLogger("app.rag.pipeline")

        self.loader = DocumentLoader()
        self.chunker = DocumentChunker(self.config)
        self.embedder = EmbeddingClient(self.config)
        self.vector_store = VectorStore(self.config)
        self.bm25 = BM25Retriever()
        self.bm25.rebuild(self.vector_store.list_chunks())
        self.hybrid = HybridRetriever(self.config, self.vector_store, self.bm25)
        self.prompt_builder = PromptBuilder()
        self.llm_client = LLMClient(self.config)
        self.evaluator = RAGEvaluator()

    async def ingest_sources(self, sources: list[str]) -> dict[str, int]:
        """Load, chunk, embed, and index a list of sources."""
        documents = self.loader.load(sources)
        chunks = self.chunker.chunk_documents(documents)
        embeddings = await self.embedder.embed_texts([chunk.content for chunk in chunks])
        self.vector_store.upsert(chunks, embeddings)
        self.bm25.rebuild(self.vector_store.list_chunks())

        self.logger.info(
            "RAG ingestion complete",
            extra={
                "source_count": len(sources),
                "document_count": len(documents),
                "chunk_count": len(chunks),
            },
        )
        return {
            "sources": len(sources),
            "documents": len(documents),
            "chunks": len(chunks),
        }

    async def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        """Retrieve relevant chunks for a query."""
        query_vector = await self.embedder.embed_query(query)
        return self.hybrid.search(query=query, query_vector=query_vector, top_k=top_k)

    async def answer_query(self, query: str, top_k: int | None = None) -> RAGQueryResult:
        """Run the full retrieval-augmented generation pipeline for a query."""
        total_start = time.perf_counter()

        retrieval_start = time.perf_counter()
        retrieved_chunks = await self.retrieve(query, top_k=top_k)
        retrieval_latency_ms = (time.perf_counter() - retrieval_start) * 1000

        filtered_chunks = [
            chunk
            for chunk in retrieved_chunks
            if chunk.fused_score >= self.config.retrieval.min_source_score
        ]
        top_score = filtered_chunks[0].fused_score if filtered_chunks else 0.0

        if not filtered_chunks or top_score < self.config.retrieval.low_confidence_threshold:
            telemetry = PipelineTelemetry(
                retrieval_latency_ms=retrieval_latency_ms,
                llm_latency_ms=0.0,
                total_latency_ms=(time.perf_counter() - total_start) * 1000,
                retrieval_scores=[self._score_log(chunk) for chunk in retrieved_chunks],
            )
            return RAGQueryResult(
                query=query,
                answer="I do not have enough context in the retrieved documents to answer confidently.",
                reasoning_summary="The retriever did not find enough high-confidence evidence.",
                insufficient_context=True,
                citations=[],
                retrieved_chunks=retrieved_chunks,
                telemetry=telemetry,
            )

        messages = self.prompt_builder.build_messages(query, filtered_chunks)
        llm_start = time.perf_counter()
        generated = await self.llm_client.generate(messages)
        llm_latency_ms = (time.perf_counter() - llm_start) * 1000

        citations = self._resolve_citations(filtered_chunks, generated.cited_chunk_ids)
        telemetry = PipelineTelemetry(
            retrieval_latency_ms=retrieval_latency_ms,
            llm_latency_ms=llm_latency_ms,
            total_latency_ms=(time.perf_counter() - total_start) * 1000,
            retrieval_scores=[self._score_log(chunk) for chunk in filtered_chunks],
        )

        self.logger.info(
            "RAG query completed",
            extra={
                "query": query,
                "retrieved_chunks": len(filtered_chunks),
                "retrieval_latency_ms": round(retrieval_latency_ms, 2),
                "llm_latency_ms": round(llm_latency_ms, 2),
            },
        )
        return RAGQueryResult(
            query=query,
            answer=generated.answer,
            reasoning_summary=generated.reasoning_summary,
            insufficient_context=generated.insufficient_context,
            citations=citations,
            retrieved_chunks=filtered_chunks,
            telemetry=telemetry,
        )

    async def evaluate_samples(self, samples: list[EvaluationSample]) -> dict[str, float]:
        """Evaluate the pipeline against a labeled evaluation set."""
        records: list[EvaluationRecord] = []
        for sample in samples:
            result = await self.answer_query(sample.question)
            records.append(
                EvaluationRecord(
                    question=sample.question,
                    answer=result.answer,
                    contexts=[chunk.content for chunk in result.retrieved_chunks],
                    ground_truth=sample.ground_truth,
                )
            )
        return self.evaluator.evaluate(records)

    @staticmethod
    def _score_log(chunk: RetrievedChunk) -> dict[str, float | str | None]:
        """Serialize retrieval scores for observability."""
        return {
            "chunk_id": chunk.chunk_id,
            "document_name": chunk.document_name,
            "vector_score": chunk.vector_score,
            "keyword_score": chunk.keyword_score,
            "fused_score": chunk.fused_score,
        }

    @staticmethod
    def _resolve_citations(chunks: list[RetrievedChunk], cited_chunk_ids: list[str]) -> list[Citation]:
        """Match model-emitted citations against retrieved chunks.

        If the model omits citations, default to the top retrieved chunk so the
        caller still gets grounded provenance.
        """
        chunk_lookup = {chunk.chunk_id: chunk for chunk in chunks}
        chosen_ids = [chunk_id for chunk_id in cited_chunk_ids if chunk_id in chunk_lookup]
        if not chosen_ids and chunks:
            chosen_ids = [chunks[0].chunk_id]

        return [
            Citation(
                chunk_id=chunk_lookup[chunk_id].chunk_id,
                document_name=chunk_lookup[chunk_id].document_name,
                source_uri=chunk_lookup[chunk_id].source_uri,
                relevance_score=chunk_lookup[chunk_id].fused_score,
            )
            for chunk_id in chosen_ids
        ]

