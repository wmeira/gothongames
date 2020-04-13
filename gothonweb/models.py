from gothonweb import db
from flask_login import UserMixin

# UserMixin provides default implementations for the methods that Flask-Login expects user objects to have.

class User(UserMixin, db.Model):   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}', {self.score})"
