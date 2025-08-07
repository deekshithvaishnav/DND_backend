# backend/app/routers/operator.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import OperatorDashboardData
from app.routers.auth import verify_role

router = APIRouter(prefix="/operator", tags=["Operator Dashboard"])

@router.get("/dashboard", response_model=OperatorDashboardData)
def get_operator_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_role(current_user, "operator")

    # Replace this with real data later
    return OperatorDashboardData(
        tools_in_use=2,
        tools_requested=5,
        reported_issues_count=1
    )
