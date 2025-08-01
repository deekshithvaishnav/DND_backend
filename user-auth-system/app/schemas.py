from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    role: str  # should be one of "officer", "supervisor", "operator"

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    password_set: Optional[bool]

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    session_id: str
    role: str


class SessionCheckResponse(BaseModel):
    valid: bool
    username: Optional[str] = None
    role: Optional[str] = None
    expires_at: Optional[datetime] = None

