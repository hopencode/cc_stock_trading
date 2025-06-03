from sqlalchemy import Column, String, BigInteger, Numeric, Float, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CustomerBalance(Base):
    __tablename__ = "customer_balance"

    a_number = Column(Numeric(8, 0), ForeignKey("account.a_number"), primary_key=True)
    stock_name = Column(String(20), ForeignKey("company.name"), primary_key=True)
    stock_count = Column(BigInteger)
    avg_buy_price = Column(Float)

    __table_args__ = (
        CheckConstraint('stock_count >= 0'),
        CheckConstraint('avg_buy_price >= 1'),
    )

    # 관계 설정
    account = relationship("Account", back_populates="customer_balances")
    company = relationship("Company", back_populates="customer_balances")


class CompanyBalance(Base):
    __tablename__ = "company_balance"

    a_number = Column(Numeric(8, 0), ForeignKey("account.a_number"), primary_key=True)
    stock_name = Column(String(20), ForeignKey("company.name"), primary_key=True)
    stock_count = Column(BigInteger)
    avg_buy_price = Column(Float)

    __table_args__ = (
        CheckConstraint('stock_count >= 0'),
        CheckConstraint('avg_buy_price >= 1'),
    )

    # 관계 설정
    account = relationship("Account", back_populates="company_balances")
    company = relationship("Company", back_populates="company_balances")
