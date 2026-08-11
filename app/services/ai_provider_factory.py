from app.services.ai_provider import AIProvider, GeminiProvider, LocalAIProvider


def get_ai_provider(provider_name: str | None = None) -> AIProvider:
    name = (provider_name or "local").lower().strip()

    if name == "gemini":
        return GeminiProvider()

    return LocalAIProvider()
