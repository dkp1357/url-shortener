import random


def test_create_url(base_url, session, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = session.post(
        f"{base_url}/urls/",
        json={"long_url": "https://openai.com"},
        headers=headers
    )
    assert r.status_code in [200, 201]
    assert "short_code" in r.json()


def test_create_custom_url(base_url, session, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    code = f"pytestcustom_{random.randint(10000, 99999)}"
    r = session.post(
        f"{base_url}/urls/",
        json={
            "long_url": "https://openai.com",
            "custom_code": code
        },
        headers=headers
    )
    assert r.status_code in [200, 201]


def test_list_urls(base_url, session, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = session.get(f"{base_url}/urls/", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_update_url(base_url, session, short_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    code = short_url["short_code"]
    r = session.put(
        f"{base_url}/urls/{code}/",
        json={"long_url": "https://github.com"},
        headers=headers
    )
    assert r.status_code == 200


def test_delete_url(base_url, session, short_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    code = short_url["short_code"]
    r = session.delete(f"{base_url}/urls/{code}/", headers=headers)
    assert r.status_code == 204