def test_post_duty_sanitises_xss_in_description(admin_client):
    payload = {
        "name": "Duty 99",
        "description": "<script>alert('xss')</script>",
    }

    response = admin_client.post("/duties", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Duty 99"
    assert data["description"] == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"


def test_post_coin_sanitises_xss_payload(admin_client):
    payload = {"name": "<iframe src=javascript:alert(xss)></iframe>"}

    response = admin_client.post("/coins", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "&lt;iframe src=javascript:alert(xss)&gt;&lt;/iframe&gt;"


def test_put_coin_sanitises_xss_payload(admin_client, test_coin):
    payload = {"name": "<img src=x onerror=alert(xss)>"}

    response = admin_client.put(f"/coins/{test_coin.id}", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "&lt;img src=x onerror=alert(xss)&gt;"