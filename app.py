from flask import Flask, session, request, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "MrPoopyButthole"
app.debug = True

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def show_home():
    """Shows main page, sets multiple sessions"""
    board = boggle_game.make_board()
    session['board'] = board
    session['times_visited'] = session.get('times_visited', 0) + 1
    session['scores'] = session.get('scores', 0)
    session['guess'] = []
    return render_template('index.html', board=board, played=session['times_visited'], score=session['scores'])

@app.route('/check-word')
def check_word():
    """Checks the user's submitted guess to see if it is a valid word and if it's on the board"""
    word = request.args['guess']

    if word in session['guess']:
        return jsonify(result="word-already-used")
    elif word in boggle_game.words and boggle_game.check_valid_word(session['board'], word) == "ok":
        guess_list = session['guess']
        guess_list.append(word)
        session['guess'] = guess_list
        return jsonify(result="ok")
    elif word in boggle_game.words and boggle_game.check_valid_word(session['board'], word) == "not-on-board":
        return jsonify(result="not-on-board")
    elif word not in boggle_game.words and boggle_game.check_valid_word(session['board'], word) == "not-word":
        return jsonify(result="not-a-word")

@app.route('/save-score', methods=['POST'])
def save_score():
    """Saves the user's score after each game and determines if it's higher or lower than the previous one"""
    new_score = request.get_json()

    if new_score['score'] > session['scores']:
        session['scores'] = new_score['score']

    return {'scores': session['scores']}
