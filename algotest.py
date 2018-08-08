from flask import Flask, render_template, request, Response
import requests
from function import algo_result
import json
from functools import reduce
import matplotlib.pyplot as plt
import matplotlib
import numpy

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.debug = True

data_store = []

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/draw')
def draw_graph():
    algo_name = request.args.get('algoname')

    for row in data_store:
        if row['algo_name'] == algo_name:
            PnL_data = row['pnl_data']

    plt.figure()

    x = numpy.arange(0, len(PnL_data), 1)
    y = numpy.array(PnL_data)
    plt.plot(x, y)
    plt.show()
    return render_template('index.html', data=data_store)

@app.route('/submit', methods=['POST'])
def get_ticker():
    ticker = request.form.get('ticker')
    signal = request.form.get('signal')
    trade = request.form.get('trade')
    algo_name = request.form.get('algo_name')

    ticker_data = requests.get("https://api.iextrading.com/1.0/stock/{}/chart/1y".format(ticker))
    print(ticker_data.content)
    prices = [row['close'] for row in json.loads(ticker_data.content.decode("utf-8"))]

    [positions, PnL] = algo_result(signal, trade, prices)
    average_pnl = reduce(lambda x, y: x + y, PnL) / len(PnL)
    data_store.append({'algo_name': algo_name, 'average_pnl': average_pnl, 'pnl_data': PnL, 'position': positions})

    return render_template('index.html', data=data_store)

if __name__ == '__main__':
    app.run()
