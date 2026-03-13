import pytest
import requests
import random
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from api.deps import get_db
from models.models import Base

# Use a local SQLite file for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    # Create the tables once per test session
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Use a fresh session that commits to the file
    session = TestingSessionLocal()

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield session

    # Clean up after the test
    session.close()
    app.dependency_overrides.clear()


BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def session():
    return requests.Session()


@pytest.fixture(scope="session")
def credentials():
    email = f"pytest_{random.randint(10000,99999)}@mail.com"
    password = "TestPassword123"
    return {"email": email, "password": password}


@pytest.fixture(scope="function")
def auth_token(session, base_url, credentials, db_session):
    session.post(
        f"{base_url}/auth/register/",
        json=credentials
    )

    r = session.post(
        f"{base_url}/auth/login/",
        json=credentials
    )

    assert r.status_code == 200
    token = r.json()["access_token"]

    session.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return token


@pytest.fixture
def short_url(session, base_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = session.post(
        f"{base_url}/urls/",
        json={"long_url": "https://example.com"},
        headers=headers
    )
    assert r.status_code in [200, 201]
    return r.json()