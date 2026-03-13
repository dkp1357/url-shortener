import random


def test_register(base_url, session):
    random_id = random.randint(10000, 99999)
    payload = {
        "email": f"reg_{random_id}@mail.com",
        "password": "StrongPassword123"
    }
    r = session.post(f"{base_url}/auth/register/", json=payload)
    assert r.status_code == 201


def test_login(base_url, session):
    payload = {
        "email": "login_test@mail.com",
        "password": "Password123"
    }

    session.post(f"{base_url}/auth/register/", json=payload)

    r = session.post(f"{base_url}/auth/login/", json=payload)

    assert r.status_code == 200
    assert "access_token" in r.json()