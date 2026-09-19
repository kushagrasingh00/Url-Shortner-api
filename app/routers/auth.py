from fastapi import APIRouter , Depends , HTTPException ,status
from app import models , database_models ,utils , Oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['Login'])

@router.post('/login')
def login_user(user_credentials:models.register_user,db:Session=Depends(get_db)):

    # checking if user exists
    user=db.query(database_models.user_schema).filter(database_models.user_schema.email == user_credentials.email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid credentials')

    # if passwrod verifies
    if not utils.verify_password(user_credentials.password ,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid credentials')

    access_token=Oauth2.create_access_token({'user_id':user.user_id})

    return {'access_token':access_token , 'token_type':'bearer'}