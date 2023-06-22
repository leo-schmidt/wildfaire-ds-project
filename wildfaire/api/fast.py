from fastapi import FastAPI, Response
import numpy as np
from PIL import Image
import cv2
import io
from pydantic import BaseModel

app = FastAPI()

# load model here
# app.state.model = ...

# define data type of the input for the API endpoint
class Data(BaseModel):
    data: list

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

    # dummy prediction
    prediction = np.zeros((64,64), dtype=np.uint8)

    # return JSON containing prediction array
    # only works if converted to a list first
    return {'fire_spread': prediction.tolist()}

@app.post('/predict_image', response_class=Response)
def predict_image():
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
