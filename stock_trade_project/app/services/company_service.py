from sqlalchemy.orm import Session
from typing import List, Dict
from app.repositories.account_repository import AccountRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.order_repository import OrderRepository
from app.schemas.account import DepositWithdrawRequest, BalanceResponse
from app.schemas.order import TradingRequest, OrderCancelRequest
from app.schemas.company import FinancialInfoCreate, FinancialInfoResponse
from app.models.account import Account
from app.services.customer_service import CustomerService
from fastapi import HTTPException, status


class CompanyService(CustomerService):  # CustomerService 상속으로 공통 기능 재사용
    def __init__(self, db: Session):
        super().__init__(db)

    def buy_stock(self, current_user: Account, request: TradingRequest) -> Dict:
        # 기업은 자사주만 매수 가능
        company_name = current_user.name

        # 기업 존재 확인
        company = self.company_repo.get_by_name(company_name)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="상장 기업 목록에 없는 기업입니다"
            )

        total_cost = request.price * request.count

        # 잔액 확인
        if current_user.cash < total_cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="잔액이 부족합니다"
            )

        # 잔액 차감
        self.account_repo.update_cash(current_user.a_number, -total_cost)

        # 매도 주문 매칭 확인
        matching_orders = self.order_repo.get_matching_orders(
            company_name, "sell", request.price, current_user.a_number
        )

        remaining_count = request.count
        concluded_count = 0

        # 매도 주문과 체결 처리
        for sell_order in matching_orders:
            if remaining_count <= 0:
                break

            if remaining_count >= sell_order.count:
                # 매도 주문 전량 체결
                self._process_sell_conclusion(sell_order.a_number, company_name, request.price, sell_order.count)
                self.order_repo.delete_order(sell_order.order_number)
                remaining_count -= sell_order.count
                concluded_count += sell_order.count
            else:
                # 매도 주문 일부 체결
                self._process_sell_conclusion(sell_order.a_number, company_name, request.price, remaining_count)
                self.order_repo.update_order_count(sell_order.order_number, sell_order.count - remaining_count)
                concluded_count += remaining_count
                remaining_count = 0

        # 체결된 수량만큼 매수 처리 (company_balance 테이블 사용)
        if concluded_count > 0:
            self.order_repo.create_buy_transaction(current_user.a_number, company_name, request.price, concluded_count)
            self.account_repo.update_company_balance(current_user.a_number, company_name, concluded_count,
                                                     request.price)
            # 주가 업데이트
            self.company_repo.update_price(company_name, request.price)

        # 미체결 수량이 있으면 매수 주문 등록
        order_number = None
        if remaining_count > 0:
            from ..schemas.order import OrderCreate
            order_data = OrderCreate(
                type="buy",
                name=company_name,
                price=request.price,
                count=remaining_count
            )
            order = self.order_repo.create_order(current_user.a_number, order_data)
            order_number = order.order_number

        return {
            "message": "자사주 매수 주문 완료",
            "order_number": order_number,
            "concluded_count": concluded_count,
            "remaining_count": remaining_count
        }

    def sell_stock(self, current_user: Account, request: TradingRequest) -> Dict:
        # 기업은 자사주만 매도 가능
        company_name = current_user.name

        # 보유 자사주 확인
        company_balances = self.account_repo.get_company_balance(current_user.a_number)
        stock_balance = next((b for b in company_balances if b.stock_name == company_name), None)

        if not stock_balance or stock_balance.stock_count < request.count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="보유 자사주가 부족합니다"
            )

        # 보유 자사주 차감
        self.account_repo.update_company_balance(current_user.a_number, company_name, -request.count, 0)

        # 매수 주문 매칭 확인
        matching_orders = self.order_repo.get_matching_orders(
            company_name, "buy", request.price, current_user.a_number
        )

        remaining_count = request.count
        concluded_count = 0

        # 매수 주문과 체결 처리
        for buy_order in matching_orders:
            if remaining_count <= 0:
                break

            if remaining_count >= buy_order.count:
                # 매수 주문 전량 체결
                self._process_buy_conclusion(buy_order.a_number, company_name, request.price, buy_order.count)
                self.order_repo.delete_order(buy_order.order_number)
                remaining_count -= buy_order.count
                concluded_count += buy_order.count
            else:
                # 매수 주문 일부 체결
                self._process_buy_conclusion(buy_order.a_number, company_name, request.price, remaining_count)
                self.order_repo.update_order_count(buy_order.order_number, buy_order.count - remaining_count)
                concluded_count += remaining_count
                remaining_count = 0

        # 체결된 수량만큼 매도 처리
        if concluded_count > 0:
            self._process_sell_conclusion(current_user.a_number, company_name, request.price, concluded_count)
            # 주가 업데이트
            self.company_repo.update_price(company_name, request.price)

        # 미체결 수량이 있으면 매도 주문 등록
        order_number = None
        if remaining_count > 0:
            from ..schemas.order import OrderCreate
            order_data = OrderCreate(
                type="sell",
                name=company_name,
                price=request.price,
                count=remaining_count
            )
            order = self.order_repo.create_order(current_user.a_number, order_data)
            order_number = order.order_number

        return {
            "message": "자사주 매도 주문 완료",
            "order_number": order_number,
            "concluded_count": concluded_count,
            "remaining_count": remaining_count
        }

    def get_balance(self, current_user: Account) -> BalanceResponse:
        company_balances = self.account_repo.get_company_balance(current_user.a_number)

        stocks = []
        for balance in company_balances:
            company = self.company_repo.get_by_name(balance.stock_name)
            valuation_amount = company.price * balance.stock_count if company else 0

            stocks.append({
                "stock_name": balance.stock_name,
                "stock_count": balance.stock_count,
                "avg_buy_price": balance.avg_buy_price,
                "current_price": company.price if company else 0,
                "valuation_amount": valuation_amount
            })

        return BalanceResponse(
            cash=current_user.cash,
            capital_gain=current_user.capital_gain,
            stocks=stocks
        )

    def cancel_order(self, current_user: Account, request: OrderCancelRequest) -> Dict:
        order = self.order_repo.get_order_by_number(request.order_number, current_user.a_number)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 계좌의 주문 내역 중 해당하는 번호의 주문이 없습니다"
            )

        if order.type == "buy":
            # 매수 주문 취소 시 현금 환불
            refund_amount = order.price * order.count
            self.account_repo.update_cash(current_user.a_number, refund_amount)
        else:
            # 매도 주문 취소 시 자사주 복원
            self.account_repo.update_company_balance(current_user.a_number, order.name, order.count, 0)

        success = self.order_repo.delete_order(request.order_number)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="주문 취소 처리 중 오류가 발생했습니다"
            )

        return {"message": f"주문번호 {request.order_number}번 취소 완료"}

    def register_financial_info(self, current_user: Account,
                                financial_data: FinancialInfoCreate) -> FinancialInfoResponse:
        # 기업은 자신의 재무정보만 등록 가능
        company_name = current_user.name

        financial_info = self.company_repo.create_or_update_financial_info(company_name, financial_data)
        return FinancialInfoResponse.from_orm(financial_info)
