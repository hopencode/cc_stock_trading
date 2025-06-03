from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.account import Account
from app.core.database import get_db
from app.core.security import SecurityService
from app.core.config import get_settings
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate, AdminCreate, LoginResponse, AccountResponse, LoginRequest

router = APIRouter()
settings = get_settings()


@router.post("/register/customer", response_model=AccountResponse)
def register_customer(
        account_data: AccountCreate,
        db: Session = Depends(get_db)
):
    """일반고객 회원가입"""
    account_data.type = "customer"
    account_repo = AccountRepository(db)

    # ID 중복 확인
    existing_account = account_repo.get_by_id(account_data.id)
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 ID입니다"
        )

    # 계좌번호 생성 (8자리 랜덤)
    import random
    attempts = 0
    while attempts < 100:
        a_number = random.randint(10000000, 99999999)
        existing_number = account_repo.get_by_account_number(a_number)
        if not existing_number:
            break
        attempts += 1

    if attempts >= 100:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="계좌번호 생성에 실패했습니다"
        )

    # 계정 생성
    account = account_repo.create_account(account_data, a_number)
    return AccountResponse.from_orm(account)


@router.post("/register/company", response_model=AccountResponse)
def register_company(
        account_data: AccountCreate,
        db: Session = Depends(get_db)
):
    """기업고객 회원가입"""
    account_data.type = "company"
    account_data.name = account_data.name.lower().capitalize()

    account_repo = AccountRepository(db)

    # 상장 기업 확인
    from ....repositories.company_repository import CompanyRepository
    company_repo = CompanyRepository(db)
    company = company_repo.get_by_name(account_data.name)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="상장 기업 목록에 없는 기업입니다"
        )

    # 기업 계정 중복 확인
    existing_company_account = db.query(Account).filter(
        Account.type == "company", Account.name == account_data.name
    ).first()
    if existing_company_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 계정이 존재하는 기업입니다"
        )

    # ID 중복 확인
    existing_account = account_repo.get_by_id(account_data.id)
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 ID입니다"
        )

    # 계좌번호 생성
    import random
    attempts = 0
    while attempts < 100:
        a_number = random.randint(10000000, 99999999)
        existing_number = account_repo.get_by_account_number(a_number)
        if not existing_number:
            break
        attempts += 1

    if attempts >= 100:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="계좌번호 생성에 실패했습니다"
        )

    # 계정 생성
    account = account_repo.create_account(account_data, a_number)

    # 자사주 전량 보유로 초기화
    from ....repositories.order_repository import OrderRepository
    from datetime import datetime

    order_repo = OrderRepository(db)
    now = datetime.now()

    # 매수 내역 생성
    buy_transaction = order_repo.create_buy_transaction(
        a_number, account_data.name, company.price, company.stock_num
    )

    # 기업 잔고 생성
    account_repo.update_company_balance(a_number, account_data.name, company.stock_num, company.price)

    return AccountResponse.from_orm(account)


@router.post("/register/admin")
def register_admin(
        admin_data: AdminCreate,
        db: Session = Depends(get_db)
):
    """관리자 회원가입"""
    account_repo = AccountRepository(db)

    # ID 중복 확인
    existing_admin = account_repo.get_admin_by_id(admin_data.id)
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 ID입니다"
        )

    # 관리자 생성
    admin = account_repo.create_admin(admin_data, admin_data.password)
    return {"message": "관리자 계정 생성 성공"}


@router.post("/login", response_model=LoginResponse)
def login(
        request: LoginRequest,
        db: Session = Depends(get_db)
):
    """로그인"""
    account_repo = AccountRepository(db)
    user_type = request.user_type

    if user_type == "admin":
        user = account_repo.get_admin_by_id(request.id)
        if not user or request.password != user.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="잘못된 인증 정보입니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_info = {"id": user.id, "type": "admin", "name": "관리자", "a_number": None}
    else:
        user = account_repo.get_by_id(request.id)
        if not user or request.password != user.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="잘못된 인증 정보입니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user.type != user_type:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="계정 유형이 일치하지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_info = AccountResponse.from_orm(user)

    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = SecurityService.create_access_token(
        data={"sub": user.id, "type": user_type},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": user_info
    }

