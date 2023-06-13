import tkinter as tk
from tkinter import filedialog
import boto3
import os

# Set up the Boto3 S3 client
s3 = boto3.client('s3')

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select a local folder
local_folder = filedialog.askdirectory(title="Select Local Folder")

# Check if a folder was selected
if not local_folder:
    print("No folder selected. Exiting.")
    exit()

# Specify the MTurk bucket name
bucket_name = 'shorttrainingmaterials'

# Get a list of files in the local folder
files = os.listdir(local_folder)

# Iterate over the files and upload them to the MTurk bucket
for file_name in files:
    local_file_path = os.path.join(local_folder, file_name)
    s3.upload_file(local_file_path, bucket_name, file_name)

    print(f"Uploaded file: {file_name}")

print("All files uploaded successfully.")
