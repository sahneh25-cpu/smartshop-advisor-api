from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dynamic_question_flow_known_category_returns_questions():
    # تست جریان عادی برای دسته بندی مشخص
    response = client.post(
        "/api/v1/ai/dynamic-question-flow",
        json={"user_query": "گوشی موبایل"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["questions"], list)
    assert len(data["questions"]) > 0

def test_dynamic_flow_extracts_info_and_filters_questions():
    # سناریو: کاربر از قبل بودجه و نوع محصول را گفته است
    user_query = "یه لپ تاپ برای برنامه نویسی با بودجه 50 میلیون میخوام"

    response = client.post(
        "/api/v1/ai/dynamic-question-flow",
        json={"user_query": user_query},
    )

    assert response.status_code == 200
    data = response.json()

    # 1. چک کردن استخراج درست نوع محصول (مقایسه مستقیم با رشته فارسی)
    assert "لپ تاپ" in data["product_type"]

    # 2. چک کردن حذف سوال بودجه (چون در کوئری بوده)
    question_keys = [q["key"] for q in data["questions"]]
    assert "budget" not in question_keys, "System should not ask for budget if it's already provided in query"
