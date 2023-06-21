
import pandas as pd

import requests

import folium
import streamlit as st

from streamlit_folium import st_folium, folium_static

from components.geocoding import nifc_active_fires
from components.geocoding import geocode_address
from components.geocoding import search_area_buffer
from components.geocoding import nasa_fire_events
from components.geocoding import map_create


st.set_page_config(page_title="WildfAIre version1", page_icon=":fire:", layout="wide")

#load active fires from NIFC service
active_fires = nifc_active_fires()

st.header=("WildfAire - wildfire tracking application")
st.title(":fire: WildfAire: wildfire tracking :fire:")

#create data entry form in sidebar
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
            street = st.text_input('Street')
            town = st.text_input('Town')
            state = st.text_input('State/County')
            zip = st.text_input('ZIP/Postcode')
            country = st.selectbox('Country', ['France', 'United Kingdom', 'United States'])
            search_area = st.number_input('Search area (km)', min_value=10, max_value=100)
            address_to_geocode = f"{street},{town},{state},{zip},{country}"
            submit_button = st.form_submit_button(label="Submit")

#if submit button is pressed then send address to the geocoder to get lat/lon
if submit_button:
    geocode_result = geocode_address(address_to_geocode)

#if no geocoding result write the error message to screen
#else send the lat/long to the NASA events API to retrieve fire events near location
    if(len(geocode_result) == 1):
         st.write(geocode_result[0])
    else:
         st.markdown('under development...creating the search area')
         #st.write(search_area_buffer(geocode_result[0], geocode_result[1]))
         ## create search buffer (50 km square around the address location)
         search_poly = search_area_buffer(geocode_result[0], geocode_result[1])
         ## call NASA event API for fire events in search area using the search square
         st.write(search_poly['bbox'])
         ###====== superseded ================================
         #fire_events = nasa_fire_events(search_poly['bbox'])
         #st.write(fire_events)
         ###==================================================

        # m = folium.Map(location=[geocode_result[0], geocode_result[1]], zoom_start=8)
         #fire_features = pd.json_normalize(active_fires['features'])

         #geo_json = folium.GeoJson(data=active_fires)
         #geo_json.add_to(m)
         #folium.features.GeoJson(active_fires, popup=folium.features.GeoJsonPopup(fields=['attr_IncidentShortDescription', 'poly_GISAcres'])).add_to(m)

         #m

         map_plot = map_create(geocode_result[0],
                                     geocode_result[1],
                                      search_poly['bbox'],
                                      active_fires)


         folium_static(map_plot)






#geocode_address(address_to_geocode)

#1. map and geocoder

    # can enter location
    # map centred on location provided




#st.markdown(''':large_red_square:''')




#2. search NASA realtime events based on location
    #sent location to NASA API to retrieve events

    #need to convert location to Km to set search area??

## NASA events API for wildfires in given date range, location and categorised as open


#3. dummy data 'forecast output'

#4. Output data - distance, location, distance, travelled, icons
            # need to embed a table wtructure here
