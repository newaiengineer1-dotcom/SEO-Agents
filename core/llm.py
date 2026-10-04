"""CrewAI LLM factory for Groq's OpenAI-compatible endpoint.

Important:
- Uses exact Groq model IDs, including the `openai/` prefix.
- Uses CrewAI's native custom_openai=True integration.
- Does not use LiteLLM.
- Keeps the existing `build_llm` interface used by agents/seo_crew.py.
"""

from __future__ import annotations

import os
from typing import Optional

from crewai import LLM

from core.config import GROQ_BASE_URL, DEFAULT_GROQ_MODEL, normalize_groq_model


def build_llm(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> LLM:
    """Build a CrewAI LLM connected directly to Groq."""
    key = (api_key or os.getenv("GROQ_API_KEY") or "").strip()
    if not key:
        raise ValueError("Groq API key is required.")

    exact_model = normalize_groq_model(model or DEFAULT_GROQ_MODEL)

    return LLM(
        model=exact_model,
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
    """Backward-compatible alias."""
    return build_llm(
        api_key=api_key,
        model=model,
        temperature=temperature,
    )
