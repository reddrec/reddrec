def is_flask_in_testing_mode():
    """
    Long name to ensure we don't call this function outside of a Flask context.
    (e.g. don't call it from an rq job)
    """
    from flask import current_app
    return bool(current_app.config.get('testing'))

def reddit_from_env():
    import os
    import praw

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
