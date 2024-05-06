from google.cloud import storage


def upload_to_gcs(bucket_name, source_file,
                  destination_blob_name):
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        source_file (str): The path to the local file to upload.
        destination_blob_name (str):
        The name to give the file in the GCS bucket.

    Returns:
        str: The public URL to access the uploaded file.
    """
    # Initialize a GCS client
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Create a blob object representing the file to upload
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(source_file)

    # Make the blob publicly accessible
    blob.make_public()

    # Return the public URL of the uploaded file
    return blob.public_url


# Example usage:
if __name__ == "__main__":
    # Replace these values with your own
    bucket_name = "your_bucket_name"
    source_file = "path_to_local_file"
    destination_blob_name = "name_of_file_in_bucket"

    # Upload the file
    public_url = upload_to_gcs(bucket_name, source_file, destination_blob_name)

    print(f"File uploaded to GCS. Public URL: {public_url}")
