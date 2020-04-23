from tests.praw.integration import IntegrationTest
from unittest import mock
from reddrec.reddit.comments import Comments

class TestReddit(IntegrationTest):

    @mock.patch("time.sleep", return_value=None)
    def test_comment_stream(self, _):
        with self.recorder.use_cassette('test_comment_stream__exact_last_10'):
            c = Comments(self.reddit, 'spez')
            recents = c.fetch_recent(n=10)

            assert len(recents) == 10
            assert recents[0].body.startswith('Think it only works on')
