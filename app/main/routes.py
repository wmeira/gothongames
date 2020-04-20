from flask import session, redirect, url_for, request, flash, render_template
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Ranking
from ..games import Gothon, available_games

@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html")

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

