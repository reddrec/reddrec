import pytest
from flask.json import dumps, loads
from reddrec import app

@pytest.fixture
def client():
    return app.test_client()

def test_index(client):
    rv = client.get('/')
    assert b'Hello recommender system!' in rv.data

def test_recommend_bad_username(client):
    rv = client.get('/recommend/Y*A(DS')

    assert rv.headers['Content-Type'] == 'application/json'
    assert rv.status_code == 400

    json = loads(rv.data)
    assert 'error' in json

def test_recommend_is_processing(client):
    rv = client.get('/recommend/GabeNewellBellevue')

    assert rv.headers['Content-Type'] == 'application/json'
    assert rv.status_code == 202

    json = loads(rv.data)
    assert 'status' in json
