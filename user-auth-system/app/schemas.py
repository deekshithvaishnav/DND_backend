from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum




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


# backend/app/schemas.py

from pydantic import BaseModel

class OfficerDashboardData(BaseModel):
    total_users: int
    pending_tool_requests: int
    reported_issues: int


class SupervisorDashboardData(BaseModel):
    tools_added_pending_approval: int
    tool_requests_to_review: int
    issues_waiting_for_officer_response: int


class OperatorDashboardData(BaseModel):
    tools_in_use: int
    tools_requested: int
    reported_issues_count: int

# backend/app/schemas.py

from datetime import datetime
from typing import List, Optional

class NotificationBase(BaseModel):
    title: str
    description: str
    target_url: str

class NotificationOut(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

class Config:
        orm_mode = True

# backend/app/schemas.py



class RequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ToolAdditionRequestCreate(BaseModel):
    tool_name: str
    range_mm: str
    make: str
    quantity: int
    location: str

class ToolAdditionRequestOut(BaseModel):
    request_id: str
    tool_name: str
    range_mm: str
    make: str
    quantity: int
    location: str
    status: RequestStatus
    supervisor_name: str
    supervisor_id: int
    officer_name: Optional[str] = None
    officer_id: Optional[int] = None
    requested_at: datetime
    reviewed_at: Optional[datetime]
    remarks: Optional[str]
    class Config:
        orm_mode = True

