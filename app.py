from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "boggy23!"


boggle_game = Boggle()

@app.route("/")
def homepage():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
    

# @app.route('/')
# def front_page():
#     board = boggle_game.make_board()
#     return render_template('index.html', board=board)

# @app.route('/board')
# def show_board():
#     boggle_game = Boggle()
#     board = boggle_game.make_board()
#     session['board'] = board
#     return render_template('index.html', board=board)

# @app.route('/guess', methods=['POST'])
# def check_word():
#     board = request.json['board']
#     word = request.json['word']
#     result = boggle_game.check_valid_word(board, word)
#     return {'result': result}