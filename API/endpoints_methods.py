#Module containing the different methods used in the endpoints
import os
import json
from flask import Flask

app = Flask(__name__)

def save_data(data, filename=None):
    '''Saves the data to the file'''
    file_path = filename

    # Read existing data if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Add the new data to the existing data
    if existing_data != data:
        existing_data.append(data)

    # Write the updated data to the file
    with open(file_path, 'w') as f:
        json.dump(existing_data, f)

def email_exists(email):
    '''Checks if the email already exists in the file'''
    file_path = "Persistence/users.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                existing_users = json.load(f)
            except json.JSONDecodeError:
                existing_users = []

        for user in existing_users:
            if user.get("email") == email:
                return True
    return False

def load_data(filename=None):
    '''Loads the data from the file'''
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {}

def amenity_exists(name):
    '''Checks if the amenity already exists in the file'''
    file_path = "Persistence/amenities.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                existing_amenities = json.load(f)
            except json.JSONDecodeError:
                existing_amenities = []

        for amenity in existing_amenities:
            if amenity.get("name") == name:
                return True
    return False
