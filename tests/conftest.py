import pytest

from app import get_app

@pytest.fixture
def app():
    flask_app = get_app()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()