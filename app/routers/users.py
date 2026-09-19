from fastapi import APIRouter , Depends , HTTPException ,status
from app import models , database_models ,utils ,Oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['user'])


# user registers
@router.post('/register' , response_model=models.response_user_register,status_code=status.HTTP_201_CREATED)
def register_user(user_credentials:models.register_user,db:Session=Depends(get_db)):

    # check if email exist
    user=db.query(database_models.user_schema).filter(database_models.user_schema.email == user_credentials.email).first()

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,detail="user exists"
        )
    
    # hash password 
    hash=utils.hash_password(user_credentials.password)
    user_credentials.password = hash

    # new user
    new_user= database_models.user_schema(**user_credentials.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# delete user
@router.delete('/user/{id}')
def user_delete(
    id:int , 
    db:Session=Depends(get_db),
    current_user:database_models.user_schema = Depends(Oauth2.get_current_user) 
    ):

    user=db.query(database_models.user_schema).filter(database_models.user_schema.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "user not found")

    db.delete(user)
    db.commit()

    return {'detail':'user deleted'}