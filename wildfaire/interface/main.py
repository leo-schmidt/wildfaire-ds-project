import numpy as np
import pandas as pd

from google.cloud import storage
from pathlib import Path
from colorama import Fore, Style
from dateutil.parser import parse

from wildfaire.params import *
from wildfaire.ML_logic.data import get_data, get_dataset
from wildfaire.ML_logic.preprocessor import preprocess_features
from wildfaire.ML_logic.registry import save_model, save_results, load_model
from wildfaire.ML_logic.model import compile_model, initialize_model, train_model

def data()

def preprocess() -> None:

def train() -> float:


def evaluate() -> float:
    """
    Evaluate the performance of the latest production model on processed data
    Return MAE as a float
    """

def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ Use case: predict")

    if X_pred is None:
        X_pred = pd.DataFrame(dict(
        pickup_datetime=[pd.Timestamp("2013-07-06 17:18:00", tz='UTC')],
        pickup_longitude=[-73.950655],
        pickup_latitude=[40.783282],
        dropoff_longitude=[-73.984365],
        dropoff_latitude=[40.769802],
        passenger_count=[1],
    ))

    model = load_model()
    assert model is not None

    X_processed = preprocess_features(X_pred)
    y_pred = model.predict(X_processed)

    print("\n✅ prediction done: ", y_pred, y_pred.shape, "\n")
    return y_pred


if __name__ == '__main__':
    preprocess()
    train()
    evaluate()
    pred()
