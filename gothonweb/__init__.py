from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xzGkV2GUaG6wzJN4wFeFzseWDnY3GkjYdVibeH7CE3w'

# SQLAlchemy (ORM) configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/gothon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Package to encrypt password
bcrypt = Bcrypt(app)

# Login manager configurations
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'error'
login_manager.login_message = 'Please log in to play the game'

# Protect site against CSRF (cross-site request forgery)
csrf = CSRFProtect(app)

# Moment - UTC time handler
moment = Moment(app)

#modules
from gothonweb import games, routes, models

# if DB is unavailable, install it
# import os

# db_path = os.path.abspath(os.getcwd()) + '/gothonweb/db/gothon.db'
# if not os.path.exists(db_path):
#     db.create_all()
#     print('SQLite Database created')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=models.User, Ranking=models.Ranking)

