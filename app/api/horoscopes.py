import streamlit as st
import pandas as pd
import requests

sign= 'aries'
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

print(response.json())