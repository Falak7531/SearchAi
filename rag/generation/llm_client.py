"""LLM client abstraction: Groq ↔ Ollama via one config flag."""
from __future__ import annotations

import re
from typing import Any

import httpx
from groq import AsyncGroq

from rag.utils import logger, require_env

_ANSWER_RE = re.compile(r"<answer>(.*?)</answer>", re.DOTALL | re.IGNORECASE)


class LLMClient:
    """Async LLM client supporting Groq and Ollama backends."""

    def __init__(self, cfg: dict[str, Any]) -> None:
        self.cfg = cfg["generation"]
        self.provider = self.cfg["provider"]
        self.temperature = self.cfg["temperature"]
        self.max_tokens = self.cfg["max_tokens"]

        if self.provider == "groq":
            self._groq = AsyncGroq(api_key=require_env("GROQ_API_KEY"))
            self._model = self.cfg["groq_model"]
        elif self.provider == "ollama":
            self._http = httpx.AsyncClient(
                base_url=self.cfg["ollama_base_url"], timeout=120.0
            )
            self._model = self.cfg["ollama_model"]
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

        logger.info("LLMClient ready: provider=%s model=%s", self.provider, self._model)

    async def generate(self, messages: list[dict[str, str]]) -> str:
        """Generate a completion and extract the <answer> block."""
        if self.provider == "groq":
            raw = await self._call_groq(messages)
        else:
            raw = await self._call_ollama(messages)
        return self._extract_answer(raw)

    async def _call_groq(self, messages: list[dict[str, str]]) -> str:
        resp = await self._groq.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return resp.choices[0].message.content or ""

    async def _call_ollama(self, messages: list[dict[str, str]]) -> str:
        payload = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }
        r = await self._http.post("/api/chat", json=payload)
        r.raise_for_status()
        return r.json()["message"]["content"]

    @staticmethod
    def _extract_answer(raw: str) -> str:
        """Strip <reasoning> CoT and return only the user-facing answer."""
        m = _ANSWER_RE.search(raw)
        if m:
            return m.group(1).strip()
        return raw.strip()
