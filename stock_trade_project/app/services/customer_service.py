from sqlalchemy.orm import Session
from typing import List, Dict
from decimal import Decimal
from app.repositories.account_repository import AccountRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.order_repository import OrderRepository
from app.schemas.account import DepositWithdrawRequest, BalanceResponse
from app.schemas.order import OrderCreate, OrderResponse, TradingRequest, OrderCancelRequest
from app.schemas.company import CompanyResponse, FinancialInfoResponse
from app.models.account import Account
from fastapi import HTTPException, status


class CustomerService:
    def __init__(self, db: Session):
        self.db = db
        self.account_repo = AccountRepository(db)
        self.company_repo = CompanyRepository(db)
        self.order_repo = OrderRepository(db)

    def deposit(self, current_user: Account, request: DepositWithdrawRequest) -> Dict:
        if request.amount == 0:
            return {"message": "잔액의 변동이 없습니다", "balance": current_user.cash}

        success = self.account_repo.update_cash(current_user.a_number, request.amount)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="입금 처리 중 오류가 발생했습니다"
            )

        updated_account = self.account_repo.get_by_account_number(current_user.a_number)
        return {
            "message": f"{request.amount}원 입금 완료",
            "balance": updated_account.cash
        }

    def withdraw(self, current_user: Account, request: DepositWithdrawRequest) -> Dict:
        if request.amount == 0:
            return {"message": "잔액의 변동이 없습니다", "balance": current_user.cash}

        if current_user.cash < request.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="잔액이 부족합니다"
            )

        success = self.account_repo.update_cash(current_user.a_number, -request.amount)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="출금 처리 중 오류가 발생했습니다"
            )

        updated_account = self.account_repo.get_by_account_number(current_user.a_number)
        return {
            "message": f"{request.amount}원 출금 완료",
            "balance": updated_account.cash
        }

    def get_company_list(self) -> List[CompanyResponse]:
        companies = self.company_repo.get_all_companies()
        return [CompanyResponse.from_orm(company) for company in companies]

    def get_company_info(self, company_name: str) -> List[FinancialInfoResponse]:
        company_name = company_name.lower().capitalize()

        # 기업 존재 확인
        company = self.company_repo.get_by_name(company_name)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="상장 기업 목록에 없는 기업입니다"
            )

        financial_infos = self.company_repo.get_financial_info(company_name)
        if not financial_infos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="등록된 재무정보가 없습니다"
            )

        return [FinancialInfoResponse.from_orm(info) for info in financial_infos]

    def get_company_orders(self, company_name: str) -> Dict:
        company_name = company_name.lower().capitalize()

        # 기업 존재 확인
        company = self.company_repo.get_by_name(company_name)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="상장 기업 목록에 없는 기업입니다"
            )

        orders = self.order_repo.get_company_orders(company_name)

        buy_orders = [{"price": o.price, "count": o.count, "type": o.type} for o in orders["buy_orders"]]
        sell_orders = [{"price": o.price, "count": o.count, "type": o.type} for o in orders["sell_orders"]]

        return {
            "company_name": company_name,
            "buy_orders": buy_orders,
            "sell_orders": sell_orders
        }

    def buy_stock(self, current_user: Account, request: TradingRequest) -> Dict:
        if not request.company_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="기업명을 입력해주세요"
            )

        company_name = request.company_name.lower().capitalize()

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

        # 체결된 수량만큼 매수 처리
        if concluded_count > 0:
            self._process_buy_conclusion(current_user.a_number, company_name, request.price, concluded_count)
            # 주가 업데이트
            self.company_repo.update_price(company_name, request.price)

        # 미체결 수량이 있으면 매수 주문 등록
        order_number = None
        if remaining_count > 0:
            order_data = OrderCreate(
                type="buy",
                name=company_name,
                price=request.price,
                count=remaining_count
            )
            order = self.order_repo.create_order(current_user.a_number, order_data)
            order_number = order.order_number

        return {
            "message": "매수 주문 완료",
            "order_number": order_number,
            "concluded_count": concluded_count,
            "remaining_count": remaining_count
        }

    def sell_stock(self, current_user: Account, request: TradingRequest) -> Dict:
        if not request.company_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="기업명을 입력해주세요"
            )

        company_name = request.company_name.lower().capitalize()

        # 보유 주식 확인
        customer_balances = self.account_repo.get_customer_balance(current_user.a_number)
        stock_balance = next((b for b in customer_balances if b.stock_name == company_name), None)

        if not stock_balance or stock_balance.stock_count < request.count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="보유 주식이 부족합니다"
            )

        # 보유 주식 차감
        self.account_repo.update_customer_balance(current_user.a_number, company_name, -request.count, 0)

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
            order_data = OrderCreate(
                type="sell",
                name=company_name,
                price=request.price,
                count=remaining_count
            )
            order = self.order_repo.create_order(current_user.a_number, order_data)
            order_number = order.order_number

        return {
            "message": "매도 주문 완료",
            "order_number": order_number,
            "concluded_count": concluded_count,
            "remaining_count": remaining_count
        }

    def get_orders(self, current_user: Account) -> List[OrderResponse]:
        orders = self.order_repo.get_orders_by_account(current_user.a_number)
        return [OrderResponse.from_orm(order) for order in orders]

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
            # 매도 주문 취소 시 주식 복원
            self.account_repo.update_customer_balance(current_user.a_number, order.name, order.count, 0)

        success = self.order_repo.delete_order(request.order_number)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="주문 취소 처리 중 오류가 발생했습니다"
            )

        return {"message": f"주문번호 {request.order_number}번 취소 완료"}

    def get_balance(self, current_user: Account) -> BalanceResponse:
        customer_balances = self.account_repo.get_customer_balance(current_user.a_number)

        stocks = []
        for balance in customer_balances:
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

    def get_portfolio_weight(self, current_user: Account) -> Dict:
        # 섹터별 보유 비중 계산
        customer_balances = self.account_repo.get_customer_balance(current_user.a_number)

        if not customer_balances:
            return {"message": "보유하고 있는 주식이 없습니다", "portfolio": []}

        sector_values = {}
        total_value = 0

        for balance in customer_balances:
            company = self.company_repo.get_by_name(balance.stock_name)
            if company:
                value = company.price * balance.stock_count
                total_value += value

                if company.sector in sector_values:
                    sector_values[company.sector] += value
                else:
                    sector_values[company.sector] = value

        portfolio = []
        for sector, value in sector_values.items():
            weight = round((value / total_value) * 100, 2) if total_value > 0 else 0
            portfolio.append({
                "sector": sector,
                "weight": f"{weight}%"
            })

        return {"portfolio": portfolio}

    def _process_buy_conclusion(self, a_number: int, company_name: str, price: int, count: int):
        """매수 체결 처리"""
        # 매수 내역 기록
        self.order_repo.create_buy_transaction(a_number, company_name, price, count)

        # 계정 타입에 따라 잔고 업데이트
        account = self.account_repo.get_by_account_number(a_number)
        if account.type == "customer":
            self.account_repo.update_customer_balance(a_number, company_name, count, price)
        else:
            self.account_repo.update_company_balance(a_number, company_name, count, price)

    def _process_sell_conclusion(self, a_number: int, company_name: str, price: int, count: int):
        """매도 체결 처리"""
        # 매도 가능한 매수 내역 조회 (FIFO)
        buy_transactions = self.order_repo.get_available_buy_transactions(a_number, company_name)

        cash_to_add = price * count
        remaining_count = count

        for buy_tx in buy_transactions:
            if remaining_count <= 0:
                break

            available_count = buy_tx.b_count - buy_tx.s_count
            if remaining_count >= available_count:
                # 해당 매수 내역 전량 매도
                self.order_repo.update_buy_transaction_sold_count(buy_tx.buy_list_number, available_count)
                sell_count = available_count
                remaining_count -= available_count
            else:
                # 해당 매수 내역 일부 매도
                self.order_repo.update_buy_transaction_sold_count(buy_tx.buy_list_number, remaining_count)
                sell_count = remaining_count
                remaining_count = 0

            # 매도 내역 기록
            self.order_repo.create_sell_transaction(a_number, company_name, buy_tx.price, price, sell_count)

            # 양도소득 계산
            capital_gain = (price - buy_tx.price) * sell_count
            self.account_repo.update_capital_gain(a_number, capital_gain)

        # 현금 추가
        self.account_repo.update_cash(a_number, cash_to_add)

        # 보유 주식 차감
        account = self.account_repo.get_by_account_number(a_number)
        if account.type == "customer":
            self.account_repo.update_customer_balance(a_number, company_name, -count, 0)
        else:
            self.account_repo.update_company_balance(a_number, company_name, -count, 0)
