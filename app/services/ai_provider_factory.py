import os

try:
    from app.services.ai_provider import AIProvider, GeminiProvider, LocalAIProvider
except ImportError:
    from app.services.ai_provider import AIProvider, LocalAIProvider
    GeminiProvider = None



def get_ai_provider(provider_name: str | None = None) -> AIProvider:
    name = (provider_name or "local").lower().strip()

    if name == "gemini":
        return GeminiProvider()

    return LocalAIProvider()

