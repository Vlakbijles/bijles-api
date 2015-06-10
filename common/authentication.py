#!/usr/bin/env python
"""
authentication.py, used for API-authentication based hmac (using sha256),
used by resources

"""


import hmac
import json
import time
import datetime

from functools import wraps
from hashlib import sha256
from config import api_users
from resources import abort


def api_validation(f):
    """
    Creates a hash and compares it with the hash that was sent,
    if these are the same the API created a correct hash and thus the API is valid.
    For the creation of the hash the following data is used:
        - Request data
        - URI path (including the query)
        - HTTP method
        - API secret key

    Use this function as a python decorator

    """

    @wraps(f)
    def wrapper(*args, **kwargs):

        data_dict = args[0].args
        utc_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))

        # Ignore requests older than 40 seconds
        if utc_now - int(data_dict['timestamp']) < 40:

            if data_dict["api_user"] in api_users:
                api_key = api_users[data_dict["api_user"]]

                # Remove hash field from json data in order to regenerate
                # original hash
                provided_hash = data_dict["hash"]
                del data_dict["hash"]
                data_json = json.dumps(data_dict, sort_keys=True, separators=(",", ":"))

                reconstructed_hash = hmac.new(str(api_key), data_json, sha256)
                reconstructed_hash.update(args[0].full_path)
                reconstructed_hash.update(args[0].method)

                if reconstructed_hash.hexdigest() == provided_hash:
                    return f(*args, **kwargs)

        return abort(401, message="Unauthorized API request")

    return wrapper
