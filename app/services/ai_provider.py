from abc import ABC, abstractmethod
from app.schemas.ai import ProductQuestionsResponse, ProductQuestion

class AIProvider(ABC):
    @abstractmethod
    def generate_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        pass

    @abstractmethod
    def complete_text(self, prompt: str) -> str:
        pass

class LocalAIProvider(AIProvider):
    def generate_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        # شبیه‌سازی سوالات بر اساس محصول
        return ProductQuestionsResponse(
            product_type=product_name,
            questions=[
                ProductQuestion(key="usage", label="کاربری شما چیست", type="choice", options=["اداری", "گیمینگ"]),
                ProductQuestion(key="budget", label="بودجه شما چقدر است", type="number"),
                ProductQuestion(key="brand_preference", label="برند خاصی مد نظر دارید؟", type="choice", options=["سامسونگ", "ال‌جی", "شیائومی", "اپل"])
            ]
        )


    def complete_text(self, prompt: str) -> str:
        # یک پاسخ JSON فرضی برای تست
        if "لپ تاپ" in prompt:
            return '{"product_type": "لپ تاپ", "budget": 50000000, "priorities": ["programming"]}'
        return '{"product_type": null, "budget": null, "priorities": []}'


class GeminiProvider(AIProvider):
    def generate_product_questions(self, product_name: str):
        # Safe fallback to keep imports/tests alive
        return LocalAIProvider().generate_product_questions(product_name)

    def complete_text(self, prompt: str) -> str:
        # Safe fallback to keep flow alive in tests
        return LocalAIProvider().complete_text(prompt)
