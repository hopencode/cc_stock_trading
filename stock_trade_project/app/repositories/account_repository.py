from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from app.models.account import Account, Admin
from app.models.transaction import CustomerBalance, CompanyBalance
from app.schemas.account import AccountCreate, AdminCreate


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, account_id: str) -> Optional[Account]:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_account_number(self, a_number: int) -> Optional[Account]:
        return self.db.query(Account).filter(Account.a_number == a_number).first()

    def get_admin_by_id(self, admin_id: str) -> Optional[Admin]:
        return self.db.query(Admin).filter(Admin.id == admin_id).first()

    def create_account(self, account_data: AccountCreate, a_number: int) -> Account:
        db_account = Account(
            id=account_data.id,
            password=account_data.password,
            a_number=a_number,
            type=account_data.type,
            name=account_data.name,
            phone=account_data.phone,
            cash=0,
            capital_gain=0
        )
        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account

    def create_admin(self, admin_data: AdminCreate) -> Admin:
        db_admin = Admin(
            id=admin_data.id,
            password=admin_data.password,
            type="admin"
        )
        self.db.add(db_admin)
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin

    def update_cash(self, a_number: int, amount: int) -> bool:
        account = self.get_by_account_number(a_number)
        if account:
            account.cash += amount
            self.db.commit()
            return True
        return False

    def update_capital_gain(self, a_number: int, gain: int) -> bool:
        account = self.get_by_account_number(a_number)
        if account:
            account.capital_gain += gain
            self.db.commit()
            return True
        return False

    def get_customer_balance(self, a_number: int) -> List[CustomerBalance]:
        return self.db.query(CustomerBalance).filter(CustomerBalance.a_number == a_number).all()

    def get_company_balance(self, a_number: int) -> List[CompanyBalance]:
        return self.db.query(CompanyBalance).filter(CompanyBalance.a_number == a_number).all()

    def update_customer_balance(self, a_number: int, stock_name: str, count: int, avg_price: float, order_repo=None, update_avg_price=True):
        balance = self.db.query(CustomerBalance).filter(
            CustomerBalance.a_number == a_number,
            CustomerBalance.stock_name == stock_name
        ).first()
        """
        개인 계정의 보유 주식(자사주) 잔고 갱신
        - count: +면 매수, -면 매도
        - avg_price: 매수 시 평균 단가, 매도 시 0 또는 무시
        - order_repo: 미체결 매도 주문 조회용(필수)
        """
        if balance:
            total_count = balance.stock_count + count
            if total_count <= 0:
                # 미체결 매도 주문이 남아있는지 확인
                if order_repo is not None:
                    unsettled_sells = order_repo.get_unsettled_sell_orders(a_number, stock_name)
                    if unsettled_sells:
                        # 미체결 매도 주문이 있으면 balance는 0으로만 갱신(삭제X)
                        balance.stock_count = 0
                    else:
                        self.db.delete(balance)
                else:
                    # order_repo를 전달받지 못한 경우 기존대로 삭제
                    self.db.delete(balance)
            else:
                if count > 0 and update_avg_price:  # 매수인 경우만 평균 단가 업데이트
                    total_cost = balance.stock_count * balance.avg_buy_price + count * avg_price
                    balance.avg_buy_price = total_cost / total_count
                balance.stock_count = total_count
        else:
            if count > 0:
                new_balance = CustomerBalance(
                    a_number=a_number,
                    stock_name=stock_name,
                    stock_count=count,
                    avg_buy_price=avg_price
                )
                self.db.add(new_balance)
        self.db.commit()

    def update_company_balance(self, a_number: int, stock_name: str, count: int, avg_price: float, order_repo=None, update_avg_price=True):
        balance = self.db.query(CompanyBalance).filter(
            CompanyBalance.a_number == a_number,
            CompanyBalance.stock_name == stock_name
        ).first()

        if balance:
            total_count = balance.stock_count + count
            if total_count <= 0:
                # 미체결 매도 주문이 남아있는지 확인
                if order_repo is not None:
                    unsettled_sells = order_repo.get_unsettled_sell_orders(a_number, stock_name)
                    if unsettled_sells:
                        # 미체결 매도 주문이 있으면 balance는 0으로만 갱신(삭제X)
                        balance.stock_count = 0
                    else:
                        self.db.delete(balance)
                else:
                    # order_repo를 전달받지 못한 경우 기존대로 삭제
                    self.db.delete(balance)
            else:
                if count > 0 and update_avg_price:  # 매수인 경우만 평균 단가 업데이트
                    total_cost = balance.stock_count * balance.avg_buy_price + count * avg_price
                    balance.avg_buy_price = total_cost / total_count
                balance.stock_count = total_count
        else:
            if count > 0:
                new_balance = CompanyBalance(
                    a_number=a_number,
                    stock_name=stock_name,
                    stock_count=count,
                    avg_buy_price=avg_price
                )
                self.db.add(new_balance)
        self.db.commit()

