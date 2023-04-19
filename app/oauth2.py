from . import schemas, database, utils
from .schemas import auth as authSchemas

from .models import models
from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from .database.database import get_db
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.user_name == username).first()
    return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    # if not utils.verify_password(password, user.hashed_password):
    #     return False
    if not (password == user.password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = authSchemas.TokenData(user_name=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.user_name)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[authSchemas.User, Depends(get_current_user)]
):
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    print(current_user.__dict__)
    return current_user
