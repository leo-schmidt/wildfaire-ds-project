import numpy as np
import time

from colorama import Fore, Style
from typing import Tuple
from google.cloud import storage
import joblib
from wildfaire.params import *

# Timing the TF import
print(Fore.BLUE + "\nLoading TensorFlow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow import keras
from keras import Model, Sequential, layers, regularizers, optimizers
from keras.callbacks import EarlyStopping

end = time.perf_counter()
print(f"\n✅ TensorFlow loaded ({round(end - start, 2)}s)")



def load_model():
    '''
    This function loads the "baseline_model.sav" file and returns the model.
    '''

    # Set your Google Cloud Storage bucket and file path
    bucket_name = BUCKET_NAME
    model_file_path = MODEL_FILE_PATH

    # Initialize a client to interact with Google Cloud Storage
    storage_client = storage.Client()

    # Retrieve the model file from Google Cloud Storage
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(model_file_path)
    blob.download_to_filename('baseline_model.sav')

    # Load the model from the downloaded file
    model = joblib.load('baseline_model.sav')

    return model

# def train_model(
#         model: Model,
#         X: np.ndarray,
#         y: np.ndarray,
#         batch_size=256,
#         patience=2,
#         validation_data=None, # overrides validation_split
#         validation_split=0.3
#     ) -> Tuple[Model, dict]:
#     """
#     Fit the model and return a tuple (fitted_model, history)
#     """
#     print(Fore.BLUE + "\nTraining model..." + Style.RESET_ALL)

#     es = EarlyStopping(
#         monitor="val_loss",
#         patience=patience,
#         restore_best_weights=True,
#         verbose=1
#     )

#     history = model.fit(
#         X,
#         y,
#         validation_data=validation_data,
#         validation_split=validation_split,
#         epochs=100,
#         batch_size=batch_size,
#         callbacks=[es],
#         verbose=0
#     )

#     print(f"✅ Model trained on {len(X)} rows with min val MAE: {round(np.min(history.history['val_mae']), 2)}")

#     return model, history

# def evaluate_model(
#         model: Model,
#         X: np.ndarray,
#         y: np.ndarray,
#         batch_size=64
#     ) -> Tuple[Model, dict]:
#     """
#     Evaluate trained model performance on the dataset
#     """

#     print(Fore.BLUE + f"\nEvaluating model on {len(X)} rows..." + Style.RESET_ALL)

#     if model is None:
#         print(f"\n❌ No model to evaluate")
#         return None

#     metrics = model.evaluate(
#         x=X,
#         y=y,
#         batch_size=batch_size,
#         verbose=0,
#         # callbacks=None,
#         return_dict=True
#     )

#     loss = metrics["loss"]
#     mae = metrics["mae"]

#     print(f"✅ Model evaluated, MAE: {round(mae, 2)}")

#     return metrics
