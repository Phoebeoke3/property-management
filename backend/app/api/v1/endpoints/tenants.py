from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.models.property import Property
from app.schemas.tenant import TenantCreate, TenantUpdate, Tenant as TenantSchema
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TenantSchema])
def get_tenants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve tenants.
    """
    tenants = db.query(Tenant).offset(skip).limit(limit).all()
    return tenants

@router.post("/", response_model=TenantSchema)
def create_tenant(
    *,
    db: Session = Depends(get_db),
    tenant_in: TenantCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new tenant.
    """
    # Verify property ownership
    property_obj = db.query(Property).filter(Property.id == tenant_in.property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    tenant = Tenant(**tenant_in.dict())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@router.get("/{tenant_id}", response_model=TenantSchema)
def get_tenant(
    *,
    db: Session = Depends(get_db),
    tenant_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get tenant by ID.
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check if user has access to this tenant's property
    property_obj = db.query(Property).filter(Property.id == tenant.property_id).first()
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return tenant

@router.put("/{tenant_id}", response_model=TenantSchema)
def update_tenant(
    *,
    db: Session = Depends(get_db),
    tenant_id: int,
    tenant_in: TenantUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update tenant.
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check if user has access to this tenant's property
    property_obj = db.query(Property).filter(Property.id == tenant.property_id).first()
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for field, value in tenant_in.dict(exclude_unset=True).items():
        setattr(tenant, field, value)
    
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@router.delete("/{tenant_id}")
def delete_tenant(
    *,
    db: Session = Depends(get_db),
    tenant_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete tenant.
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check if user has access to this tenant's property
    property_obj = db.query(Property).filter(Property.id == tenant.property_id).first()
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(tenant)
    db.commit()
    return {"message": "Tenant deleted successfully"} 