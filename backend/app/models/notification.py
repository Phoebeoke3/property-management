from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class NotificationType(str, enum.Enum):
    RENT_EXPIRY = "rent_expiry"
    PAYMENT_DUE = "payment_due"
    MAINTENANCE = "maintenance"
    GENERAL = "general"

class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    READ = "read"
    FAILED = "failed"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    
    # Delivery details
    email_sent = Column(Boolean, default=False)
    sms_sent = Column(Boolean, default=False)
    push_sent = Column(Boolean, default=False)
    
    # Scheduled delivery
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    read_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="notifications") 