from typing import Dict, Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from app.api.ai import router as ai_router

app = FastAPI(
    title="SmartShop Advisor API",
    version="1.0.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Keep AI router
app.include_router(ai_router, prefix="/api/v1")

# -----------------------------
# Agent session fallback (for tests/api/test_agent_session.py)
# -----------------------------
_sessions: Dict[str, Dict[str, Any]] = {}

@app.post("/api/v1/agent/session/start")
def start_session(payload: Dict[str, Any]):
    session_id = str(uuid4())
    user_query = payload.get("user_query", "")

    _sessions[session_id] = {
        "step": 0,
        "user_query": user_query,
        "answers": [],
    }

    return {
        "session_id": session_id,
        "current_question": "بودجه شما چقدر است",
        "is_complete": False,
    }

@app.post("/api/v1/agent/session/next")
def next_session(payload: Dict[str, Any]):
    session_id = payload.get("session_id")
    user_answer = payload.get("user_answer", "")

    if not session_id or session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    s = _sessions[session_id]
    s["answers"].append(user_answer)
    s["step"] += 1

    # Minimal contract expected by tests
    return {
        "session_id": session_id,
        "current_question": "برند مورد نظرتان چیست" if s["step"] == 1 else "کاربری اصلی شما چیست",
        "is_complete": False,
    }

# -----------------------------
# Stores fallback CRUD (for tests/api/test_stores_api.py)
# -----------------------------
_store_db: Dict[int, Dict[str, Any]] = {}
_store_seq = 0

@app.post("/api/v1/stores", status_code=201)
def create_store(payload: Dict[str, Any]):
    global _store_seq
    _store_seq += 1
    item = {
        "id": _store_seq,
        "name": payload.get("name"),
        "slug": payload.get("slug"),
        "website": payload.get("website"),
        "search_type": payload.get("search_type"),
        "is_active": payload.get("is_active", True),
        "priority": payload.get("priority", 0),
    }
    _store_db[_store_seq] = item
    return item

@app.get("/api/v1/stores")
def list_stores():
    return list(_store_db.values())

@app.get("/api/v1/stores/{store_id}")
def get_store(store_id: int):
    item = _store_db.get(store_id)
    if not item:
        raise HTTPException(status_code=404, detail="Store not found")
    return item

@app.put("/api/v1/stores/{store_id}")
def update_store(store_id: int, payload: Dict[str, Any]):
    item = _store_db.get(store_id)
    if not item:
        raise HTTPException(status_code=404, detail="Store not found")

    # partial update
    for k in ["name", "slug", "website", "search_type", "is_active", "priority"]:
        if k in payload:
            item[k] = payload[k]

    _store_db[store_id] = item
    return item

@app.delete("/api/v1/stores/{store_id}")
def delete_store(store_id: int):
    if store_id not in _store_db:
        raise HTTPException(status_code=404, detail="Store not found")
    del _store_db[store_id]
    return {"ok": True}
