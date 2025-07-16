from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.rental_agreement import AgreementStatus

class RentalAgreementBase(BaseModel):
    agreement_number: str
    start_date: datetime
    end_date: datetime
    monthly_rent: float
    security_deposit: float
    lease_terms: Optional[str] = None
    utilities_included: bool = False
    pet_policy: Optional[str] = None

class RentalAgreementCreate(RentalAgreementBase):
    property_id: int
    tenant_id: int

class RentalAgreementUpdate(BaseModel):
    agreement_number: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    monthly_rent: Optional[float] = None
    security_deposit: Optional[float] = None
    lease_terms: Optional[str] = None
    utilities_included: Optional[bool] = None
    pet_policy: Optional[str] = None
    status: Optional[AgreementStatus] = None
    is_active: Optional[bool] = None
    signed_at: Optional[datetime] = None

class RentalAgreementInDBBase(RentalAgreementBase):
    id: int
    property_id: int
    tenant_id: int
    status: AgreementStatus
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    signed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RentalAgreement(RentalAgreementInDBBase):
    pass

class RentalAgreementWithDetails(RentalAgreement):
    property: dict  # Will be populated with property details
    tenant: dict    # Will be populated with tenant details 