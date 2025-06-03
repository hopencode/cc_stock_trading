from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.dependencies import get_customer_service, customer_required
from app.services.customer_service import CustomerService
from app.schemas.account import DepositWithdrawRequest, BalanceResponse
from app.schemas.order import TradingRequest, OrderResponse, OrderCancelRequest
from app.schemas.company import CompanyResponse, FinancialInfoResponse

router = APIRouter()

@router.post("/deposit")
def deposit(
    request: DepositWithdrawRequest,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """입금"""
    return customer_service.deposit(current_user, request)

@router.post("/withdraw")
def withdraw(
    request: DepositWithdrawRequest,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """출금"""
    return customer_service.withdraw(current_user, request)

@router.get("/companies", response_model=List[CompanyResponse])
def get_company_list(
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """상장 기업 목록 조회"""
    return customer_service.get_company_list()

@router.get("/companies/{company_name}/info", response_model=List[FinancialInfoResponse])
def get_company_info(
    company_name: str,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """기업 재무정보 조회"""
    return customer_service.get_company_info(company_name)

@router.get("/companies/{company_name}/orders")
def get_company_orders(
    company_name: str,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """기업 호가창 조회"""
    return customer_service.get_company_orders(company_name)

@router.post("/trading/buy")
def buy_stock(
    request: TradingRequest,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """주식 매수"""
    return customer_service.buy_stock(current_user, request)

@router.post("/trading/sell")
def sell_stock(
    request: TradingRequest,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """주식 매도"""
    return customer_service.sell_stock(current_user, request)

@router.get("/orders", response_model=List[OrderResponse])
def get_orders(
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """주문 조회"""
    return customer_service.get_orders(current_user)

@router.delete("/orders")
def cancel_order(
    request: OrderCancelRequest,
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """주문 취소"""
    return customer_service.cancel_order(current_user, request)

@router.get("/balance", response_model=BalanceResponse)
def get_balance(
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """잔고 조회"""
    return customer_service.get_balance(current_user)

@router.get("/portfolio/weight")
def get_portfolio_weight(
    customer_service: CustomerService = Depends(get_customer_service),
    current_user = Depends(customer_required)
):
    """포트폴리오 비중 조회"""
    return customer_service.get_portfolio_weight(current_user)
