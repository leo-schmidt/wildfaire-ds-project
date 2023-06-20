import requests
#import geopandas as gpd
#from shapely.geometry import Point
#import matplotlib.pyplot as plt


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



def nasa_fire_events(latitude, longitude):
    #to do
    '''
    1. create a search area around house equivalent to 100 km x 100 km



    2. build api call

    3. send to api

    4. process return - error handling if no results
    '''
    # Generate some sample data
    #p1 = Point((1,2))
    #p2 = Point((6,8))
    #points = gpd.GeoSeries([p1,p2])

    # Buffer the points using a square cap style
    # Note cap_style: round = 1, flat = 2, square = 3
    #buffer = points.buffer(2, cap_style = 3)

    # Plot the results
    #fig, ax1 = plt.subplots()
    #buffer.boundary.plot(ax=ax1, color = 'slategrey')
    #points.plot(ax = ax1, color = 'red')
