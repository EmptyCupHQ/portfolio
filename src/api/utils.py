import json
import os.path


def load_json(file_path):
    """
    Reads from JSON file and returns data.
    If file not found, creates a new one.
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as wf:
            json.dump({}, wf)

    with open(file_path, 'r') as rf:
        data = json.load(rf)
    if not data:
        return False

    return data


def save_json(file_path, data):
    """
    Writes to a JSON file.
    """
    try: 
        with open(file_path, 'w') as wf:
            json.dump(data, wf)
    except Exception as e:
        return False
    
    return True
