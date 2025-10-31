from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """Stores user authentication information."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chats = relationship("ChatSession", back_populates="owner")


class ChatSession(Base):
    """Groups messages into a single conversation."""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="New Chat")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    pending_action = Column(String(100), nullable=True)
    owner = relationship("User", back_populates="chats")
    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    """Stores individual chat messages, content, and the vector embedding."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    content = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ✅ Add this line
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- The 1536-dimension vector field ---
    # embedding = Column(Vector(1536), nullable=True)

    session = relationship("ChatSession", back_populates="messages")
