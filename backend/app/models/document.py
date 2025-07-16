from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)  # in bytes
    file_type = Column(String)  # MIME type
    
    # Document metadata
    document_type = Column(String)  # lease_agreement, id_proof, etc.
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    rental_agreement_id = Column(Integer, ForeignKey("rental_agreements.id"), nullable=True)
    
    # Relationships
    property = relationship("Property", back_populates="documents")
    rental_agreement = relationship("RentalAgreement", back_populates="documents") 