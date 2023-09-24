import streamlit as st
from datetime import datetime
import requests
from streamlit_card import card
from PIL import Image

from geopy import Nominatim
from timezonefinder import TimezoneFinder
from tzwhere import tzwhere
from pytz import timezone, utc

import numpy as np
import functools
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos
from skyfield.projections import build_stereographic_projection

st.set_page_config(
    page_icon ="👽",
    layout = "wide",
    page_title="SkyChart",
)

if 'loggedin' not in st.session_state:
    st.session_state['loggedin'] = False
if 'name_input' not in st.session_state:
    st.session_state['name_input'] = ""
if 'date_input' not in st.session_state:
    st.session_state['date_input'] = ""
if 'loc_input' not in st.session_state:
    st.session_state['loc_input'] = ""

def determine_sign(date):
   # checks month and date within the valid range
   # of a specified zodiac
   day = date.day
   month = date.month
   astro_sign = ""

   if month == 12:
      astro_sign = 'Sagittarius' if (day < 22) else 'capricorn'
   elif month == 1:
      astro_sign = 'Capricorn' if (day < 20) else 'aquarius'
   elif month == 2:
      astro_sign = 'Aquarius' if (day < 19) else 'pisces'
   elif month == 3:
      astro_sign = 'Pisces' if (day < 21) else 'aries'
   elif month == 4:
      astro_sign = 'Aries' if (day < 20) else 'taurus'
   elif month == 5:
      astro_sign = 'Taurus' if (day < 21) else 'gemini'
   elif month == 6:
      astro_sign = 'Gemini' if (day < 21) else 'cancer'
   elif month == 7:
      astro_sign = 'Cancer' if (day < 23) else 'leo'
   elif month == 8:
      astro_sign = 'Leo' if (day < 23) else 'virgo'
   elif month == 9:
      astro_sign = 'Virgo' if (day < 23) else 'libra'
   elif month == 10:
      astro_sign = 'Libra' if (day < 23) else 'scorpio'
   elif month == 11:
      astro_sign = 'scorpio' if (day < 22) else 'sagittarius'
   return astro_sign

def horoscope_endpoint(sign):
    timePeriod= 'today'

    #api-endpoint
    url = "https://daily-horoscope-api.p.rapidapi.com/api/Daily-Horoscope-English/"

    #params
    querystring = {"zodiacSign":"aries","timePeriod":"weekly"}

    headers = {
	    "X-RapidAPI-Key": "3fe8a5d459msh0c45c5c28b47e78p1dd4f0jsnc127cb1787cb",
	    "X-RapidAPI-Host": "daily-horoscope-api.p.rapidapi.com"
    }

    #sending get request and saving the response as response object
    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
 
def map_gen(day, zip_code):
    # load celestial data
    tf = TimezoneFinder()
    # de421 shows position of earth and sun in space
    eph = load('de421.bsp')

    # hipparcos dataset contains star location data
    with load.open(hipparcos.URL) as f:
        stars = hipparcos.load_dataframe(f)

    location = zip_code
    when = str(day) + ' 00:00'

    # get latitude and longitude of our location 
    locator = Nominatim(user_agent='akshitha')
    location = locator.geocode(location)
    lat, long = location.latitude, location.longitude

    # convert date string into datetime object
    dt = datetime.strptime(when, '%Y-%m-%d %H:%M')

    # define datetime and convert to utc based on our timezone
    timezone_str = tf.timezone_at(lng=long, lat=lat)
    local = timezone(timezone_str)

    # get UTC from local timezone and datetime
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(utc)


    # find location of earth and sun and set the observer position
    sun = eph['sun']
    earth = eph['earth']

    # define observation time from our UTC datetime
    ts = load.timescale()
    t = ts.from_datetime(utc_dt)

    # define an observer using the world geodetic system data
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)

    # define the position in the sky where we will be looking
    position = observer.from_altaz(alt_degrees=90, az_degrees=0)

    # center the observation point in the middle of the sky
    ra, dec, distance = observer.radec()
    center_object = Star(ra=ra, dec=dec)

    # find where our center object is relative to earth and build a projection with 180 degree view
    center = earth.at(t).observe(center_object)
    projection = build_stereographic_projection(center)
    field_of_view_degrees = 180.0

    # calculate star positions and project them onto a plain space
    star_positions = earth.at(t).observe(Star.from_dataframe(stars))
    stars['x'], stars['y'] = projection(star_positions)

    chart_size = 10
    max_star_size = 100
    limiting_magnitude = 10

    bright_stars = (stars.magnitude <= limiting_magnitude)
    magnitude = stars['magnitude'][bright_stars]

    fig, ax = plt.subplots(figsize=(chart_size, chart_size))
    
    border = plt.Circle((0, 0), 1, color='navy', fill=True)
    ax.add_patch(border)

    marker_size = max_star_size * 10 ** (magnitude / -2.5)

    ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
           s=marker_size, color='white', marker='.', linewidths=0, 
           zorder=2)

    horizon = Circle((0, 0), radius=1, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)


    # other settings
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    plt.axis('off')

    #plt.show()
    plt.savefig("map.jpg")

if st.session_state['loggedin']==False:
    st.title("Welcome to SkyChart 🌓")
    st.subheader("A place for those curious about their pattern with the stars.")
    with st.form("my_form"):
        st.subheader("Create Your Personal Card")
        st.session_state['name_input'] = st.text_input("Name")
        st.session_state['date_input'] = st.date_input("Date of Birth", min_value=datetime(1950, 1, 1), value=None)
        st.session_state['loc_input'] = st.text_input("Zipcode of Your Birthcity")

        # Every form must have a submit button.
        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: rgb(0, 0, 102);
            color: rgb(255, 255, 255);
        }
        </style>""", unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit")
   
    if submitted:
        st.session_state['loggedin']=True
        st.rerun()
    
elif st.session_state['loggedin']==True:
    st.title("Hello, " + str(st.session_state['name_input']) + ".")
    sign = determine_sign(st.session_state['date_input'])
    st.write ("Created on " + st.session_state['date_input'].strftime("%B %d, %Y"))
    st.write(sign.upper() + "🌙")

    st.subheader("Today's Vision 👁️")
    horoscope = horoscope_endpoint(sign=sign)
    st.write("A DAY OF REFLECTION AWAITS YOU ")
    st.write(horoscope['prediction'])

    map_gen(day=st.session_state['date_input'], zip_code=st.session_state['loc_input'])
    image = Image.open('map.jpg')
    st.image(image, caption='The Sky on The Day You Were Born')
        
