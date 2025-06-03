from sqlalchemy import Column, String, BigInteger, Numeric, Date, Time, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class OrderList(Base):
    __tablename__ = "order_list"

    a_number = Column(Numeric(8, 0), ForeignKey("account.a_number"), primary_key=True)
    type = Column(String(4))
    name = Column(String(20))
    price = Column(BigInteger)
    count = Column(BigInteger)
    order_number = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)

    __table_args__ = (
        CheckConstraint('price >= 1'),
        CheckConstraint('count >= 1'),
        CheckConstraint('order_number >= 1'),
    )

    # 관계 설정
    account = relationship("Account", back_populates="orders")


class BuyList(Base):
    __tablename__ = "buy_list"

    buy_list_number = Column(BigInteger, primary_key=True, unique=True)
    a_number = Column(Numeric(8, 0), ForeignKey("account.a_number"), primary_key=True)
    name = Column(String(20))
    price = Column(BigInteger)
    b_date = Column(Date)
    b_time = Column(Time)
    b_count = Column(BigInteger)
    s_count = Column(BigInteger, default=0)

    __table_args__ = (
        CheckConstraint('buy_list_number >= 1'),
        CheckConstraint('price >= 1'),
        CheckConstraint('b_count >= 1'),
        CheckConstraint('b_count >= s_count'),
        CheckConstraint('s_count >= 0'),
    )

    # 관계 설정
    account = relationship("Account", back_populates="buy_transactions")


class SellList(Base):
    __tablename__ = "sell_list"

    sell_list_number = Column(BigInteger, primary_key=True, unique=True)
    a_number = Column(Numeric(8, 0), ForeignKey("account.a_number"), primary_key=True)
    name = Column(String(20))
    b_price = Column(BigInteger)
    s_price = Column(BigInteger)
    s_date = Column(Date)
    s_time = Column(Time)
    s_count = Column(BigInteger)

    __table_args__ = (
        CheckConstraint('sell_list_number >= 1'),
        CheckConstraint('b_price >= 1'),
        CheckConstraint('s_price >= 1'),
        CheckConstraint('s_count >= 1'),
    )

    # 관계 설정
    account = relationship("Account", back_populates="sell_transactions")
