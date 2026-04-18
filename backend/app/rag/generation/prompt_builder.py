"""Prompt construction for grounded RAG generation."""

from __future__ import annotations

from app.rag.types import RetrievedChunk


STRICT_SYSTEM_PROMPT = """You are a retrieval-augmented assistant.

Rules:
1. Answer ONLY from the supplied context.
2. Do not use outside knowledge, even if you believe it is correct.
3. If the context is insufficient, set "insufficient_context" to true and say you do not have enough context.
4. Keep the reasoning_summary short and evidence-based. Do not reveal hidden chain-of-thought.
5. Return valid JSON with these keys:
   - reasoning_summary: string
   - answer: string
   - insufficient_context: boolean
   - citations: array of chunk IDs used in the answer
"""


class PromptBuilder:
    """Build grounded prompts from retrieved chunks."""

    def build_messages(self, query: str, chunks: list[RetrievedChunk]) -> list[dict[str, str]]:
        """Create chat messages for the configured LLM client."""
        context_blocks = []
        for chunk in chunks:
            context_blocks.append(
                "\n".join(
                    [
                        f"[chunk_id] {chunk.chunk_id}",
                        f"[document_name] {chunk.document_name}",
                        f"[source_uri] {chunk.source_uri}",
                        f"[relevance_score] {chunk.fused_score:.4f}",
                        "[content]",
                        chunk.content,
                    ]
                )
            )

        context_separator = "\n\n---\n\n"
        user_prompt = (
            "User question:\n"
            f"{query}\n\n"
            "Retrieved context:\n"
            f"{context_separator.join(context_blocks)}"
        )
        return [
            {"role": "system", "content": STRICT_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
