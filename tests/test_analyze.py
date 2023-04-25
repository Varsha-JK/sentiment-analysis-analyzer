import json
from app import app

def test_analyze():
    response = app.test_client().get('/analyze/books')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res) is dict
    assert res['status'] == 'success'
    assert response.status_code == 200


def test_collector_connection():
    response = app.test_client().get('/analyze/books')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res) is dict
    assert res['status'] == 'success'
    assert response.status_code == 200