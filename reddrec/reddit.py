import praw
import numpy as np
import re
from .data_deps import DataDeps

class Comments:

    def __init__(self, reddit, username, subreddits=None):
        DataDeps.inject(self, subreddits=subreddits)

        self.reddit = reddit
        self.user = reddit.redditor(username)

    def fetch_ratings(self, n_comments=1000, normalize=True):
        """
        Create ratings row vector for the user based on their comment history
        """

        recents = self.fetch_recent(n_comments)
        comment_subs = map(lambda r: r.subreddit.display_name.lower(), recents)
        vec = np.zeros(len(self.subreddits))

        for sub in comment_subs:
            idx = self.subs_index.get(sub)
            if idx is not None:
                vec[idx] += 1

        if normalize:
            vec /= np.linalg.norm(vec)

        return vec

    def fetch_recent(self, n):
        return list(self.user.comments.new(limit=n))

def hot_posts(reddit, subreddit_name, n=10):
   subreddit = reddit.subreddit(subreddit_name)
   return list(subreddit.hot(limit=n))

def usernames(reddit, posts, up_to=0):
    usernames = set()

    for comments in map(lambda p: p.comments.list(), posts):
        for comment in comments:
            if type(comment) is praw.models.Comment and comment.author:
                name = comment.author.name
                usernames.add(name.lower())

            if up_to > 0 and len(usernames) == up_to:
                return usernames

    return usernames


VALID_USER_REGEXP = re.compile('[a-zA-Z\\-_\\d]+')

def valid_username(username):
    """
    We only want to process valid Reddit usernames.
    Rules found at: https://www.reddit.com/register
    """

    if not (3 <= len(username) <= 20):
        return False

    if VALID_USER_REGEXP.fullmatch(username) is None:
        return False

    return True
