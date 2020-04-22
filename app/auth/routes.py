from flask import redirect, url_for, request, flash, render_template, current_app
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .forms import LoginForm, SignupForm
from .. import db
from ..models import User
from ..email import send_email

#before_request: blueprint scope
#before_app_request: application scope
@auth.before_app_request
def before_request():
    if not request.path.startswith('/static') \
        and request.blueprint not in ['auth', 'main'] \
        and current_user.is_authenticated \
        and current_user.confirmed is False:
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GET', 'POST'])
def login():    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
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
            token = user.generate_confirmation_token()
            send_email(email_data, 'Confirm your account!', 'mail/new_user', user=user, token=token)
        flash(f'Player \'{username}\' registered! A confirmation e-mail has been sent to you!', 'success')
        return redirect(url_for('.login'))
    else:
        form.password.data = ''
        form.confirm.data = ''
    return render_template("auth/signup.html", form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired. '
              'A new confirmation e-mail has been sent to you. Check your e-mail!', 'error')
        new_token = current_user.generate_confirmation_token()
        send_email(email_data, 'Confirm your account!', 
                   'mail/new_user', user=current_user, token=new_token)
    return redirect(url_for('main.home'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    new_token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your account!', 
                   'mail/new_user', user=current_user, token=new_token)
    flash('A new confirmation email has been sent to you by e-mail.', 'success')
    return redirect(url_for('main.home'))
