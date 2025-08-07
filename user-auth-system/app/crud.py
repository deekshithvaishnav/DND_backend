from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEFAULT_PASSWORD = "12345678"  # Default password for new users

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, username: str, role: str):
    hashed_password = get_password_hash(DEFAULT_PASSWORD)
    db_user = models.User(username=username, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

import uuid
from sqlalchemy.orm import Session
from app.models import ToolAdditionRequest, User
from app.schemas import ToolAdditionRequestCreate, ToolAdditionRequestOut, RequestStatus


# Supervisor creates tool request
def create_tool_request(db: Session, data: ToolAdditionRequestCreate, supervisor_id: int, supervisor_name: str):
    new_request = ToolAdditionRequest(
        tool_name=data.tool_name,
        range_mm=data.range_mm,
        make=data.make,
        quantity=data.quantity,
        location=data.location,
        supervisor_id=supervisor_id,
        supervisor=User(id=supervisor_id, username=supervisor_name),  # Optional
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


# Officer approves or rejects a request
def update_tool_request_status(
    db: Session,
    request_id: str,
    status: RequestStatus,
    officer_id: int,
    officer_name: str,
    remarks: str
):
    request = db.query(ToolAdditionRequest).filter_by(request_id=request_id).first()
    if not request:
        return None
    request.status = status
    request.reviewed_at = datetime.utcnow()
    request.officer_id = officer_id
    request.remarks = remarks
    request.officer = User(id=officer_id, username=officer_name)
    db.commit()
    db.refresh(request)
    return request


# Get all requests (Officer history or Supervisor view)
def get_tool_requests(db: Session, supervisor_id: int = None):
    query = db.query(ToolAdditionRequest)
    if supervisor_id:
        query = query.filter(ToolAdditionRequest.supervisor_id == supervisor_id)
    return query.order_by(ToolAdditionRequest.requested_at.desc()).all()
