import boto3
import os

# Set up the Boto3 S3 client
s3 = boto3.client('s3')

# Specify the local folder path
local_folder = '/path/to/local/folder'

# Specify the MTurk bucket name
bucket_name = 'your-mturk-bucket-name'

# Get a list of files in the local folder
files = os.listdir(local_folder)

# Iterate over the files and upload them to the MTurk bucket
for file_name in files:
    local_file_path = os.path.join(local_folder, file_name)
    s3.upload_file(local_file_path, bucket_name, file_name)

    print(f"Uploaded file: {file_name}")

print("All files uploaded successfully.")
