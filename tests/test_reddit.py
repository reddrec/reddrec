from reddrec.reddit import Comments, hot_posts, usernames, valid_username
import numpy as np

def test_valid_username():
    # Proper symbols
    assert valid_username('_example-123')
    assert not valid_username('_*example-123')
    assert not valid_username('spaces arent valid')

    # Proper lengths
    assert valid_username('lol')
    assert valid_username('A' * 20)
    assert not valid_username('xD')
    assert not valid_username('A' * 21)
    assert not valid_username('')

def test_fetch_recent(i9n):
    with i9n.recorder.use_cassette('Comments.fetch_recent'):
        c = Comments(i9n.reddit, 'spez')
        recents = c.fetch_recent(n=10)

        assert len(recents) == 10
        assert recents[0].body.startswith('Think it only works on')

def test_fetch_ratings(i9n):
    with i9n.recorder.use_cassette('Comments.fetch_ratings'):
        c = Comments(i9n.reddit, 'GabeNewellBellevue')

        ratings = c.fetch_ratings(n_comments=200, normalize=False)
        norm = np.linalg.norm(ratings)
        np.testing.assert_almost_equal(norm, 47.9374593)

        # Default behavior is normalized
        ratings2 = c.fetch_ratings(n_comments=200)
        norm2 = np.linalg.norm(ratings2)
        np.testing.assert_almost_equal(norm2, 1.0)

def test_hot_posts(i9n):
    with i9n.recorder.use_cassette('Reddit.hot_posts'):
        posts = hot_posts(i9n.reddit, 'globaloffensive')
        assert(len(posts) == 10)
        assert(posts[0].id == 'g5eht2')
        assert(posts[-1].id == 'gamfpm')

def test_usernames(i9n):
    with i9n.recorder.use_cassette('Reddit.usernames'):
        posts = hot_posts(i9n.reddit, 'globaloffensive')
        unique_users = usernames(i9n.reddit, posts)
        assert len(unique_users) == 799

def test_usernames_up_to(i9n):
    with i9n.recorder.use_cassette('Reddit.usernames_up_to'):
        posts = hot_posts(i9n.reddit, 'globaloffensive')
        unique_users = usernames(i9n.reddit, posts, up_to=15)
        assert len(unique_users) == 15
