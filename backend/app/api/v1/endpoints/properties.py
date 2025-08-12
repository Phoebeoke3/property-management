from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.property import Property
from app.models.tenant import Tenant
from app.schemas.property import PropertyCreate, PropertyUpdate, Property as PropertySchema
from app.schemas.tenant import TenantCreate
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PropertySchema])
def get_properties(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve properties.
    """
    properties = db.query(Property).offset(skip).limit(limit).all()
    return properties

@router.post("/", response_model=PropertySchema)
def create_property(
    *,
    db: Session = Depends(get_db),
    property_in: PropertyCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new property.
    """
    property_obj = Property(
        **property_in.dict(exclude={"tenant"}),
        owner_id=current_user.id
    )
    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)

    # If tenant details are provided, create the tenant and link to property
    if property_in.tenant:
        tenant_data = property_in.tenant.dict()
        tenant_data["property_id"] = property_obj.id
        tenant_obj = Tenant(**tenant_data)
        db.add(tenant_obj)
        db.commit()
        db.refresh(tenant_obj)

    return property_obj

@router.get("/{property_id}", response_model=PropertySchema)
def get_property(
    *,
    db: Session = Depends(get_db),
    property_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get property by ID.
    """
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Check if user has access to this property
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return property_obj

@router.put("/{property_id}", response_model=PropertySchema)
def update_property(
    *,
    db: Session = Depends(get_db),
    property_id: int,
    property_in: PropertyUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update property.
    """
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Check if user has access to this property
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for field, value in property_in.dict(exclude_unset=True).items():
        setattr(property_obj, field, value)
    
    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)
    return property_obj

@router.delete("/{property_id}")
def delete_property(
    *,
    db: Session = Depends(get_db),
    property_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete property.
    """
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Check if user has access to this property
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(property_obj)
    db.commit()
    return {"message": "Property deleted successfully"} 