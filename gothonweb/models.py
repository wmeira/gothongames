from gothonweb import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    user = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)