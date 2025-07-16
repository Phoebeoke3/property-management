from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.document import Document
from app.models.property import Property
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_documents(
    property_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve documents.
    """
    query = db.query(Document)
    
    if property_id:
        # Verify property ownership
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if not property_obj:
            raise HTTPException(status_code=404, detail="Property not found")
        
        if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        query = query.filter(Document.property_id == property_id)
    else:
        # Get documents from properties owned by current user
        if current_user.role.value != "admin":
            property_ids = [p.id for p in db.query(Property).filter(Property.owner_id == current_user.id).all()]
            query = query.filter(Document.property_id.in_(property_ids))
    
    documents = query.offset(skip).limit(limit).all()
    return documents

@router.post("/upload")
async def upload_document(
    *,
    db: Session = Depends(get_db),
    property_id: int,
    document_type: str,
    title: str,
    description: str = None,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Upload a document.
    """
    # Verify property ownership
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Validate file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Validate file size
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Create document record
    document = Document(
        title=title,
        description=description,
        file_name=file.filename,
        file_path=file_path,
        file_size=len(content),
        file_type=file.content_type,
        document_type=document_type,
        property_id=property_id
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "message": "Document uploaded successfully",
        "document": {
            "id": document.id,
            "title": document.title,
            "file_name": document.file_name,
            "document_type": document.document_type,
            "created_at": document.created_at
        }
    }

@router.get("/{document_id}")
def get_document(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get document by ID.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if user has access to this document's property
    property_obj = db.query(Property).filter(Property.id == document.property_id).first()
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return {
        "id": document.id,
        "title": document.title,
        "description": document.description,
        "file_name": document.file_name,
        "file_size": document.file_size,
        "file_type": document.file_type,
        "document_type": document.document_type,
        "is_verified": document.is_verified,
        "created_at": document.created_at,
        "file_url": f"/uploads/{os.path.basename(document.file_path)}"
    }

@router.delete("/{document_id}")
def delete_document(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete document.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if user has access to this document's property
    property_obj = db.query(Property).filter(Property.id == document.property_id).first()
    if current_user.role.value != "admin" and property_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Delete file from filesystem
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        # Log error but continue with database deletion
        print(f"Error deleting file {document.file_path}: {str(e)}")
    
    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"} 