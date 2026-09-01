import json
from typing import Any, Dict, Optional
from app.schemas.ai import UserIntent
from app.services.ai_provider import AIProvider


class QueryUnderstandingService:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def interpret(
        self, user_query: str, current_answers: Optional[Dict[str, Any]] = None
    ) -> UserIntent:
        answers = current_answers or {}
        prompt = f"""
You are an expert shopping assistant helper agent.
Extract structured information from the user query and current answers.

Return ONLY valid JSON with this exact schema:
{{
  "product_type": string | null,
  "budget": integer | null,
  "priorities": list[string],
  "extracted_features": object,
  "missing_slots": list[string]
}}

User Query: "{user_query}"
Current User Answers: {json.dumps(answers, ensure_ascii=False)}
"""

        try:
            raw_response = self.provider.complete_text(prompt)

            ticks = chr(96) * 3
            clean = raw_response.strip()
            clean = clean.replace(f"{ticks}json", "").replace(ticks, "").strip()

            data = json.loads(clean)

            product_type = data.get("product_type")
            budget = data.get("budget")
            priorities = data.get("priorities", []) or []
            extracted_features = data.get("extracted_features", {}) or {}
            missing_slots = data.get("missing_slots", []) or []

            # ادغام پاسخ‌های کاربر با نتایج هوش مصنوعی
            if not budget and "budget" in answers:
                try:
                    budget = float(answers["budget"])
                except (ValueError, TypeError):
                    pass

            # محاسبه هوشمند فیلدهای مفقود در صورتی که مدل آنها را خالی فرستاده باشد
            if not missing_slots:
                if budget is None and "budget" not in answers:
                    missing_slots.append("budget")
                if not priorities and "usage" not in answers:
                    missing_slots.append("usage")
                if "brand_preference" not in answers and "brand" not in extracted_features:
                    missing_slots.append("brand_preference")

            return UserIntent(
                product_type=product_type,
                budget=budget,
                priorities=priorities,
                extracted_features=extracted_features,
                missing_slots=missing_slots,
            )
        except Exception:
            # Fallback امن
            fallback_missing = []
            if "budget" not in answers:
                fallback_missing.append("budget")
            if "usage" not in answers:
                fallback_missing.append("usage")

            return UserIntent(
                product_type=None,
                budget=None,
                priorities=[],
                extracted_features={},
                missing_slots=fallback_missing,
            )
