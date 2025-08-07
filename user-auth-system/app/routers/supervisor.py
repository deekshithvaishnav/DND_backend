# backend/app/routers/supervisor.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import SupervisorDashboardData
from app.routers.auth import verify_role

router = APIRouter(prefix="/supervisor", tags=["Supervisor Dashboard"])

@router.get("/dashboard", response_model=SupervisorDashboardData)
def get_supervisor_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_role(current_user, "supervisor")

    # Dummy data for now; later you can query the actual DB
    return SupervisorDashboardData(
        tools_added_pending_approval=5,
        tool_requests_to_review=8,
        issues_waiting_for_officer_response=2
    )
