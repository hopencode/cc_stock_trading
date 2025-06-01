from pydantic import BaseModel, validator
from typing import Optional, List
from decimal import Decimal


class AccountBase(BaseModel):
    name: str
    phone: str
    type: str


class AccountCreate(AccountBase):
    id: str
    password: str

    @validator('id')
    def validate_id(cls, v):
        if len(v) > 10:
            raise ValueError('ID는 10자 이내여야 합니다')
        if not v.isalnum():
            raise ValueError('ID는 알파벳과 숫자만 포함해야 합니다')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) > 12:
            raise ValueError('비밀번호는 12자 이내여야 합니다')
        if not v.isalnum():
            raise ValueError('비밀번호는 알파벳과 숫자만 포함해야 합니다')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if not v.startswith('010-') or len(v) != 13:
            raise ValueError('전화번호는 010-XXXX-XXXX 형식이어야 합니다')
        return v


class AccountResponse(AccountBase):
    a_number: Decimal
    cash: int
    capital_gain: int

    class Config:
        from_attributes = True


class AdminCreate(BaseModel):
    id: str
    password: str

    @validator('id')
    def validate_id(cls, v):
        if len(v) > 10:
            raise ValueError('ID는 10자 이내여야 합니다')
        if not v.isalnum():
            raise ValueError('ID는 알파벳과 숫자만 포함해야 합니다')
        return v


class LoginRequest(BaseModel):
    id: str
    password: str
    user_type: str  # customer, admin, company


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: AccountResponse


class DepositWithdrawRequest(BaseModel):
    amount: int

    @validator('amount')
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('금액은 0 이상이어야 합니다')
        return v


class BalanceResponse(BaseModel):
    cash: int
    capital_gain: int
    stocks: List[dict]
