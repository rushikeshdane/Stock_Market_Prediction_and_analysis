import numpy as np
#import ta as ta
#from pandas_datareader.data import DataReader
import yfinance as yf
from nsepy import get_history
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_plotly
# from nsetools import Nse
import matplotlib.pyplot as plt

# nse = Nse()
nse50 = pd.read_csv('https://archives.nseindia.com/content/indices/ind_nifty50list.csv')
symbols = nse50['Symbol'].to_list()


@st.cache_data
def get_sector(sector):
    df = pd.read_csv('ind_nifty50list.csv')
    sector_data = df[df['Symbol'].isin(nse50[nse50['Industry'] == sector]['Symbol'])]
    # sector_data.drop(['xDt', 'caAct'], axis=1, inplace=True)
    return sector_data


@st.cache_data
def get_stock_data(stockname):
    end = datetime.now()
    start = datetime(end.year - 5, end.month, end.day)

    data = yf.download(stockname, start, end)

    return data


# For Screener
@st.cache_data
def get_screen_data(stockname):
    # end = datetime.time()
    # start = datetime(end.year, end.month, end.day-1)
    #
    # data = yf.download(stockname, start, end)
    #
    # return data

    # *********************************************************************************

    data = yf.download(stockname,
                       #period='5d',
                       interval='1d')

    # Filter the data to only show data from the latest date
    latest_date = data.index.date[-1]
    df_latest = data[data.index.date == latest_date]
    return df_latest


def info(stock_data):
    last_day = stock_data.tail(1)
    open = round(last_day['Open'].values[0], 2)
    close = round(last_day['Close'].values[0], 2)
    high = round(last_day['High'].values[0], 2)
    low = round(last_day['Low'].values[0], 2)
    volume = round(last_day['Volume'].values[0], 2)

    return open, close, high, low, volume


def trend(stock_name, title):
    fig = px.line(x=stock_name.index, y=stock_name['Close'], template='plotly_dark', title='Trend for last year in ' +
                                                                                           '{0}'.format(title),
                  width=1000)
    fig.update_layout(xaxis_title="Date", yaxis_title='Price')
    return st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------

def prophet_preprocessing(data):  # ds and Y for fbprophet 
    df_train = data[['Close']]
    df_train['Date'] = data.index

    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    return df_train


@st.cache_data
def predictions(df, time=365):
    m = Prophet()  # importing model
    m.fit(df)
    future = m.make_future_dataframe(periods=time)  # forcasting parameter
    prediction = m.predict(future)

    return prediction


def forcast(df, time=365):
    m = Prophet()  # importing model
    m.fit(df)
    future = m.make_future_dataframe(periods=time)  # forcasting parameter
    prediction = m.predict(future)

    fig = plot_plotly(m, prediction)
    fig.update_layout(title='Forcast for next ' + '{0}'.format(time) + ' days')
    fig.update_layout(xaxis_title="Year", yaxis_title="Price", showlegend=True)
    # fig.show()

    return st.plotly_chart(fig, use_container_width=True)


def next_10_forcast(data):
    import datetime as dt
    todays = dt.datetime.today().strftime("%m/%d/%Y")
    df2 = data.loc[data['ds'] > todays]
    # df2[['ds','trend','yhat']].head(10)
    df2.rename(columns={'ds': 'Date', 'yhat': 'Prediction'}, inplace=True)
    df2
    df3 = df2[['Date', 'Prediction']].reset_index(drop=True)
    df3.index += 1
    return df3.head(10)


import plotly.graph_objects as go


def candle(stock1, title1):
    fig = go.Figure(data=[go.Candlestick(x=stock1.index,
                                         open=stock1['Open'],
                                         high=stock1['High'],
                                         low=stock1['Low'],
                                         close=stock1['Close'])])
    fig.update_layout(title='Trend for last 90 days in ' +
                            '{0}'.format(title1), height=700)

    return st.plotly_chart(fig, use_container_width=True)

# news_api_key = 'OkITeNpaVH9kf_2VdYYXQgXKycxAo7ko1j1yqgD5zjU'
