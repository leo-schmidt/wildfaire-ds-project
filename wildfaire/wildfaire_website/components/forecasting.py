
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
import haversine

from rasterio.transform import from_origin
from wildfaire.api.fast import app
from geocube.api.core import make_geocube
from haversine import inverse_haversine, Direction
from utils import get_project_root

#make API post request ## send to API
def raster_creation(forecast_fires):
    '''
    functions creates raster files with name 'OBJECTID_raster.tif' for wildfire
    polygons in the search area. Files are 64 x 64 pixels of approx 1 km resolution
    files are saved in root directoy of the Wildfaire package
    '''

    project_root = get_project_root()
    print(f'hello {project_root}')

    #create list of polygon ID's for code ot itterate over
    polygon_IDs = forecast_fires['OBJECTID'].tolist()
    delIDs = []
    fires =[]

    #for each fire polygon create a raster grid
    for i in polygon_IDs:

        x = forecast_fires.loc[forecast_fires['OBJECTID'] == i]

        ##extract centroid of polygon (give a lat/lon of location)
        fire_centroid = x.centroid
        centroid_x = fire_centroid.geometry.x.iloc[0]
        centroid_y = fire_centroid.geometry.y.iloc[0]

        #calculate 1 km in lat/lon for centroid - using haversine method. used
        testkm = inverse_haversine((centroid_y,centroid_x), 1, Direction.WEST)
        lon_res = round(centroid_x - testkm[1],5)
        testkm = inverse_haversine((centroid_y,centroid_x), 1, Direction.SOUTH)
        lat_res = round(centroid_y - testkm[0],5)

        vector_fn = x

        out_grid = make_geocube(
            vector_data=vector_fn,
            measurements=["OBJECTID"],
            resolution=(lat_res, -lon_res),
            fill=0
            )

        #convert grid to values of 0 and 1 and create numpy array
        feature_val = np.unique(out_grid['OBJECTID'])[0]
        cube_np = out_grid['OBJECTID'].to_numpy()
        cube_np[cube_np > 0] = 1

        #print(f'array total: {np.sum(cube_np)} for {feature_val}')

        if np.sum(cube_np) == 0:

           delIDs.append(i)
          # print(delIDs)

        else:
            #extract the dimensions of initial raster
            x_width = out_grid.dims['x']
            y_width = out_grid.dims['y']
            wildfaire_dim = 64

            #calculate padding required to make a 64 x 64 grid.
            top_padding = (wildfaire_dim - y_width) // 2
            bottom_padding = wildfaire_dim - y_width - top_padding
            left_padding = (wildfaire_dim - x_width) // 2
            right_padding = wildfaire_dim - x_width - left_padding

            #get top left coordinate from original array
            top_coords = [float(max(out_grid.coords['y'])), float(min(out_grid.coords['x']))]

            #calculate the top left corner

            top_coords[0] = top_coords[0] + (bottom_padding * lat_res) + (lat_res/2)
            top_coords[1] = top_coords[1] - (left_padding * lon_res) - (lon_res/2)

            #pad the cube with padding
            cube_padded = np.pad(cube_np,
                                pad_width=((top_padding, bottom_padding),
                                            (right_padding, left_padding)),
                                mode='constant', constant_values=0)

            # flip array back to correct orientation (for some reason the padding
            # inverts the array - no idea why!!)
            cube_flipped = np.flip(cube_padded)

            #array_values.append(cube_flipped)

            ### create the tif file
            transform = from_origin(top_coords[1], top_coords[0], lon_res, lat_res)

            new_dataset = rasterio.open(f'{project_root}/rasters/{i}_raster.tif', 'w', driver='GTiff',
                                        height = cube_flipped.shape[0],
                                        width = cube_flipped.shape[1],
                                        count=1,
                                        dtype=str(cube_flipped.dtype),
                                        crs='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',
                                        transform=transform)


            new_dataset.write(cube_flipped, 1)
            new_dataset.close()

            fire_dict = {"polygon_id": i}
            with rasterio.open(f'{project_root}/rasters/{i}_raster.tif') as raster_img:
                        fire_array = raster_img.read()
                        bounds = raster_img.bounds
                        fire_dict["bound"] = bounds
                        fire_dict["values"] = fire_array


            fires.append(fire_dict)

    #print(f'hello: {delIDs}')
    #polygon_IDs = [x for x in polygon_IDs if x not in delIDs]

    return fires
