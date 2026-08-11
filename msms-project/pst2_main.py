# pst2_main.py - The Persistent Application

import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            # Load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # Dictionary structure for starting fresh lists
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # open file in write mode and format output with indent = 4 
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")


#test script/ main block

if __name__== "__main__":
    load_data()  #loading existing data to create default structure on first run 
    save_data() #save the initial/loaded data to msms.json