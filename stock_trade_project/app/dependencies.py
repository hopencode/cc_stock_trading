from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.services.admin_service import AdminService
from app.services.customer_service import CustomerService
from app.services.company_service import CompanyService

def get_admin_service(db: Session = Depends(get_db)) -> AdminService:
    return AdminService(db)

def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db)

def get_company_service(db: Session = Depends(get_db)) -> CompanyService:
    return CompanyService(db)

# 역할 기반 의존성
admin_required = require_role(["admin"])
customer_required = require_role(["customer"])
company_required = require_role(["company"])
customer_or_company_required = require_role(["customer", "company"])
