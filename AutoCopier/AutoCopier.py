import os
import shutil
import schedule
import time
import ftplib
from datetime import date
from ftplib import FTP

def get_directories(source_ftp):
    directories = []

    ftp = FTP(source_ftp)
    ftp.login()

    # List all items in the given path
    items = ftp.nlst()

    # Iterate over the items and collect directories
    for item in items:
        # Check if the item is a directory
        if ftp.nlst(item) != ['.', '..']:
            directories.append('/'+item+'/')
    
    return directories

def copy_unique_files(source_ftp, source_dirs, destination_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Connect to the FTP server
    ftp = FTP(source_ftp)
    ftp.login()

    for source_dir in source_dirs:
        # Change to the desired FTP directory
        ftp.cwd(source_dir)

        # List the files in the FTP directory
        file_list = ftp.nlst()

        # Copy unique .mov files to the destination directory
        copied_files = []  # To store the names of copied files

        for file_name in file_list:
            source_path = os.path.join(source_dir, file_name)
            destination_path = os.path.join(destination_dir, file_name)

            # Check if the file already exists in the destination directory
            if not os.path.exists(destination_path):
                # Check if the file is available on the FTP server
                try:
                    ftp.retrbinary("RETR " + file_name, open(destination_path, "wb").write)
                    print(f"Copied {file_name} to {destination_dir}")
                    copied_files.append(file_name)
                except ftplib.error_perm as e:
                    if str(e).startswith("550"):
                        print(f"File {file_name} is unavailable for copying.")
                    else:
                        print(f"Failed to copy {file_name}: {e}")

        # Verify if the files were copied successfully
        destination_files = os.listdir(destination_dir)

        for file in copied_files:
            if file not in destination_files:
                print(f"Failed to copy {file} to {destination_dir}")
            else:
                print(f"{file} successfully copied to {destination_dir}")

    # Disconnect from the FTP server
    ftp.quit()

# Specify the FTP details and directories
SegmentoID = input("Identify the Segmento: ")
SOURCE_ftp = input("Hyperdeck IP Address: ")

source_ftp = SOURCE_ftp  # Replace with the appropriate FTP URL

source_directories = get_directories(source_ftp)

directory_name = SegmentoID + "_Recordings_" + str(date.today())
os.makedirs(directory_name, exist_ok=True)

destination_directory = directory_name

# Schedule the script to run at a specific time (e.g., 8:00 AM)
Time = input("Enter the time for copying to occur (24 hr format): ")
schedule.every().day.at(Time).do(copy_unique_files, source_ftp, source_directories, destination_directory)

while True:
    schedule.run_pending()
    time.sleep(1)
