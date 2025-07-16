from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TenantBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: Optional[datetime] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    employer: Optional[str] = None
    job_title: Optional[str] = None
    monthly_income: Optional[int] = None

class TenantCreate(TenantBase):
    property_id: int

class TenantUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    employer: Optional[str] = None
    job_title: Optional[str] = None
    monthly_income: Optional[int] = None
    is_active: Optional[bool] = None

class TenantInDBBase(TenantBase):
    id: int
    property_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Tenant(TenantInDBBase):
    pass

class TenantWithProperty(Tenant):
    property: dict  # Will be populated with property details 