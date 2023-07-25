import streamlit as st
from PIL import Image

image = Image.open('logo.jpg')
st.sidebar.image(image, width=300)

my_list = ["Strong Buy (Represented by dark Green color)", "Buy (Represented by light green color)", "Neutral ("
                                                                                                     "Represented by "
                                                                                                     "Grey color)",
           "Sell (Represented by light red color)", "Strong sell (Represented by dark red color)"]

st.subheader('Welcome to the Help and Documentation page for the Stock Price Predictor and Screener Web Application.')

st.markdown('<h5> ∎ What is Stock Screener ?</u></h5>', unsafe_allow_html=True)

st.info('A stock screener is a tool or software that allows investors to filter and screen stocks based on specific '
        'criteria or parameters, such as market capitalization, P/E ratio, dividend yield, and industry sector. It '
        'helps investors quickly identify potential investment opportunities and compare companies. Stock screeners '
        'can be used by both novice and professional investors to save time and effort in sorting through thousands '
        'of stocks. ')

st.markdown('<h5> ∎ What is Stock Price Prediction System ? ', unsafe_allow_html=True)

st.info(
    'A stock price prediction system is a software or tool that uses various techniques, including machine learning '
    'and deep learning, to forecast the future price of a stock. It takes historical data, market trends, '
    'and other relevant factors into consideration to predict the stocks future performance. Investors use these '
    'systems to make informed investment decisions and optimize their returns')
st.markdown("""<hr style="height:7px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
# ################################################################################################################################################
st.markdown(""" <h5>∎  Getting Started: </h5>""", unsafe_allow_html=True)
st.markdown(
    '''- **To use the app, go to the homepage which is for Stock Screener. There is a dropdown for selecting 
    sectors.By selecting a sector you can view stocks related to that selected sector.** ''')

st.markdown(
    '''- **There are 3 filters namely Top gainers, Top losers and most active stocks to filter the stocks based on 
    certain criteria** ''')

st.markdown(
    '''- **Then go to the second page which is for forecasting. Select the stock from the dropdown menu. And then 
    give the number of days in the text box for prediction and press the Enter button.** ''')

st.markdown(
    '''- **There is a check box ‘View Forecasting’. By clicking on it you can get a predicted price of stock for 
    certain number of days provided by the user.** ''')
# st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.markdown(
    '''- **There is another check box ‘Show Buy/Sell Signal’. By clicking on it you can get indication for buying or 
    selling the stock.  There are 5 signals for buying or selling stocks -**''')
for i, item in enumerate(my_list):
    st.markdown('_______________***' + f"{i + 1}. {item}" + '***')
st.markdown(''' - **There is one more button ‘News’ which shows the top 5 news related to the selected stocks.**''')
st.markdown("""<hr style="height:7px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.markdown('<h5>∎ Features :', unsafe_allow_html=True)
st.markdown(
    '''- **Stock Price Prediction: Our app uses deep learning with the Prophet library to predict stock prices for 
    the selected timeframe.**''')
st.markdown(
    '''- **Stock Screener: Our app also includes a stock screener that allows you to screen stocks based on certain 
    criteria. You can select from a range of criteria such as sector, Top gainers, Top losers and Most active 
    stocks.**''')
st.markdown('''- **Historical Data: Our app allows you to view the historical stock data for the selected stock.**''')
st.markdown(
    '''- **Chart Visualization: Our app provides a visual representation of the stock prices and the predicted prices 
    using interactive charts.**''')

# #########################################################################################################################
st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.markdown('<h5> ∎ Support:', unsafe_allow_html=True)
st.markdown('**If you have any questions or need assistance with the app, please contact our support team**')
st.markdown("- **Email - support@gmail.com**")

st.markdown('<h4>Thank you for using our Stock Price Predictor and Screener Web App…!', unsafe_allow_html=True)


# # Set the page title
# st.title("Help and Documentation")
# st.write("\n")
# # Display the overview
# st.header("Overview:")
# st.write("Our web app uses deep learning to predict stock prices and screen stocks based on certain criteria. The app "
#          "allows you to select the stock ticker and select the prediction timeframe to view the future price and you "
#          "can also filter the stocks using some screening criteria.")
#
# # Display the stock screener information
# st.subheader("What is Stock Screener -")
# st.write("A stock screener is a tool or software that allows investors to filter and screen stocks based on specific "
#          "criteria or parameters, such as market capitalization, P/E ratio, dividend yield, and industry sector. It "
#          "helps investors quickly identify potential investment opportunities and compare companies. Stock screeners "
#          "can be used by both novice and professional investors to save time and effort in sorting through thousands "
#          "of stocks.")
#
# # Display the stock price prediction system information
# st.subheader("What is stock price prediction system -")
# st.write("A stock price prediction system is a software or tool that uses various techniques, including machine "
#          "learning and deep learning, to forecast the future price of a stock. It takes historical data, "
#          "market trends, and other relevant factors into consideration to predict the stock's future performance. "
#          "Investors use these systems to make informed investment decisions and optimize their returns.")
#
# st.write("\n")
# st.write("\n")
#
# # Display the getting started information
# st.header("Getting Started:")
# st.write("1)To use the app, go to the homepage which is for Stock Screener. There is a dropdown for selecting sectors. "
#          "By selecting a sector you can view stocks related to that selected sector. ")
# st.write("2)There are 3 filters namely Top gainers, Top losers and most active stocks to filter the stocks based on "
#          "certain criteria.")
# st.write("3)Then go to the second page which is for forecasting. Select the stock from the dropdown menu. And then "
#          "give the number of days in the text box for prediction and press the Enter button. ")
# st.write( "4)There is a check box ‘View Forecasting’. By clicking on it you can get a predicted price of stock for a "
#          "certain number of days provided by the user.")
# st.write("5)There is another check box ‘Show Buy/Sell Signal’. By clicking on it you can get an indication for buying "
#          "or selling the stock.")
#
# st.write("a)Strong Buy (Represented by dark Green color)")
# st.write("b)Buy (Represented by light green color)")
# st.write("c)Neutral (Represented by Grey color)")
# st.write("d)Sell (Represented by light red color)")
# st.write("e)Strong sell (Represented by dark red color)")
#
# st.write("There is one more button ‘News’ which shows the top 5 news related to the selected stocks.")
#
# st.write("\n")
# st.write("\n")
# # Display the features information
# st.header("Features:")
# st.write("1. Stock Price Prediction: Our app uses deep learning with the Prophet library to predict stock prices for "
#          "the selected timeframe.")
# st.write("2. Stock Screener: Our app also includes a stock screener that allows you to screen stocks based on certain "
#          "criteria. You can select from a range of criteria such as sector, Top gainers, Top losers and Most active "
#          "stocks.")
# st.write("3. Historical Data: Our app allows you to view the historical stock data for the selected stock.")
# st.write("4. Chart Visualization: Our app provides a visual representation of the stock prices and the predicted "
#          "prices using interactive charts.")
#
# st.write("\n")
# st.write("\n")
# # Display the support information
# st.header("Support:")
# st.write("If you have any questions or need assistance with the app, please contact our support team.")
# st.write("Email ID - support@gmail.com")
#
# st.write("\n")
# st.write("\n")
# st.write("\n")
# # Display the thank you message
# st.subheader("Thank you for using our Stock Price Predictor and Screener Web App…!")
