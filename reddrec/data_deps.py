import pickle
import os
import numpy as np
from .utils import lookup_table

class DataDeps:
    """
    Container class for data-dependencies required by the app.

    Data-dependencies are defined as any immutable data that we require to be
    loaded into app memory at startup. For example, the list of subreddits is a
    data-dependency since it does not change during runtime but gets generated
    ahead of time.

    Note:
        Lots of c&p'd code. Anyways in the future maybe we can have a better
        solution than this mess.
    """

    _already_setup = False

    _subreddits = None
    _subs_index = None
    _matrix = None

    @staticmethod
    def subreddits():
        if not DataDeps._already_setup:
            DataDeps.setup()
        return DataDeps._subreddits

    @staticmethod
    def subs_index():
        if not DataDeps._already_setup:
            DataDeps.setup()
        return DataDeps._subs_index

    @staticmethod
    def matrix():
        if not DataDeps._already_setup:
            DataDeps.setup()
        return DataDeps._matrix

    @staticmethod
    def inject(instance, subreddits=None, matrix=None):
        """
        Inject data-dependencies into instance for missing kwargs.

        TODO: make this a decorator? hide above methods in favor of this?
        """

        if subreddits:
            instance.subreddits = subreddits
            instance.subs_index = lookup_table(subreddits)
        else:
            instance.subreddits = DataDeps.subreddits()
            instance.subs_index = DataDeps.subs_index()

        if matrix:
            instance.matrix = matrix
        else:
            instance.matrix = DataDeps.matrix()

    @staticmethod
    def setup(deps={}):
        """
        There are some data dependencies that are required for the server to
        run. We simply load them from disk and demarshal with pickle.
        """

        if DataDeps._already_setup:
            raise Exception('DataDeps setup() called twice without teardown().')

        DataDeps._already_setup = True

        DataDeps._setup_subreddits(deps)
        DataDeps._setup_matrix(deps)

    @staticmethod
    def teardown():
        DataDeps._already_setup = False

    @staticmethod
    def _setup_subreddits(deps):
        subreddits = None

        if 'subreddits' in deps:
            subreddits = deps['subreddits']
        else:
            path = os.path.join(os.path.dirname(__file__),
                    '../datadeps/gen/subreddits.pickle')

            with open(path, 'rb') as f:
                subreddits = pickle.load(f)

        if type(subreddits) is not list:
            raise Exception('Subreddits data dep must be a list')

        # Normalize to lowercased subreddits and build index off of that.
        # Our index is lowercase, so always call str.lower before querying it.
        DataDeps._subreddits = [sub.lower() for sub in subreddits]
        DataDeps._subs_index = lookup_table(DataDeps._subreddits)

    @staticmethod
    def _setup_matrix(deps):
        matrix = None

        if 'matrix' in deps:
            matrix = deps['matrix']
        else:
            path = os.path.join(os.path.dirname(__file__),
                    '../datadeps/gen/matrix.pickle')

            with open(path, 'rb') as f:
                matrix = pickle.load(f)

        matrix = matrix.astype('float64')

        if len(matrix.shape) != 2 or not np.issubdtype(matrix.dtype, np.floating):
            raise Exception('Matrix must be 2d ndarray of floating point numbers')

        DataDeps._matrix = matrix
