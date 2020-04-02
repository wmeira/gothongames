from flask import session, redirect, url_for, escape, request
from flask import render_template
from gothonweb import planisphere, app

@app.route('/')
def index():
    # isso é usado para configurar a seção com valores iniciais
    session['room_name'] = planisphere.START
    return redirect(url_for("game"))

@app.route("/game", methods=['GET', 'POST'])
def game():
    room_name = session.get('room_name')

    if request.method == 'GET':
        if room_name:
            room = planisphere.load_room(room_name)
            return render_template("show_room.html", room=room)
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
