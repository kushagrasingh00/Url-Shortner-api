from fastapi import FastAPI , status
import pytest
from fastapi.middleware.cors import CORSMiddleware
from app import models
import jwt
from app.Oauth2 import SECRET,ALGORITHM


def test_register_user(client):
    response = client.post('/register' , json ={'email':'test@gmail.com' , 'password':'test123'})

    assert response.status_code == 201
    assert response.json()['email'] == 'test@gmail.com'

    # method 2
    new_user = models.response_user_register(**response.json())
    assert new_user.email == 'test@gmail.com'


def test_register_duplicate_email(client,create_test_user):
    response = client.post('/register' , json = {'email':'testuser1@gmial.com' , 'password':'test123'})

    assert response.status_code == 409
    assert response.json()['detail'] == 'user exists'


def test_user_login(client,create_test_user):

    response=client.post('/login' , json={'email':create_test_user.email , 'password':'test123'})

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'

    # method 1
    # login_result = models.token(**response.json())
    # payload = jwt.decode( login_result.access_token   ,SECRET,algorithms=[ALGORITHM])
    
    payload = jwt.decode(response.json()['access_token'],SECRET,algorithms=[ALGORITHM])

    assert payload.get("user_id") == create_test_user.user_id 

def test_login_wrong_password(client,create_test_user):
    response = client.post('/login' , json={'email':create_test_user.email , 'password':'WRONG PASSWORD'})

    assert response.status_code == 401
    assert response.json()['detail'] == 'invalid credentials'

def test_login_nonexistent_user(client,create_test_user):
    response = client.post('/login' , json={'email': 'nonexistent@gmial.com' , 'password':'WRONG PASSWORD'} )

    assert response.status_code == 401
    assert response.json()['detail'] == 'invalid credentials'


# test delete user
def test_delete_user(authorized_client , create_test_user):

    response=authorized_client.delete(f'/user/{create_test_user.user_id}')

    assert response.status_code == 200
