import praw
import numpy as np

class Comments:

    def __init__(self, reddit, username, subreddits=None):

        self.reddit = reddit
        self.user = reddit.redditor(username)

        if subreddits:
            from .utils import lookup_table
            self.subreddits = subreddits
            self.subs_index = lookup_table(subreddits)
        else:
            from .data_deps import DataDeps
            self.subreddits = DataDeps.subreddits()
            self.subs_index = DataDeps.subs_index()

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

def usernames(reddit, posts):
    usernames = set()

    for comments in map(lambda p: p.comments.list(), posts):
        for comment in comments:
            if type(comment) is praw.models.Comment and comment.author:
                name = comment.author.name
                usernames.add(name.lower())

    return usernames
