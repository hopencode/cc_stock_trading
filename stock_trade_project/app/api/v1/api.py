from fastapi import APIRouter
from app.api.v1.endpoints import auth, admin, customer, company

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(customer.router, prefix="/customer", tags=["customer"])
api_router.include_router(company.router, prefix="/company", tags=["company"])
