from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.rental_agreement import RentalAgreement, AgreementStatus
from app.models.property import Property
from app.schemas.rental_agreement import RentalAgreementCreate, RentalAgreementUpdate, RentalAgreement as RentalAgreementSchema
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[RentalAgreementSchema])
def get_rental_agreements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve rental agreements.
    """
    if current_user.role.value == "admin":
        agreements = db.query(RentalAgreement).offset(skip).limit(limit).all()
    else:
        # Get agreements from properties owned by current user
        property_ids = [p.id for p in db.query(Property).filter(Property.owner_id == current_user.id).all()]
        agreements = db.query(RentalAgreement).filter(RentalAgreement.property_id.in_(property_ids)).offset(skip).limit(limit).all()
    return agreements

@router.post("/", response_model=RentalAgreementSchema)
def create_rental_agreement(
    *,
    db: Session = Depends(get_db),
    agreement_in: RentalAgreementCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new rental agreement.
    """
    # Verify property ownership
    property_obj = db.query(Property).filter(Property.id == agreement_in.property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Generate unique agreement number
    agreement_number = f"AG-{datetime.now().strftime('%Y%m%d')}-{property_obj.id:04d}"
    
    agreement = RentalAgreement(
        **agreement_in.dict(),
        agreement_number=agreement_number
    )
    db.add(agreement)
    db.commit()
    db.refresh(agreement)
    return agreement

@router.get("/{agreement_id}", response_model=RentalAgreementSchema)
def get_rental_agreement(
    *,
    db: Session = Depends(get_db),
    agreement_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get rental agreement by ID.
    """
    agreement = db.query(RentalAgreement).filter(RentalAgreement.id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Rental agreement not found")
    
    # Check if user has access to this agreement's property
    property_obj = db.query(Property).filter(Property.id == agreement.property_id).first()
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return agreement

@router.put("/{agreement_id}", response_model=RentalAgreementSchema)
def update_rental_agreement(
    *,
    db: Session = Depends(get_db),
    agreement_id: int,
    agreement_in: RentalAgreementUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update rental agreement.
    """
    agreement = db.query(RentalAgreement).filter(RentalAgreement.id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Rental agreement not found")
    
    # Check if user has access to this agreement's property
    property_obj = db.query(Property).filter(Property.id == agreement.property_id).first()
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for field, value in agreement_in.dict(exclude_unset=True).items():
        setattr(agreement, field, value)
    
    db.add(agreement)
    db.commit()
    db.refresh(agreement)
    return agreement

@router.post("/{agreement_id}/sign")
def sign_rental_agreement(
    *,
    db: Session = Depends(get_db),
    agreement_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Sign a rental agreement.
    """
    agreement = db.query(RentalAgreement).filter(RentalAgreement.id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Rental agreement not found")
    
    # Check if user has access to this agreement's property
    property_obj = db.query(Property).filter(Property.id == agreement.property_id).first()
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    agreement.status = AgreementStatus.ACTIVE
    agreement.signed_at = datetime.utcnow()
    
    db.add(agreement)
    db.commit()
    db.refresh(agreement)
    
    return {"message": "Rental agreement signed successfully", "agreement": agreement}

@router.get("/expiring-soon")
def get_expiring_agreements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get rental agreements expiring soon (within 30 days).
    """
    from datetime import timedelta
    
    expiry_date = datetime.utcnow() + timedelta(days=30)
    
    if current_user.role.value == "admin":
        agreements = db.query(RentalAgreement).filter(
            RentalAgreement.end_date <= expiry_date,
            RentalAgreement.status == AgreementStatus.ACTIVE
        ).all()
    else:
        property_ids = [p.id for p in db.query(Property).filter(Property.owner_id == current_user.id).all()]
        agreements = db.query(RentalAgreement).filter(
            RentalAgreement.property_id.in_(property_ids),
            RentalAgreement.end_date <= expiry_date,
            RentalAgreement.status == AgreementStatus.ACTIVE
        ).all()
    
    return {"expiring_agreements": agreements} 