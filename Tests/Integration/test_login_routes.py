# def test_user_logs_in_successfully(client):
#     response = client.post(
#         "/api/login", json={"username": "user", "password": "user123"}
#     )
#     assert response.status_code == 200
#
#
# def test_admin_logs_in_successfully(client):
#     response = client.post(
#         "/api/login", json={"username": "admin", "password": "admin123"}
#     )
#     assert response.status_code == 200
#
#
# def test_incorrect_user_password_returns_401(client):
#     response = client.post(
#         "/api/login", json={"username": "user", "password": "user321"}
#     )
#     assert response.status_code == 401
#
#
# def test_incorrect_admin_password_returns_401(client):
#     response = client.post(
#         "/api/login", json={"username": "admin", "password": "admin321"}
#     )
#     assert response.status_code == 401
#
#
# def test_incorrect_user_username_returns_401(client):
#     response = client.post(
#         "/api/login", json={"username": "resu", "password": "user123"}
#     )
#     assert response.status_code == 401
#
#
# def test_incorrect_admin_username_returns_401(client):
#     response = client.post(
#         "/api/login", json={"username": "nimda", "password": "admin123"}
#     )
#     assert response.status_code == 401
#
# def test_authenticated_user_redirected_from_login_page(user_client):
#     response = user_client.get("/")
#
#     assert response.status_code == 302
#     assert response.headers["Location"] == "/apprenticeduties"
#
# def test_authenticated_admin_redirected_from_login_page(admin_client):
#     response = admin_client.get("/")
#
#     assert response.status_code == 302
#     assert response.headers["Location"] == "/apprenticeduties"
#
def test_logout_redirects_to_login_page(user_client):
    response = user_client.get("/api/logout")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"