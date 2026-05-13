import pytest
from app import app as my_app

@pytest.fixture
def app():
    yield my_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_post_method_returns_200(client):
    form_data = {"duties": ["Duty 1", "Duty 2", "Duty 3"]}
    response = client.post('/', data=form_data)
    assert response.status_code == 200

def test_app_post_method_returns_400(client):
    form_data = {}
    response = client.post('/', data=form_data)
    assert response.status_code == 400

def test_duties_persistence_after_refresh(client):
    form_data = {"duties": ["Duty 1"]}
    client.post('/', data=form_data)
    response = client.get('/')
    assert b"<strong>Duty 1</strong>" in response.data

def test_remove_app_route_returns_200(client):
    response = client.get('/remove/1', follow_redirects=True)

    assert response.status_code == 200

# def test_duty_removed_when_remove_button_is_clicked(client):
#     form_data = {"duties": ["Duty 1"]}
#     client.post('/', data=form_data)
#     response = client.get('/remove/1', follow_redirects=True)
#
#     assert b"<strong>Duty 1</strong>" not in response.data
