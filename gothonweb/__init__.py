from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xzGkV2GUaG6wzJN4wFeFzseWDnY3GkjYdVibeH7CE3w'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/gothon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#package to encrypt password
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

#protect site against CSRF (cross-site request forgery)
csrf = CSRFProtect(app)

#modules
from gothonweb import planisphere, routes, models

# if DB is unavailable
import os.path
if os.path.exists('/db/gothon.db') is False:
    db.create_all()
    print('SQLite Database created')


    