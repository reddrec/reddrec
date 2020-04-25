from flask.json import dumps, loads

def test_recommend_bad_username(i9n, client):
    with i9n.recorder.use_cassette('Routes.recommend_bad_username'):
        rv = client.get('/recommend/Y*A(DS')

        assert rv.headers['Content-Type'] == 'application/json'
        assert rv.status_code == 400

        json = loads(rv.data)
        assert 'error' in json

def test_recommend_is_completed(i9n, client):
    with i9n.recorder.use_cassette('Routes.recommend_is_completed'):
        rv = client.get('/recommend/GabeNewellBellevue')

        assert rv.headers['Content-Type'] == 'application/json'
        assert rv.status_code == 200

        json = loads(rv.data)
        assert json['username'] == 'gabenewellbellevue'
        assert len(json['recommendations']) == 3

def test_recommend_is_processing(i9n, async_client):
    with i9n.recorder.use_cassette('Routes.recommend_is_processing'):
        rv = async_client.get('/recommend/spez')

        assert rv.headers['Content-Type'] == 'application/json'
        assert rv.status_code == 202

        json = loads(rv.data)
        assert 'status' in json
