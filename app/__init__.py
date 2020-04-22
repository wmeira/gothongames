from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_migrate import Migrate
from flask_mail import Mail
from config import config

# Mail 
mail = Mail()

# SQLAlchemy (ORM) configurations
db = SQLAlchemy()

# Package to encrypt password
bcrypt = Bcrypt()

# Login manager configurations
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = 'error'
login_manager.login_message = 'Please log in to play'

# Protect site against CSRF (cross-site request forgery)
csrf = CSRFProtect()

# Moment - UTC time handler
moment = Moment()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .game import game as game_blueprint
    app.register_blueprint(game_blueprint, url_prefix='/game')
    
    return app
