from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager, bcrypt
# from werkzeug.security import generate_password_hash, check_password_hash

# UserMixin provides default implementations for the methods that Flask-Login
# expects user objects to have.


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # self.password_hash = generate_password_hash(password) #werkzeug
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def verify_password(self, password):
        # return check_password_hash(self.password_hash, password) #werkzeug
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except BaseException:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return "User('{}', '{}', '{}', {})" .format(self.id,
                                                    self.username,
                                                    self.email,
                                                    self.confirmed)


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
        return (Ranking.query.filter_by(game=game)
                             .order_by(Ranking.score.desc())[:ntop])

    @classmethod
    def get_best_user_score(cls, user_id, game):
        """
        Get best score of a user in a given game.
        """
        return (Ranking.query.filter_by(game=game, user_id=user_id)
                             .order_by(Ranking.score.desc())
                             .first())

    def __repr__(self):
        return "Ranking('{}', '{}', '{}', {}, {})".format(self.id,
                                                          self.user_id,
                                                          self.game,
                                                          self.score,
                                                          self.ts)


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))
