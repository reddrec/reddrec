import numpy as np
from .reddit import Comments
from .data_deps import DataDeps

class Recommender:

    def __init__(self, reddit, username, subreddits=None, matrix=None):
        DataDeps.inject(self, subreddits=subreddits, matrix=matrix)

        self._reset()
        self.reddit = reddit
        self.username = username

    def perform(self):
        self._reset()

        # TODO: Can we automatically inject downwards? i.e. we should be able to
        # omit subreddits=self.subreddits and magically have
        # Comments.subreddits==self.subreddits.

        c = Comments(self.reddit, self.username, subreddits=self.subreddits)

        if c.user.id is None:
            # The user could not be found on Reddit
            return

        # TODO: Maybe normalize the ratings. Currently rows DataDeps.matrix() are not
        # normalized so we do not normalize in fetch_ratings.

        user_ratings = c.fetch_ratings(normalize=False)
        neighbor_ratings = self._most_similar_row(user_ratings)
        non_visited = self._filter_visited(user_ratings, neighbor_ratings)

        # Sort in decreasing order by rating
        recommendations = sorted(non_visited, key=lambda tup: -tup[1])

        self._recommendations = self._build_list(recommendations)
        self._redditor_found = True

    @property
    def redditor_found(self):
        return self._redditor_found

    @property
    def recommendations(self):
        return self._recommendations

    def _most_similar_row(self, ratings):
        """
        Find the row vector in the matrix that is most similar to the given ratings.
        """

        max_similarity_index = 0
        max_similarity = -1

        for i, row in enumerate(self.matrix):
            test_similarity = self._similarity(ratings, row)
            if test_similarity > max_similarity:
                max_similarity_index = i
                max_similarity = test_similarity

        return self.matrix[max_similarity_index]

    def _similarity(self, a, b):
        """
        Cosine similarity between vectors a and b
        """

        A = np.linalg.norm(a)
        B = np.linalg.norm(b)

        if A * B == 0:
            return 0

        return a.dot(b) / (A * B)

    def _filter_visited(self, user_ratings, neighbor_ratings):
        """
        Get a new list of (subreddit, neighbor_rating) only where the
        corresponding user rating is zero and the neighbor rating is non-zero.

        The end result is a list containing candidate recommendations.
        """

        non_visited = []

        for i, rating in enumerate(user_ratings):
            if rating == 0 and neighbor_ratings[i] != 0:
                non_visited.append((self.subreddits[i], neighbor_ratings[i]))

        return non_visited

    def _build_list(self, recommendations):
        """
        Create list like: [{'subreddit': subreddit, 'confidence': rating}]
        """

        return [{'subreddit': r[0], 'confidence': r[1]} for r in recommendations]

    def _reset(self):
        self._redditor_found = False
        self._recommendations = None
