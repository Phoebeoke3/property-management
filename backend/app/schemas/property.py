from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.tenant import TenantCreate

class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[float] = None
    year_built: Optional[int] = None
    monthly_rent: Optional[float] = None
    security_deposit: Optional[float] = None
    utilities_included: bool = False

class PropertyCreate(PropertyBase):
    tenant: Optional[TenantCreate] = None

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[float] = None
    year_built: Optional[int] = None
    monthly_rent: Optional[float] = None
    security_deposit: Optional[float] = None
    utilities_included: Optional[bool] = None
    is_available: Optional[bool] = None
    is_active: Optional[bool] = None

class PropertyInDBBase(PropertyBase):
    id: int
    owner_id: int
    is_available: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Property(PropertyInDBBase):
    pass

class PropertyWithOwner(Property):
    owner: dict  # Will be populated with owner details 