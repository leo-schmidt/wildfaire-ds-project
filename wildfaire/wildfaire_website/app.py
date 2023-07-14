import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import os
import glob
import requests

from streamlit_folium import folium_static

from components.geocoding import nifc_active_fires
from components.geocoding import geocode_address
from components.geocoding import search_area_buffer
from components.geocoding import process_wildfires
from components.geocoding import map_create
from components.geocoding import map_create_forecast
#from components.geocoding import pseudo_data

from components.forecasting import raster_creation
from components.forecasting import forecast_raster_creation

from utils import get_project_root

from wildfaire.earthengine.earthengine import get_ee_data
from wildfaire.params import API_URL

project_root = get_project_root()

## RA - start map at US scale, plot all fires
## RA - select fire (address or coordinate)

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
                "on wildfires near your location"
    )

    with st.form(key='address'):
            ##address details to be submitted to geocoding API
            street = st.text_input('Street')
            town = st.text_input('Town')
            state = st.text_input('State/County')
            zip = st.text_input('ZIP/Postcode')
            country = st.selectbox('Country', ['United States', 'France', 'United Kingdom'])
            search_area = st.number_input('Search area (km)', min_value=10, max_value=500)
            address_to_geocode = f"{street},{town},{state},{zip},{country}"
            submit_button = st.form_submit_button(label="Submit")



#RA have a 'predict button'

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

            ##pseudo model - manipulation of data
            #    forecast_fires = pseudo_data(selected_wildfires)

            ##pseudo raster
                #extract data from nifc geopanda
                #rasterIDs = raster_creation(selected_wildfires)
                rasters = raster_creation(selected_wildfires)
                rasterIDs = [raster['polygon_id'] for raster in rasters]

                st.write(f'Fires found: ', len(rasters))
            ###################################################################################
            ## send selected geopanda to wildfAIre API here

                ee_data = []
                for fire in rasters:

                    coordinates = fire['bound']
                    # get data from Google Earth Engine
                    # RA - date to be dynamic?? Today - a number??
                    data = get_ee_data('2023-07-01', coordinates)

                    # synthetic NDVI data
                    # train data mean
                    data['NDVI'] = np.ones((64,64), dtype=np.uint8) * 5157.625
                    # train data range
                    #data['NDVI'] = np.random.uniform(-10000, 10000, (64,64))

                    # feature selection
                    # somehow lost NDVI on the way so omitting that for now
                    features = ['elevation', 'th', 'vs',  'tmmn', 'tmmx', 'sph', 'pr', 'pdsi', 'NDVI', 'population', 'erc']

                    # extract features and stack arrays
                    feature_array = np.stack([data[feature] for feature in features], axis=2)
                    # stack FireMask from NIFC data on top
                    feature_array = np.concatenate([feature_array, fire['values'].reshape((64,64,1))], axis=2)
                    # store in a list with one item for each fire
                    ee_data.append(feature_array)

                #2. call wildfaire api
                    # reshape to 32x32 for the model
                    #feature_array = feature_array[::2,::2,:].reshape(1,32,32,12)
                    feature_array = feature_array.reshape(1,64,64,12)

                ## RA - make coordinate dynamic
                    input_dict = {
                    'lon' : -119.117,
                    'lat' : 46.201,
                    'input_features' : feature_array.tolist()
                    }


                    response = requests.post(f"{API_URL}/predict", json=input_dict)
                    print(response)
                    prediction = response.json()
                    prediction = prediction['fire_spread'][0]
                    #prediction = feature_array[:,:,:,-1].reshape(64,64)
                    #prediction for a single fire - need to create a raster
                    prediction_array = np.array(prediction, dtype=float).reshape(64,64)

                    forecast_rasters = forecast_raster_creation(fire,
                                                                prediction_array)

                    #st.write(prediction_array.shape)
                    #fig, ax = plt.subplots(2,1)
                    #ax[0].imshow(feature_array[:,:,:,-1].reshape(32,32), cmap='gray')
                    #ax[1].imshow(prediction_array, cmap='gray')
                    #st.pyplot(fig)


                    #st.write('Features retrieved from EE: ', data.keys())
                    #st.write('Somehow lost NDVI on the way so omitting that for now.')
                    #st.write('Feature array shape: ', ee_data[0].shape)

            ####################################################################################
            ## plot data and results
                col1, col2 = st.columns(2)

                map_plot = map_create(geocode_result[0],
                                      geocode_result[1],
                                      search_poly,
                                      selected_wildfires,
                                      other_wildfires,
                                      rasterIDs)

                col1.header("fire today :round_pushpin:")
                with col1:
                    folium_static(map_plot)

                map_plot2 = map_create_forecast(geocode_result[0],
                                      geocode_result[1],
                                      search_poly,
                                      rasterIDs)

                col2.header("fire tomorrow 	:round_pushpin:")
                with col2:
                    folium_static(map_plot2)

            else:
                st.write('no active wildfires in search area :thumbsup:')
