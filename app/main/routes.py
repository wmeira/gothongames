from flask import session, redirect, url_for, request, flash, render_template, current_app, abort
from flask_login import login_required, login_user, logout_user, current_user
from . import main
from .forms import LoginForm, SignupForm
from .. import db, bcrypt
from ..models import User, Ranking
from ..games import Gothon, available_games
from ..email import send_email

def is_safe_url(url):
    """
    Simple implementation to check if next URL is safe
    """    
    if not url:
        return False
    url = url.strip()
    return url[0] == '/' and '?' not in url


@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html")

@main.route('/login', methods=['GET', 'POST'])
def login():    
    if current_user.is_authenticated == True:
        return redirect(url_for('.home'))
    
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome, {username}!', 'success')
            next = request.args.get('next')                    
            if not is_safe_url(next):
                return redirect(url_for('.home'))
            return redirect(next)            
        else:
            flash('Login Unsuccessful. Please check username and password', 'error')
    return render_template("login.html", form=form)

@main.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email_data = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username, email=email_data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        if current_app.config['MAIL_USERNAME']:
            send_email(email_data, 'Welcome to GothonWeb!', 'mail/new_user', user=user)
        flash(f'Player name \'{username}\' registered with success! Login to play!', 'success')
        return redirect(url_for('.login'))
    else:
        form.password.data = ''
        form.confirm.data = ''
    return render_template("signup.html", form=form)

@main.route("/ranking", methods=['GET'])
def ranking():
    global_ranking = {}
    user_ranking = {}
    for game in available_games.keys(): 
        best_five_scores = Ranking.get_best_scores(game, 5)
        
        if current_user.is_authenticated:
            best_user_score = Ranking.get_best_user_score(current_user.username, game)
            user_ranking[game] = best_user_score
        else:
            user_ranking[game] = None
        global_ranking[game] = best_five_scores
    return render_template("ranking.html", global_ranking=global_ranking, user_ranking=user_ranking)


@main.route("/game/gothon", methods=['GET', 'POST'])
@login_required
def game_gothon():
    # TODO check if I am entering in the game right now, if so, starts the session
    #session['room_name'] = Gothon.start_room

    # session['room_name']
    # session['trials']
    # session['tips']
    # session['lifes']

    room_name = session.get('room_name')

    if request.method == 'GET':
        if room_name:
            room = Gothon.load_room(room_name)
            return render_template("/game/gothon.html", room=room)
        else: 
            return render_template("/game/you_died.html")
    else:
        action = request.form.get('action')

        if room_name and action:
            room = Gothon.load_room(room_name)
            next_room = room.go(action)

            if not next_room:
                session['room_name'] = Gothon.name_room(room)
            else:
                session['room_name'] = Gothon.name_room(next_room)
            
            return redirect(url_for(".game_gothon"))


@main.route("/game/riddlemaster", methods=['GET', 'POST'])
@login_required
def game_riddlemaster():
    #TODO game as a route parameter
    return render_template("/game/riddlemaster.html")

