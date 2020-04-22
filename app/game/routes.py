from flask import session, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from . import game
from .. import db
from .forms import GameForm
from ..games import available_games


@game.route("/<name>", methods=['GET', 'POST'])
@login_required
def play(name):
    form = GameForm()
    game = available_games[name]
    print(f"Game {game}")
    if session.get('game') or session.get('game') != name \
        or request.referer is None \
        or 'game' not in request.referer:
        
        session['room_name'] = game.start_room.name
        session['game'] = name
        session['trials'] = 0
        session['score'] = 0
        # session['lifes'] = game.start_life

    print(session.get('room_name'))
    room_name = session.get('room_name')

    if not game or not room_name:
        return render_template()

    if form.validate_on_submit():
        action = form.action.data

        if action:
            room = game.load_room(room_name)
            next_room = room.go(action)

            if not next_room:
                session['room_name'] = game.name_room(room)
            else:
                session['room_name'] = game.name_room(next_room)
            
            return redirect(url_for(".game_gothon"))
    
    if room_name:
        room = game.load_room(room_name)
        return render_template(f"/game/{session.get('game')}.html", room=room, form=form)
    return render_template("/game/you_died.html")
    
    