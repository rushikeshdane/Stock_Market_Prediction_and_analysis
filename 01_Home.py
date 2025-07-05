from prediction_helper import get_stock_data, info, trend, prophet_preprocessing, forcast, candle, predictions, \
    next_10_forcast
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
# from nsetools import Nse
import plotly.express as px
import pandas as pd
import json
from datetime import date, timedelta
from nsepy import get_history
from prediction_helper import get_sector, get_stock_data, get_screen_data
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

nse51 = pd.read_csv('ind_nifty50list.csv')
symbols = nse51['Symbol'].to_list()
sym = nse51['Symbol'].to_frame()
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


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


st.title('Stock Price Screener Application')
lottie_coding = load_lottiefile("AA.json")  # m4.json is name of our downloaded json file

st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="high", height=420
)

list_of_sector = nse51['Industry'].unique()
input_sector = st.sidebar.selectbox('Select Sector', options=list_of_sector)

if input_sector:
    st.subheader('       ' + input_sector + ' Stocks')
    st.table(get_sector(input_sector))

nifty50_symbols = ["ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO",
                   "BAJFINANCE", "BAJAJFINSV", "BHARTIARTL", "BPCL", "BRITANNIA",
                   "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GAIL",
                   "GRASIM", "HCLTECH", "HDFC", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO",
                   "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK", "INFY",
                   "IOC", "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI",
                   "NESTLEIND", "NTPC", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE",
                   "SBIN", "SHREECEM", "SUNPHARMA", "TATAMOTORS", "TATASTEEL",
                   "TATACONSUM", "TITAN", "TCS", "ULTRACEMCO", "UPL", "WIPRO"]

# Creating Dataframe for Screener
nifty50_data = {}
for symbol in nifty50_symbols:
    nifty50_data[symbol] = get_screen_data(symbol + ".NS")

# Combine the stock data into a single DataFrame
nifty50_df = pd.concat(nifty50_data.values(),
                       keys=nifty50_data.keys(),
                       names=["Symbol", "Date"])

# Reset the index of the DataFrame
nifty50_df.reset_index(inplace=True)

# Merge the DataFrame with the sector data
# sector_data = pd.read_csv("nifty50_sectors.csv")
# nifty50_df = pd.merge(nifty50_df, sector_data, on="Symbol")

nifty50_df['%change'] = ((nifty50_df['Close'] - nifty50_df['Open']) / nifty50_df['Open']) * 100


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# Filters

filters = st.sidebar.radio('Select Category ', ('Top Gainers', 'Top Losers', 'Most Active'))

if filters == 'Top Gainers':
    gainers = nifty50_df.sort_values(by=['%change'], ascending=False)[:10]
    st.columns(3)[1].subheader('Top Gainers in NSE')
    # st.write(top_gainers)
    st.write(gainers)
    #     gain = pd.DataFrame(nse.get_top_gainers())

    fig = px.bar(gainers, x='Symbol', y='%change', color_discrete_sequence=['green'], template='simple_white')
    fig.update_layout(xaxis_title="Symbol ", yaxis_title="Percent Change")
    st.plotly_chart(fig, use_container_width=True)
    st.write('   ')
    # st.dataframe(gainers)
    top_gainer = convert_df(gainers.head(10))
    st.download_button(
        label="Download data as CSV",
        data=top_gainer,
        file_name='top_gainer.csv',
        mime='text/csv',
    )

if filters == 'Top Losers':
    loosers = nifty50_df.sort_values(by=['%change'], ascending=True)[:10].reset_index()
    st.columns(3)[1].subheader('Top Loosers in NSE')
    st.dataframe(loosers)
    fig1 = px.histogram(loosers, x='Symbol', y='%change', color_discrete_sequence=['red'], template='simple_white')
    fig1.update_layout(xaxis_title="Symbols", yaxis_title="Percent Change")
    # fig1.update_layout(title_text='Top Loosers',title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)
    st.write('   ')
    top_looser = convert_df(loosers)
    st.download_button(
        label="Download data as CSV",
        data=top_looser,
        file_name='top_loosers.csv',
        mime='text/csv',
    )

if filters == 'Most Active':
    active = nifty50_df.sort_values(by=['Volume'], ascending=False)[:10].reset_index()
    st.columns(3)[1].subheader('Most Active Stocks')
    st.dataframe(active)
    fig1 = px.histogram(active, x='Symbol', y='Volume', color_discrete_sequence=['Orange'], template='simple_white')
    fig1.update_layout(xaxis_title="Symbols", yaxis_title="Volume")
    # fig1.update_layout(title_text='Most Active Stocks',title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)
    st.write('   ')
    mst_act = convert_df(active)
    st.download_button(
        label="Download data as CSV",
        data=mst_act,
        file_name='Most_active.csv',
        mime='text/csv',
    )
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
