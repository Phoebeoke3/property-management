from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, default="USA")
    
    # Property details
    property_type = Column(String)  # apartment, house, commercial, etc.
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    square_feet = Column(Float)
    year_built = Column(Integer)
    
    # Financial details
    monthly_rent = Column(Float)
    security_deposit = Column(Float)
    utilities_included = Column(Boolean, default=False)
    
    # Status
    is_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    tenants = relationship("Tenant", back_populates="property")
    documents = relationship("Document", back_populates="property")
    rental_agreements = relationship("RentalAgreement", back_populates="property") 