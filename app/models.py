from pydantic import BaseModel , EmailStr , AnyHttpUrl , ConfigDict
from datetime import datetime
from typing import Optional

class register_user(BaseModel):
    email:EmailStr
    password:str

class response_user_register(BaseModel):
    email:EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    
class token_data(BaseModel):
    id:Optional[int] = None

class token(BaseModel):
    access_token:str
    token_type:str



class CreateLinkRequest(BaseModel):
    original_url :AnyHttpUrl

class response_generate_link(BaseModel):
    link:str

class response_get_all_links(BaseModel):
    original_url: str
    short_url: str
    clicks: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)