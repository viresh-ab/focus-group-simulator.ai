"""OpenAI-compatible LLM integration for local or hosted endpoints."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import requests


class LocalLLMClient:
    """Simple client for OpenAI-compatible /chat/completions APIs."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        timeout_seconds: int = 120,
    ) -> None:
        # Backward compatibility with existing LOCAL_* variables.
        self.base_url = (
            base_url
            or os.getenv("LLM_BASE_URL")
            or os.getenv("LOCAL_LLM_BASE_URL")
            or "https://api.openai.com/v1"
        ).rstrip("/")
        self.model = model or os.getenv("LLM_MODEL") or os.getenv("LOCAL_LLM_MODEL") or "gpt-4o-mini"
        self.api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("LOCAL_LLM_API_KEY") or ""
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str, system_prompt: str = "You are a helpful assistant.", temperature: float = 0.7) -> str:
        url = f"{self.base_url}/chat/completions"
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout_seconds)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


def format_messages(messages: List[Dict[str, str]]) -> str:
    """Optional helper if you later need to debug multi-turn prompts."""
    return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
