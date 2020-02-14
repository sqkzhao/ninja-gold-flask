from flask import Flask, session, redirect, request, render_template
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'totallytopsecret'

@app.route('/')
def index():
    if 'gold' not in session:
        session['gold'] = 0
        session['move'] = 0
        session['end_game'] = False
    if 'activities' not in session:
        session['activities'] = []
        session['activities'].insert(0,"Game Began")
    return render_template('index.html', gold=session['gold'], activities=session['activities'])

@app.route('/process_money', methods=['POST'])
def process_money():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if session['end_game']:
        return redirect('/')
    if session['move'] > 14 and not session['end_game']:
        if session['gold'] >= 500:
            session['activities'].insert(1, f"You won! ({now}) - Reset to play agian!")
        else:
            session['activities'].insert(1, f"You lost.. ({now}) - Reset to play agian..")
        session['end_game'] = True
        return redirect('/')

    if request.form['action'] == "casino":
        gold = random.randint(0, 50)
        if random.randint(1, 4)%2 == 1:
            session['gold'] -= gold
            session['activities'].insert(1, f"Entered a casino and lost {gold} golds.. Ouch.. ({now})")
        else:
            session['gold'] += gold
            session['activities'].insert(1, f"Entered a casino and earned {gold} golds! Yeah! ({now})")
    else:
        if request.form['action'] == "farm":
            gold = random.randint(10, 20)
        if request.form['action'] == "cave":
            gold = random.randint(5, 10)
        if request.form['action'] == "house":
            gold = random.randint(2, 5)
        session['gold'] += gold
        session['activities'].insert(1, f"Earned {gold} golds from the {request.form['action']}! ({now})")
        # message = f"<li style="color: green;">{gold}</li>"
        # in html: {{message|safe}}
    session['move'] += 1
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')

app.run(debug=True)