#!/bin/bash

# Set environment variables from params.py
source params.py

# Set environment variables
export DATA_SIZE=$DATA_SIZE
export CHUNK_SIZE=$CHUNK_SIZE
export MODEL_TARGET=$MODEL_TARGET
export GCP_PROJECT=$GCP_PROJECT
export GCP_REGION=$GCP_REGION
export BUCKET_NAME=$BUCKET_NAME
export INSTANCE=$INSTANCE
export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
export MLFLOW_EXPERIMENT=$MLFLOW_EXPERIMENT
export MLFLOW_MODEL_NAME=$MLFLOW_MODEL_NAME
export PREFECT_FLOW_NAME=$PREFECT_FLOW_NAME
export PREFECT_LOG_LEVEL=$PREFECT_LOG_LEVEL
export EVALUATION_START_DATE=$EVALUATION_START_DATE
export GCR_IMAGE=$GCR_IMAGE
export GCR_REGION=$GCR_REGION
export GCR_MEMORY=$GCR_MEMORY

# Execute model training
python model_training.py

# Upload the trained model to GCS
python upload_to_gcs.py

# Deploy the model on ML Engine
gcloud ai-platform models create $MLFLOW_MODEL_NAME --regions=$GCP_REGION
gcloud ai-platform versions create your_version_name --model=$MLFLOW_MODEL_NAME --origin=gs://$BUCKET_NAME/models --runtime-version=2.7 --framework="scikit-learn"

# (Optional) Deploy the model with Cloud Run
gcloud run deploy your_cloud_run_service --image=$GCR_IMAGE --platform=managed --region=$GCR_REGION --memory=$GCR_MEMORY
