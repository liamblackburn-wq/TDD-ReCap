import uuid
from src.models import Duty

def test_get_duties_endpoint(client, test_duty):

        # ACT: Hit the Flask endpoint. Hit it HARD
        response = client.get('/duties')
        assert response.status_code == 200

        # ASSERT: Gimme data, verify it matches
        data = response.get_json()
        print(data)
        returned_coin = next(item for item in data if item['id'] == str(test_duty.id))

        assert returned_coin['name'] == 'DUTY_TEST'
        assert returned_coin['description'] == 'TEST DESCRIPTION'

def test_add_duty(client):

    payload = {
        'id': str(uuid.uuid4()),
        'name': 'POST_DUTY_TEST',
        'description': 'TEST DESCRIPTION'
    }

    response = client.post('/duties', json=payload)
    assert response.status_code == 201

    data = response.get_json()
    print(data)
    assert data['name'] == 'POST_DUTY_TEST'

    Duty.delete().where(Duty.id == payload['id']).execute()

def test_db_can_not_have_duplicate_duty_names(client, test_duty):

    #first duty created in pytest test_duty fixture
    payload = {
        'id': str(uuid.uuid4()),
        'name': 'DUTY_TEST',
        'description': 'TEST DESCRIPTION'
    }

    response = client.post('/duties', json=payload)
    data = response.get_json()
    assert response.status_code == 409
    assert data['error'] == 'Duty already exists'