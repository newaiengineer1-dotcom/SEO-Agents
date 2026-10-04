from dataclasses import dataclass

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b"

@dataclass(frozen=True)
class AppConfig:
    model: str = DEFAULT_MODEL
    temperature: float = 0.2
    max_tokens: int = 6000
