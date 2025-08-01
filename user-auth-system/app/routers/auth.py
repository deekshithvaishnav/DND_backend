from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.database import get_db
from app import models, schemas, crud
from app.utils.password import verify_password, hash_password


router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


@router.post("/login", response_model=schemas.LoginResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if db_user.role != "operator":
        existing_session = crud.get_session_by_role(db, db_user.role)
        if existing_session:
            crud.delete_session(db, existing_session.session_id)

    session_id = str(uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    crud.create_session(db, user_id=db_user.id, session_id=session_id, expires_at=expires_at)

    return schemas.LoginResponse(message="Login successful", session_id=session_id, role=db_user.role)


@router.get("/check-session/{session_id}", response_model=schemas.SessionCheckResponse)
def check_session(session_id: str, db: Session = Depends(get_db)):
    session = crud.get_session_by_id(db, session_id)
    if not session or session.expires_at < datetime.now(timezone.utc):
        if session:
            crud.delete_session(db, session_id)
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    return schemas.SessionCheckResponse(valid=True, role=session.user.role)


@router.post("/logout")
def logout(session_id: str, db: Session = Depends(get_db)):
    crud.delete_session(db, session_id)
    return {"message": "Logged out successfully"}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
