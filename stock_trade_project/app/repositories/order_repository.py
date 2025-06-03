from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderList, BuyList, SellList
from app.schemas.order import OrderCreate


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, a_number: int, order_data: OrderCreate) -> OrderList:
        max_order_number = self.db.query(func.max(OrderList.order_number)).scalar() or 0
        new_order_number = max_order_number + 1

        db_order = OrderList(
            order_number=new_order_number,
            a_number=a_number,
            type=order_data.type,
            name=order_data.name,
            price=order_data.price,
            count=order_data.count
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get_orders_by_account(self, a_number: int) -> List[OrderList]:
        return self.db.query(OrderList).filter(OrderList.a_number == a_number).all()

    # order_repository.py

    def get_unsettled_sell_orders(self, a_number: int, company_name: str) -> List[OrderList]:
        """해당 계좌, 종목에 대해 미체결 매도 주문만 조회"""
        return self.db.query(OrderList).filter(
            OrderList.a_number == a_number,
            OrderList.name == company_name,
            OrderList.type == "sell"
        ).all()

    def get_order_by_number(self, order_number: int, a_number: int = None) -> Optional[OrderList]:
        query = self.db.query(OrderList).filter(OrderList.order_number == order_number)
        if a_number:
            query = query.filter(OrderList.a_number == a_number)
        return query.first()

    def delete_order(self, order_number: int) -> bool:
        order = self.get_order_by_number(order_number)
        if order:
            self.db.delete(order)
            self.db.commit()
            return True
        return False

    def get_matching_orders(self, company_name: str, order_type: str, price: int, exclude_account: int) -> List[
        OrderList]:
        return self.db.query(OrderList).filter(
            and_(
                OrderList.name == company_name,
                OrderList.type == order_type,
                OrderList.price == price,
                OrderList.a_number != exclude_account
            )
        ).order_by(OrderList.order_number).all()

    def update_order_count(self, order_number: int, new_count: int):
        order = self.get_order_by_number(order_number)
        if order:
            order.count = new_count
            self.db.commit()

    def get_company_orders(self, company_name: str) -> dict:
        buy_orders = self.db.query(OrderList).filter(
            and_(OrderList.name == company_name, OrderList.type == "buy")
        ).order_by(OrderList.price.desc()).all()

        sell_orders = self.db.query(OrderList).filter(
            and_(OrderList.name == company_name, OrderList.type == "sell")
        ).order_by(OrderList.price.desc()).all()

        return {
            "buy_orders": buy_orders,
            "sell_orders": sell_orders
        }

    def create_buy_transaction(self, a_number: int, company_name: str, price: int, count: int) -> BuyList:
        # 최대 buy_list_number 조회
        max_number = self.db.query(BuyList.buy_list_number).order_by(BuyList.buy_list_number.desc()).first()
        buy_list_number = (max_number[0] + 1) if max_number and max_number[0] else 1

        now = datetime.now()
        db_buy = BuyList(
            buy_list_number=buy_list_number,
            a_number=a_number,
            name=company_name,
            price=price,
            b_date=now.date(),
            b_time=now.time(),
            b_count=count,
            s_count=0
        )
        self.db.add(db_buy)
        self.db.commit()
        self.db.refresh(db_buy)
        return db_buy

    def create_sell_transaction(self, a_number: int, company_name: str, buy_price: int, sell_price: int,
                                count: int) -> SellList:
        # 최대 sell_list_number 조회
        max_number = self.db.query(SellList.sell_list_number).order_by(SellList.sell_list_number.desc()).first()
        sell_list_number = (max_number[0] + 1) if max_number and max_number[0] else 1

        now = datetime.now()
        db_sell = SellList(
            sell_list_number=sell_list_number,
            a_number=a_number,
            name=company_name,
            b_price=buy_price,
            s_price=sell_price,
            s_date=now.date(),
            s_time=now.time(),
            s_count=count
        )
        self.db.add(db_sell)
        self.db.commit()
        self.db.refresh(db_sell)
        return db_sell

    def get_available_buy_transactions(self, a_number: int, company_name: str) -> List[BuyList]:
        return self.db.query(BuyList).filter(
            and_(
                BuyList.a_number == a_number,
                BuyList.name == company_name,
                BuyList.b_count > BuyList.s_count
            )
        ).order_by(BuyList.b_date, BuyList.b_time).all()

    def update_buy_transaction_sold_count(self, buy_list_number: int, additional_sold: int):
        buy_transaction = self.db.query(BuyList).filter(BuyList.buy_list_number == buy_list_number).first()
        if buy_transaction:
            buy_transaction.s_count += additional_sold
            self.db.commit()
