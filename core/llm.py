"""CrewAI LLM factory for Groq's OpenAI-compatible API.

Uses CrewAI's native custom_openai=True integration and does not require LiteLLM.
"""

from __future__ import annotations

import os
from typing import Optional

from crewai import LLM


GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def normalize_groq_model(model: Optional[str]) -> str:
    """Return a valid Groq model ID without provider prefixes."""
    value = (model or "openai/gpt-oss-20b").strip()

    # Remove prefixes that can cause CrewAI provider parsing errors.
    if value.startswith("custom_openai/"):
        value = value[len("custom_openai/"):]
    if value.startswith("groq/"):
        value = value[len("groq/"):]

    # Groq's current GPT-OSS model IDs use the openai/ prefix.
    if value in {"gpt-oss-20b", "openai/gpt-oss-20b"}:
        return "openai/gpt-oss-20b"
    if value in {"gpt-oss-120b", "openai/gpt-oss-120b"}:
        return "openai/gpt-oss-120b"

    return value


def build_groq_llm(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> LLM:
    """Build a CrewAI LLM using Groq's OpenAI-compatible endpoint."""
    key = (api_key or os.getenv("GROQ_API_KEY") or "").strip()
    if not key:
        raise ValueError("Groq API key is required.")

return LLM(
    model=groq_model,
    custom_openai=True,
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key.strip(),
    temperature=temperature,
)
