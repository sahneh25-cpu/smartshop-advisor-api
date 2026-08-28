from pydantic import BaseModel


class StartSessionRequest(BaseModel):
    user_query: str


class StartSessionResponse(BaseModel):
    session_id: str
    current_question: str
    is_complete: bool = False


class NextSessionRequest(BaseModel):
    session_id: str
    user_answer: str


class NextSessionResponse(BaseModel):
    session_id: str
    current_question: str
    is_complete: bool = False
