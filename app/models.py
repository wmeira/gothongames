from . import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime

# UserMixin provides default implementations for the methods that Flask-Login expects user objects to have.
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', ')"

class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False, default=0)
    game = db.Column(db.String(40), nullable=False)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('rankings', lazy=True))

    @classmethod
    def get_best_scores(cls, game, ntop): 
        """
        Get the n top best scores in a given game

        :param game name
        :param ntop is the n top best scores
        """
        return Ranking.query.filter_by(game=game).order_by(Ranking.score.desc())[:ntop]

    @classmethod
    def get_best_user_score(cls, user_id, game): 
        """
        Get best score of a user in a given game.
        """
        return Ranking.query.filter_by(game=game, user_id=user_id).order_by(Ranking.score.desc()).first()

    def __repr__(self):
        return f"Ranking('{self.id}', '{self.user_id}', '{self.game}', {self.score}, {self.timestamp})"



@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))