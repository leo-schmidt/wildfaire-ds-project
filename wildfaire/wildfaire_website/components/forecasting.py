
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

from rasterio.transform import from_origin
from wildfaire.api.fast import app
from geocube.api.core import make_geocube

#make API post request ## send to API
def raster_creation(forecast_fires):
    '''
    functions creates raster files with name 'OBJECTID_raster.tif' for wildfire
    polygons in the search area. Files are 64 x 64 pixels of approx 1 km resolution
    files are saved in root directoy of the Wildfaire package
    '''

    #create list of polygon ID's for code ot itterate over
    polygon_IDs = forecast_fires['OBJECTID'].tolist()

    #for each fire polygon create a raster grid
    for i in polygon_IDs:
        x = forecast_fires.loc[forecast_fires['OBJECTID'] == i]
        vector_fn = x
        out_grid = make_geocube(
            vector_data=vector_fn,
            measurements=["OBJECTID"],
            resolution=(0.01, -0.01),
            fill=0
            )

        #convert grid to values of 0 and 1 and create numpy array
        feature_val = np.unique(out_grid['OBJECTID'])[1]
        cube_np = out_grid['OBJECTID'].to_numpy()
        cube_np[cube_np > 0] = 1

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
        top_coords[0] = top_coords[0] + (bottom_padding * 0.009043717) + 0.004521859
        top_coords[1] = top_coords[1] - (left_padding * 0.017100201) - 0.008550101

        #pad the cube with padding
        cube_padded = np.pad(cube_np,
                            pad_width=((top_padding, bottom_padding),
                                        (right_padding, left_padding)),
                            mode='constant', constant_values=0)

        # flip array back to correct orientation (for some reason the padding
        # inverts the array - no idea why!!)
        cube_flipped = np.flip(cube_padded)

        ### create the tiff file
        transform = from_origin(top_coords[1], top_coords[0], 0.01, 0.01)

        new_dataset = rasterio.open(f'{i}_raster.tif', 'w', driver='GTiff',
                                    height = cube_flipped.shape[0],
                                    width = cube_flipped.shape[1],
                                    count=1,
                                    dtype=str(cube_flipped.dtype),
                                    crs='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',
                                    transform=transform)

        new_dataset.write(cube_flipped, 1)
        new_dataset.close()

    return polygon_IDs
