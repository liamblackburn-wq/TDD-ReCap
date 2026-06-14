import uuid
from src.models import Duty

def test_get_duties_endpoint(client, test_duty):

        # ACT: Hit the Flask endpoint. Hit it HARD
        response = client.get('/duties')
        assert response.status_code == 200

        # ASSERT: Gimme data, verify it matches
        data = response.get_json()
        print(data)
        returned_duty = next(item for item in data if item['id'] == str(test_duty.id))

        assert returned_duty['name'] == 'Duty 1'
        assert returned_duty['description'] == 'TEST DESCRIPTION'

def test_create_duty_returns_201(client):

    payload = {
        'id': str(uuid.uuid4()),
        'name': 'Duty 1',
        'description': 'TEST DESCRIPTION'
    }

    response = client.post('/duties', json=payload)
    data = response.get_json()
    print(data)
    assert response.status_code == 201
    assert data['name'] == 'Duty 1'

    Duty.delete().where(Duty.id == payload['id']).execute()

def test_invalid_duty_returns_400(client):
    payload = {
        'id': str(uuid.uuid4()),
        'name': 'TEAPOT',
        'description': 'TEST DESCRIPTION'
    }

    response = client.post('/duties', json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert "Duty name must start with 'Duty' followed by a number." in data['error']

def test_db_can_not_have_duplicate_duty_names(client, test_duty):

    #first duty created in pytest test_duty fixture
    payload = {
        'id': str(uuid.uuid4()),
        'name': 'Duty 1',
        'description': 'TEST DESCRIPTION'
    }

    response = client.post('/duties', json=payload)
    data = response.get_json()
    assert response.status_code == 409
    assert data['error'] == 'Duty already exists'