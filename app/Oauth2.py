from fastapi import Depends ,HTTPException , status
from jose import jwt , JWTError
from datetime import datetime , timedelta
from fastapi.security import OAuth2PasswordBearer
from app import models ,database_models
from sqlalchemy.orm import Session
from app.database import get_db
import os

SECRET = os.getenv("SECRET_KEY")
ALGORITHM="HS256"
EXPIRE_TIME=30

Oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(payload:dict):
    to_encode = payload.copy()
    # add expiratoin time in payload
    expire=datetime.now()+timedelta(minutes=EXPIRE_TIME)

    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode , SECRET ,algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt(token:str , credentials_Exception):
    try:
        payload=jwt.decode(token,SECRET,algorithms=[ALGORITHM])   

        user_id = payload.get('user_id')

        if user_id is None:
            raise credentials_Exception

        token_data=models.token_data(id=user_id)
        
    except JWTError:
        raise credentials_Exception

    return token_data

def get_current_user(token:str =  Depends(Oauth2_scheme),db:Session=Depends(get_db)):

    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})

    # token_data consist of user_id
    token_data=verify_jwt(token,credentials_exception)

    # using the id to find user

    user=db.query(database_models.user_schema).filter(database_models.user_schema.user_id == token_data.id).first()

    return user
