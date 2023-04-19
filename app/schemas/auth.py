from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_name: str | None = None

    class Config:
        orm_mode = True


class User(BaseModel):
    user_name: str
    is_disabled: bool | None = None

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str

    class Config:
        orm_mode = True
