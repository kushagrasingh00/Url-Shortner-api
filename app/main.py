from fastapi import FastAPI
from app import database_models
from app.database import engine
from .routers import users , auth , links

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)  

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(links.router)

@app.get('/')
def read_root():
    return {'detail':'welcome to URL shortner'}
