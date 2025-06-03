from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.company import Company, FinancialInfo
from app.schemas.company import CompanyCreate, FinancialInfoCreate


class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_companies(self) -> List[Company]:
        return self.db.query(Company).order_by(Company.total_price.desc()).all()

    def get_by_name(self, name: str) -> Optional[Company]:
        return self.db.query(Company).filter(Company.name == name).first()

    def create_company(self, company_data: CompanyCreate) -> Company:
        total_price = company_data.price * company_data.stock_num
        db_company = Company(
            name=company_data.name,
            price=company_data.price,
            stock_num=company_data.stock_num,
            total_price=total_price,
            sector=company_data.sector
        )
        self.db.add(db_company)
        self.db.commit()
        self.db.refresh(db_company)
        return db_company

    def update_sector(self, company_name: str, sector: str) -> bool:
        company = self.get_by_name(company_name)
        if company:
            company.sector = sector
            self.db.commit()
            return True
        return False

    def update_price(self, company_name: str, price: int) -> bool:
        company = self.get_by_name(company_name)
        if company:
            company.price = price
            company.total_price = price * company.stock_num
            self.db.commit()
            return True
        return False

    def delete_company(self, company_name: str) -> bool:
        company = self.get_by_name(company_name)
        if company:
            # 재무정보도 함께 삭제 (CASCADE)
            self.db.delete(company)
            self.db.commit()
            return True
        return False

    def get_financial_info(self, company_name: str) -> List[FinancialInfo]:
        return self.db.query(FinancialInfo).filter(
            FinancialInfo.name == company_name
        ).order_by(FinancialInfo.year.desc()).all()

    def create_or_update_financial_info(self, company_name: str, financial_data: FinancialInfoCreate) -> FinancialInfo:
        existing = self.db.query(FinancialInfo).filter(
            FinancialInfo.name == company_name,
            FinancialInfo.year == financial_data.year
        ).first()

        if existing:
            existing.sales = financial_data.sales
            existing.business_profits = financial_data.business_profits
            existing.pure_profits = financial_data.pure_profits
            self.db.commit()
            return existing
        else:
            new_info = FinancialInfo(
                name=company_name,
                year=financial_data.year,
                sales=financial_data.sales,
                business_profits=financial_data.business_profits,
                pure_profits=financial_data.pure_profits
            )
            self.db.add(new_info)
            self.db.commit()
            self.db.refresh(new_info)
            return new_info
