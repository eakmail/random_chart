from ast import arg
from operator import ge
from random import random
import time
import flask
from flask import request, jsonify, render_template
from threading import Event, Thread

app = flask.Flask(__name__)
app.config["DEBUG"] = True

event = Event()

tickers = [[0] for i in range(100)]

@app.route('/')
def index():
    return render_template('index.html') # https://jinja.palletsprojects.com/en/3.1.x/templates/

# http://localhost:4999/api/v1/tickers?ticker=1&start=1
@app.route('/api/v1/tickers', methods=['GET'])
def get_tickers():
    if ('ticker' in request.args) & ('start' in request.args):
        ticker = int(request.args['ticker'])
        start = int(request.args['start'])
    else:
        return "Error: No ticker and start fields provided. Please specify an ticker and start."

    print("%i %i", start, len(tickers[ticker]))

    while (start == len(tickers[ticker])):
        event.wait(timeout = 1)
        event.clear()

    print("%i %i", start, len(tickers[ticker]))

    return jsonify(tickers[ticker][start:])

@app.route('/api/v1/start_time', methods=['GET'])
def get_start_time():
    return jsonify(start_time)

def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement

def append_ticker(ticker):
    last = ticker[-1]
    ticker.append(last + generate_movement())
    return ticker

def generate_tickers_loop():
    global tickers
    while True:        
        time.sleep(1.0)
        tickers = [append_ticker(ticker) for ticker in tickers]
        event.set()

thread = Thread(target=generate_tickers_loop)

start_time = int(time.time())

thread.start()            
    
app.run(port=4999)
