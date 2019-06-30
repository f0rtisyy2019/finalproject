from joblib import dump, load
import os
import pandas as pd
import numpy as np

import sqlalchemy
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from scraping import scrape
from news_scraping import news_scrape
import pyEX as p
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib
from joblib import load
from model import modelColumns

from OptimalPortfolio import optPortfolio
from UserPortfolio import userPortfolio
from Plots import ScatterResults
from Plots import Radar
from Plots import Scatter3d

application = app = Flask(__name__)

# Database Setup
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:f0rtisyy@localhost/stockpy"
db = SQLAlchemy(app)

class symbols(db.Model):
    symbol = db.Column(db.String(10), primary_key=True)
    stock_name = db.Column(db.String(80), unique=True)

    def __init__(self, symbol, stock_name):
        self.symbol = symbol
        self.stock_name = stock_name

    def __repr__(self):
        return self.symbol


def interprete_user_input(data):
    car_age_mean = 4.29170400885157
    car_age_std = 2.951528451522811
    mileage_mean = 47817.15397998972
    mileage_std = 33004.03467591136

    #initialize the target vector with zero values
    user_input = np.zeros(878)
    user_input[0] = (data['mileage']-mileage_mean)/mileage_std
    user_input[1] = (data['year']-car_age_mean)/car_age_std

    #convert the input to match the column name and find the index
    maker_col = 'Make_' + data['maker']
    maker_ind = modelColumns.index(maker_col)
    user_input[maker_ind] = 1

    model_col = 'Model_' + data['model']
    model_ind = modelColumns.index(model_col)
    user_input[model_ind] = 1

    return user_input

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/single")
def single():
    return render_template("single.html")

@app.route("/robert")
def robert():
    return render_template("robert.html")

@app.route("/ali")
def ali():
    return render_template("ali.html")

@app.route("/carmelo", methods = ['POST', 'GET'])
def carmelo():
    scatterJson = {}
    scatterJson3d = {}
    radarJson = {}
    if request.method == 'POST':
        user = {'ticker1': '','amount1': '','ticker2': '','amount2': '','ticker3': '','amount3': '',}
        result1 = 0
        result2 = 0
        result3 = 0
        share1 = 0
        share2 = 0
        share3 = 0
        try:
            user['start_date'] = request.form['start_date']
            user['ticker1'] = request.form['ticker1']
            user['amount1'] = request.form['amount1']
            user['ticker2'] = request.form['ticker2']
            user['amount2'] = request.form['amount2']
            user['ticker3'] = request.form['ticker3']
            user['amount3'] = request.form['amount3']
        except:
            print('user input fetch error')

        try:
            symbols = [request.form['ticker1'], request.form['ticker2'], request.form['ticker3']]
            weights = [float(request.form['amount1'])/(float(request.form['amount1'])+float(request.form['amount2'])+ float(request.form['amount3'])),
                        float(request.form['amount2'])/(float(request.form['amount1'])+float(request.form['amount2'])+ float(request.form['amount3'])),
                        float(request.form['amount3'])/(float(request.form['amount1'])+float(request.form['amount2'])+ float(request.form['amount3']))]

            opt = optPortfolio(symbols, str(request.form['start_date']))
            opt_sharpe = opt[0]
            opt_lowrisk = opt[1]
            opt_df = opt[2]

            user = userPortfolio(symbols, weights, request.form['start_date'])

            scatterJson = ScatterResults(opt_df, opt_sharpe, opt_lowrisk, user)
            radarJson = Radar(opt_sharpe, opt_lowrisk, user)
            scatterJson3d = Scatter3d(opt_df)
        except:
            print("tikcer1 search fail")

    return render_template("carmelo.html", graphJSON=scatterJson, graphJSON1=scatterJson3d, graphJSON2=radarJson)

@app.route("/aftab")
def aftab():
    return render_template("aftab.html")

@app.route("/adriel")
def adriel():
    return render_template("adriel.html")

@app.route("/george")
def george():
    return render_template("george.html")

@app.route("/car_price", methods=['POST', 'GET'])
def car_price():
    price_pred = 0
    if request.method == 'POST':
        car = {'maker': '', 'model': '', 'year': 0.0, 'mileage': 0.0}
        try:
            car['maker'] = request.form['maker']
            car['model'] = request.form['model']
            car['year'] = 2019 - float(request.form['year'])
            car['mileage'] = float(request.form['mileage'])
 
            load_gbr_model = load('model/used_car_model.joblib')
            ipt = interprete_user_input(car)
            price_pred = str(int(load_gbr_model.predict([ipt])[0]))
        except:
            print("FAIL TO PARSE FORM INFO!")
        return price_pred

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        user = {'name': '','email': '','start_date': '','ticker1': '','amount1': '','ticker2': '','amount2': '','ticker3': '','amount3': '',}
        result1 = 0
        result2 = 0
        result3 = 0
        share1 = 0
        share2 = 0
        share3 = 0
        try:
            user['name'] = request.form['name']
            user['email'] = request.form['email']
            user['start_date'] = request.form['start_date']
            user['ticker1'] = request.form['ticker1']
            user['amount1'] = request.form['amount1']
            user['ticker2'] = request.form['ticker2']
            user['amount2'] = request.form['amount2']
            user['ticker3'] = request.form['ticker3']
            user['amount3'] = request.form['amount3']
        except:
            print('user input fetch error')

        try:
            df1 = p.chartDF(request.form['ticker1'], '5y').reset_index()
            start_price1 = df1.loc[df1['date'] ==
                                  request.form['start_date']]['close'].item()
            end_price1 = df1.iloc[-1:, 4].item()
            share1 = float(request.form['amount1']) / start_price1
            result1 = (end_price1 - start_price1) * share1
        except:
            print("tikcer1 search fail")

        try:
            df2 = p.chartDF(request.form['ticker2'], '5y').reset_index()
            start_price2 = df2.loc[df2['date'] ==
                                   request.form['start_date']]['close'].item()
            end_price2 = df2.iloc[-1:, 4].item()
            share2 = float(request.form['amount2']) / start_price2
            result2 = (end_price2 - start_price2) * share2
        except:
            print("tikcer2 search fail")

        try:
            df3 = p.chartDF(request.form['ticker3'], '5y').reset_index()
            start_price3 = df3.loc[df3['date'] ==
                                   request.form['start_date']]['close'].item()
            end_price3 = df3.iloc[-1:, 4].item()
            share3 = float(request.form['amount3']) / start_price3
            result3 = (end_price3 - start_price3) * share3
        except:
            print("tikcer3 search fail")

        result = result1 + result2 + result3
        result = round(result, 2)
        user['share'] = [share1, share2, share3]
        print(result)
        print(user)
    return render_template("result.html", result = result, user = user)

@app.route("/ticker")
def ticker():
    """Return a list of symbol names."""
    symb = [str(sy) for sy in symbols.query.all()]
    return jsonify(symb)

@app.route('/scrape')
def topGainLose():
    return jsonify(Stocks=scrape())

@app.route("/news/<symbol>")
def topNews(symbol):
    return jsonify(News=news_scrape(symbol))


if __name__ == "__main__":
    app.run()
