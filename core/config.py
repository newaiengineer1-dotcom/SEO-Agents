from dataclasses import dataclass

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b"
SUPPORTED_MODELS = (
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
)

def normalize_groq_model(model: str) -> str:
    value = (model or DEFAULT_MODEL).strip()
    # Accept old UI values such as gpt-oss-20b and normalize them to the
    # exact IDs published by Groq.
    aliases = {
        "gpt-oss-20b": "openai/gpt-oss-20b",
        "gpt-oss-120b": "openai/gpt-oss-120b",
    }
    value = aliases.get(value, value)
    if value not in SUPPORTED_MODELS:
        raise ValueError(
            f"Unsupported Groq model '{model}'. Choose one of: {', '.join(SUPPORTED_MODELS)}"
        )
    return value

@dataclass(frozen=True)
class AppConfig:
    model: str = DEFAULT_MODEL
    temperature: float = 0.2
    max_tokens: int = 6000
