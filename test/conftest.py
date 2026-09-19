from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
from app import database_models
from app.database import get_db
from starlette.testclient import TestClient as TestClient
from app.main import app
from app import utils
from app.Oauth2 import create_access_token

db_url="postgresql://postgres:1105@localhost:5432/Url Shortner Test"
engine=create_engine(db_url)

testing_session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

@pytest.fixture()
def session():
    # drop all the previous tables in the databse
    database_models.Base.metadata.drop_all(bind=engine) 
    # create new table
    database_models.Base.metadata.create_all(bind=engine)

    db=testing_session()  
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def create_test_user(session):
    password = 'test123'
    hashed_pass = utils.hash_password(password)
    user = database_models.user_schema(
        email='testuser1@gmial.com',
        password=hashed_pass)
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

# generate jwt token
@pytest.fixture()
def token(create_test_user):

    return create_access_token({'user_id':create_test_user.user_id})

# create login client
@pytest.fixture()
def authorized_client(client,token):
    client.headers = {**client.headers,"Authorization":f"Bearer {token}"}
    return client


# creating demo links for database
@pytest.fixture()
def dummy_links(session, create_test_user):
    links = [
        database_models.link_schema(
            original_url="https://google.com/",
            short_code=utils.create_short_code(),
            user_id=create_test_user.user_id
        ),
        database_models.link_schema(
            original_url="https://uber.com/",
            short_code=utils.create_short_code(),
            user_id=create_test_user.user_id
        ),
        database_models.link_schema(
            original_url="https://instagram.com/",
            short_code=utils.create_short_code(),
            user_id=create_test_user.user_id
        )
    ]

    session.add_all(links)
    session.commit()

    return links