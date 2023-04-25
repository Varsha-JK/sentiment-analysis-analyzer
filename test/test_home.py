import pytest
from app import app # Flask instance of the API

def test_home_route():
    response = app.test_client().get('/')
    assert response.status_code == 200