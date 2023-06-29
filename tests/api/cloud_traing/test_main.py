from unittest.mock import patch
import shutil
import pytest
import pickle
import glob
import numpy as np
import pandas as pd
from pathlib import Path
from wildfaire.params import *
import os
from google.cloud import storage, bigquery, logging_v2, pubsub

DATA_SIZE = "1k"
CHUNK_SIZE = 200

MIN_DATE='2009-01-01'
MAX_DATE='2015-01-01'

@patch("wildfaire.params.DATA_SIZE", new=DATA_SIZE)
@patch("wildfaire.params.CHUNK_SIZE", new=CHUNK_SIZE)
class TestMain():
    """Assert that code logic runs and outputs the correct type. Do not check model performance"""


    # Test if the project is authenticated
    def test_authentication():
        # Google Cloud Storage authentication test
        storage_client = storage.Client()
        assert storage_client.project == os.environ.get("GCP_PROJECT")

        # Google BigQuery authentication test
        bigquery_client = bigquery.Client()
        assert bigquery_client.project == os.environ.get("GCP_PROJECT")

        # Google Cloud Logging authentication test
        logging_client = logging_v2.LoggingServiceV2Client()
        assert logging_client.project == os.environ.get("GCP_PROJECT")

        # Google Cloud Pub/Sub authentication test
        pubsub_client = pubsub.PublisherClient()
        assert pubsub_client.project_path(os.environ.get("GCP_PROJECT"))
