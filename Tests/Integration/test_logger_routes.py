from app import _db_connect


def test_logs_successfully_returns(admin_client):
    response = admin_client.get("/api/logs")
    assert response.status_code == 200


def test_unauthorised_user_returns_401(client):
    response = client.get("/api/logs")
    assert response.status_code == 401


def test_none_admin_user_returns_403(user_client):
    response = user_client.get("/api/logs")
    assert response.status_code == 403

def test_static_files_do_not_access_database(client):
    client.get("/static/favicon.ico")
    response = _db_connect()
    assert response is None