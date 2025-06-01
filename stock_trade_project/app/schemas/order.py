from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import date, time


class OrderBase(BaseModel):
    name: str
    price: int
    count: int


class OrderCreate(OrderBase):
    type: str  # buy or sell

    @validator('name')
    def validate_name(cls, v):
        if len(v) > 20:
            raise ValueError('기업명은 20자 이내여야 합니다')
        return v.lower().capitalize()

    @validator('price', 'count')
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('가격과 수량은 1 이상이어야 합니다')
        return v

    @validator('type')
    def validate_type(cls, v):
        if v not in ['buy', 'sell']:
            raise ValueError('주문 유형은 buy 또는 sell이어야 합니다')
        return v


class OrderResponse(OrderBase):
    type: str
    order_number: int
    a_number: int

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    orders: List[OrderResponse]


class OrderCancelRequest(BaseModel):
    order_number: int

    @validator('order_number')
    def validate_order_number(cls, v):
        if v <= 0:
            raise ValueError('주문번호는 1 이상이어야 합니다')
        return v


class CompanyOrderResponse(BaseModel):
    company_name: str
    buy_orders: List[dict]
    sell_orders: List[dict]


class TradingRequest(BaseModel):
    company_name: Optional[str] = None  # customer용, company는 자사주
    price: int
    count: int

    @validator('price', 'count')
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('가격과 수량은 1 이상이어야 합니다')
        return v
