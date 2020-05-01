from reddrec.recommender import Recommender

def test_full(i9n):
    with i9n.recorder.use_cassette('Recommender.full'):
        r = Recommender(i9n.reddit, 'GabeNewellBellevue')
        r.perform()
        assert r.redditor_found == True
        assert len(r.recommendations) > 0
        assert 'subreddit' in r.recommendations[0]
        assert 'confidence' in r.recommendations[0]
