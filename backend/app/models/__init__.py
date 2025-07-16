# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .property import Property
from .tenant import Tenant
from .document import Document
from .rental_agreement import RentalAgreement
from .notification import Notification

# Import Base from database module
from app.core.database import Base

__all__ = [
    "Base",
    "User",
    "Property", 
    "Tenant",
    "Document",
    "RentalAgreement",
    "Notification"
] 