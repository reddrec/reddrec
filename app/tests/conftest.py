import pytest
from betamax import Betamax
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
