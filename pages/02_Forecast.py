from prediction_helper import get_stock_data, info, trend, prophet_preprocessing, forcast, candle, predictions, \
    next_10_forcast
import streamlit as st
from PIL import Image
from prophet import Prophet
from prophet.plot import plot_plotly
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

st.set_page_config(layout="wide", page_title="MET Project")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

stocks = ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV',
          'BPCL', 'BHARTIARTL',
          'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK',
          'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR',
          'HDFC', 'ICICIBANK', 'ITC',
          'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC', 'NESTLEIND', 'ONGC',
          'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN', 'SUNPHARMA', 'TCS',
          'TATACONSUM', 'TATAMOTORS', 'TATASTEEL',
          'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']

# Page setting

st.title('Stock Price Predictor')

image = Image.open('logo.jpg')
st.sidebar.image(image, width=300)

input_stock = st.sidebar.selectbox('Select your stock ', options=[x + '.NS' for x in stocks])
ticker = str(input_stock)
# stock1 = get_stock_data(input_stock)
data_load_state = st.sidebar.text('Loading Data...')
stock1 = get_stock_data(input_stock)
data_load_state.text('Data Loaded Successfully')

time = st.sidebar.number_input('Select number of days for forecasting', value=365)
time = int(time)

open = info(stock1)[0]
close = info(stock1)[1]
high = info(stock1)[2]
low = info(stock1)[3]
volume = info(stock1)[4]

b1, b2, b3, b4, b5 = st.columns(5)
b1.metric("Open", open)
b2.metric("Close", close)
b3.metric("High", high)
b4.metric("Low", low)
b5.metric('Volume', volume)

st.write(input_stock[-3])
trend(stock1, input_stock)

pricing_data, tech_indicator = st.tabs(["Pricing Data", "Technical Analysis"])

with pricing_data:
    st.subheader('Price Movements')
    data2 = stock1.tail(30).iloc[::-1]
    data2['%change'] = stock1['Adj Close'] / stock1['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return = data2['%change'].mean() * 252 * 100
    st.write('Annual Return is', str(annual_return), '%')
    stedev = np.std(data2['%change']) * np.sqrt(252)
    st.write('Standard Deviation is', str(stedev * 100), '%')

with tech_indicator:
    options = ['macd', 'rsi', 'bollinger_bands', 'momentum']
    selected_option = st.selectbox('Select an indicator:', options)
    if selected_option == 'macd':
        def macd(data):
            macd = ta.macd(data['Close'])
            return macd
        macd_indicator = macd(stock1.tail(365))
        st.line_chart(macd_indicator)

    if selected_option == 'rsi':
        def rsi(data, period=14):
            rsi = ta.rsi(data['Close'], length=period)
            return rsi
        rsi_indicator = rsi(stock1.tail(365))
        st.line_chart(rsi_indicator)

    if selected_option == 'bollinger_bands':
        def bollinger_bands(data, period=20):
            bb = ta.bbands(data['Close'], length=period)
            return bb
        bb_indicator = bollinger_bands(stock1.tail(365))
        st.line_chart(bb_indicator)

    if selected_option == 'momentum':
        def momentum(data, period=10):
            mom = data['Close'].diff(period)
            return mom
        mom_10 = momentum(stock1.tail(365), 10)
        st.line_chart(mom_10)

# For Candlestick Chart
candle(stock1.tail(90), input_stock)

# Forcasting
forcasted_data = prophet_preprocessing(stock1)
pred_val = predictions(forcasted_data, time=time)

pred = pred_val['yhat'].to_list()


# Testing the Predictions
train = forcasted_data.iloc[:-365, :]
test = forcasted_data.iloc[-365:, :]

# Create and fit the Prophet model
model = Prophet()
model.fit(train)

# Generate predictions for the testing set
forecast = model.predict(test)

# Calculate the mean absoulte error and mean absolute percentage error
mae = mean_absolute_error(test['y'], forecast['yhat'])
mape = mean_absolute_percentage_error(test['y'], forecast['yhat'])

accuracy = 100 - (mae / test['y'].mean()) * 100

data_variable = st.sidebar.checkbox('View Forecasting')

if data_variable:
    forcast(forcasted_data, time=time)
    st.write("<span style='font-size:20px'><b>Predicted value after " + str(time) + " days is " + str(pred[-1]) + "</b></span>", unsafe_allow_html=True)

    # st.write("Percentage Change - ",change[-1])
    st.write("<span style='font-size:20px'><b>Forecast for next 10 days - </b></span>",unsafe_allow_html=True)
    st.write(next_10_forcast(pred_val))

    st.write('Mean Absolute percentage Error:', str(mape))
    st.write('Accuracy:', str(accuracy), '%')


# Buy/Sell Signal -
# Calculate Simple Moving Average (SMA)
sma_20 = stock1['Close'].rolling(window=20).mean()
sma_50 = stock1['Close'].rolling(window=50).mean()

# Calculate Exponential Moving Average (EMA)
ema_12 = stock1['Close'].ewm(span=12, adjust=False).mean()
ema_26 = stock1['Close'].ewm(span=26, adjust=False).mean()

# Calculate signal
if sma_20[-1] > sma_50[-1] and ema_12[-1] > ema_26[-1]:
    signal = "Strong buy"
    color = "green"
elif sma_20[-1] > sma_50[-1] or ema_12[-1] > ema_26[-1]:
    signal = "buy"
    color = "lightgreen"
elif sma_20[-1] < sma_50[-1] and ema_12[-1] < ema_26[-1]:
    signal = "Strong sell"
    color = "red"
elif sma_20[-1] < sma_50[-1] or ema_12[-1] < ema_26[-1]:
    signal = "sell"
    color = "pink"
else:
    signal = "neutral"
    color = "gray"

# Create line chart with signal markers
fig = go.Figure()
fig.add_trace(go.Scatter(x=stock1.index, y=stock1['Close'], name="Stock Price", mode="lines"))

if signal == "Strong buy":
    fig.add_trace(
        go.Scatter(x=[stock1.index[-1]], y=[stock1['Close'][-1]], mode="markers", marker=dict(color=color, size=15),
                   name="Strong Buy Signal"))
elif signal == "Strong sell":
    fig.add_trace(
        go.Scatter(x=[stock1.index[-1]], y=[stock1['Close'][-1]], mode="markers", marker=dict(color=color, size=15),
                   name="Strong Sell Signal"))
elif signal == "sell":
    fig.add_trace(
        go.Scatter(x=[stock1.index[-1]], y=[stock1['Close'][-1]], mode="markers", marker=dict(color=color, size=15),
                   name="Sell Signal"))
elif signal == "buy":
    fig.add_trace(
        go.Scatter(x=[stock1.index[-1]], y=[stock1['Close'][-1]], mode="markers", marker=dict(color=color, size=15),
                   name="Buy Signal"))

fig.update_layout(title=f"{input_stock} Stock Price", xaxis_title="Date", yaxis_title="Price ($)")

sig = st.sidebar.checkbox("Show Buy/Sell Signal")

if sig:
    st.subheader("Signal for Buy/Sell Stock")
    st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=[signal], y=[1], marker=dict(color=color)))
    fig.update_layout(title=f"{ticker} Stock Signal", xaxis_title="", yaxis_title="", height=90,
                      margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig)

    st.subheader(f"Signal: {signal}")


# For News
news = st.button('news')

from stocknews import StockNews

if news:
    st.write(input_stock[-5])
    # st.header('News of {0}'.format(input_stock[:-5]))
    st.subheader(f'Top 5 News related to {ticker} stock ')
    sn = StockNews(input_stock[:-5], save_news=False)
    df_news = sn.read_rss()
    for i in range(5):
        st.subheader(f'News {i + 1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'news sentiment {news_sentiment}')
