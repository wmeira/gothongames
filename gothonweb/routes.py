from flask import session, redirect, url_for, escape, request, flash, render_template
from flask_login import login_required, login_user, logout_user, current_user
from gothonweb import app, db, login_manager, bcrypt
from gothonweb.models import User, Ranking
from gothonweb.forms import LoginForm, SignupForm
from gothonweb.games import Gothon, available_games

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'error')
    return render_template("login.html", form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Player name \'{username}\' registered with success! Login to play!', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route("/game/gothon", methods=['GET', 'POST'])
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
            
            return redirect(url_for("game_gothon"))


@app.route("/game/mosquito", methods=['GET', 'POST'])
@login_required
def game_mosquito():
    #TODO game as a route parameter
    return render_template("/game/mosquito.html")


@app.route("/ranking", methods=['GET'])
def ranking():
    global_ranking = {}
    user_ranking = {}
    for game in available_games: 
        best_five_scores = Ranking.get_best_scores(game, 5)
        
        if current_user:
            best_user_score = Ranking.get_best_user_score(current_user.username, game)
        global_ranking[game] = best_five_scores
        user_ranking[game] = best_user_score
    print(global_ranking)
    return render_template("ranking.html", global_ranking=global_ranking, user_ranking=user_ranking)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("/errors/404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("/errors/500.html"), 500