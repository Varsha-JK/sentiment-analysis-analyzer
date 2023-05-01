import json


def test_home_route(app, client):
    response = client.get('/')
    assert response.status_code == 200

def test_analyze_route(app, client, topic):
    response = client.get('/analyze/{}'.format(topic))
    res = json.loads(response.data.decode('utf-8'))
    assert type(res) is dict
    assert res['status'] == 'success'
    assert response.status_code == 200


def test_sentiment_route(app, client, topic):
    response = client.get('/analyze/{}/sentiment'.format(topic))
    assert response.status_code == 200

def test_wordcloud_route(app, client, topic):
    response = client.get('/analyze/{}/wordcloud'.format(topic))
    print(response)
    assert response.status_code == 200