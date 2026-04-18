"""Shared helpers used across the RAG package."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator

from app.rag.types import Citation, RetrievedChunk

__all__ = ["timed", "format_citations", "truncate"]


@contextmanager
def timed() -> Iterator[dict[str, float]]:
    """Context manager that measures elapsed wall-clock time in seconds.

    Usage::

        with timed() as t:
            do_work()
        print(t["elapsed"])
    """
    bucket: dict[str, float] = {"elapsed": 0.0}
    start = time.perf_counter()
    try:
        yield bucket
    finally:
        bucket["elapsed"] = time.perf_counter() - start


def format_citations(chunks: list[RetrievedChunk]) -> list[Citation]:
    """Convert retrieved chunks into lightweight :class:`Citation` records."""
    return [
        Citation(
            chunk_id=c.chunk_id,
            document_name=c.document_name,
            source_uri=c.source_uri,
            relevance_score=c.fused_score,
        )
        for c in chunks
    ]


def truncate(text: str, max_chars: int) -> str:
    """Truncate ``text`` to ``max_chars`` characters, adding an ellipsis."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"
