"""Central configuration for the SEO Premium Agent."""

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Only use complete Groq model IDs here.
SUPPORTED_GROQ_MODELS = (
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
)

DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"


def normalize_groq_model(model: str | None) -> str:
    """Convert legacy/short model names to exact Groq model IDs."""
    value = (model or DEFAULT_GROQ_MODEL).strip()

    # Legacy provider prefixes.
    if value.startswith("custom_openai/"):
        value = value[len("custom_openai/"):]
    if value.startswith("groq/"):
        value = value[len("groq/"):]

    aliases = {
        "gpt-oss-20b": "openai/gpt-oss-20b",
        "gpt-oss-120b": "openai/gpt-oss-120b",
        "openai/gpt-oss-20b": "openai/gpt-oss-20b",
        "openai/gpt-oss-120b": "openai/gpt-oss-120b",
    }
    normalized = aliases.get(value, value)

    if normalized not in SUPPORTED_GROQ_MODELS:
        raise ValueError(
            f"Unsupported Groq model '{model}'. "
            f"Choose one of: {', '.join(SUPPORTED_GROQ_MODELS)}"
        )

    return normalized
