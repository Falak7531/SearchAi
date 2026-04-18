"""LLM client abstraction for Groq and Ollama chat generation."""

from __future__ import annotations

import json
import re

import httpx

from app.rag.config import RAGConfig
from app.rag.types import GeneratedAnswer


class LLMClient:
    """Generate grounded answers with Groq or Ollama."""

    def __init__(self, config: RAGConfig):
        """Initialize the selected LLM provider."""
        self.config = config
        self.provider = config.generation.provider.lower()
        self._groq_client = None

        if self.provider == "groq":
            from groq import AsyncGroq
            api_key = config.get_env("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY is required when generation.provider=groq.")
            self._groq_client = AsyncGroq(api_key=api_key)
        elif self.provider != "ollama":
            raise ValueError(f"Unsupported generation provider: {self.provider}")

    async def generate(self, messages: list[dict[str, str]]) -> GeneratedAnswer:
        """Generate a grounded answer and parse it into structured output."""
        if self.provider == "groq":
            return await self._generate_groq(messages)
        return await self._generate_ollama(messages)

    async def _generate_groq(self, messages: list[dict[str, str]]) -> GeneratedAnswer:
        """Call Groq Chat Completions with JSON output."""
        response = await self._groq_client.chat.completions.create(
            model=self.config.generation.groq_model,
            messages=messages,
            temperature=self.config.generation.temperature,
            max_tokens=self.config.generation.max_tokens,
            response_format={"type": "json_object"},
        )
        raw_content = response.choices[0].message.content or "{}"
        return self._parse_json_response(raw_content)

    async def _generate_ollama(self, messages: list[dict[str, str]]) -> GeneratedAnswer:
        """Call a local Ollama instance with chat-style messages."""
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{self.config.generation.ollama_base_url}/api/chat",
                json={
                    "model": self.config.generation.ollama_model,
                    "messages": messages,
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": self.config.generation.temperature,
                        "num_predict": self.config.generation.max_tokens,
                    },
                },
            )
            response.raise_for_status()
            raw_content = response.json().get("message", {}).get("content", "{}")
        return self._parse_json_response(raw_content)

    def _parse_json_response(self, raw_content: str) -> GeneratedAnswer:
        """Parse the model's JSON response with a defensive fallback."""
        try:
            payload = json.loads(raw_content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw_content, re.DOTALL)
            if not match:
                return GeneratedAnswer(
                    answer=raw_content.strip(),
                    reasoning_summary="The model returned an unstructured response.",
                    insufficient_context=False,
                    cited_chunk_ids=[],
                    raw_response=raw_content,
                )
            payload = json.loads(match.group(0))

        return GeneratedAnswer(
            answer=str(payload.get("answer", "")).strip(),
            reasoning_summary=str(payload.get("reasoning_summary", "")).strip(),
            insufficient_context=bool(payload.get("insufficient_context", False)),
            cited_chunk_ids=[str(item) for item in payload.get("citations", [])],
            raw_response=raw_content,
        )

