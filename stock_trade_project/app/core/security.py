from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.repositories.account_repository import AccountRepository

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


class SecurityService:
    @staticmethod
    def verify_password(plain_password: str, stored_password: str) -> bool:
        return plain_password == stored_password

    @staticmethod
    def get_password_hash(password: str) -> str:
        return password

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        user_type: str = payload.get("type")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    account_repo = AccountRepository(db)
    user = account_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


def require_role(allowed_roles: List[str]):
    def role_dependency(current_user=Depends(get_current_user)):
        if current_user.type not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user

    return role_dependency
