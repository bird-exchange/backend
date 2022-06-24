import pytest
from backend.app import create_app


@pytest.fixture
def app():
    app = create_app(test_config=True)
    yield app
