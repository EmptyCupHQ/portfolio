import json

from flask import abort

import utils
from config import DB


def load():
    try:
        db = utils.load_json(DB['json_path'])
    except (FileNotFoundError, json.JSONDecodeError, PermissionError, IOError):
        abort(500, description='Cannot read from Database')
    return db


def save(db):
    try:
        utils.save_json(DB['json_path'], db)
    except (FileNotFoundError, PermissionError, TypeError, IOError):
        abort(500, description='Cannot write to Database')


# decorator to check if user exists
def if_pro_exists(func):
    def wrapper(pid, *args, **kwargs):
        daba = load()
        if pid not in daba:
            abort(404, description='User with %s does not exist' % pid)
        return func(pid, *args, **kwargs)
    return wrapper