from flask import session, redirect, url_for, escape, request, flash, render_template
from flask_login import login_required, login_user, logout_user, current_user
from gothonweb import planisphere, app, db, login_manager, bcrypt
from gothonweb.models import User
from gothonweb.forms import LoginForm, SignupForm

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/home")
@login_required
def home():
    session['room_name'] = planisphere.START
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'error')
    return render_template("login.html", form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Player name {username} registered with success! Login to play!', 'success')
        return redirect(url_for('login'))
    else:
        #TODO error messages
        print(form.validate)
    return render_template("signup.html", form=form)


@app.route("/game/gothon", methods=['GET', 'POST'])
@login_required
def game_gothon():
    room_name = session.get('room_name')
    if request.method == 'GET':
        if room_name:
            room = planisphere.load_room(room_name)
            return render_template("/game/gothon.html", room=room)
        else: 
            return render_template("/game/you_died.html")
    else:
        action = request.form.get('action')

        if room_name and action:
            room = planisphere.load_room(room_name)
            next_room = room.go(action)

            if not next_room:
                session['room_name'] = planisphere.name_room(room)
            else:
                session['room_name'] = planisphere.name_room(next_room)
            
            return redirect(url_for("game_gothon"))


@app.route("/game/mosquito", methods=['GET', 'POST'])
@login_required
def game_mosquito():
    #TODO game as a route parameter
    return render_template("/game/mosquito.html")