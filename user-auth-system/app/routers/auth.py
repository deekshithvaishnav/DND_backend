from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.database import get_db
from app import models, schemas, crud
from app.utils.password import verify_password, hash_password
from app.models import User
from app.utils.token import create_password_reset_token, verify_token
from app.utils.email_utils import send_reset_email
from fastapi import Body
from app.utils.password import get_password_hash
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from app.config import settings  # Assuming you have SECRET_KEY and ALGORITHM stored here

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def decode_jwt_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

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

@router.post("/auth/request-reset")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_password_reset_token({"sub": user.username})
    await send_reset_email(user.email, token)
    return {"message": "Reset link sent"}

@router.post("/auth/reset-password")
def reset_password(token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)):
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    username = data.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "Password updated successfully"}



def verify_role(user: User, required_role: str):
    if user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only {required_role.capitalize()} can access this endpoint."
        )
    
# backend/app/auth.py

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")  # adjust if needed

# app/routers/auth.py


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
