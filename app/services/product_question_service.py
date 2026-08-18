from app.schemas.ai import ProductQuestionsResponse
from app.services.ai_provider import AIProvider
from app.services.query_understanding_service import QueryUnderstandingService

class ProductQuestionService:
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider
        # ایجاد نمونه از مفسر پرسش
        self.interpreter = QueryUnderstandingService(provider)

    def get_product_questions(self, product_name: str) -> ProductQuestionsResponse:
        return self.provider.generate_product_questions(product_name)

    def get_dynamic_questions(self, user_query: str) -> ProductQuestionsResponse:
        # 1. استخراج اطلاعات ساختاریافته (اینجا بودجه و نوع محصول در میاد)
        intent = self.interpreter.interpret(user_query)
        
        # 2. تعیین نام محصول برای فرستادن به AI Provider
        # اگر اینترپتر محصول را پیدا کرد (مثلا "لپ تاپ") از همان استفاده کن
        # در غیر این صورت به عنوان fallback از کل کوئری استفاده کن
        final_product_type = intent.product_type if intent.product_type else user_query
        
        # 3. گرفتن سوالات پایه از AI Provider
        response = self.provider.generate_product_questions(final_product_type)
        
        # 4. اعمال فیلترینگ بر اساس اطلاعاتی که از قبل داریم
        filtered_questions = response.questions
        
        # اگر بودجه شناسایی شده سوال بودجه را حذف کن
        if intent.budget is not None:
            filtered_questions = [q for q in filtered_questions if q.key != "budget"]
            
        # خروجی نهایی باید شامل نوع محصول استخراج شده باشد
        return ProductQuestionsResponse(
            product_type=final_product_type,
            questions=filtered_questions
        )
