import flask
import random

import countries

app = flask.Flask(__name__, static_url_path='/')

def randomized() -> dict:
    return random.choice(countries.data)

said = None
correct = None

@app.route('/')
def index():
    global said
    global correct
    
    correct = randomized()
    
    choose = [correct, randomized(), randomized(), randomized(), randomized()]
    random.shuffle(choose)

    was_correct = flask.request.cookies.get('said') == flask.request.cookies.get('correct')
    score = flask.request.cookies.get('score')

    if not score:
        score = '0'


    resp = flask.make_response(flask.render_template('index.html',
        flag=correct['code'],
        choose=choose,
        last=flask.request.cookies.get('correct'),
        score=score,
        color='green' if was_correct else 'red'
    ))
    resp.set_cookie('score', str(int(score)+2) if was_correct else str(int(score)-1))
    
    return resp

@app.route('/choose/<name>')
def country(name):
    global said
    global correct
    
    said = name
    resp = flask.make_response(flask.redirect('/'))
    
    if correct:
        resp.set_cookie('said', said)
        resp.set_cookie('correct', correct['name'])
    
    return resp

app.run(port=4949, debug=True)