import json
import os

# The name of the file where all your data will be permanently saved
DATA_FILE = "app_data.json"

DB = {
    "users": {
        "admin": "password"  # A default test account
    }, 
    "solo_projects": [],  
    "group_projects": []  
}

def load_data():
    """Loads data from the JSON file into the DB dictionary when the app starts."""
    global DB
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                loaded_data = json.load(f)
                # Update our DB dictionary with the saved data
                DB.update(loaded_data)
        except json.JSONDecodeError:
            print("No existing data found or file is empty. Starting fresh!")

def save_data():
    """Saves the current state of the DB dictionary to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(DB, f, indent=4)