# backend/app/routers/officer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import OfficerDashboardData
from app.routers.auth import verify_role


router = APIRouter(prefix="/officer", tags=["Officer Dashboard"])

@router.get("/dashboard", response_model=OfficerDashboardData)
def get_officer_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_role(current_user, "officer")

    # You can build real stats here. For now, return sample data.
    return OfficerDashboardData(
        total_users=25,
        pending_tool_requests=4,
        reported_issues=3
    )
