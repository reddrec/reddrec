import praw
from reddrec.reddit import USER_AGENT

class Comments:

    def __init__(self, reddit, username):
        self.reddit = reddit
        self.user = reddit.redditor(username)

    def fetch_recent(self, n=100):
        print
        pass
