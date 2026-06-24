import uuid
from src.models import Coin


def test_get_coins_endpoint(client, test_coin):
    # ACT: Hit the Flask endpoint. Hit it HARD
    response = client.get('/coins')
    assert response.status_code == 200

    # ASSERT: Gimme data, verify it matches
    data = response.get_json()
    print(data)
    returned_coin = next(item for item in data if item['id'] == str(test_coin.id))

    assert returned_coin['id'] == str(test_coin.id)
    assert returned_coin['name'] == 'COIN_TEST'


def test_add_coin(client):
    payload = {
        'id': str(uuid.uuid4()),
        'name': 'POST_COIN_TEST'
    }

    response = client.post('/coins', json=payload)
    assert response.status_code == 201

    data = response.get_json()
    print(data)
    assert data['name'] == 'POST_COIN_TEST'
    assert data['id'] == str(payload['id'])

    Coin.delete().where(Coin.id == payload['id']).execute()


def test_db_can_not_have_duplicate_coin_names(client, test_coin):
    # first coin created in pytest test_coin fixture
    payload = {
        'id': str(uuid.uuid4()),
        'name': 'COIN_TEST'
    }

    response = client.post('/coins', json=payload)
    data = response.get_json()
    assert response.status_code == 409
    assert data['error'] == 'Coin already exists'

def test_db_rejects_coin_names_that_contain_numbers(client):
    payload = {
        'id': str(uuid.uuid4()),
        'name': 'COIN_TEST_123'
    }

    response = client.post('/coins', json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert data['error'] == 'Coin names cannot contain numbers.'