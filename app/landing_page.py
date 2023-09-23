import streamlit as st
import datetime
import pandas as pd
 
with st.form("my_form"):
   name_input = st.text_input("Enter name")
   date_input = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
   loc_input = st.text_input("Location by Zip")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("name", name_input, "date", date_input, "loc", loc_input)