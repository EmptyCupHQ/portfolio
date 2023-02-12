from flask import abort
import json
import os.path


def read_db(db):
    """
    Reads from database and returns data.
    If database is not found, creates a new one.
    """
    if not os.path.exists('./'+db):
        with open(db, 'w') as wf:
            json.dump({}, wf)
    with open(db, 'r') as rf:
        data = json.load(rf)
    if data == {}:
        abort(500, description="Database is empty")
    elif not data:
        abort(500, description="Could not read from database")
    return data


def write_db(db, data):
    """
    Writes to database.
    """
    try:
        with open(db, 'w') as wf:
            json.dump(data, wf)
    except:
        abort(500, description="Could not write to database")
