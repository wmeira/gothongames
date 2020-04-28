from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
from ..games import Room


class GameForm(FlaskForm):
    action = StringField('Action', validators=[DataRequired()])
    submit = SubmitField('Submit')


class GameQuizForm(FlaskForm):
    action = RadioField('Action')
    submit = SubmitField('Submit')

    def __init__(self, room, *args, **kwargs):
        super(GameQuizForm, self).__init__(*args, **kwargs)
        self.action.choices = [(key, key) for key in room.paths.keys()]
        self.room = room
