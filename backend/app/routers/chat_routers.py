# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app import models
# from app.ai_service import generate_ai_response
# from app.routers.auth_router import get_current_user
# from pydantic import BaseModel
# router = APIRouter(prefix="/chat", tags=["Chat"])


# class ChatRequest(BaseModel):
#     message: str


# @router.post("/send_message")
# def send_message(
#     request: ChatRequest,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     message = request.message
#     """
#     Receives a message from the authenticated user, generates an AI response,
#     saves both to the same chat session, and returns them.
#     """

#     # ✅ Ensure session exists or create a new one
#     session = db.query(models.ChatSession).filter_by(
#         user_id=current_user.id).first()
#     if not session:
#         session = models.ChatSession(user_id=current_user.id, title="New Chat")
#         db.add(session)
#         db.commit()
#         db.refresh(session)

#     # 1️⃣ Save user message
#     user_msg = models.ChatMessage(session_id=session.id, content=message)
#     db.add(user_msg)
#     db.commit()
#     db.refresh(user_msg)

#     # 2️⃣ Generate AI response
#     ai_reply = generate_ai_response(message)

#     # 3️⃣ Save AI message
#     ai_msg = models.ChatMessage(session_id=session.id, content=ai_reply)
#     db.add(ai_msg)
#     db.commit()
#     db.refresh(ai_msg)

#     # 4️⃣ Return both
#     return {
#         "session_id": session.id,
#         "user_id": current_user.id,
#         "user_message": user_msg.content,
#         "ai_response": ai_msg.content
#     }

# backend/app/routers/chat_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.routers.auth_router import get_current_user
from app.ai_service import generate_ai_response  # your existing LLM wrapper
from app.weather_service import get_weather_by_city
from app.utils.weather_utils import get_weather
from app.models import ChatSession, ChatMessage

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(
        ChatSession.id == request.session_id).first()

    user_message = ChatMessage(
        session_id=session.id, content=request.message, role="user")
    db.add(user_message)
    db.commit()

    # 🔹 Handle pending weather action
    if session.pending_action == "awaiting_city":
        city = request.message.strip()
        weather_info = get_weather(city)

        bot_reply = ChatMessage(session_id=session.id,
                                content=weather_info, role="assistant")
        db.add(bot_reply)

        # Reset pending action
        session.pending_action = None
        db.commit()
        return {"reply": weather_info}

    # 🔹 If user asks for weather
    if any(word in request.message.lower() for word in ["weather", "whether", "temperature", "forecast"]):
        session.pending_action = "awaiting_city"
        db.commit()

        prompt = "Please provide the name of the city you want the weather for."
        bot_reply = ChatMessage(session_id=session.id,
                                content=prompt, role="assistant")
        db.add(bot_reply)
        db.commit()
        return {"reply": prompt}

    # 🔹 Default chatbot response (for normal questions)
    response = generate_ai_response(request.message)
    ai_msg = models.ChatMessage(session_id=session.id,
                                content=response, role="assistant")
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)

    return {"reply": response}


@router.post("/send_message")
def send_message(request: ChatRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    message_text = request.message.strip()

    # find latest session or create
    session = db.query(models.ChatSession).filter_by(
        user_id=current_user.id).order_by(models.ChatSession.created_at.desc()).first()
    if not session:
        session = models.ChatSession(user_id=current_user.id, title="New Chat")
        db.add(session)
        db.commit()
        db.refresh(session)

    # If session.pending_action ==   "awaiting_city", treat this message as city name
    if session.pending_action == "awaiting_city":
        city = message_text
        try:
            weather_msg = get_weather_by_city(city)
        except ValueError as e:
            # invalid city or OWM returned error
            ai_msg_text = f"Sorry, I couldn't retrieve weather for '{city}'. Please provide a valid city name."
            # store the AI message and keep pending_action as awaiting_city (so user can try again)
            ai_msg = models.ChatMessage(
                session_id=session.id, content=ai_msg_text, role="assistant")
            db.add(ai_msg)
            db.commit()
            db.refresh(ai_msg)
            return {"session_id": session.id, "user_message": message_text, "ai_response": ai_msg_text}
        except Exception:
            ai_msg_text = "Sorry, I couldn't retrieve the weather data at the moment. Please try again later."
            ai_msg = models.ChatMessage(
                session_id=session.id, content=ai_msg_text, role="assistant")
            db.add(ai_msg)
            db.commit()
            db.refresh(ai_msg)
            return {"session_id": session.id, "user_message": message_text, "ai_response": ai_msg_text}

        # on success: save user message and AI weather response, and CLEAR pending_action
        user_msg = models.ChatMessage(
            session_id=session.id, content=message_text, role="user")
        db.add(user_msg)
        ai_msg = models.ChatMessage(
            session_id=session.id, content=weather_msg, role="assistant")
        db.add(ai_msg)

        session.pending_action = None
        db.commit()
        db.refresh(ai_msg)
        return {"session_id": session.id, "user_message": message_text, "ai_response": weather_msg}

    # Normal flow: check if the user asked for weather in this message (simple keyword detection)
    lower = message_text.lower()
    if "weather" in lower or "what's the weather" in lower or "what is the weather" in lower:
        # save user message
        user_msg = models.ChatMessage(
            session_id=session.id, content=message_text, role="user")
        db.add(user_msg)
        # set session to await city
        session.pending_action = "awaiting_city"
        # prompt user
        prompt = "Please provide the name of the city you want the weather for."
        ai_msg = models.ChatMessage(
            session_id=session.id, content=prompt, role="assistant")
        db.add(ai_msg)
        db.commit()
        db.refresh(ai_msg)
        return {"session_id": session.id, "user_message": message_text, "ai_response": prompt}

    # Otherwise: normal LLM path
    # store user message
    user_msg = models.ChatMessage(
        session_id=session.id, content=message_text, role="user")
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # call your LLM wrapper function — it returns a string
    ai_response = generate_ai_response(message_text)

    ai_msg = models.ChatMessage(
        session_id=session.id, content=ai_response, role="assistant")
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)

    return {"session_id": session.id, "user_message": message_text, "ai_response": ai_response}
