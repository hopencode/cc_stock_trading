from sqlalchemy import Column, String, BigInteger, CheckConstraint, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Company(Base):
    __tablename__ = "company"

    name = Column(String(20), primary_key=True)
    price = Column(BigInteger)
    stock_num = Column(BigInteger)
    total_price = Column(BigInteger)
    sector = Column(String(25))

    __table_args__ = (
        CheckConstraint('price >= 1'),
        CheckConstraint('stock_num >= 1'),
        CheckConstraint('total_price >= 1'),
    )

    # 관계 설정
    financial_infos = relationship("FinancialInfo", back_populates="company")
    customer_balances = relationship("CustomerBalance", back_populates="company")
    company_balances = relationship("CompanyBalance", back_populates="company")


class FinancialInfo(Base):
    __tablename__ = "financial_info"

    name = Column(String(20), ForeignKey("company.name"), primary_key=True)
    year = Column(Numeric(4, 0), primary_key=True)
    sales = Column(BigInteger)
    business_profits = Column(BigInteger)
    pure_profits = Column(BigInteger)

    __table_args__ = (
        CheckConstraint('year >= 1900'),
        CheckConstraint('sales >= 0'),
    )

    # 관계 설정
    company = relationship("Company", back_populates="financial_infos")
