import json
import requests
import streamlit as st

st.title('Estimate the :blue[_Price_] of your :car: now')

with open('cars_data.json') as user_file:
  file_contents = user_file.read()

# loading cars data for user input dropdowns
cars_data = json.loads(file_contents)

# milage
milage = st.sidebar.number_input('Insert a number')

# make - brand name
make = st.sidebar.selectbox(
    'What is the brand of your car',
    list(cars_data["make"]))

# model 
model = st.sidebar.selectbox(
    'What is the model of your car',
    list(cars_data["model"]))

# fuel 
fuel = st.sidebar.selectbox(
    'What is the used fuel type?',
    list(cars_data["fuel"]))

# gear
gear = st.sidebar.radio(
    "Choose the car gear:",
    list(cars_data["gear"]))

# offer
offer = st.sidebar.radio(
    "Choose the offer:",
    list(cars_data["offerType"]))

# hp
hp = st.sidebar.slider(
    'Select the horsepower',
    0, 1000, (30))

# year
year = st.sidebar.slider(
    'Select car year',
    1950, 2023, (2019))

# main page view upon pressing predict
if st.sidebar.button('Predict'):
    st.write(f'The current milage is :green[{milage}]') # api validation to int
    st.write(f'Car maker is :green[{make}]')
    st.write(f'Car model is :green[{model}]')
    st.write(f'Car model is :green[{fuel}]')
    st.write(f'Gear :green[{gear}]')
    st.write(f'OfferTpe :green[{offer}]')
    st.write(f'HorsePower: :green[{hp}]')
    st.write(f'Year: :green[{year}]')

    payload = json.dumps({
    "milage": milage,
    "make": make,
    "model": model,
    "fuel": fuel,
    "gear": gear,
    "offerType": offer,
    "hp": hp,
    "year": year
    })
    reqUrl = "http://178.128.80.51/predict_price"
    response = requests.request("GET", reqUrl, data=payload)
    if response.status_code == 200:
        prediction = json.loads(response.text)
        price = round(prediction["price"], 2)
        st.success(f" This car is worth {price}€")
    else:
        st.error(f"Something went wrong:\n {response}")