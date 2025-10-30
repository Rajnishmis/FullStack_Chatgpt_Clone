from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.ai_service import generate_ai_response
from app.routers.auth_router import get_current_user
from pydantic import BaseModel
router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("/send_message")
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    message = request.message
    """
    Receives a message from the authenticated user, generates an AI response,
    saves both to the same chat session, and returns them.
    """

    # ✅ Ensure session exists or create a new one
    session = db.query(models.ChatSession).filter_by(
        user_id=current_user.id).first()
    if not session:
        session = models.ChatSession(user_id=current_user.id, title="New Chat")
        db.add(session)
        db.commit()
        db.refresh(session)

    # 1️⃣ Save user message
    user_msg = models.ChatMessage(session_id=session.id, content=message)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 2️⃣ Generate AI response
    ai_reply = generate_ai_response(message)

    # 3️⃣ Save AI message
    ai_msg = models.ChatMessage(session_id=session.id, content=ai_reply)
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)

    # 4️⃣ Return both
    return {
        "session_id": session.id,
        "user_id": current_user.id,
        "user_message": user_msg.content,
        "ai_response": ai_msg.content
    }
