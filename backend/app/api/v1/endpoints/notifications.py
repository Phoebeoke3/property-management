from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.notification import Notification, NotificationStatus, NotificationType
from app.schemas.notification import NotificationCreate, Notification as NotificationSchema
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[NotificationSchema])
def get_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve notifications for current user.
    """
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    return notifications

@router.get("/unread")
def get_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get unread notifications count.
    """
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.status == NotificationStatus.PENDING
    ).count()
    
    return {"unread_count": unread_count}

@router.post("/{notification_id}/read")
def mark_notification_read(
    *,
    db: Session = Depends(get_db),
    notification_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Mark notification as read.
    """
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.status = NotificationStatus.READ
    notification.read_at = datetime.utcnow()
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return {"message": "Notification marked as read"}

@router.post("/mark-all-read")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Mark all notifications as read.
    """
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.status == NotificationStatus.PENDING
    ).update({
        Notification.status: NotificationStatus.READ,
        Notification.read_at: datetime.utcnow()
    })
    
    db.commit()
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
def delete_notification(
    *,
    db: Session = Depends(get_db),
    notification_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete notification.
    """
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notification deleted successfully"} 