from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class GameForm(FlaskForm):
    action = StringField('Action', validators=[DataRequired()])
    submit = SubmitField('Submit')
     


