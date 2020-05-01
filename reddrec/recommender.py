import numpy as np
from .reddit import Comments

class Recommender:

    def __init__(self, reddit, username, subreddits, matrix):
        self.reddit = reddit
        self.username = username
        self.subreddits = subreddits
        self.matrix = matrix
        self._user_exists = False
        self._recommendations = None

    def perform(self):
        pass

    def user_exists(self):
        # return self._user_exists
        return True

    def recommendations(n=3):
        # return self._recommendations
        return [
            {
                'subreddit': 'pi',
                'confidence': 3.1415927
            },
            {
                'subreddit': 'phi',
                'confidence': 1.61803399
            },
            {
                'subreddit': 'e',
                'confidence': 2.7182818
            },
        ]
