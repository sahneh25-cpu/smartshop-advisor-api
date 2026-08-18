import pytest
from unittest.mock import MagicMock, patch
from app.services.advisor import AdvisorService

@pytest.fixture
def advisor_service():
    return AdvisorService()

@pytest.mark.asyncio
async def test_recommend_success(advisor_service):
    mock_response = MagicMock()
    mock_response.text = '{"analysis": "test", "recommendations": ["item"], "next_questions": ["q"]}'
    with patch.object(advisor_service.client.models, "generate_content", return_value=mock_response):
        result = await advisor_service.recommend("laptop")
    assert result["analysis"] == "test"

@pytest.mark.asyncio
async def test_safe_parse_json_with_markdown(advisor_service):
    json_text = '{"analysis": "md", "recommendations": [], "next_questions": []}'
    fence = chr(96) * 3
    markdown_text = f"{fence}json\n{json_text}\n{fence}"
    result = advisor_service._safe_parse_json(markdown_text)
    assert result["analysis"] == "md"
