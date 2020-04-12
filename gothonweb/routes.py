from flask import session, redirect, url_for, escape, request
from flask import render_template
from flask_login import login_required, login_user, logout_user
from gothonweb import planisphere, app, db, login_manager
from gothonweb.models import User


@login_manager.user_loader
def get_user(user):
    return User.query.get(user)


@app.route('/', methods=['GET'])
@login_required()
def index():
    session['room_name'] = planisphere.START
    return render_template("index.html")

@app.route('/login', methods=['GET'])
def get_login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def post_login():
    user = request.form(['user'])
    password = request.form(['password'])
    user = User.query.filter_by(user=user).first()
    login_user(user)
    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

@app.route('/signup', methods=['POST'])
def post_signup():
    user = request.form['username']
    password = request.form['password']
    user = User(user=user, password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(user).first()
    login_user(user)
    return redirect('/')

@app.route("/game/gothon", methods=['GET', 'POST'])
@login_required
def game_gothan():
    room_name = session.get('room_name')
    if request.method == 'GET':
        if room_name:
            room = planisphere.load_room(room_name)
            return render_template("gothon.html", room=room)
        else: 
            return render_template("you_died.html")
    else:
        action = request.form.get('action')

        if room_name and action:
            room = planisphere.load_room(room_name)
            next_room = room.go(action)

            if not next_room:
                session['room_name'] = planisphere.name_room(room)
            else:
                session['room_name'] = planisphere.name_room(next_room)
            
            return redirect(url_for("game"))


@app.route("/game/mosquito", methods=['GET', 'POST'])
@login_required
def game_mosquito():
    #TODO game as a route parameter
    return render_template("mosquito.html")