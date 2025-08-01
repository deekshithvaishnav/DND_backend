# app/models.py
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

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
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "officer", "supervisor", "operator"
    first_login = Column(Boolean, default=None)  # null means first login
    is_logged_in = Column(Boolean, default=False)  # for session control
