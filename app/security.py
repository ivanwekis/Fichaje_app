from app import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(username: str):
    expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.utcnow() + expires_delta
    to_encode = {"username": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), username=None):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_payload: str = payload.get("username")
        if user_payload is None or (user_payload != username):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {"username": username}
