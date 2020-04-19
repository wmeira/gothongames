import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Ranking

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Ranking=Ranking)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import pytest
    if test_names:  
        tests = list(test_names)
    else:
        tests = ['tests']
    tests.append('-v')
    pytest.main(args=tests)