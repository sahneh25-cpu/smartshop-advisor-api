from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.schemas.agent import (
    StartSessionRequest,
    StartSessionResponse,
    NextSessionRequest,
    NextSessionResponse,
)

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])

_sessions: dict[str, dict[str, object]] = {}


@router.post("/session/start", response_model=StartSessionResponse)
async def start_session(payload: StartSessionRequest) -> StartSessionResponse:
    session_id = str(uuid4())
    _sessions[session_id] = {
        "user_query": payload.user_query,
        "step": 1,
        "answers": [],
    }
    return StartSessionResponse(
        session_id=session_id,
        current_question="بودجه‌ات حدوداً چقدره؟",
        is_complete=False,
    )


@router.post("/session/next", response_model=NextSessionResponse)
async def next_session(payload: NextSessionRequest) -> NextSessionResponse:
    session = _sessions.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session["answers"].append(payload.user_answer)
    session["step"] = int(session["step"]) + 1

    if session["step"] == 2:
        return NextSessionResponse(
            session_id=payload.session_id,
            current_question="برند خاصی مدنظرته؟",
            is_complete=False,
        )

    return NextSessionResponse(
        session_id=payload.session_id,
        current_question="ممنون، اطلاعات کافی داریم.",
        is_complete=True,
    )
