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

    def update_customer_balance(self, a_number: int, stock_name: str, count: int, avg_price: float):
        balance = self.db.query(CustomerBalance).filter(
            CustomerBalance.a_number == a_number,
            CustomerBalance.stock_name == stock_name
        ).first()

        if balance:
            # 기존 보유 주식이 있는 경우
            total_count = balance.stock_count + count
            if total_count <= 0:
                self.db.delete(balance)
            else:
                if count > 0:  # 매수인 경우만 평균 단가 업데이트
                    total_cost = balance.stock_count * balance.avg_buy_price + count * avg_price
                    balance.avg_buy_price = total_cost / total_count
                balance.stock_count = total_count
        else:
            # 새로운 주식 보유
            if count > 0:
                new_balance = CustomerBalance(
                    a_number=a_number,
                    stock_name=stock_name,
                    stock_count=count,
                    avg_buy_price=avg_price
                )
                self.db.add(new_balance)

        self.db.commit()

    def update_company_balance(self, a_number: int, stock_name: str, count: int, avg_price: float):
        balance = self.db.query(CompanyBalance).filter(
            CompanyBalance.a_number == a_number,
            CompanyBalance.stock_name == stock_name
        ).first()

        if balance:
            total_count = balance.stock_count + count
            if total_count <= 0:
                self.db.delete(balance)
            else:
                if count > 0:  # 매수인 경우만 평균 단가 업데이트
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
