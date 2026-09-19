import pytest
from app import database_models , models


def test_generate_link( authorized_client):
    response = authorized_client.post('/links' , json = { "original_url": "https://instagram.com/" } )

    assert response.status_code == 201

    data=response.json()
    assert "link" in data

    # checking if links start with localhost
    assert data["link"].startswith('http://localhost:8000')


# checking if the link got stored in the database
def test_link_stored(authorized_client , session):
    response = authorized_client.post('/links' , json={"original_url": "https://google.com/"})

    assert response.status_code == 201

    data = response.json()

    link = session.query(
        database_models.link_schema).filter(
        database_models.link_schema.original_url == "https://google.com/").first()

    assert link is not None



# get all links 
def test_get_all_links(authorized_client,dummy_links):

    response=authorized_client.get('/links')

    assert response.status_code ==200

    data = response.json()

    # as data is a list we have to iterate inside the list
    for link in data:
        assert "original_url" in link
        assert "short_url" in link
        assert "clicks" in link
        assert "created_at" in link


# delete links
def test_delete_links(authorized_client , dummy_links):
    
    link = dummy_links[0]

    response = authorized_client.delete(f'/links/{link.id}')

    assert response.status_code == 200

    assert response.json()['detail'] == 'link deleted'

    