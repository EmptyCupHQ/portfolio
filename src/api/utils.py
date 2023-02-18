import json


def load_json(filep):
    """
    Reads from JSON file and returns data.
    """
    with open(filep, 'r') as rf:
        data = json.load(rf)
        return data 


def save_json(filep, data):
    """
    Writes to a JSON file.
    """
    with open(filep, 'w') as wf:
        json.dump(data, wf)
