from app.schemas.ai import ProductQuestion, ProductQuestionsResponse
from app.services.ai_provider import AIProvider
from app.services.category_questions import all_questions_for, product_type_label


class LocalAIProvider(AIProvider):
    def generate_product_questions(
        self,
        product_name: str,
    ) -> ProductQuestionsResponse:
        raw = all_questions_for(product_name, {})
        return ProductQuestionsResponse(
            product_type=product_type_label(product_name),
            questions=[ProductQuestion.model_validate(q) for q in raw],
        )

    def complete_text(self, prompt: str) -> str:
        from app.services.ai_provider import LocalAIProvider as CoreLocal

        return CoreLocal().complete_text(prompt)
