# app/models.py
from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import enum
import uuid
from .database import Base

Base = declarative_base()

class SessionTable(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    session_id = Column(String, unique=True, index=True)
    role = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "officer", "supervisor", "operator"
    first_login = Column(Boolean, default=None)  # null means first login
    is_logged_in = Column(Boolean, default=False)  # for session control

# backend/app/models.py


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    role = Column(String, nullable=True)  # Optional: For broadcasting
    title = Column(String)
    description = Column(String)
    target_url = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

# Add in User model:
User.notifications = relationship("Notification", back_populates="user", cascade="all, delete")

# backend/app/models.py



class RequestStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ToolAdditionRequest(Base):
    __tablename__ = "tool_addition_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, default=lambda: f"REQ-{uuid.uuid4().hex[:8].upper()}")  # Unique
    tool_name = Column(String)
    range_mm = Column(String)
    make = Column(String)
    quantity = Column(Integer)
    location = Column(String)

    status = Column(Enum(RequestStatus), default=RequestStatus.pending)
    supervisor_id = Column(Integer, ForeignKey("users.id"))
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    requested_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    remarks = Column(String, nullable=True)

    supervisor = relationship("User", foreign_keys=[supervisor_id])
    officer = relationship("User", foreign_keys=[officer_id])
