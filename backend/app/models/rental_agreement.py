from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class AgreementStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"

class RentalAgreement(Base):
    __tablename__ = "rental_agreements"

    id = Column(Integer, primary_key=True, index=True)
    agreement_number = Column(String, unique=True, nullable=False)
    
    # Agreement details
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    monthly_rent = Column(Float, nullable=False)
    security_deposit = Column(Float, nullable=False)
    
    # Terms
    lease_terms = Column(Text)
    utilities_included = Column(Boolean, default=False)
    pet_policy = Column(String)
    
    # Status
    status = Column(Enum(AgreementStatus), default=AgreementStatus.DRAFT)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    signed_at = Column(DateTime)
    
    # Foreign keys
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    # Relationships
    property = relationship("Property", back_populates="rental_agreements")
    tenant = relationship("Tenant", back_populates="rental_agreements")
    documents = relationship("Document", back_populates="rental_agreement") 