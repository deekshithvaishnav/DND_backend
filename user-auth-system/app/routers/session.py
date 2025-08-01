# routers/session.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import SessionTable
from datetime import datetime, timezone

router = APIRouter()

@router.get("/session-check")
def check_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(SessionTable).filter(SessionTable.session_id == session_id).first()

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    if session.expiry < datetime.now(timezone.utc):
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired")

    return {"message": "Session is valid", "role": session.role, "username": session.username}
