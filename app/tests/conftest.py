import pytest
from app import create_app, db
from app.settings import TestingConfig


@pytest.fixture
def app():
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    yield app.test_client()
