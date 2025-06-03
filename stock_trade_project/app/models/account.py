from sqlalchemy import Column, Integer, String, BigInteger, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(String(10))
    password = Column(String(12))
    a_number = Column(Numeric(8, 0), primary_key=True, unique=True)
    type = Column(String(8))
    name = Column(String(20))
    phone = Column(String(13))
    cash = Column(BigInteger, default=0)
    capital_gain = Column(BigInteger, default=0)

    __table_args__ = (
        CheckConstraint('a_number > 0'),
        CheckConstraint('cash >= 0'),
    )

    # 관계 설정
    customer_balances = relationship("CustomerBalance", back_populates="account")
    company_balances = relationship("CompanyBalance", back_populates="account")
    orders = relationship("OrderList", back_populates="account")
    buy_transactions = relationship("BuyList", back_populates="account")
    sell_transactions = relationship("SellList", back_populates="account")


class Admin(Base):
    __tablename__ = "admin"

    id = Column(String(10), primary_key=True)
    password = Column(String(12))
    type = Column(String(5), default="admin")
