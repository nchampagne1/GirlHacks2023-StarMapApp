import streamlit as st
import datetime
import requests
from streamlit_card import card
from PIL import Image

if 'loggedin' not in st.session_state:
    st.session_state['loggedin'] = False
if 'name_input' not in st.session_state:
    st.session_state['name_input'] = ""
if 'date_input' not in st.session_state:
    st.session_state['date_input'] = ""
if 'loc_input' not in st.session_state:
    st.session_state['loc_input'] = ""

def determine_sign(date_input):
    sign = "Leo"
    return sign

def horoscope_endpoint(sign):
    timePeriod= 'today'

    #api-endpoint
    url = "https://daily-horoscope-api.p.rapidapi.com/api/Daily-Horoscope-English/"

    #params
    querystring = {"zodiacSign":"aries","timePeriod":"weekly"}

    headers = {
	    "X-RapidAPI-Key": "9e8a986006msh75a31c2f395a481p10bc2bjsn5f445be82718",
	    "X-RapidAPI-Host": "daily-horoscope-api.p.rapidapi.com"
    }

    #sending get request and saving the response as response object
    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
 
if st.session_state['loggedin']==False:
    with st.form("my_form"):
        st.session_state['name_input'] = st.text_input("Enter name")
        st.session_state['date_input'] = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
        st.session_state['loc_input'] = st.text_input("Location by Zip")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
   
    if submitted:
        st.session_state['loggedin']=True
        st.rerun()
    
elif st.session_state['loggedin']==True:
    st.header("Hello, " + str(st.session_state['name_input']) + ".")
    sign = determine_sign(st.session_state['date_input'])
    st.write(sign.upper())

    st.subheader("Your Horoscope")
    horoscope = horoscope_endpoint(sign=sign)
    st.write("A DAY OF REFLECTION")
    st.write(horoscope)

    image = Image.open('map.jpg')
    st.image(image, caption='The Sky When You Were Born')
        
