from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import utils, oauth2
from ..schemas import auth as authSchema
from ..models import models
from ..database.database import get_db
from ..repository import crud

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = oauth2.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_disabled == True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="bye")

    access_token_expires = timedelta(hours=20)
    access_token = oauth2.create_access_token(
        data={
            "sub": user.user_name,
            "p_version": user.password_version,
            "is_admin": user.is_admin,
        },
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "is_admin": user.is_admin,
    }


@router.get("/users/me/", response_model=authSchema.User)
async def read_users_me(
    current_user: Annotated[authSchema.User, Depends(oauth2.get_current_active_user)]
):
    return current_user
