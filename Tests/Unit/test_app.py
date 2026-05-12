def test_app_post_method_returns_200(client):
    form_data = {"duties": ["Duty 1", "Duty 2", "Duty 3"]}
    response = client.post('/', data=form_data)
    assert response.status_code == 200