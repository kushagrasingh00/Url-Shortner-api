from fastapi import APIRouter , Depends , HTTPException ,status
from app import models , database_models ,utils , Oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from typing import List


router = APIRouter(tags=['links'])


# ROUTE - To Generate Links
@router.post('/links',response_model=models.response_generate_link,status_code=status.HTTP_201_CREATED)
def create_link(
    link_data:models.CreateLinkRequest,
    db:Session=Depends(get_db),
    current_user: database_models.user_schema = Depends(Oauth2.get_current_user)):
    
    while True:
        current_short_code = utils.create_short_code()

        existing_code = db.query(database_models.link_schema).filter(database_models.link_schema.short_code == current_short_code).first()

        if not existing_code:
            break

    new_obj=database_models.link_schema(
        
        original_url=str(link_data.original_url) ,
        short_code = current_short_code ,
        user_id=current_user.user_id)    
    
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)

    return {"link":f"http://localhost:8000/{new_obj.short_code}"}

# ------------------------------------------------------------------------------------------------------------------------------------------

# Get All links Of the User
@router.get('/links', response_model=List[models.response_get_all_links])
def get_all_links(
    db:Session=Depends(get_db),
    current_user:database_models.user_schema = Depends(Oauth2.get_current_user)
    ):

    user_links=db.query(database_models.link_schema).filter(database_models.link_schema.user_id == current_user.user_id).all()

    results = []
    for link in user_links:
        results.append({
            "original_url": link.original_url,
            "short_url": f"http://localhost:8000/{link.short_code}",
            "clicks": link.clicks,
            "created_at": link.created_at
        })
    return results


# ------------------------------------------------------------------------------------------------------------------------------------------

# route - REDIRECTING TO LINK

@router.get('/{short_code}',status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect_url(short_code:str,db:Session=Depends(get_db)):

    query = db.query(database_models.link_schema).filter(database_models.link_schema.short_code == short_code).first()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='not found')

    # increasing click counts per successfull click
    query.clicks+=1
    db.commit()

    return RedirectResponse(query.original_url)


# ------------------------------------------------------------------------------------------------------------------------------------------

# route - Delete Link

@router.delete('/links/{id}')
def delete_link(
    id:int , 
    db:Session=Depends(get_db),
    current_user:database_models.user_schema = Depends(Oauth2.get_current_user) 
    ):

    # verify if the user is deleting its own 
    user=db.query(
        database_models.link_schema).filter(
        database_models.link_schema.user_id == current_user.user_id , 
        database_models.link_schema.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "user not found")


    db.delete(user)
    db.commit()

    return {'detail':'link deleted'}




