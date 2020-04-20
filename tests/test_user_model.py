from app import db, create_app
from app.models import User
from pytest import raises, fixture


@fixture
def app_context():
    # setup
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    
    yield
    
    # teardown
    db.session.remove()
    db.drop_all()
    app_context.pop()

def test_password_setter(app_context):
    u = User(password='cat')
    assert u.password_hash is not None

def test_no_password_getter(app_context):
    u = User(password='cat')
    with raises(AttributeError):
        u.password

def test_password_verification(app_context):
    u = User(password='cat')
    assert u.verify_password('cat')
    assert not u.verify_password('dog')

def test_password_salts_are_random(app_context):
    u = User(password='cat')
    u2 = User(password='cat')
    assert u.password_hash != u2.password_hash