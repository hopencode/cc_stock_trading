from pydantic import BaseModel, validator
from typing import Optional, List
from decimal import Decimal


class CompanyBase(BaseModel):
    name: str
    sector: str


class CompanyCreate(CompanyBase):
    price: int
    stock_num: int

    @validator('name')
    def validate_name(cls, v):
        if len(v) > 20:
            raise ValueError('기업명은 20자 이내여야 합니다')
        if not v.replace(' ', '').isalpha():
            raise ValueError('기업명은 알파벳만 포함해야 합니다')
        return v.lower().capitalize()

    @validator('price', 'stock_num')
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('가격과 주식 수는 1 이상이어야 합니다')
        return v

    @validator('sector')
    def validate_sector(cls, v):
        if len(v) > 25:
            raise ValueError('섹터명은 25자 이내여야 합니다')
        return v


class CompanyResponse(CompanyBase):
    price: int
    stock_num: int
    total_price: int

    class Config:
        from_attributes = True


class CompanyListResponse(BaseModel):
    companies: List[CompanyResponse]


class SectorUpdateRequest(BaseModel):
    company_name: str
    sector: str

    @validator('company_name')
    def validate_company_name(cls, v):
        if len(v) > 20:
            raise ValueError('기업명은 20자 이내여야 합니다')
        return v.lower().capitalize()


class FinancialInfoBase(BaseModel):
    year: int
    sales: int
    business_profits: int
    pure_profits: int


class FinancialInfoCreate(FinancialInfoBase):
    @validator('year')
    def validate_year(cls, v):
        if v < 1900 or v > 9999:
            raise ValueError('연도는 1900-9999 사이여야 합니다')
        return v

    @validator('sales')
    def validate_sales(cls, v):
        if v < 0:
            raise ValueError('매출은 0 이상이어야 합니다')
        return v


class FinancialInfoResponse(FinancialInfoBase):
    name: str

    class Config:
        from_attributes = True
