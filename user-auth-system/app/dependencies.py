# backend/app/dependencies.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.routers.auth import decode_jwt_token
from typing import Generator
from app.routers.auth import decode_jwt_token

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency: Get current user from token
def get_current_user(token: str = Depends(decode_jwt_token), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == token["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user