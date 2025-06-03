from fastapi import APIRouter, Depends
from typing import List
from app.dependencies import get_company_service, company_required
from app.services.company_service import CompanyService
from app.schemas.account import DepositWithdrawRequest, BalanceResponse
from app.schemas.order import TradingRequest, OrderResponse, OrderCancelRequest
from app.schemas.company import CompanyResponse, FinancialInfoResponse, FinancialInfoCreate

router = APIRouter()

@router.post("/deposit")
def deposit(
    request: DepositWithdrawRequest,
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """입금"""
    return company_service.deposit(current_user, request)

@router.post("/withdraw")
def withdraw(
    request: DepositWithdrawRequest,
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """출금"""
    return company_service.withdraw(current_user, request)

@router.get("/companies", response_model=List[CompanyResponse])
def get_company_list(
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """상장 기업 목록 조회"""
    return company_service.get_company_list()

@router.get("/companies/{company_name}/info", response_model=List[FinancialInfoResponse])
def get_company_info(
    company_name: str,
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """기업 재무정보 조회"""
    return company_service.get_company_info(company_name)

@router.get("/companies/{company_name}/orders")
def get_company_orders(
    company_name: str,
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """기업 호가창 조회"""
    return company_service.get_company_orders(company_name)

@router.post("/trading/buy")
def buy_stock(
    request: TradingRequest,
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """자사주 매수"""
    return company_service.buy_stock(current_user, request)

@router.post("/trading/sell")
def sell_stock(
    request: TradingRequest,
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """자사주 매도"""
    return company_service.sell_stock(current_user, request)

@router.get("/orders", response_model=List[OrderResponse])
def get_orders(
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """주문 조회"""
    return company_service.get_orders(current_user)

@router.delete("/orders")
def cancel_order(
    request: OrderCancelRequest,
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """주문 취소"""
    return company_service.cancel_order(current_user, request)

@router.get("/balance", response_model=BalanceResponse)
def get_balance(
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """잔고 조회"""
    return company_service.get_balance(current_user)

@router.post("/financial-info", response_model=FinancialInfoResponse)
def register_financial_info(
    financial_data: FinancialInfoCreate,
    company_service: CompanyService = Depends(get_company_service),
    current_user = Depends(company_required)
):
    """재무정보 등록"""
    return company_service.register_financial_info(current_user, financial_data)
