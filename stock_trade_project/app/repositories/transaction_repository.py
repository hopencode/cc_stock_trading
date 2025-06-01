from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.models.transaction import BuyList, SellList
from app.models.order import OrderList

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_data):
        try:
            self.db.begin()
            self.db.execute(text("LOCK TABLE order_list IN EXCLUSIVE MODE"))
            max_order_number = self.db.query(func.max(OrderList.order_number)).scalar() or 0
            new_order_number = max_order_number + 1

            db_order = OrderList(
                order_number=new_order_number,
                a_number=order_data.a_number,
                type=order_data.type,
                name=order_data.name,
                price=order_data.price,
                count=order_data.count
            )
            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)
            return db_order
        except Exception as e:
            self.db.rollback()
            raise e

    def create_buy_order(self, buy_data):
        try:
            self.db.begin()
            self.db.execute(text("LOCK TABLE buy_list IN EXCLUSIVE MODE"))
            max_buy_number = self.db.query(func.max(BuyList.buy_list_number)).scalar() or 0
            new_buy_number = max_buy_number + 1

            db_buy = BuyList(
                buy_list_number=new_buy_number,
                a_number=buy_data.a_number,
                name=buy_data.name,
                price=buy_data.price,
                count=buy_data.count
            )
            self.db.add(db_buy)
            self.db.commit()
            self.db.refresh(db_buy)
            return db_buy
        except Exception as e:
            self.db.rollback()
            raise e

    def create_sell_order(self, sell_data):
        try:
            self.db.begin()
            self.db.execute(text("LOCK TABLE sell_list IN EXCLUSIVE MODE"))
            max_sell_number = self.db.query(func.max(SellList.sell_list_number)).scalar() or 0
            new_sell_number = max_sell_number + 1

            db_sell = SellList(
                sell_list_number=new_sell_number,
                a_number=sell_data.a_number,
                name=sell_data.name,
                price=sell_data.price,
                count=sell_data.count
            )
            self.db.add(db_sell)
            self.db.commit()
            self.db.refresh(db_sell)
            return db_sell
        except Exception as e:
            self.db.rollback()
            raise e

    def get_orders_by_account(self, a_number):
        return self.db.query(OrderList).filter(OrderList.a_number == a_number).all()

    def cancel_order(self, order_number):
        order = self.db.query(OrderList).filter(OrderList.order_number == order_number).first()
        if order:
            self.db.delete(order)
            self.db.commit()
            return True
        return False
