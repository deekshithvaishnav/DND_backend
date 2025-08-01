from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
import uuid
from fastapi import APIRouter
from app import models, schemas, database
from app.utils.password import verify_password, hash_password

from app.database import get_db

router = APIRouter()

@router.post("/login", response_model=schemas.LoginResponse)
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    from app.routers import auth
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Remove old session for the same role (only for non-operators)
    if user.role != "operator":
        existing_session = db.query(models.Session).filter(models.Session.role == user.role).first()
        if existing_session:
            db.delete(existing_session)
            db.commit()

    # ✅ Create new session
    new_session_id = str(uuid.uuid4())
    expiry = datetime.now(timezone.utc) + timedelta(hours=1)

    new_session = models.Session(
        session_id=new_session_id,
        username=user.username,
        role=user.role,
        expiry=expiry
    )
    db.add(new_session)
    db.commit()

    return schemas.LoginResponse(session_id=new_session_id, role=user.role)
