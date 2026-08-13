from app import _db_connect


def test_home_route_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_user_logs_in_successfully(client):
    response = client.post(
        "/api/login", json={"username": "user", "password": "user123"}
    )
    assert response.status_code == 200


def test_admin_logs_in_successfully(client):
    response = client.post(
        "/api/login", json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200


def test_incorrect_user_password_returns_401(client):
    response = client.post(
        "/api/login", json={"username": "user", "password": "user321"}
    )
    assert response.status_code == 401


def test_incorrect_admin_password_returns_401(client):
    response = client.post(
        "/api/login", json={"username": "admin", "password": "admin321"}
    )
    assert response.status_code == 401


def test_incorrect_user_username_returns_401(client):
    response = client.post(
        "/api/login", json={"username": "resu", "password": "user123"}
    )
    assert response.status_code == 401


def test_incorrect_admin_username_returns_401(client):
    response = client.post(
        "/api/login", json={"username": "nimda", "password": "admin123"}
    )
    assert response.status_code == 401


def test_static_files_do_not_access_database(client):
    client.get("/static/favicon.ico")
    response = _db_connect()
    assert response is None


def test_logs_successfully_returns(admin_client):
    response = admin_client.get("/api/logs")
    assert response.status_code == 200


def test_unauthorised_user_returns_401(client):
    response = client.get("/api/logs")
    assert response.status_code == 401


def test_none_admin_user_returns_403(user_client):
    response = user_client.get("/api/logs")
    assert response.status_code == 403
