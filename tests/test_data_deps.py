import pytest
from reddrec.data_deps import DataDeps

@pytest.fixture
def mock_deps():
    import numpy as np

    matrix = np.array([
        [10,  4,  0],
        [ 0,  0,  1],
        [ 2, 23,  0],
        [ 0,  0, 99],
        [ 0,  1, 50]
    ])

    deps = {
        'subreddits': ['Valorant', 'GlobalOffensive', 'Minecraft'],
        'matrix': matrix
    }

    return deps

def test_data_deps_exist(mock_deps):
    DataDeps.setup(mock_deps)

    assert DataDeps.subreddits() == ['valorant', 'globaloffensive', 'minecraft']

    assert 'globaloffensive' in DataDeps.subs_index()
    assert 'GlobalOffensive' not in DataDeps.subs_index()
    assert DataDeps.subs_index()['globaloffensive'] == 1

    assert DataDeps.matrix().shape == (5, 3)
    assert DataDeps.matrix().dtype == 'float64'
    assert DataDeps.matrix()[0][0] == 10.0
    assert DataDeps.matrix()[-1][-1] == 50.0

def test_setup_and_teardown(mock_deps):
    import copy
    mock_deps2 = copy.deepcopy(mock_deps)

    DataDeps.setup(mock_deps)
    assert DataDeps.subreddits()[0] == 'valorant'
    DataDeps.teardown()

    mock_deps2['subreddits'].insert(0, 'TF2')
    DataDeps.setup(mock_deps2)
    assert DataDeps.subreddits()[0] == 'tf2'
