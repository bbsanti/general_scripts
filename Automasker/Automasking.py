import json
import shutil
import os
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox

def copy_json_file(json_file):
    json_dir = os.path.dirname(json_file)
    base_name = os.path.basename(json_file)
    new_file = os.path.splitext(base_name)[0] + '_automasked.json'
    new_file_path = os.path.join(json_dir, new_file)
    shutil.copy2(json_file, new_file_path)
    return new_file_path




def update_json(json_file, target_dict, updated_values, data=None):
    if data is None:
        with open(json_file, 'r') as file:
            data = json.load(file)

    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_dict:
                # Update the values in the dictionary
                for key, new_value in updated_values.items():
                    data[target_dict][key] = new_value
                break
            else:
                update_json(json_file, target_dict, updated_values, data[key])

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def copy_directory(src_dir, dst_dir):
    shutil.copytree(src_dir, dst_dir)


# Prompt the user to select a JSON file
json_file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

# Check if a file was selected
if json_file:
    json_dir = os.path.dirname(json_file)
    new_json_file = os.path.join(json_dir, copy_json_file(json_file))


    folder_path = os.path.join(json_dir, os.path.splitext(os.path.basename(json_file))[0])
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        folder_name = os.path.basename(folder_path)

        # Extract the base folder name and extension
        base_folder_name, folder_extension = os.path.splitext(folder_name)

        # Add the suffix to the base folder name
        new_folder = base_folder_name + folder_extension + '_automasked'

        new_folder_path = os.path.join(json_dir, new_folder)
        copy_directory(folder_path, new_folder_path)

    # Example target dictionary and updated values
    target_dict = 'masks'
    updated_values = {
        'autoDetectInterval': 100,
        'segmentationHeight': 1080,
        'segmentationWidth': 1920,
    }

    # Call the update_json function
    update_json(new_json_file, target_dict, updated_values)

    print("JSON file updated successfully!")
