def test_home_route_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200

def test_custom_404_handler(client):
    response = client.get('/non-existent-route')
    assert response.status_code == 404
    assert response.json == {"error": "Page not found"}

def test_admin_route_blocked_for_guest(client):
    response = client.post('/coins', json={'name': 'Test Coin'})
    assert response.status_code == 401
