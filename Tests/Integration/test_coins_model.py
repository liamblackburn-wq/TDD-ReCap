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

def test_delete_coin_successfully(client):
    coin = Coin.create(name='COIN_TEST')

    response = client.delete(f'/coins/{coin.id}')
    data = response.get_json()

    assert response.status_code == 200
    assert data['message'] == 'Coin deleted successfully'

    assert Coin.select().where(Coin.id == coin.id).count() == 0

def test_delete_coin_endpoint_returns_404(client):
    response = client.delete(f'/coins/{uuid.uuid4()}')

    data = response.get_json()
    assert response.status_code == 404

    assert data['error'] == 'Coin does not exist'

def test_put_request_updates_coin_name(client):
    coin = Coin.create(name='COIN_TEST')

    json_payload = {
        "name": "NIOC_TSET"
    }

    response = client.put(f'/coins/{coin.id}', json=json_payload)
    data = response.get_json()

    db_coin = Coin.get_by_id(coin.id)

    assert response.status_code == 200
    assert data['name'] == 'NIOC_TSET'
    assert db_coin.name == 'NIOC_TSET'

def test_update_coin_endpoint_returns_404_if_uuid_not_found(client):
    random_uuid = uuid.uuid4()
    payload = {'name': 'NON_EXISTENT_COIN'}

    response = client.put(f'/coins/{random_uuid}', json=payload)
    data = response.get_json()

    assert response.status_code == 404
    assert data['error'] == 'Coin does not exist'





