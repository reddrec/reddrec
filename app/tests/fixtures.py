import pytest
from reddrec import create_app

# https://github.com/pallets/flask/blob/1.1.2/examples/tutorial/tests/conftest.py

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client():
    return app.test_client()
