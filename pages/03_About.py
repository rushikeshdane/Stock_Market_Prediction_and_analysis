import streamlit as st
from PIL import Image

image = Image.open('logo.jpg')
st.sidebar.image(image,width=300)

image = Image.open('clg_logo.jpg')

st.image(image)
st.write('<h2><b><u>Department of Computer Engineering</h2>',unsafe_allow_html=True)
st.columns(3)[1].header('  Project')

st.info("The nonlinear nature of the Stock Market has made its research one of the most trending and crucial topics all around the world. People decide to invest in the stock market on the basis of some priorresearch knowledge or some prediction. In terms of prediction people often look for tools or methods thatwould minimize their risks and maximize their profits and hence stock price prediction takes on aninfluential role in the ever challenging stock market business. Adopting traditional methodologies such asfundamental and technical analysis doesn’t seem to ensure the consistency and accuracy in theprediction. As a result, machine learning technologies have become the recent trend in the stock marketprediction, whose prediction is based on the existing stock market values eventually as an outcome oftraining on their previous values.")

st.columns(3)[1].header('- Made By -')

st.markdown('''
- **Abhishek Prakash Zodage -https://www.linkedin.com/in/abhishek-zodage-886199218/**



''')

st.markdown(''' - **Abhishek Bhagwat Mali - https://www.linkedin.com/in/abhishek-mali-4b959b230/**
''')
st.markdown('''- **Pratik Santosh More - https://www.linkedin.com/in/pratik-more-754l/**
''')
st.markdown('''- **Danish Haneef Sayyed - https://www.linkedin.com/in/danish-sayyed-a1a407210/**

''')

#st.columns(3)[1].subheader('- Project Coordinator -')
st.write('________________________________________________________________________________________________')

st.markdown('''
- **Project Guide** - Prof. Pankaj Devre

'''
)
st.markdown('''- **Project Supervisor** - Prof. Priti Metange''')