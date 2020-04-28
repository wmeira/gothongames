from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (DataRequired, InputRequired, EqualTo,
                                Length, Email, Regexp)
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Username must have only letter,'
                                              ' numbers, dots or underscores')
                                       ])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=1, max=40)])
    email = StringField('E-mail',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                             validators=[
                                 InputRequired(),
                                 Length(min=8, max=200,
                                        message=('A password should have at '
                                                 'least 8 characters')),
                                 EqualTo('confirm',
                                         message='Passwords must match')
                             ])
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'This username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. '
                                  'Please choose a different one.')
