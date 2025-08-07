# backend/app/routers/notifications.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models import Notification
from app.schemas import NotificationOut
from typing import List


router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[NotificationOut])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Notification).filter(
        (Notification.user_id == current_user.id) | 
        (Notification.role == current_user.role)
    ).order_by(Notification.created_at.desc()).all()

@router.post("/{notification_id}/mark-read")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif or (notif.user_id != current_user.id and notif.role != current_user.role):
        raise HTTPException(status_code=404, detail="Notification not found")

    notif.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}
