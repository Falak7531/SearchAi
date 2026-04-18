"""Document chunking using LangChain's recursive text splitter."""

from __future__ import annotations

import hashlib

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.config import RAGConfig
from app.rag.types import ChunkRecord, RawDocument


class DocumentChunker:
    """Split source documents into retrieval-friendly chunks."""

    def __init__(self, config: RAGConfig):
        """Create a chunker from the shared YAML config."""
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunking.chunk_size,
            chunk_overlap=config.chunking.chunk_overlap,
            separators=config.chunking.separators,
            add_start_index=True,
        )

    def chunk_documents(self, documents: list[RawDocument]) -> list[ChunkRecord]:
        """Split multiple documents into chunk records with source tracking."""
        chunks: list[ChunkRecord] = []
        for document in documents:
            chunks.extend(self.chunk_document(document))
        return chunks

    def chunk_document(self, document: RawDocument) -> list[ChunkRecord]:
        """Split a single document into stable chunk records."""
        split_docs = self._splitter.create_documents(
            texts=[document.content],
            metadatas=[document.metadata | {"document_id": document.document_id}],
        )

        chunks: list[ChunkRecord] = []
        for index, split_doc in enumerate(split_docs):
            chunk_text = split_doc.page_content.strip()
            if not chunk_text:
                continue
            start_index = split_doc.metadata.get("start_index", 0)
            chunk_id = hashlib.sha1(
                f"{document.document_id}:{index}:{chunk_text}".encode("utf-8")
            ).hexdigest()
            chunks.append(
                ChunkRecord(
                    chunk_id=chunk_id,
                    document_id=document.document_id,
                    document_name=document.document_name,
                    source_uri=document.source_uri,
                    content=chunk_text,
                    chunk_index=index,
                    token_count=len(chunk_text.split()),
                    metadata=document.metadata | {"start_index": start_index},
                )
            )
        return chunks

