import json
from app.schemas.ai import UserIntent
from app.services.ai_provider import AIProvider


class QueryUnderstandingService:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def interpret(self, user_query: str) -> UserIntent:
        prompt = f"""
You are an expert shopping assistant.
Extract structured information from the user query.

Return ONLY valid JSON with this exact schema:
{{
  "product_type": string | null,
  "budget": integer | null,
  "priorities": list[string],
  "extracted_features": object
}}

User Query: "{user_query}"
"""

        try:
            raw_response = self.provider.complete_text(prompt)

            ticks = chr(96) * 3
            clean = raw_response.strip()
            clean = clean.replace(f"{ticks}json", "").replace(ticks, "").strip()

            data = json.loads(clean)

            return UserIntent(
                product_type=data.get("product_type"),
                budget=data.get("budget"),
                priorities=data.get("priorities", []) or [],
                extracted_features=data.get("extracted_features", {}) or {},
            )
        except Exception:
            return UserIntent(
                product_type=None,
                budget=None,
                priorities=[],
                extracted_features={},
            )
