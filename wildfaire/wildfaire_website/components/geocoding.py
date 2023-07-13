import geopandas as gpd
import pandas as pd
import numpy as np

import requests
import nifc_wildfires
import folium
import pyproj
import rasterio

from datetime import datetime
from folium.raster_layers import ImageOverlay
from math import sqrt
from shapely import wkt
from shapely.ops import transform
from shapely.geometry import Point, polygon, mapping, shape

from utils import get_project_root

project_root = get_project_root()
#print(f'hello {project_root}')

def nifc_active_fires():
    '''
    load data from the NIFC website using the nifc_wildfires package
    convert raw data to geopanda data frame
    '''
    data = nifc_wildfires.get_active_perimeters()
    gdf_af = gpd.GeoDataFrame.from_features(data)
    gdf_af.set_crs('epsg:4326')
    gdf_af['distance'] = np.nan

    return gdf_af

def geocode_address(input_address):
    '''
    Nominatim geocoder to convert the given address to lat/lon. Will return an
    error if no result generated
    '''
    url = "https://nominatim.openstreetmap.org"

    params = {
        'q': input_address,
        'format': 'json'
    }

    response = requests.get(url, params=params).json()
    repsonse_length = len(response)
    print(response)
    if(repsonse_length == 0):
        return [':warning: Could not geocode the address - check address and try again :warning:']
    else:
        return [response[0]['lat'], response[0]['lon']]


def search_area_buffer(latitude, longitude, search_area):
    '''
    Create a search area polygon required for selecting features for model and
    plotting on output map.
    reprojecting the lat/lon required to calculate search buffer in KM. May need
    to be changed if different geographies used.
    *2 in calculation - search area assumed to be a radius value not diameter
    '''
    gs = gpd.GeoSeries(wkt.loads(f'POINT ({longitude} {latitude})'))
    gdf_sa = gpd.GeoDataFrame(geometry=gs)
    gdf_sa.crs='EPSG:4326'
    gdf_sa = gdf_sa.to_crs('EPSG:3857')
    res = gdf_sa.buffer(
        distance=(search_area*2*1000)/sqrt(2)
    )

    search_poly = mapping(res.to_crs('EPSG:4326'))
    return search_poly

def process_wildfires(latitude, longitude, active_fires, search_area):
    '''
    perform euclidean distance analysis to select fire features for forecasting
    '''

    TransformPoint = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32148")
    search_centroid = TransformPoint.transform(latitude, longitude)
    search_centroid = Point(search_centroid)

    project = pyproj.Transformer.from_proj(
        pyproj.Proj(init='epsg:4326'), # source coordinate system
        pyproj.Proj(init='epsg:32148')) # destination coordinate system

    for index, row in active_fires.iterrows():
        #create polygon object per row to calculate distance
        #geo: dict = {'type': row['geometry.type'], 'coordinates': row['geometry.coordinates']}
        #polygon: Polygon = shape(geo)

        polygon_feat_proj = transform(project.transform, row['geometry'])
        active_fires.at[index,'distance'] = (round(search_centroid.distance(polygon_feat_proj.boundary)/1000))

    selected_wildfires = active_fires.loc[active_fires['distance'] < search_area]
    other_wildfires = active_fires.loc[active_fires['distance'] >= search_area]

    return selected_wildfires, other_wildfires


def map_create(latitude, longitude,
               search_poly,
               active_fires,
               other_wildfires,
               rasterIDs):
    '''
    stitch data together for plotting on a folium map
    map will contain:
     1.  - search area around address
     2.  - selected/not selected fire data
     3.  - forecast data returned from model
    '''
    def get_color(x):
        '''
        if value = 1 (fire) then set colour to red with no opacity (1)
        if value = 0 (no fire) set to black with high opacity (0.2)
        '''
        if x == 1:
            return (255, 0, 0, 1)
        elif x == 0:
            return (0, 0, 0, 0.1)
        else:
            raise ValueError()

    #initiate map - centred on geocode lat/lon - can we make the zoom start scaled to search area??
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    #add search area to map
    geo_json_search = folium.GeoJson(data=search_poly, style_function=lambda x: {"fillColor": "grey", 'color': '#228B22'})
    geo_json_search.layer_name = 'Search area'
    m.add_child(geo_json_search)

    #add selected fires to map
    for _, r in active_fires.iterrows():
        geo_active_fires = gpd.GeoSeries(r['geometry']).to_json()
        geo_active_fires = folium.GeoJson(data=geo_active_fires, style_function=lambda x: {"fillColor": "red", 'color': '#000000'})
        geo_active_fires.layer_name = f'wildfire - {r["poly_IncidentName"]} - {r["OBJECTID"]}'

        ### NEED TO SOLVE THIS - no content in popup ################################################
        #iframe = folium.IFrame('Date:' + datetime.utcfromtimestamp(int(r["poly_CreateDate"])/1000) + '<br>' + 'Fire area (ac): ' + round(r["poly_GISAcres"]) + '<br>')
        label = folium.Html(f'<b>date: {datetime.utcfromtimestamp(int(r["attr_ModifiedOnDateTime_dt"])/1000)}</b><br><br><b>Fire area (ac): {round(r["poly_GISAcres"])}</b>', script=True)
        geo_active_fires.add_child(folium.Popup(label, min_width=250, max_width=250)) #creates popup but no content????
        ##############################################################################################
        m.add_child(geo_active_fires)

    #add forecast to map
    #for _, f in forecast_fires.iterrows():
    #    geo_forecast_fires = gpd.GeoSeries(f['geometry']).to_json()
    #    geo_forecast_fires = folium.GeoJson(data=geo_forecast_fires, style_function=lambda x: {"fillColor": "orange", 'color': '#871212'})

    #    m.add_child(geo_forecast_fires)

    for i in rasterIDs:
        raster_img = rasterio.open(f"{project_root}/rasters/{i}_raster.tif")
        array = raster_img.read()
        bounds = raster_img.bounds

        x1,y1,x2,y2 = raster_img.bounds
        bbox = [(bounds.bottom, bounds.left), (bounds.top, bounds.right)]

        img = folium.raster_layers.ImageOverlay(
            image=np.moveaxis(array, 0, -1),
            name='raster mask',
            opacity=1,
            bounds=bbox,
            interactive=True,
            cross_origin=False,
            zindex=1,
            colormap=lambda x: get_color(x)
        )
        img.layer_name = f'raster mask - {i}'
        img.add_to(m)

    #add other fires to map

    for _, s in other_wildfires.iterrows():
        geo_other_fires = gpd.GeoSeries(s['geometry']).to_json()
        geo_other_fires = folium.GeoJson(data=geo_other_fires, show=False, style_function=lambda x: {"fillColor": "purple", 'color': '#000000'})
        geo_other_fires.layer_name = f'other fires - {s["poly_IncidentName"]}'
        m.add_child(geo_other_fires)

    #add layer control widget to map
    folium.LayerControl().add_to(m)

    #return map to app.py
    return m


def map_create_forecast(latitude,
                        longitude,
                        search_poly,
                        rasterIDs):
    '''
    stitch data together for plotting on a folium map
    map will contain:
     1.  - search area around address
     2.  - selected/not selected fire data
     3.  - forecast data returned from model
    '''
    def get_color(x):
        '''
        if value = 1 (fire) then set colour to red with no opacity (1)
        if value = 0 (no fire) set to black with high opacity (0.2)
        '''
        if x > 0.5:
            return (255, 0, 0, 1)
        elif x < 0.5:
            return (1, 0, 0, 0.1)
        else:
            raise ValueError()

    #initiate map - centred on geocode lat/lon - can we make the zoom start scaled to search area??
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    #add search area to map
    geo_json_search = folium.GeoJson(data=search_poly, style_function=lambda x: {"fillColor": "grey", 'color': '#228B22'})
    geo_json_search.layer_name = 'Search area'
    m.add_child(geo_json_search)

    for i in rasterIDs:
        raster_img = rasterio.open(f"{project_root}/rasters/{i}_forecast_raster.tif")
        array = raster_img.read()
        bounds = raster_img.bounds

        x1,y1,x2,y2 = raster_img.bounds
        bbox = [(bounds.bottom, bounds.left), (bounds.top, bounds.right)]

        img = folium.raster_layers.ImageOverlay(
            image=np.moveaxis(array, 0, -1),
            name='raster mask',
            opacity=1,
            bounds=bbox,
            interactive=True,
            cross_origin=False,
            zindex=1,
            colormap=lambda x: get_color(x)
        )
        img.layer_name = f'raster mask - {i}'
        img.add_to(m)

    #add layer control widget to map
    folium.LayerControl().add_to(m)

    #return map to app.py
    return m




def pseudo_data(selected_fires):
    '''
    manipulate polygons 'forecast'
    '''
    forecast_fires = selected_fires.translate(0.1,0.2)
    forecast_fires = gpd.GeoDataFrame(forecast_fires)
    forecast_fires.rename(columns={0: 'geometry'}, inplace=True)

    return forecast_fires


### DEPRECATED FUNCTION - IGNORE ###
def nasa_fire_events(search_poly):
    '''
    calls the NASA eonet service for wildfire events.
    Good for testing but only near real time and not as detailed as NASA FIRM or NIFC data
    (see function below) which is live.
    '''
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
