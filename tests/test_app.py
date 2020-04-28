from flask import current_app
from app import create_app, db
from pytest import fixture

app = create_app('testing')
web = app.test_client()


@fixture
def app_context():
    # setup
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield

    # teardown
    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_app_exists(app_context):
    assert current_app is not None


def test_app_is_testing(app_context):
    assert (current_app.config['TESTING'])


def test_index():
    rv = web.get('/', follow_redirects=True)
    assert rv.status_code == 200
