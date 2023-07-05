import os
from google.cloud import storage

def upload_file_to_gcs(local_file_path, bucket_name, gcs_file_path):
    """
    Upload a file to Google Cloud Storage (GCS).
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_file_path)
    blob.upload_from_filename(local_file_path)
    print(f"File uploaded to GCS: {gcs_file_path}")

def main():
    """
    Main function for uploading a file to GCS.
    """
    # Specify the local file path
    local_file_path = 'trained_model.sav'  # Specify the path to the local file

    # Specify the GCS bucket name and file path
    bucket_name = 'your_bucket_name'
    gcs_file_path = 'models/trained_model.sav'  # Specify the desired file path in GCS

    # Upload thefile to GCS
    upload_file_to_gcs(local_file_path, bucket_name, gcs_file_path)

if __name__ == '__main__':
    main()
