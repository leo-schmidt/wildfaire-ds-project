import streamlit as st
import requests
from components.geocoding import geocode_address
from components.geocoding import nasa_fire_events

st.set_page_config(page_title="WildfAIre version1", page_icon=":fire:", layout="wide")

#from components.sidebar import sidebar
#from components.geocoding import geocode_address

st.header=("WildfAire - wildfire tracking application")
st.title(":fire: WildfAire: wildfire tracking :fire:")

#call sidebar function from sidebar.py to create data entry sidebar
with st.sidebar:
    ## basic markdown instructions
    st.markdown(
            "How to use WildfAIire: \n"
            "1. Enter your address\n"
            "2. WildfAIre will return information \n"
                "on wildfires near your loction"
    )

    with st.form(key='address'):
            ##address details to be submitted to geocoding API
            street = st.text_input('Street', key='my_street')
            town = st.text_input('Town', key='my_town')
            state = st.text_input('State/County', key='my_county')
            zip = st.text_input('ZIP/Postcode', key='my_postcode')
            country = st.selectbox('Country', ['France', 'United Kingdom', 'United States'], key='my_country')
            address_to_geocode = f"{street},{town},{state},{zip},{country}"
            submit_button = st.form_submit_button(label="Submit")

#if submit button is pressed then send address to the geocoder to get lat/lon
if submit_button:
    geocode_result = geocode_address(address_to_geocode)
#if the no geocoding result then write the error message to screen
#else send the lat/long to the NASA events API to retrieve fire events near location
    if(len(geocode_result) == 1):
         st.write(geocode_result[0])
    else:
         st.markdown('under development...creating the search area')
        # fire_events = nasa_fire_events(geocode_result[0], geocode_result[1])









#geocode_address(address_to_geocode)

#1. map and geocoder

    # can enter location
    # map centred on location provided

#user_address = sidebar.address
#st.write(st.session_state['value'])

#street = st.text_input('Street')
#town = st.text_input('Town')
#state = st.text_input('State/County')
#zip = st.text_input('ZIP/Postcode')
#country = st.selectbox('Country', ['France', 'United Kingdom', 'United States'])

#address = f"{street},{town},{state},{country}"



#st.markdown(''':large_red_square:''')




#2. search NASA realtime events based on location
    #sent location to NASA API to retrieve events

    #need to convert location to Km to set search area??

## NASA events API for wildfires in given date range, location and categorised as open
##https://eonet.gsfc.nasa.gov/api/v3/events?category=wildfires&start=2022-01-01&end=2023-06-19&status=open&bbox=-111.00,50.73,-58.71,12.89


#3. dummy data 'forecast output'

#4. Output data - distance, location, distance, travelled, icons
            # need to embed a table wtructure here
