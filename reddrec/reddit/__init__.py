import os
import praw
from reddrec.reddit.comments import Comments

def reddit_from_env():
    client_id = os.environ['reddrec_praw_client_id']
    client_secret = os.environ['reddrec_praw_client_secret']
    username = os.environ['reddrec_praw_username']
    password = os.environ['reddrec_praw_password']
    user_agent = os.environ['reddrec_praw_user_agent']

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

__all__ = [
    'reddit_from_env',
    'Comments'
]
