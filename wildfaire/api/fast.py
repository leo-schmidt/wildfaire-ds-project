from fastapi import FastAPI, Response
import numpy as np
from PIL import Image
import io
from pydantic import BaseModel

#from wildfaire.ML_logic.registry import load_model
from tensorflow.keras.models import load_model
import os
from wildfaire.params import BUCKET_NAME
from google.cloud import storage

from wildfaire.hooks.custom_loss import custom_loss, loss


app = FastAPI()

# load model here
client = storage.Client()

# Path to newest model
bucket_name = BUCKET_NAME

#downloading newest model
bucket = client.get_bucket(bucket_name)
blobs = bucket.list_blobs(prefix='Model/')

#Filter to have the most recent model
h5_files = [blob for blob in blobs if blob.name.endswith('.h5')]
h5_files.sort(key=lambda x: x.updated, reverse=True)

# Downloading the most recent
if h5_files:
    latest_file = h5_files[0]
    latest_file.download_to_filename('baseline_model.h5')

    app.state.model = load_model("baseline_model.h5", custom_objects={'loss': loss})
    print('Model loaded.')

else:
    print("Aucun fichier .h5 trouvé dans le bucket.")




# define data type of the input for the API endpoint
class Data(BaseModel):
    lon: str
    lat: str
    input_features: list

# landing page
@app.get("/")
def root():
    return {
    'greeting': 'Hello, this is the landing page for the WildfAIre API.'
    }

@app.post("/predict")
def predict(data: Data):
    """
    Make a single prediction.
    Input: List created from array of size 64x64x12.
    Returns: Dummy Numpy array of size 64x64 filled with zeros.
    """

    # input data
    lon = data.lon
    lat = data.lat
    input_features = data.input_features

    # dummy prediction

    # prediction = np.zeros((64,64), dtype=np.uint8)

    # prediction
    prediction = app.state.model.predict(input_features)


    # return JSON containing prediction array
    # only works if converted to a list first
    return {
            'lon' : lon,
            'lat' : lat,
            'fire_spread': prediction.tolist()
            }

@app.post('/predict_image', response_class=Response)
def predict_image(data: Data):
    """
    Make a single prediction.
    Input: List created from array of size 64x64x12.
    Returns: HTML response containing dummy black .png image of size 64 x 64.
    """

    # dummy prediction
    prediction = np.zeros((64,64), dtype=np.uint8)

    # create image from prediction
    im = Image.fromarray(prediction, mode='L')

    # save image to an in-memory bytes buffer
    with io.BytesIO() as buf:
        im.save(buf, format='PNG')
        im_bytes = buf.getvalue()

    # return HTML response containing image
    headers = {'Content-Disposition': 'inline; filename="fire_spread.png"'}
    return Response(im_bytes, headers=headers, media_type='image/png')
