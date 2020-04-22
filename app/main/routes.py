from flask import render_template
from flask_login import current_user
from . import main
from ..models import Ranking
from ..games import available_games

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