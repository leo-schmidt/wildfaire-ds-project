import ee
import ee_utils
from export_ee_data import _get_time_slices

def get_ee_data(start_date,
                geometry = ee_utils.COORDINATES['US'],
                kernel_size = 64
    ):

    ### INITIALIZE GEE API ###
    ee.Initialize()

    ### DEFINE CONSTANTS ###

    start_date = ee.Date(start_date)

    sampling_scale = 1000 # meters

    geometry = ee.Geometry.Rectangle(geometry)

    ### STATIC DATA ###

    # Get elevation data
    elevation = ee_utils.get_image(ee_utils.DataType.ELEVATION_SRTM)

    # Get population data
    # and select the most recent
    population = ee_utils.get_image_collection(ee_utils.DataType.POPULATION)
    population = population.sort('system:time_start', False).first().rename('population')

    ### DYNAMIC DATA ###

    # (Drought, vegetation, weather, fire)

    # extract projection from weather data
    # later needed to reproject all data to the same specifications
    projection = ee_utils.get_image_collection(ee_utils.DataType.WEATHER_GRIDMET)
    projection = projection.first().select(ee_utils.DATA_BANDS[ee_utils.DataType.WEATHER_GRIDMET][0]).projection()

    # scale 20000 m
    # not sure what happens when changing this
    resampling_scale = (ee_utils.RESAMPLING_SCALE[ee_utils.DataType.WEATHER_GRIDMET])

    # window from start date to 1 day later
    window = 1 # length in days
    window_start = start_date

    # time slice of dynamic data
    # according to window defined above
    # returns list of extracted EE images
    # check _get_time_slices source code for more information
    time_slices = _get_time_slices(window_start, window, projection, resampling_scale)

    ### COMBINE DATA AND MAKE FIRE MASKS ###

    # Input features (X)
    # Create list of all images: elevation, population, dynamic data
    image_list = [elevation, population] + time_slices[:-1]

    # Target (y)
    detection = time_slices[-1]

    #
    arrays = ee_utils.convert_features_to_arrays(image_list, kernel_size)
    to_sample = detection.addBands(arrays)

    fire_count = ee_utils.get_detection_count(
        detection,
        geometry=geometry,
        sampling_scale=10 * sampling_scale,
    )

    # limit sampling to avoid EE server errors
    sampling_limit_per_call = 1

    # create samples
    samples = ee_utils.extract_samples(
        to_sample,
        detection_count=1,
        geometry=geometry,
        sampling_ratio=0,  # Only extracting examples with fire.
        sampling_limit_per_call=sampling_limit_per_call,
        resolution=sampling_scale,
    )

    return samples
