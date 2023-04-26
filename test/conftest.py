import pytest
from app import app as backend_app

@pytest.fixture
def app():
    yield backend_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def topic():
    yield "music"