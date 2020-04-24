import pytest
import tests.praw.integration as praw_i9n
from reddrec import create_app

@pytest.fixture
def test_config(i9n):
    return {
        'testing': True,
        'datadeps': {},
        'prawtest_reddit': i9n.reddit
    }

@pytest.fixture
def client(test_config):
    app = create_app(test_config=test_config)
    return app.test_client()

@pytest.fixture
def async_client(test_config):
    test_config['testing.async_queue'] = True
    app = create_app(test_config=test_config)
    return app.test_client()

@pytest.fixture
def i9n():
    i9n = praw_i9n.IntegrationTest()
    i9n.setup()
    return i9n
