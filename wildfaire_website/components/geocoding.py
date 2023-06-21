import requests
import geopandas as gpd
import pandas as pd
import shapely
import nifc_wildfires
import folium
import json
from math import sqrt
from shapely import wkt
from shapely.geometry import polygon, mapping


def geocode_address(input_address):
    url = "https://nominatim.openstreetmap.org"

    params = {
        'q': input_address,
        'format': 'json'
    }

    response = requests.get(url, params=params).json()
    repsonse_length = len(response)

    if(repsonse_length == 0):
        return ['Could not geocode the address, please try again']
    else:
        return [response[0]['lat'], response[0]['lon']]



def search_area_buffer(latitude, longitude, distance=25000/sqrt(2)):
    #to do
    '''
    1. create a search area around house equivalent to 50 km x 50 km
    '''
    gs = gpd.GeoSeries(wkt.loads(f'POINT ({longitude} {latitude})'))
    gdf = gpd.GeoDataFrame(geometry=gs)
    gdf.crs='EPSG:4326'
    gdf = gdf.to_crs('EPSG:3857')
    res = gdf.buffer(
        distance=distance,
        cap_style=3,
    )

    search_poly = mapping(res.to_crs('EPSG:4326'))
    return search_poly

'''
calls the NASA eonet service for wildfire events.
Good for testing but near real time and not as detailed as teh NASA FIRM data
(see function below) which is live.
'''
def nasa_fire_events(search_poly):

    lon_min = search_poly[0]
    lat_min = search_poly[1]
    lon_max = search_poly[2]
    lat_max = search_poly[3]

    nasa_url = "https://eonet.gsfc.nasa.gov/api/v3/events?category=wildfires"
    search_start_date = "&start=2022-01-01"
    search_end_date = "end=2023-06-19"
    search_status = 'open'
    search_coordinates = f"&bbox={lon_min},{lat_max},{lon_max},{lat_min}"

    nasa_url = f"{nasa_url}{search_start_date}{search_end_date}{search_status}{search_coordinates}"
    params = {'format': 'json'}

    response = requests.get(nasa_url, params=params).json()

    if (len(response['events']) == 0):
        return ['No active wildfires in your search area']
    else:
        return response


def nifc_active_fires():
    return nifc_wildfires.get_active_perimeters()


def map_create(latitude, longitude, search_poly, active_fires):

    m = folium.Map(location=[latitude, longitude], zoom_start=8)
    fire_features = pd.json_normalize(active_fires['features'])

    geo_json = folium.GeoJson(data=active_fires)
    geo_json.add_to(m)
    folium.features.GeoJson(active_fires, popup=folium.features.GeoJsonPopup(fields=['attr_IncidentShortDescription', 'poly_GISAcres'])).add_to(m)

    return m

def nasa_firm_events(search_poly):
    '''
    21/06: Will work on this once technical issues at FIRM are resolved (can't genreate a map_key)
    service desk submitted and waiting on response.
    '''
    1+1
