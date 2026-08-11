from __future__ import annotations

import json
from typing import Protocol

import httpx

from app.core.config import settings
from app.schemas.ai import ProductQuestion, ProductQuestionsResponse


class AIProvider(Protocol):
    def generate_product_questions(
        self,
        product_name: str,
    ) -> ProductQuestionsResponse:
        ...


class LocalAIProvider:
    def generate_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        return ProductQuestionsResponse(
            product_type=product_name,
            questions=[
                ProductQuestion(
                    key="budget",
                    label="بودجه شما چقدر است؟",
                    type="text",
                    options=[],
                    help_text="محدوده قیمت موردنظر را بنویسید.",
                ),
                ProductQuestion(
                    key="brand",
                    label="برند خاصی مدنظر دارید؟",
                    type="text",
                    options=[],
                    help_text="اگر برند خاصی ترجیح می‌دهید، وارد کنید.",
                ),
                ProductQuestion(
                    key="usage",
                    label="بیشتر برای چه کاری می‌خواهید؟",
                    type="text",
                    options=[],
                    help_text="مثلاً کار، بازی، عکاسی یا استفاده روزمره.",
                ),
            ],
        )


class GeminiProvider:
    def generate_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        if not settings.gemini_api_key:
            return LocalAIProvider().generate_product_questions(product_name)

        url = f"{settings.gemini_base_url}/models/gemini-1.5-flash:generateContent"
        headers = {
            "x-goog-api-key": settings.gemini_api_key,
            "Content-Type": "application/json",
        }

        prompt = f"""
You are a shopping assistant.
Generate a JSON object in Persian for this product query: "{product_name}"

Return ONLY valid JSON with this exact structure:
{{
  "product_type": "string",
  "questions": [
    {{
      "key": "string",
      "label": "string",
      "type": "text",
      "options": [],
      "help_text": "string or null"
    }}
  ]
}}

Rules:
- Return 3 to 5 questions
- Use Persian text for labels and help_text
- Keep keys short and snake_case
- Do not include any extra text
""".strip()

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                    ]
                }
            ]
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
                .strip()
            )

            parsed = json.loads(text)

            questions = [
                ProductQuestion(
                    key=item["key"],
                    label=item["label"],
                    type=item.get("type", "text"),
                    options=item.get("options", []),
                    help_text=item.get("help_text"),
                )
                for item in parsed["questions"]
            ]

            return ProductQuestionsResponse(
                product_type=parsed.get("product_type", product_name),
                questions=questions,
            )

        except Exception:
            return LocalAIProvider().generate_product_questions(product_name)


class AIProviderFactory:
    @staticmethod
    def create() -> AIProvider:
        provider = (settings.ai_provider or "local").lower()
        if provider == "gemini":
            return GeminiProvider()
        return LocalAIProvider()
