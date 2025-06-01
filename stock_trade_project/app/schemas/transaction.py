from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    a_number: int
    type: str  # "buy" or "sell"
    name: str  # 회사명
    price: int
    count: int

class BuyOrderCreate(BaseModel):
    a_number: int
    name: str
    price: int
    count: int

class SellOrderCreate(BaseModel):
    a_number: int
    name: str
    price: int
    count: int

class OrderResponse(BaseModel):
    order_number: int
    a_number: int
    type: str
    name: str
    price: int
    count: int

    class Config:
        orm_mode = True

class BuyOrderResponse(BaseModel):
    buy_list_number: int
    a_number: int
    name: str
    price: int
    count: int

    class Config:
        orm_mode = True

class SellOrderResponse(BaseModel):
    sell_list_number: int
    a_number: int
    name: str
    price: int
    count: int

    class Config:
        orm_mode = True
