import pytest
from app import app as backend_app
from unittest.mock import Mock


@pytest.fixture
def app():
    yield backend_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def topic():
    yield "music"


@pytest.fixture
def mock_api_request(mocker):
    mock = Mock(status_code=200)
    mock.json.return_value = {"status":200}
    mocker.patch("requests.get", return_value=mock)
    return mock
