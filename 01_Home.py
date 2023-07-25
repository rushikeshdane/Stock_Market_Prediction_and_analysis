# from app import  get_data, load_data , sma_screener
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

nse51 = pd.read_csv('https://archives.nseindia.com/content/indices/ind_nifty50list.csv')
symbols = nse51['Symbol'].to_list()
sym = nse51['Symbol'].to_frame()

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
