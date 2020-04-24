import pytest
import tests.praw.integration as praw_i9n
from reddrec import create_app

def test_config():
    return {
        'testing': True,
        'datadeps': {},
    }

@pytest.fixture
def client():
    app = create_app(test_config=test_config())
    return app.test_client()

@pytest.fixture
def async_client():
    conf = test_config()
    conf['testing.async_queue'] = True
    app = create_app(test_config=conf)
    return app.test_client()

@pytest.fixture
def i9n():
    i9n = praw_i9n.IntegrationTest()
    i9n.setup()
    return i9n
