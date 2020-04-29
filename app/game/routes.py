from flask import redirect, url_for, request, render_template
from flask import current_app, session, flash
from flask_login import login_required, current_user
from . import game
from .. import db
from ..models import Ranking
from .forms import GameForm, GameQuizForm
from ..games import available_games
import pickle


@game.route("/<name>", methods=['GET', 'POST'])
@login_required
def play(name):
    if not available_games[name]:
        session.pop('game')
        return abort(404)

    if not session.get('game'):
        game = available_games[name]()
    else:
        game = pickle.loads(session.get('game'))
        if (game.name != name
                or request.referrer is None
                or (request.referrer and 'game' not in request.referrer)
                or game.is_game_over()):
            game = available_games[name]()

    current_room = game.current_room
    if current_room.is_quiz():
        form = GameQuizForm(current_room)
    else:
        form = GameForm()

    if form.validate_on_submit():
        action = form.action.data
        new_room, msg = game.go(action)
        if msg is not None and msg != '':
            # wrong answer
            flash(msg, 'error')
            if not game.current_room.is_quiz():
                form.action.data = ''

        if game.is_game_over():
            # game_over
            r = Ranking(game=game.name, score=game.calculated_score(),
                        user=current_user._get_current_object())
            db.session.add(r)
            db.session.commit()
            session['game'] = pickle.dumps(game)
            return redirect(url_for(".gameover"))

        # next room
        if new_room != current_room:
            if not current_room.is_quiz():
                flash("You passed!", "success")
        else:
            game.trials += 1  # same room, new trial
        session['game'] = pickle.dumps(game)
        return redirect(url_for('.play', name=game.name))

    session['game'] = pickle.dumps(game)
    return render_template(f"/game/game.html", form=form, game=game)


@game.route("/gameover", methods=['GET'])
@login_required
def gameover():
    if session.get('game'):
        game = pickle.loads(session.get('game'))
        if game.is_game_over():
            session.pop('game')
            return render_template("/game/gameover.html", game=game)
    return redirect(url_for('main.home'))
