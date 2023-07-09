
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import os
import glob

from streamlit_folium import st_folium, folium_static

from components.geocoding import nifc_active_fires
from components.geocoding import geocode_address
from components.geocoding import search_area_buffer
from components.geocoding import process_wildfires
from components.geocoding import map_create
from components.geocoding import pseudo_data

from components.forecasting import raster_creation
from utils import get_project_root

from wildfaire.earthengine.earthengine import get_ee_data

project_root = get_project_root()

#print(f'hello {project_root}')

st.set_page_config(page_title="WildfAIre version1", page_icon=":fire:", layout="wide")

#load active fires from NIFC service
active_fires = nifc_active_fires()

st.header=("WildfAIre - wildfire tracking application")
st.title(":fire: WildfAIre: wildfire tracking :fire:")

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

    removing_files = glob.glob(f'{project_root}/rasters/*.tif')
    for i in removing_files:
        os.remove(i)

    #delete any rasters from previous searched
    #os.remove(file) for file in os.listdir(f'{project_root}/rasters/') if file.endswith('.tif')

    geocode_result = geocode_address(address_to_geocode)

#if no geocoding result write the error message to screen
#else send the lat/long to the NASA events API to retrieve fire events near location
    if(len(geocode_result) == 1):
         st.write(geocode_result[0])
    else:

         with st.spinner('building map results...please wait'):
            ## create search buffer (50 km square around the address location)
            search_poly = search_area_buffer(geocode_result[0], geocode_result[1], search_area)

          #  print(get_project_root)

            ## analyse wildfire data with search area
            selected_wildfires, other_wildfires = process_wildfires(geocode_result[0],
                                                                    geocode_result[1],
                                                                    active_fires,
                                                                    search_area)
            if len(selected_wildfires.index) > 0:

            ###################################################################################
            ## send selected geopanda to wildfAIre API here

            ##pseudo model - manipulation of data
                forecast_fires = pseudo_data(selected_wildfires)

            ##pseudo raster
                #extract data from nifc geopanda
                #rasterIDs = raster_creation(selected_wildfires)
                rasters = raster_creation(selected_wildfires)
                rasterIDs = [raster['polygon_id'] for raster in rasters]

            ## merge tifs with ee data
                fire = rasters[0]
                coordinates = fire['bound']
                data = get_ee_data('2023-07-01', coordinates)
                data

            #2. call wildfaire api
                #response = requests.post("http://localhost:8000/predict", json=input_dict)
                #return response.json()

            ####################################################################################
            ## plot data and results

                map_plot = map_create(geocode_result[0],
                                      geocode_result[1],
                                      search_poly,
                                      selected_wildfires,
                                      other_wildfires,
                                      forecast_fires,
                                      rasterIDs)

                folium_static(map_plot)

            else:
                st.write('no active wildfires in search area :thumbsup:')
