from crewai import LLM
from .config import GROQ_BASE_URL, DEFAULT_MODEL

def build_llm(api_key: str, model: str = DEFAULT_MODEL, temperature: float = 0.2):
    if not api_key or not api_key.strip():
        raise ValueError("A Groq API key is required.")
    return LLM(
        model=model,
        custom_openai=True,
        base_url=GROQ_BASE_URL,
        api_key=api_key.strip(),
        temperature=temperature,
    )
