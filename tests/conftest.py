import pytest

from backend.app import create_app
from backend.db import db_session, drop_all, engine
from tests.factories import BirdFactory


@pytest.fixture
def app():
    app = create_app()

    app.connection = engine.connect()

    yield app

    app.connection.close()
    drop_all(engine)


@pytest.fixture(scope="function")
def session(app):
    app.transaction = app.connection.begin()
    ctx = app.app_context()
    ctx.push()

    session = db_session()

    BirdFactory._meta.sqlalchemy_session = session

    yield session

    app.transaction.close()
    session.close()
    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
