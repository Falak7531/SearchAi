"""Production-ready RAG pipeline package."""
try:
    from rag.pipeline import RAGPipeline
    __all__ = ["RAGPipeline"]
except ImportError:
    # Graceful degradation if deps missing
    __all__ = []
