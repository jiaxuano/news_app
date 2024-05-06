from google.cloud import storage
import csv

# Create a client to interact with the storage
storage_client = storage.Client()

# Specify the GCS bucket name and the file path
bucket_name = "swiftnewsresults"
blob_name = "news/First Republic Bank.csv"

# Get the bucket and the blob (file)
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(blob_name)

# Download the blob's content as a string
file_content = blob.download_as_string()

# Process the file content as needed
file_content_decoded = file_content.decode('utf-8')  # Decode the bytes to string
csv_data = [line.split(',') for line in file_content_decoded.split('\n') if line]  # Assuming CSV format

# Save the data to a CSV file locally
local_csv_file = "local_file.csv"
with open(local_csv_file, "w", newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(csv_data)

print(f"CSV file saved locally: {local_csv_file}")
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                                                                                                                                                                                       
                                                                                                                                                               
