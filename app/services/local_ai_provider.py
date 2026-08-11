from app.schemas.ai import ProductQuestion
from app.schemas.ai import ProductQuestionsResponse
from app.services.ai_provider import AIProvider


class LocalAIProvider(AIProvider):
    def generate_product_questions(
        self,
        product_name: str,
    ) -> ProductQuestionsResponse:
        normalized_name = product_name.strip()

        if "تلویزیون" in normalized_name:
            return ProductQuestionsResponse(
                product_type="تلویزیون",
                questions=[
                    ProductQuestion(
                        key="screen_size",
                        label="چه سایزی برای تلویزیون مدنظر دارید؟",
                        type="select",
                        options=[
                            "32 اینچ",
                            "43 اینچ",
                            "50 اینچ",
                            "55 اینچ",
                            "65 اینچ",
                            "75 اینچ",
                        ],
                        help_text=(
                            "برای اتاق کوچک 32 تا 43، پذیرایی متوسط 50 تا 55 "
                            "و سالن بزرگ 65 اینچ به بالا مناسب‌تر است."
                        ),
                    ),
                    ProductQuestion(
                        key="resolution",
                        label="کیفیت تصویر موردنظرتان چیست؟",
                        type="select",
                        options=["Full HD", "4K", "8K"],
                        help_text="برای خرید معمولی، 4K انتخاب رایج و مناسب‌تری است.",
                    ),
                    ProductQuestion(
                        key="budget",
                        label="بودجه تقریبی شما چقدر است؟",
                        type="text",
                        options=[],
                        help_text="بودجه کمک می‌کند گزینه‌های نامرتبط حذف شوند.",
                    ),
                ],
            )

        return ProductQuestionsResponse(
            product_type=normalized_name,
            questions=[
                ProductQuestion(
                    key="budget",
                    label="بودجه تقریبی شما چقدر است؟",
                    type="text",
                    options=[],
                    help_text=None,
                ),
                ProductQuestion(
                    key="brand",
                    label="برند خاصی مدنظرتان است؟",
                    type="text",
                    options=[],
                    help_text=None,
                ),
                ProductQuestion(
                    key="main_priority",
                    label="مهم‌ترین اولویت شما چیست؟",
                    type="select",
                    options=[
                        "قیمت مناسب",
                        "کیفیت بالا",
                        "امکانات بیشتر",
                        "برند معتبر",
                    ],
                    help_text=None,
                ),
            ],
        )
