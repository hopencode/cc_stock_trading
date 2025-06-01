from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.dependencies import get_admin_service, admin_required
from app.services.admin_service import AdminService
from app.schemas.company import CompanyCreate, CompanyResponse, SectorUpdateRequest

router = APIRouter()

@router.post("/companies", response_model=CompanyResponse)
def register_company(
    company_data: CompanyCreate,
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(admin_required)
):
    """기업 상장"""
    return admin_service.register_company(company_data)

@router.delete("/companies/{company_name}")
def delete_company(
    company_name: str,
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(admin_required)
):
    """기업 상장 폐지"""
    success = admin_service.delete_company(company_name)
    if success:
        return {"message": f"기업 {company_name} 상장 폐지 완료"}
    else:
        raise HTTPException(status_code=404, detail="기업을 찾을 수 없습니다")

@router.get("/companies", response_model=List[CompanyResponse])
def get_company_list(
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(admin_required)
):
    """상장 기업 목록 조회"""
    return admin_service.get_company_list()

@router.put("/companies/sector")
def update_company_sector(
    request: SectorUpdateRequest,
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(admin_required)
):
    """기업 섹터 수정"""
    success = admin_service.update_company_sector(request)
    if success:
        return {"message": f"{request.company_name}의 섹터 수정 완료"}
    else:
        raise HTTPException(status_code=404, detail="기업을 찾을 수 없습니다")
