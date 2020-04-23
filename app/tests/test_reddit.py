from reddrec.reddit.comments import Comments

def test_comment_stream(i9n):
    with i9n.recorder.use_cassette('Reddit.test_comment_stream__exact_last_10'):
        c = Comments(i9n.reddit, 'spez')
        recents = c.fetch_recent(n=10)

        assert len(recents) == 10
        assert recents[0].body.startswith('Think it only works on')
