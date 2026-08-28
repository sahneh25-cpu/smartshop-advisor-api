import json
import logging
import os
from abc import ABC, abstractmethod
import requests

from app.schemas.ai import ProductQuestionsResponse, ProductQuestion

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    @abstractmethod
    def generate_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        pass

    @abstractmethod
    def complete_text(self, prompt: str) -> str:
        pass


class LocalAIProvider(AIProvider):
    def generate_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        return ProductQuestionsResponse(
            product_type=product_name,
            questions=[
                ProductQuestion(
                    key="usage",
                    label="کاربری شما چیست؟",
                    type="choice",
                    options=[
                        "عمومی و روزمره",
                        "حرفه‌ای و تخصصی",
                        "اقتصادی",
                        "گیمینگ/سرگرمی",
                    ],
                ),
                ProductQuestion(
                    key="budget",
                    label="بودجه شما چقدر است؟ (تومان)",
                    type="number",
                    options=[],
                ),
                ProductQuestion(
                    key="brand_preference",
                    label="برند خاصی مد نظر دارید؟",
                    type="choice",
                    options=["سامسونگ", "اپل", "شیائومی", "ایسوس", "سایر"],
                ),
            ],
        )

    def complete_text(self, prompt: str) -> str:
        if "لپ‌تاپ" in prompt or "لپ تاپ" in prompt:
            return '{"product_type": "لپ تاپ", "budget": 50000000, "priorities": ["programming"]}'
        return '{"product_type": null, "budget": null, "priorities": []}'


class GeminiProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.base_url = os.getenv(
            "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
        ).rstrip("/")
        self.model = "gemini-1.5-flash"
        self.fallback = LocalAIProvider()

    def _call_gemini(self, prompt: str) -> str:
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not set. Falling back to local.")
            return ""

        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "response_mime_type": "application/json",
            },
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=12)
            if response.status_code == 200:
                data = response.json()
                if "raw_text" in data:
                    return data["raw_text"]
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logger.error(
                    f"Gemini API error: {response.status_code} - {response.text}"
                )
                return ""
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return ""

    def generate_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        prompt = (
            f'You are a smart shopping advisor. The user is looking to buy: "{product_name}". '
            "Analyze the product and generate 2 to 4 crucial dynamic questions in Persian. "
            "Extract the clean product_type name in Persian. "
            "Return ONLY a JSON object matching this schema: "
            '{"product_type": "string", "questions": [{"key": "string", "label": "string", "type": "choice|number|text", "options": ["string"]}]}'
        )
        raw_text = self._call_gemini(prompt)
        if raw_text:
            try:
                clean = raw_text.strip().strip("`")
                if clean.startswith("json"):
                    clean = clean[4:].strip()
                data = json.loads(clean)
                return ProductQuestionsResponse(**data)
            except Exception as e:
                logger.error(f"Failed to parse Gemini response: {e}")

        return self.fallback.generate_product_questions(product_name)

    def complete_text(self, prompt: str) -> str:
        raw_text = self._call_gemini(prompt)
        if raw_text:
            return raw_text
        return self.fallback.complete_text(prompt)
