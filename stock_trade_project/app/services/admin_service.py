from sqlalchemy.orm import Session
from typing import List

from app.models.account import Account
from app.repositories.company_repository import CompanyRepository
from app.repositories.account_repository import AccountRepository
from app.schemas.company import CompanyCreate, CompanyResponse, SectorUpdateRequest
from app.core.security import SecurityService
from fastapi import HTTPException, status


class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.company_repo = CompanyRepository(db)
        self.account_repo = AccountRepository(db)

    def register_company(self, company_data: CompanyCreate) -> CompanyResponse:
        # 기업명 중복 확인
        existing_company = self.company_repo.get_by_name(company_data.name)
        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 상장된 기업입니다"
            )

        company = self.company_repo.create_company(company_data)
        return CompanyResponse.from_orm(company)

    def delete_company(self, company_name: str) -> bool:
        company_name = company_name.lower().capitalize()

        # 기업 존재 확인
        company = self.company_repo.get_by_name(company_name)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="상장 기업 목록에 없는 기업입니다"
            )

        # 기업 계정이 있는 경우 자사주 보유 확인
        company_accounts = self.db.query(Account).filter(
            Account.name == company_name, Account.type == "company"
        ).all()

        if company_accounts:
            for account in company_accounts:
                company_balance = self.account_repo.get_company_balance(account.a_number)
                company_stock = next((b for b in company_balance if b.stock_name == company_name), None)

                if not company_stock or company_stock.stock_count != company.stock_num:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="해당 기업이 보유하고 있는 자사주 지분이 부족합니다"
                    )

        return self.company_repo.delete_company(company_name)

    def get_company_list(self) -> List[CompanyResponse]:
        companies = self.company_repo.get_all_companies()
        return [CompanyResponse.from_orm(company) for company in companies]

    def update_company_sector(self, request: SectorUpdateRequest) -> bool:
        company_name = request.company_name.lower().capitalize()

        # 기업 존재 확인
        company = self.company_repo.get_by_name(company_name)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="상장 기업 목록에 없는 기업입니다"
            )

        return self.company_repo.update_sector(company_name, request.sector)
