import json
import re
from typing import Any, Dict
from google import genai
from app.core.config import settings

class AdvisorService:
    def __init__(self, provider=None) -> None:
        self.provider = provider
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_id = "gemini-2.0-flash"

    async def recommend(self, user_input: str, history: list | None = None) -> Dict[str, Any]:
        prompt = f"User Input: {user_input}\nReturn ONLY a JSON object."
        try:
            response = self.client.models.generate_content(model=self.model_id, contents=prompt)
            return self._safe_parse_json(response.text)
        except Exception as e:
            return {"analysis": "Error", "recommendations": [], "next_questions": [], "error": str(e)}

    def _safe_parse_json(self, text: str) -> Dict[str, Any]:
        try:
            cleaned = text.strip()
            fence = chr(96) * 3
            if cleaned.startswith(f"{fence}json"):
                cleaned = cleaned[len(f"{fence}json"):].lstrip()
            elif cleaned.startswith(fence):
                cleaned = cleaned[len(fence):].lstrip()
            if cleaned.endswith(fence):
                cleaned = cleaned[:-len(fence)].rstrip()
            if cleaned.startswith("{") and cleaned.endswith("}"):
                return json.loads(cleaned)
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise ValueError("No JSON")
        except Exception:
            return {"analysis": "Failed", "recommendations": [], "next_questions": ["Clarify?"], "raw_text": text[:200]}

