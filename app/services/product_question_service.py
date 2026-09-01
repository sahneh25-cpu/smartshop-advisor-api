from typing import Any, Dict, Optional

from app.schemas.ai import ProductQuestion, ProductQuestionsResponse
from app.services.ai_provider import AIProvider
from app.services.category_questions import product_type_label, unanswered_questions
from app.services.query_understanding_service import QueryUnderstandingService


class ProductQuestionService:
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider
        self.interpreter = QueryUnderstandingService(provider)

    def get_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        return self.provider.generate_product_questions(product_name)

    def get_dynamic_questions(
        self, user_query: str, current_answers: Optional[Dict[str, Any]] = None
    ) -> ProductQuestionsResponse:
        answers = current_answers or {}
        intent = self.interpreter.interpret(user_query, answers)

        final_product_type = intent.product_type or product_type_label(user_query)

        try:
            response = self.provider.generate_product_questions(final_product_type)
        except Exception:
            response = ProductQuestionsResponse(
                product_type=final_product_type, questions=[]
            )

        catalog = unanswered_questions(user_query or final_product_type, answers)
        if catalog:
            questions = [ProductQuestion.model_validate(q) for q in catalog]
        else:
            questions = list(response.questions or [])

        skip_budget = intent.budget is not None or "budget" in answers
        if skip_budget:
            questions = [q for q in questions if q.id != "budget" and q.key != "budget"]

        missing_slots = set(intent.missing_slots or [])
        if missing_slots:
            slotted = [q for q in questions if q.id in missing_slots or q.key in missing_slots]
            if slotted:
                questions = slotted

        answered_keys = {k for k, v in answers.items() if v not in (None, "", "انتخاب کنید")}
        questions = [q for q in questions if q.id not in answered_keys and q.key not in answered_keys]

        return ProductQuestionsResponse(
            product_type=final_product_type,
            questions=questions,
        )
