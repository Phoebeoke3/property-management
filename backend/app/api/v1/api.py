from fastapi import APIRouter
from app.api.v1.endpoints import auth, properties, tenants, rental_agreements, documents, notifications

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(rental_agreements.router, prefix="/rental-agreements", tags=["rental-agreements"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"]) 