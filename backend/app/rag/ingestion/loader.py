"""Source loaders for ingesting PDFs, text files, CSVs, and web pages."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from app.rag.types import RawDocument


class DocumentLoader:
    """Load heterogeneous content sources into a normalized document format."""

    def load(self, sources: Iterable[str]) -> list[RawDocument]:
        """Load multiple sources into memory."""
        documents: list[RawDocument] = []
        for source in sources:
            documents.extend(self.load_one(source))
        return documents

    def load_one(self, source: str) -> list[RawDocument]:
        """Load a single source based on its protocol or file extension."""
        if source.startswith("http://") or source.startswith("https://"):
            return [self._load_web(source)]

        path = Path(source)
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return self._load_pdf(path)
        if suffix == ".txt":
            return [self._load_text(path)]
        if suffix == ".csv":
            return self._load_csv(path)
        raise ValueError(f"Unsupported source type for ingestion: {source}")

    def _load_text(self, path: Path) -> RawDocument:
        """Load a plain-text file as a single document."""
        content = path.read_text(encoding="utf-8")
        return RawDocument(
            document_id=self._stable_id(str(path)),
            document_name=path.name,
            source_uri=str(path.resolve()),
            content=content,
            metadata={"source_type": "text"},
        )

    def _load_pdf(self, path: Path) -> list[RawDocument]:
        """Load a PDF file page-by-page.

        Page-level documents are easier to trace back to citations than one
        giant document, at the cost of slightly more metadata volume.
        """
        reader = PdfReader(str(path))
        documents: list[RawDocument] = []
        for page_number, page in enumerate(reader.pages, start=1):
            content = (page.extract_text() or "").strip()
            if not content:
                continue
            documents.append(
                RawDocument(
                    document_id=self._stable_id(f"{path}:{page_number}"),
                    document_name=f"{path.name}#page-{page_number}",
                    source_uri=str(path.resolve()),
                    content=content,
                    metadata={"source_type": "pdf", "page_number": page_number},
                )
            )
        return documents

    def _load_csv(self, path: Path) -> list[RawDocument]:
        """Load a CSV file row-by-row for granular provenance."""
        documents: list[RawDocument] = []
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row_number, row in enumerate(reader, start=1):
                content = "\n".join(f"{key}: {value}" for key, value in row.items())
                documents.append(
                    RawDocument(
                        document_id=self._stable_id(f"{path}:{row_number}"),
                        document_name=f"{path.name}#row-{row_number}",
                        source_uri=str(path.resolve()),
                        content=content,
                        metadata={"source_type": "csv", "row_number": row_number},
                    )
                )
        return documents

    def _load_web(self, url: str) -> RawDocument:
        """Fetch and clean a web page into text."""
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style", "noscript"]):
            element.extract()
        content = " ".join(soup.get_text(separator=" ").split())
        title = soup.title.text.strip() if soup.title and soup.title.text else url
        return RawDocument(
            document_id=self._stable_id(url),
            document_name=title,
            source_uri=url,
            content=content,
            metadata={"source_type": "web"},
        )

    @staticmethod
    def _stable_id(seed: str) -> str:
        """Generate a stable ID so repeated ingests deduplicate cleanly."""
        return hashlib.sha1(seed.encode("utf-8")).hexdigest()

