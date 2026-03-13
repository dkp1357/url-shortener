# test_logout.py
def test_logout(base_url, session, credentials):
    r = session.post(f"{base_url}/auth/login/", json=credentials)
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = session.post(f"{base_url}/auth/logout/", headers=headers)
    assert r.status_code == 200


def test_token_blacklist(base_url, session, credentials):
    r = session.post(f"{base_url}/auth/login/", json=credentials)
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    session.post(f"{base_url}/auth/logout/", headers=headers)

    r = session.get(f"{base_url}/auth/me/", headers=headers)
    assert r.status_code in [401, 403]

    session.headers.pop("Authorization", None)