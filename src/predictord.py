from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('stock_tool', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    template = 'predictord/index.html'
    error = None
    if request.method == 'POST':
        stock = request.form['stock']
        method = request.form['method']
        period = request.form['period']
        if not stock:
            error = 'Stock not informed.'
        if error is None:
            data=create_data(stock,period,method)
            return render_template(template, chart_data=data)
        flash(error)
    return render_template(template)    

def buy_sell_macd(data):
    import numpy as np
    bid = []
    ask = []
    flag = -1
    for i in range(len(data)):
        b = np.nan
        a = np.nan
        if data['MACD'][i] > data['Signal'][i] and flag != 1:
            b = data['Close'][i]
            flag = 1
        if data['MACD'][i] < data['Signal'][i] and flag != 0:
            a = data['Close'][i]
            flag = 0
        bid.append(b)
        ask.append(a)
    return (bid, ask)

def buy_sell_sma(data):
    import numpy as np
    bid = []
    ask = []
    flag = -1    
    for i in range(len(data)):
        b = np.nan
        a = np.nan
        if data['SMA30'][i] > data['SMA100'][i] and flag != 1:
            b = data['Close'][i]
            flag = 1
        if data['SMA30'][i] < data['SMA100'][i] and flag != 0:
            a = data['Close'][i]
            flag = 0
        bid.append(b)
        ask.append(a)
    return (bid, ask)

def buy_sell(data, method):
    if method == "sma":
        return buy_sell_sma(data)
    if method == "macd":
        return buy_sell_macd(data)    

def get_sma(stock_history):
    import pandas as pd
    sma30 = pd.DataFrame()
    sma30['Close'] = stock_history['Close'].rolling(window=30).mean()
    sma100 = pd.DataFrame()
    sma100['Close'] = stock_history['Close'].rolling(window=100).mean()
    data = {}
    data['SMA30'] = sma30['Close']
    data['SMA100'] = sma100['Close']
    return data

def get_macd(stock_history):
    short_ema = stock_history.Close.ewm(span=12,adjust=False).mean()
    long_ema = stock_history.Close.ewm(span=26,adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9,adjust=False).mean()
    data = {}
    data['MACD'] = macd
    data['Signal'] = signal
    return data

def get_stock_info(stock, period, method):
    import yfinance as yf
    stock_name = stock
    stock_period = period
    ticker = yf.Ticker(stock_name)
    stock_history = ticker.history(period=stock_period)
    if method == "sma":
        sma = get_sma(stock_history)
        stock_history['SMA30'] = sma['SMA30']
        stock_history['SMA100'] = sma['SMA100']
    if method == "macd":
        macd = get_macd(stock_history)
        stock_history['MACD'] = macd['MACD']
        stock_history['Signal'] = macd['Signal']
    bs = buy_sell(stock_history, method)
    stock_history['BID'] = bs[0]
    stock_history['ASK'] = bs[1]
    info = {}
    info['company'] = ticker.info['longName']
    info['history'] = stock_history
    info['recommendations'] = ticker.recommendations.tail().to_html()
    return info

def get_chart_data_for_history(stock_history):
    history = {}
    history['x'] = stock_history.index.to_list()
    history['y'] = stock_history['Close']
    history['type'] = 'scatter'
    history['name'] = 'Closing price'
    return history

def get_chart_data_for_sma30(stock_history):
    sma30 = {}
    sma30['x'] = stock_history.index.to_list()
    sma30['y'] = stock_history['SMA30']
    sma30['type'] = 'scatter'
    sma30['name'] = 'SMA30'
    return sma30

def get_chart_data_for_sma100(stock_history):
    sma100 = {}
    sma100['x'] = stock_history.index.to_list()
    sma100['y'] = stock_history['SMA100']
    sma100['type'] = 'scatter'
    sma100['name'] = 'SMA100'
    return sma100

def get_chart_data_for_macd(stock_history):
    macd = {}
    macd['x'] = stock_history.index.to_list()
    macd['y'] = stock_history['MACD']
    macd['type'] = 'scatter'
    macd['name'] = 'MACD'
    return macd

def get_chart_data_for_signal(stock_history):
    signal = {}
    signal['x'] = stock_history.index.to_list()
    signal['y'] = stock_history['Signal']
    signal['type'] = 'scatter'
    signal['name'] = 'Signal'
    return signal

def get_bid_marker():
    bid_marker = {}    
    bid_marker['color'] = 'green'
    bid_marker['symbol'] = 'triangle-up'
    bid_marker['size'] = 10
    return bid_marker

def get_chart_data_for_bid(stock_history):
    bid = {}
    bid['x'] = stock_history.index.to_list()
    bid['y'] = stock_history['BID']
    bid['type'] = 'scatter'
    bid['name'] = 'BID'
    bid['mode'] = 'markers'
    bid['marker'] = get_bid_marker()
    return bid

def get_ask_marker():
    ask_marker = {}
    ask_marker['color'] = 'orange'
    ask_marker['symbol'] = 'triangle-down'
    ask_marker['size'] = 10
    return ask_marker

def get_chart_data_for_ask(stock_history):
    ask = {}
    ask['x'] = stock_history.index.to_list()
    ask['y'] = stock_history['ASK']
    ask['type'] = 'scatter'
    ask['name'] = 'ASK'
    ask['mode'] = 'markers'
    ask['marker'] = get_ask_marker()
    return ask

def get_chart_data_for_layout(stock_company, method):
    layout = {}
    layout['title'] = '{} closing price history w/ BID & ASK signals {}-based'.format(stock_company, method)
    layout['font'] = {}
    layout['font']['family'] = 'Ubuntu'
    layout['font']['size'] = 18    
    return layout

def create_data(stock,period,method):
    import plotly
    import json  
    stock_info = get_stock_info(stock, period, method)
    chart_data = {}    
    chart_data['company'] = stock_info['company']
    chart_data['stock'] = stock
    chart_data['period'] = period
    chart_data['method'] = method
    chart_data['recommendations'] = stock_info['recommendations']
    chart_data['history'] = get_chart_data_for_history(stock_info['history'])    
    if 'sma' in method:
        chart_data['sma30'] = get_chart_data_for_sma30(stock_info['history'])
        chart_data['sma100'] = get_chart_data_for_sma100(stock_info['history'])
    if 'macd'in method:
        chart_data['macd'] = get_chart_data_for_macd(stock_info['history'])
        chart_data['signal'] = get_chart_data_for_signal(stock_info['history'])
    chart_data['bid'] = get_chart_data_for_bid(stock_info['history'])
    chart_data['ask'] = get_chart_data_for_ask(stock_info['history'])
    chart_data['layout'] = get_chart_data_for_layout(stock_info['company'], chart_data['method'])
    return json.dumps(chart_data, cls=plotly.utils.PlotlyJSONEncoder)


