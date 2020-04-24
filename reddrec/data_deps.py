import pickle
import os

class DataDeps:
    _already_setup = False

    _subreddits = None
    _subs_index = dict()

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
    def setup(deps={}):
        """
        There are some data dependencies that are required for the server to
        run. We simply load them from disk and demarshal with pickle.
        """

        if DataDeps._already_setup:
            return

        DataDeps._already_setup = True

        if 'subreddits' in deps:
            DataDeps._subreddits = deps['subreddits']
        else:
            path = os.path.join(os.path.dirname(__file__),
                    '../datadeps/gen/subreddits.pickle')

            with open(path, 'rb') as f:
                DataDeps._subreddits = pickle.load(f)

        if type(DataDeps._subreddits) is not list:
            raise Exception('Subreddits data dep must be a list')

        for i, sub in enumerate(DataDeps._subreddits):
            DataDeps._subs_index[sub.lower()] = i
