import pytest
import tests.praw.integration as praw_i9n
from reddrec import create_app

@pytest.fixture
def client():
    app = create_app(test_config={'testing': True})
    return app.test_client()

@pytest.fixture
def async_client():
    app = create_app(test_config={
        'testing': True,
        'testing.async_queue': True
    })
    return app.test_client()

@pytest.fixture
def i9n():
    i9n = praw_i9n.IntegrationTest()
    i9n.setup()
    return i9n
