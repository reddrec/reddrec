from reddrec.reddit import Comments, reddit_from_env
from reddrec.data_deps import DataDeps
import numpy as np

def recommend(username, testing_mode):
    """
    Performs subreddit recommendations for Reddit user given by username.

    Returns dict of recommendations if they could be found.
    Returns None when recommendations cannot be made (e.g. user doesn't exist).
    """

    reddit = None

    if testing_mode:
        # Safe since testing mode uses a synchronous queue that has access to
        # the Flask current_app object.
        from flask import current_app
        reddit = current_app.config.get('prawtest_reddit')
    else:
        reddit = reddit_from_env()

    c = Comments(reddit, username)

    ratings = c.fetch_ratings(normalize=False)
    sorted_indices = ratings.argsort()[::-1] # Greatest to least order
    subs = DataDeps.subreddits()

    mk_recommendation = lambda i: { 'subreddit': subs[i], 'confidence': ratings[i] }

    top_3 = [mk_recommendation(i) for i in sorted_indices[:3]]

    return {
        'username': username,
        'recommendations': top_3
    }
