from boggle import Boggle
from flask import Flask, render_template, session, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from boggle import *

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def homepage():
    """Shows the boggle gameboard"""
    print(request.headers)

    board = boggle_game.make_board()
    session['board'] = board
    print(session, board)
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    return render_template('homepage.html', board=board, highscore=highscore, nplays=nplays)

@app.route('/check-word')
def check_word():
    """Check if the word is valid in the dictionary"""
    
    word = request.args['word']
    board = session['board']
    print(board, word.upper())
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})
    

@app.route('/post-score', methods=['POST'])
def post_score():
    """Update the scores"""

    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord = score > highscore)