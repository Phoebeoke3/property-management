from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.notification import NotificationType, NotificationStatus

class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: NotificationType

class NotificationCreate(NotificationBase):
    user_id: int
    scheduled_at: Optional[datetime] = None

class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    status: Optional[NotificationStatus] = None
    email_sent: Optional[bool] = None
    sms_sent: Optional[bool] = None
    push_sent: Optional[bool] = None

class NotificationInDBBase(NotificationBase):
    id: int
    user_id: int
    status: NotificationStatus
    email_sent: bool
    sms_sent: bool
    push_sent: bool
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Notification(NotificationInDBBase):
    pass 