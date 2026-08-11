import os
import json
from typing import List, Dict, Optional
from google import genai


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash-exp"

    def analyze_and_rank_products(
        self,
        query: str,
        products: List[Dict],
        use_case: Optional[str] = None,
        priorities: Optional[List[str]] = None,
        smart_answers: Optional[Dict] = None,
    ) -> tuple:
        if not products:
            return [], "هیچ محصولی یافت نشد."

        context_parts = [f"کاربر به دنبال: {query}"]
        if use_case:
            context_parts.append(f"موارد استفاده: {use_case}")
        if priorities:
            context_parts.append(f"اولویت‌ها: {', '.join(priorities)}")
        if smart_answers:
            answers_str = "\n".join([f"- {q}: {a}" for q, a in smart_answers.items()])
            context_parts.append(f"پاسخ‌های کاربر:\n{answers_str}")
        context = "\n".join(context_parts)

        products_summary = [
            {
                "index": idx,
                "name": p.get("title", p.get("name", "نامشخص")),
                "price": p.get("price", 0),
                "source": p.get("source", ""),
            }
            for idx, p in enumerate(products)
        ]

        backtick3 = chr(96) * 3
        prompt = (
            "شما یک مشاور خرید هوشمند هستید.\n"
            + context
            + "\n\nلیست محصولات:\n"
            + json.dumps(products_summary, ensure_ascii=False, indent=2)
            + "\n\nمحصولات را رتبه‌بندی کن و توضیح فارسی 2-3 جمله‌ای بده.\n"
            + "خروجی فقط JSON باشد:\n"
            + '{"ranked_indices": [0, 1, 2], "explanation": "توضیح فارسی"}'
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            result_text = response.text.strip()
            result_text = result_text.replace(backtick3 + "json", "").replace(backtick3, "").strip()
            result = json.loads(result_text)
            ranked_indices = result.get("ranked_indices", list(range(len(products))))
            explanation = result.get("explanation", "تحلیل انجام شد.")
            ranked_products = [products[i] for i in ranked_indices if i < len(products)]
            return ranked_products, explanation
        except Exception as e:
            print(f"Gemini error: {e}")
            return products, "رتبه‌بندی هوشمند موقتا غیرفعال است."
