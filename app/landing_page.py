import streamlit as st
import pandas as pd
 
with st.form("my_form"):
   st.write("Inside the form")
   name_input = st.text_input("Enter name")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val, "name", name_input)

st.write("Outside the form")