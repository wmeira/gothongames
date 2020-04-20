from flask import session, redirect, url_for, request, flash, render_template, current_app
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .forms import LoginForm, SignupForm
from .. import db
from ..models import User
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(f'Welcome, {username}!', 'success')
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                return redirect(url_for('main.home'))
            return redirect(next)            
        flash('Login Unsuccessful. Invalid username or password. ', 'error')
    return render_template("auth/login.html", form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'error')
    return redirect(url_for('main.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email_data = form.email.data
        password = form.password.data
        user = User(username=form.username.data, email=email_data, password=password)
        db.session.add(user)
        db.session.commit()
        if current_app.config['MAIL_USERNAME']:
            send_email(email_data, 'Welcome to GothonWeb!', 'mail/new_user', user=user)
        flash(f'Player name \'{username}\' registered with success! Login to play!', 'success')
        return redirect(url_for('.login'))
    else:
        form.password.data = ''
        form.confirm.data = ''
    return render_template("auth/signup.html", form=form)
