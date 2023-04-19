from datetime import datetime, timedelta
import jose.jwt as jwt

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def create_access_token():
    expire = datetime.utcnow() + timedelta(minutes=30)
    expire_timestamp = int(expire.timestamp())
    encoded_jwt = jwt.encode(
        {"iss": "myapp", "iat": datetime.utcnow()},
        SECRET_KEY,
        algorithm=ALGORITHM,
        exp=expire_timestamp,
    )
    return encoded_jwt


def get_current_user():
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


print(create_access_token())
