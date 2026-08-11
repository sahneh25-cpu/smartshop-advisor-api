from app.schemas.ai import ProductQuestionsResponse
from app.services.ai_provider import AIProvider


class ProductQuestionService:
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider

    def get_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        return self.provider.generate_product_questions(product_name)
