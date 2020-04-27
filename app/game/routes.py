from flask import session, redirect, url_for, request, flash, render_template, current_app
from flask_login import login_required, current_user
from . import game
from .. import db
from ..models import Ranking
from .forms import GameForm, GameQuizForm
from ..games import available_games
import pickle

def clear_session(): 
    session.pop('game')

@game.route("/<name>", methods=['GET', 'POST'])
@login_required
def play(name):
    if not available_games[name]:
        clear_session()
        return abort(404)

    if not session.get('game'):        
        game = available_games[name]()
        current_app.logger.debug("new game (without session)")
    else:
        game = pickle.loads(session.get('game'))
        if game.name != name \
            or request.referrer is None \
            or (request.referrer and 'game' not in request.referrer):
            game = available_games[name]()
            current_app.logger.debug("new game (different game)") 

    current_app.logger.debug(game.current_room.name)

    if game.current_room.is_quiz():
        form = GameQuizForm(game.current_room)
    else:
        form = GameForm()

    if form.validate_on_submit():
        action = form.action.data
        game.trials += 1
        new_room, msg = game.go(action)
        current_app.logger.debug(new_room.name)
        current_app.logger.debug(game.current_room.name)
        if msg is not None and msg != '':
            flash(msg, 'error')
            if not game.current_room.is_quiz():                
                form.action.data = ''
        else:
            #game over
            if game.current_room in ["death", "The End"]:
                r = Ranking(game=game.name, score=game.calculate_score(), user=current_user)
                db.session.add(r)
                db.session.commit()
            else:
                session['game'] = pickle.dumps(game)
            return redirect(url_for(".play", name=game.name))
            
    session['game'] = pickle.dumps(game)
    return render_template(f"/game/game.html", form=form, game=game)
    
    # room_name = session.get('room_name')
    

    # if form.validate_on_submit():
    #     action = form.action.data

    #     if action:
    #         room = game.load_room(room_name)
    #         next_room = room.go(action)

    #         if not next_room:
    #             session['room_name'] = game.name_room(room)
    #         else:
    #             session['room_name'] = game.name_room(next_room)
            
    #         return redirect(url_for(".game_gothon"))
    
    return render_template("/game/you_died.html")
    
    