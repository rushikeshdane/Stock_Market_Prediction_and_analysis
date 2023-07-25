from prediction_helper import get_stock_data, info, trend, prophet_preprocessing, forcast
import streamlit as st
from PIL import Image
from stocknews import StockNews
from prophet import Prophet
from prophet.plot import plot_plotly
from datetime import datetime

st.set_page_config(layout="wide", page_title="Stock Predictor")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

stocks = ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV',
          'BPCL', 'BHARTIARTL',
          'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK',
          'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR',
          'HDFC', 'ICICIBANK', 'ITC', 'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC',
          'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN', 'SUNPHARMA', 'TCS',
          'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']

# Page setting


st.title("Stock Price Predictor and Screener")
image = Image.open('logo.jpg')
st.sidebar.image(image, width=300)
input_stock = st.sidebar.selectbox('Select your stock ', options=[x + '.NS' for x in stocks])
# stock1 = get_stock_data(input_stock)
data_load_state = st.sidebar.text('Loading data...')
stock1 = get_stock_data(input_stock)
data_load_state.text('Data loaded successfully')

time = st.sidebar.number_input('Select number of days for forcasting', value=30)
time = int(time)

open = info(stock1)[0]
close = info(stock1)[1]
high = info(stock1)[2]
low = info(stock1)[3]
volume = info(stock1)[4]

data_var = st.checkbox("View Dataset")

b1, b2, b3, b4, b5 = st.columns(5)
b1.metric("Open", open)
b2.metric("Close", close)
b3.metric("High", high)
b4.metric("Low", low)
b5.metric('Volume', volume)
st.write(input_stock[-3])

if data_var:
    st.write(stock1.tail(7))

trend(stock1, input_stock)

forcasted_data = prophet_preprocessing(stock1)

pred = st.sidebar.checkbox("View Forecasting")

if pred:
    forcast(forcasted_data, time=time)

news = st.button('News')

if news:
    st.write(input_stock[-5])
    st.header('News of {0}'.format(input_stock[:-5]))
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
