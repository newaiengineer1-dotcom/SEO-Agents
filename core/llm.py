"""CrewAI LLM factory for Groq OpenAI-compatible API.

Backward-compatible exports:
- build_llm: existing agents/seo_crew.py interface
- build_groq_llm: explicit Groq factory

This uses CrewAI's native custom_openai=True integration and does not require LiteLLM.
"""

from __future__ import annotations

import os
from typing import Optional

from crewai import LLM

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def normalize_groq_model(model: Optional[str]) -> str:
    """Normalize common user/provider prefixes to a Groq model ID."""
    value = (model or "openai/gpt-oss-20b").strip()

    if value.startswith("custom_openai/"):
        value = value[len("custom_openai/"):]
    if value.startswith("groq/"):
        value = value[len("groq/"):]

    if value in {"gpt-oss-20b", "openai/gpt-oss-20b"}:
        return "openai/gpt-oss-20b"
    if value in {"gpt-oss-120b", "openai/gpt-oss-120b"}:
        return "openai/gpt-oss-120b"

    return value


def build_llm(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> LLM:
    """Build the LLM using the interface expected by seo_crew.py."""
    key = (api_key or os.getenv("GROQ_API_KEY") or "").strip()
    if not key:
        raise ValueError("Groq API key is required.")

    return LLM(
        model=normalize_groq_model(model),
        custom_openai=True,
        base_url=GROQ_BASE_URL,
        api_key=key,
        temperature=temperature,
    )


def build_groq_llm(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> LLM:
    """Alias for callers using the explicit Groq factory name."""
    return build_llm(
        api_key=api_key,
        model=model,
        temperature=temperature,
    )
