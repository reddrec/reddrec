def recommend(username):
    """
    Performs subreddit recommendations for Reddit user given by username.

    Returns dict of recommendations if they could be found.
    Returns None when recommendations cannot be made (e.g. user doesn't exist).
    """

    import random
    import time
    from flask.json import dumps

    fake_data = {
        'username': username,
        'recommendations': [
            {'subreddit': 'xbox', 'confidence': random.random()},
            {'subreddit': 'ps4',  'confidence': random.random()},
            {'subreddit': 'pc',   'confidence': random.random()},
        ]
    }

    time.sleep(3)

    if random.random() < 0.5:
        raise Exception('recommend: fake exception')

    if random.random() < 0.5:
        return None # signifies 'cannot recommend'

    return fake_data
