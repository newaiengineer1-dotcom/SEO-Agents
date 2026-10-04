from __future__ import annotations

from crewai import LLM
from .config import GROQ_BASE_URL, DEFAULT_MODEL, normalize_groq_model


def build_llm(api_key: str, model: str = DEFAULT_MODEL, temperature: float = 0.2):
    if not api_key or not api_key.strip():
        raise ValueError("A Groq API key is required.")

    # IMPORTANT: CrewAI/LiteLLM provider parsing can strip the first model
    # namespace. The custom_openai/ prefix makes the literal Groq model ID
    # `openai/gpt-oss-20b` reach Groq unchanged.
    groq_model = normalize_groq_model(model)
    crew_model = f"custom_openai/{groq_model}"

    return LLM(
        model=crew_model,
        base_url=GROQ_BASE_URL,
        api_key=api_key.strip(),
        temperature=temperature,
    )
