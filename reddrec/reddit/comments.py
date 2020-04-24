import praw
import numpy as np
from reddrec import DataDeps

class Comments:

    def __init__(self, reddit, username):
        self.reddit = reddit
        self.user = reddit.redditor(username)

    def fetch_ratings(self, n_comments=1000, normalize=True):
        recents = self.fetch_recent(n_comments)
        comment_subs = map(lambda r: r.subreddit.display_name.lower(), recents)
        vec = np.zeros(len(DataDeps.subreddits()))

        for sub in comment_subs:
            idx = DataDeps.subs_index().get(sub)
            if idx is not None:
                vec[idx] += 1

        if normalize:
            vec /= np.linalg.norm(vec)

        return vec

    def fetch_recent(self, n):
        return list(self.user.comments.new(limit=n))
