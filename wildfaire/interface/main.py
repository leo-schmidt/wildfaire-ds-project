import numpy as np
import pandas as pd

from google.cloud import storage
from pathlib import Path
from colorama import Fore, Style
from dateutil.parser import parse

from wildfaire.params import *
from wildfaire.ML_logic.data import get_file_paths, get_dataset
from wildfaire.ML_logic.preprocessor import preprocess_features
from wildfaire.ML_logic.model import load_model

def data():
    train_pattern, test_pattern, eval_pattern = get_file_paths
    train_set = get_dataset(train_pattern)
    test_set = get_dataset(test_pattern)   #USEFUL IF WE WANT TO TRAIN ON THE CLOUD
    eval_set = get_dataset(eval_pattern)
    return train_set, test_set, eval_set


def preprocess() -> None:
    return None            #USEFUL IF WE WANT TO TRAIN ON THE CLOUD
def train() -> float:
    return None        #USEFUL IF WE WANT TO TRAIN ON THE CLOUD

def evaluate() -> float:
    """
    Evaluate the performance of the latest production model on processed data
    Return MAE as a float
    """             #USEFUL IF WE WANT TO TRAIN ON THE CLOUD
    return None
def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction using the latest trained model
    """


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
